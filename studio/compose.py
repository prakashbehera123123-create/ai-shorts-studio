"""Deterministic draft render: voiceover -> timed captions -> Pillow frames -> FFmpeg MP4 -> validation."""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import MediaToolError, StudioError
from .manifest import COLUMNS
from .media import check_summary, require_tool, run_ffprobe, summarize
from .render_config import RenderConfig
from .status import Status, load_status, parse_status
from .storyboard import load_storyboard
from .archive import archive_previous_render
from .compose_types import SceneTiming
from .tts import WordTime, map_word_times, spoken_tokens, synthesize_sapi
from .visuals import CardRenderer, Cue, chunk_caption, readability_problems, time_cues, to_srt

FFMPEG_TIMEOUT_SECONDS = 600
MAX_SAPI_RATE = 4  # beyond this the placeholder voice gets hard to follow
RUNTIME_HEADROOM_SECONDS = 1.0
PRE_LOUDNORM = "aresample=48000,aformat=channel_layouts=stereo,"  # measure and apply on the stereo signal we deliver
MANUAL_VOICEOVER = Path("voiceover") / "voiceover.wav"


@dataclass
class RenderReport:
    video_id: str
    voice_source: str
    renderer: str = "cards"
    tempo: float | None = None
    tts_rate: int | None = None
    output: str = ""
    duration_seconds: float = 0.0
    scenes: list[dict[str, Any]] = field(default_factory=list)
    cues: int = 0
    probe: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def run_ffmpeg(args: list[str], log: Path) -> None:
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-y", *args]
    log.parent.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=FFMPEG_TIMEOUT_SECONDS, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError(f"ffmpeg timed out after {FFMPEG_TIMEOUT_SECONDS}s") from exc
    with log.open("a", encoding="utf-8") as fh:
        fh.write("$ " + " ".join(cmd) + "\n" + (p.stderr or "")[-4000:] + "\n")
    if p.returncode != 0:
        raise MediaToolError(f"ffmpeg failed (exit {p.returncode}); see {log}")


def parse_loudnorm_json(stderr: str) -> dict[str, str]:
    """The JSON block that `loudnorm=print_format=json` prints at the end of stderr."""
    start, end = stderr.rfind("{"), stderr.rfind("}")
    if start < 0 or end < start:
        raise MediaToolError("loudnorm measurement produced no JSON")
    data = json.loads(stderr[start:end + 1])
    for key in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset"):
        if key not in data:
            raise MediaToolError(f"loudnorm measurement missing {key}")
    return data


def two_pass_loudnorm_filter(audio: Path, rcfg: RenderConfig) -> str:
    """Measure, then normalise with a single linear gain. Single-pass loudnorm undershoots on speech with pauses."""
    target = f"I={rcfg.loudness_lufs:g}:TP={rcfg.true_peak_db:g}:LRA=11"
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-i", str(audio),
           "-af", f"{PRE_LOUDNORM}loudnorm={target}:print_format=json", "-f", "null", "-"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=FFMPEG_TIMEOUT_SECONDS, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("loudness measurement timed out") from exc
    if p.returncode != 0:
        raise MediaToolError("loudness measurement failed")
    m = parse_loudnorm_json(p.stderr or "")
    return (f"{PRE_LOUDNORM}loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")


def snap(t: float, fps: int) -> float:
    return round(round(t * fps) / fps, 6)


def source_lines(sources_md: str) -> dict[str, str]:
    """S id -> 'Source: <publisher> · <published>' from the sources.md table."""
    out: dict[str, str] = {}
    for line in sources_md.splitlines():
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) >= 5 and re.fullmatch(r"S\d+", cells[0]):
            publisher = re.sub(r"\s*\(.*?\)", "", cells[2]).strip()
            date = cells[3] if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[3]) else ""
            out[cells[0]] = f"Source: {publisher}" + (f" · {date}" if date else "")
    return out


def scene_pauses(scenes: list[dict[str, Any]]) -> list[float]:
    """Directed pause after each scene in seconds (storyboard v2 `voice.pause_after_ms`; 0 when absent)."""
    return [int((s.get("voice") or {}).get("pause_after_ms", 0)) / 1000 for s in scenes]


def plan_timings(speech: list[float], padding: float, fps: int, pauses: list[float] | None = None) -> list[SceneTiming]:
    timings, t = [], 0.0
    pauses = pauses or [0.0] * len(speech)
    for i, (s, pause) in enumerate(zip(speech, pauses), start=1):
        end = snap(t + s + padding + pause, fps)
        timings.append(SceneTiming(i, t, s, end))
        t = end
    return timings


def scaled_timings(scenes: list[dict[str, Any]], audio_seconds: float, fps: int) -> list[SceneTiming]:
    """Manual voiceover: keep storyboard proportions, stretched to the recorded length."""
    board_total = float(scenes[-1]["end_seconds"])
    k = audio_seconds / board_total
    out = []
    for s in scenes:
        start, end = snap(float(s["start_seconds"]) * k, fps), snap(float(s["end_seconds"]) * k, fps)
        out.append(SceneTiming(int(s["id"]), start, end - start, end))
    out[-1].end = snap(audio_seconds, fps)
    return out


def build_cues(scenes: list[dict[str, Any]], timings: list[SceneTiming], style: dict[str, Any], fps: int) -> list[Cue]:
    cues: list[Cue] = []
    for scene, tm in zip(scenes, timings):
        chunks = chunk_caption(str(scene["narration"]), int(style["caption_max_words"]), int(style["caption_max_chars"]))
        scene_cues = time_cues(tm.scene_id, tm.start, tm.speech, chunks)
        snapped = [Cue(c.scene_id, snap(c.start, fps), snap(c.end, fps), c.text) for c in scene_cues]
        snapped[-1] = Cue(tm.scene_id, snapped[-1].start, tm.end, snapped[-1].text)  # hold last line through padding
        cues.extend(c for c in snapped if c.end > c.start)
    for i in range(1, len(cues)):  # make cues gapless so the frame list covers the whole timeline
        prev, cur = cues[i - 1], cues[i]
        if abs(prev.end - cur.start) > 1e-6:
            cues[i] = Cue(cur.scene_id, prev.end, cur.end, cur.text)
    return cues


def scene_word_times(scenes: list[dict[str, Any]], timings: list[SceneTiming], marks: list[list[tuple[int, int]]],
                     rcfg: RenderConfig) -> list[list[WordTime]]:
    """Absolute word timings per scene: SAPI boundaries when available, else spread over the scene's speech."""
    out = []
    for s, tm, mk in zip(scenes, timings, marks):
        orig, spoken = spoken_tokens(str(s["narration"]), rcfg.pronunciations)
        local = map_word_times(orig, spoken, mk, tm.speech)
        out.append([WordTime(w.text, round(tm.start + w.start, 3), round(tm.start + w.end, 3)) for w in local])
    return out


def _finish_motion(folder: Path, cfg: ProductionConfig, rcfg: RenderConfig, board: dict[str, Any], timings: list[SceneTiming],
                   marks: list[list[tuple[int, int]]], narration: Path, total: float, rep: RenderReport, log: Path,
                   local_words: list[list[WordTime]] | None = None) -> RenderReport:
    from .motion_spec import build_spec, captions_srt, run_renderer

    rep.renderer = "motion"
    scenes = board["scenes"]
    if local_words is not None:  # engine without word boundaries (clone): estimated per scene, shift to absolute
        words = [[WordTime(w.text, round(tm.start + w.start, 3), round(tm.start + w.end, 3)) for w in lw]
                 for lw, tm in zip(local_words, timings)]
    else:
        words = scene_word_times(scenes, timings, marks, rcfg)
    spec = build_spec(board, timings, words, (folder / "sources.md").read_text(encoding="utf-8"), rcfg.fps, rcfg.crf, rcfg.preset)
    motion_dir = folder / "assets" / "motion"
    motion_dir.mkdir(parents=True, exist_ok=True)
    spec_path = motion_dir / "spec.json"
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    render_dir = folder / "render"
    silent = render_dir / "video_silent.mp4"
    rep.warnings.append(f"motion renderer: {run_renderer(spec_path, silent, rcfg.browser_channel, log)}")
    from .scene3d import apply_3d, render_3d_clips

    clips = render_3d_clips(folder, board, timings, rcfg, log)  # empty unless a scene opted into 3D
    if clips:
        apply_3d(silent, clips, rcfg, log)
        rep.warnings.append("3D scenes " + ", ".join(f"{c.scene_id} ({'cached' if c.cached else 'rendered'})" for c in clips)
                            + " via HyperFrames")
    (render_dir / "captions.srt").write_text(captions_srt(spec["captions"]), encoding="utf-8")

    sound_rows: list[list[str]] = []
    audio = narration
    if rcfg.sound.get("enabled"):
        from .sound import build_mix, licence_row

        audio, cues, bed = build_mix(narration, narration.with_name("mix.wav"), board, timings, total, folder.name, rcfg, log)
        rep.warnings.append(f"sound: bed {bed.name}, {len(cues)} SFX " + ", ".join(f"{c.name}@{c.time:g}s" for c in cues))
        used = [bed] + sorted({c.path for c in cues})
        for i, p in enumerate(used, start=1):
            row = licence_row(p)
            kind = "music bed" if p == bed else "sound effect"
            atype = "generated_audio" if row.get("license") == "self-generated" else "licensed_stock"
            sound_rows.append([f"A{i:03d}", "assets/library/audio/" + row["file"], atype, row.get("source_url", ""),
                               row.get("creator", ""), row.get("license", ""), "", "no", kind])
    if any("icon_svg" in json.dumps(ss.get("visual", {})) for ss in spec["scenes"]):
        sound_rows.append(["I001", "vendor/node_modules/lucide-static/icons", "licensed_stock", "https://lucide.dev",
                           "Lucide contributors", "ISC", "https://github.com/lucide-icons/lucide/blob/main/LICENSE", "no",
                           "icons drawn in motion graphics"])
    out = render_dir / "draft.mp4"
    run_ffmpeg([
        "-i", str(silent), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-t", f"{total:.3f}", "-c:v", "copy",
        "-af", f"{two_pass_loudnorm_filter(audio, rcfg)},aresample={rcfg.audio_sample_rate}",
        "-c:a", "aac", "-b:a", rcfg.audio_bitrate, "-ac", "2", "-movflags", "+faststart", str(out),
    ], log)
    silent.unlink(missing_ok=True)

    rep.output = out.relative_to(folder).as_posix()
    rep.probe = summarize(run_ffprobe(out), rep.output)
    rep.duration_seconds = rep.probe["duration_seconds"]
    rep.errors.extend(check_summary(rep.probe, cfg))
    if abs(rep.duration_seconds - total) > 0.25:
        rep.errors.append(f"output {rep.duration_seconds}s differs from planned {total:.2f}s")
    rep.scenes = [{"id": t.scene_id, "start": t.start, "speech": round(t.speech, 3), "end": t.end} for t in timings]
    rep.cues = len(spec["captions"])
    if rep.voice_source == "sapi":
        rep.warnings.append("Voice is the Windows SAPI placeholder; record voiceover/voiceover.wav or approve a better local TTS before publishing")
    fallback = [s["id"] for s, ss in zip(scenes, spec["scenes"]) if not s.get("visual") and ss["visual"]["template"] == "kinetic"
                and s.get("visual_form") not in ("kinetic_type", "title_card")]
    if fallback:
        rep.warnings.append(f"scenes {fallback} had no structured 'visual' and fell back to kinetic type")
    write_manifest(folder, rep.voice_source, rcfg, len(spec["scenes"]), renderer="motion",
                   extra_rows=[_clip3d_row(folder, c) for c in clips] + sound_rows)
    (render_dir / "render_report.json").write_text(json.dumps(rep.__dict__, indent=2) + "\n", encoding="utf-8")
    return rep


def _clip3d_row(folder: Path, clip: Any) -> list[str]:
    rel = clip.path.relative_to(folder).as_posix()
    return [f"G3D{clip.scene_id:02d}", rel, "generated_graphic", "", "AI Shorts Studio via HyperFrames + Three.js",
            "internal-generated", "", "no", f"3D scene {clip.scene_id}; procedural/CC0 models only; record any model licence here"]


def write_manifest(folder: Path, voice_source: str, rcfg: RenderConfig, frame_count: int, renderer: str = "cards",
                   extra_rows: list[list[str]] | None = None) -> None:
    font = Path(rcfg.style["font_bold"]).name
    if voice_source == "manual":
        voice_row = ["V001", "voiceover/voiceover.wav", "user_asset", "", "channel owner", "owner-recorded", "", "no", "User-recorded narration"]
    elif voice_source == "clone":
        voice_row = ["V001", "voiceover/narration.wav", "generated_audio", "https://github.com/resemble-ai/chatterbox",
                     "Chatterbox (Resemble AI) cloning the channel owner's own voice", "MIT (model); voice: channel owner, consented",
                     "https://github.com/resemble-ai/chatterbox/blob/master/LICENSE", "no",
                     "AI-cloned narration of the owner's voice from voice/reference.wav; disclose as synthetic; output carries Resemble PerTh watermark"]
    else:
        voice_row = ["V001", "voiceover/narration.wav", "generated_audio", "", "Windows SAPI", f"local TTS ({rcfg.tts_voice})", "", "no",
                     "PLACEHOLDER draft voice; replace with recorded or approved TTS before publishing"]
    visual_row = (
        ["F001", f"assets/motion/spec.json ({frame_count} scenes)", "generated_graphic", "", "AI Shorts Studio motion engine", "internal-generated", "", "no",
         "Motion graphics rendered by studio/motion/engine.html from storyboard"]
        if renderer == "motion" else
        ["F001", f"assets/frames/ ({frame_count} PNG)", "generated_graphic", "", "AI Shorts Studio render pipeline", "internal-generated", "", "no",
         "Text cards drawn by studio/visuals.py from storyboard"])
    rows = [
        visual_row,
        voice_row,
        ["T001", font, "font", "", "Microsoft (Windows system font)", "Windows system font", "", "no",
         "Verify Microsoft font terms for video use before publishing"],
    ] + list(extra_rows or [])
    path = folder / "assets" / "manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(COLUMNS)
        w.writerows(rows)


def fit_sapi_rate(scenes: list[dict[str, Any]], vo_dir: Path, rcfg: RenderConfig, cfg: ProductionConfig
                  ) -> tuple[list[float], int, list[list[tuple[int, int]]]]:
    """Synthesize every scene; step the SAPI rate up (max MAX_SAPI_RATE) until the draft fits the runtime cap.

    Deterministic: same text + config always picks the same rate. Raises if even the fastest allowed rate is too long,
    because the right fix then is a shorter script, not unintelligible speech.
    """
    limit = cfg.max_duration - RUNTIME_HEADROOM_SECONDS
    total = 0.0
    for rate in range(rcfg.tts_rate, max(rcfg.tts_rate, MAX_SAPI_RATE) + 1):
        trial = replace(rcfg, tts_rate=rate)
        speech, marks = [], []
        for s in scenes:
            wav = vo_dir / f"scene_{int(s['id']):02d}.wav"
            marks.append(synthesize_sapi(str(s["narration"]), wav, trial))
            speech.append(float(summarize(run_ffprobe(wav))["duration_seconds"]))
        total = sum(speech) + rcfg.scene_padding * len(scenes) + sum(scene_pauses(scenes))
        if total <= limit:
            return speech, rate, marks
    raise StudioError(f"Narration needs {total:.1f}s even at SAPI rate {MAX_SAPI_RATE}; shorten the script below {limit:g}s")


def render_production(folder: Path, cfg: ProductionConfig, rcfg: RenderConfig, voice: str = "auto") -> RenderReport:
    status = parse_status(load_status(folder / "status.json")["status"])
    if status.rank < Status.SCRIPT_READY.rank:
        raise StudioError(f"{folder.name} is {status.value}; render needs SCRIPT_READY or later")
    board = load_storyboard(folder / "storyboard.json", cfg, require_scenes=True)
    scenes = board["scenes"]
    manual = folder / MANUAL_VOICEOVER
    if voice == "auto":
        voice = "manual" if manual.is_file() else rcfg.tts_engine
    if voice == "manual" and not manual.is_file():
        raise StudioError(f"Manual voiceover requested but {manual} does not exist")
    if voice not in ("manual", "sapi", "clone"):
        raise StudioError(f"Unknown voice source '{voice}'")

    rep = RenderReport(video_id=folder.name, voice_source=voice)
    render_dir, vo_dir, frames_dir = folder / "render", folder / "voiceover", folder / "assets" / "frames"
    log = render_dir / "ffmpeg.log"
    log.unlink(missing_ok=True)
    for d in (render_dir, vo_dir):
        d.mkdir(exist_ok=True)
    archive_previous_render(render_dir)  # keep every earlier draft under render/versions/
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    a_rate = str(rcfg.audio_sample_rate)

    marks: list[list[tuple[int, int]]] = [[] for _ in scenes]
    local_words: list[list[WordTime]] | None = None
    if voice in ("sapi", "clone"):
        if voice == "sapi":
            speech, rate, marks = fit_sapi_rate(scenes, vo_dir, rcfg, cfg)
            rep.tts_rate = rate
        else:
            from .clone_voice import synthesize_scenes

            speech, local_words, tempo, summary = synthesize_scenes(
                scenes, vo_dir, rcfg, cfg, board.get("language_id", "en" if board.get("language") == "English" else "hi"),
                scene_pauses(scenes), RUNTIME_HEADROOM_SECONDS)
            rep.tempo = tempo
            rep.warnings.append(f"voice clone: {summary}; tempo {tempo}x")
        timings = plan_timings(speech, rcfg.scene_padding, rcfg.fps, scene_pauses(scenes))
        concat = vo_dir / "concat.txt"
        lines = []
        for s, tm in zip(scenes, timings):
            src = vo_dir / f"scene_{int(s['id']):02d}.wav"
            padded = vo_dir / f"scene_{int(s['id']):02d}_padded.wav"
            run_ffmpeg(["-i", str(src), "-af", f"apad=whole_dur={tm.end - tm.start:.6f}", "-t", f"{tm.end - tm.start:.6f}",
                        "-ar", a_rate, "-ac", "1", str(padded)], log)
            lines.append(f"file '{padded.resolve().as_posix()}'")
        concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
        narration = vo_dir / "narration.wav"
        run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(narration)], log)
    else:
        narration = manual
        timings = scaled_timings(scenes, float(summarize(run_ffprobe(manual))["duration_seconds"]), rcfg.fps)

    total = timings[-1].end
    if rcfg.renderer == "motion" and board.get("schema_version", 1) >= 2:
        return _finish_motion(folder, cfg, rcfg, board, timings, marks, narration, total, rep, log, local_words)
    cues = build_cues(scenes, timings, rcfg.style, rcfg.fps)
    srcs = source_lines((folder / "sources.md").read_text(encoding="utf-8"))
    renderer = CardRenderer(rcfg.style)
    frame_list = []
    for i, cue in enumerate(cues, start=1):
        scene = next(s for s in scenes if int(s["id"]) == cue.scene_id)
        sline = next((srcs[x] for x in scene["source_ids"] if x in srcs), "")
        png = frames_dir / f"f{i:03d}.png"
        metrics = renderer.render(str(scene["on_screen_text"]), cue.text, sline, cue.end / total, png)
        for p in readability_problems(metrics, rcfg.style):
            rep.errors.append(f"frame {png.name} ('{cue.text}'): {p}")
        frame_list.append(f"file '{png.resolve().as_posix()}'\nduration {cue.end - cue.start:.6f}")
    frame_list.append(f"file '{(frames_dir / f'f{len(cues):03d}.png').resolve().as_posix()}'")
    frames_txt = frames_dir / "frames.txt"
    frames_txt.write_text("\n".join(frame_list) + "\n", encoding="utf-8")
    (render_dir / "captions.srt").write_text(to_srt(cues), encoding="utf-8")

    out = render_dir / "draft.mp4"
    run_ffmpeg([
        "-f", "concat", "-safe", "0", "-i", str(frames_txt), "-i", str(narration),
        "-map", "0:v", "-map", "1:a", "-t", f"{total:.3f}",
        "-vf", f"fps={rcfg.fps},format=yuv420p", "-c:v", "libx264", "-preset", rcfg.preset, "-crf", str(rcfg.crf),
        "-af", f"{two_pass_loudnorm_filter(narration, rcfg)},aresample={a_rate}",
        "-c:a", "aac", "-b:a", rcfg.audio_bitrate, "-ac", "2", "-movflags", "+faststart", str(out),
    ], log)

    rep.output = out.relative_to(folder).as_posix()
    rep.probe = summarize(run_ffprobe(out), rep.output)
    rep.duration_seconds = rep.probe["duration_seconds"]
    rep.errors.extend(check_summary(rep.probe, cfg))
    if abs(rep.duration_seconds - total) > 0.25:
        rep.errors.append(f"output {rep.duration_seconds}s differs from planned {total:.2f}s")
    rep.scenes = [{"id": t.scene_id, "start": t.start, "speech": round(t.speech, 3), "end": t.end} for t in timings]
    rep.cues = len(cues)
    if voice == "sapi":
        rep.warnings.append("Voice is the Windows SAPI placeholder; record voiceover/voiceover.wav or approve a better local TTS before publishing")
    rep.warnings.append("Scene visuals are text cards; storyboard diagram descriptions are not drawn yet")
    write_manifest(folder, voice, rcfg, len(cues))
    (render_dir / "render_report.json").write_text(json.dumps(rep.__dict__, indent=2) + "\n", encoding="utf-8")
    return rep
