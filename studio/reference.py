"""Reference-video analysis: compact, model-friendly evidence from local video files.

Produces per video (in an output dir that must stay git-ignored, since references are third-party):
  summary.json        metadata, shot statistics, loudness, pauses, speech rate
  transcript.srt      local whisper.cpp transcript (FFmpeg `whisper` filter), if a model is available
  opening_sheet.jpg   first seconds at 2 fps (hook analysis)
  shots_sheet.jpg     one frame per detected shot (visual language and pacing)
Nothing is uploaded; nothing large is loaded into the model.
"""
from __future__ import annotations

import json
import re
import statistics
import subprocess
from pathlib import Path
from typing import Any

from .errors import MediaToolError
from .media import require_tool, run_ffprobe, summarize
from .qa import parse_loudness, parse_srt

ANALYSIS_TIMEOUT = 900
OPENING_SECONDS = 6
MAX_SHOT_FRAMES = 30


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", Path(name).stem.lower()).strip("-")
    return s[:60] or "video"


def _ff(args: list[str], cwd: Path | None = None) -> str:
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-nostats", *args]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=ANALYSIS_TIMEOUT, cwd=cwd, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("ffmpeg analysis timed out") from exc
    if p.returncode != 0:
        raise MediaToolError(f"ffmpeg failed: {(p.stderr or '')[-400:]}")
    return p.stderr or ""


SAMPLE_FPS = 4
THUMB_W, THUMB_H = 32, 56
LAG_FRAMES = 2  # compare with the frame 0.5 s earlier, so dissolves register as well as hard cuts
MIN_GAP_S = 0.75


def frame_differences(video: Path, band: tuple[float, float] | None = None) -> list[float]:
    """Mean absolute luma difference between each tiny frame and the one LAG_FRAMES earlier.

    `band` = (top, height) as fractions of frame height restricts the measurement to a horizontal band,
    e.g. the visual zone, so caption changes do not count as visual change.
    """
    crop = f"crop=iw:ih*{band[1]}:0:ih*{band[0]}," if band else ""
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-loglevel", "error", "-i", str(video),
           "-vf", f"fps={SAMPLE_FPS},{crop}scale={THUMB_W}:{THUMB_H},format=gray", "-f", "rawvideo", "-"]
    try:
        p = subprocess.run(cmd, capture_output=True, timeout=ANALYSIS_TIMEOUT, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("frame sampling timed out") from exc
    if p.returncode != 0:
        raise MediaToolError("frame sampling failed")
    size = THUMB_W * THUMB_H
    frames = [p.stdout[i:i + size] for i in range(0, len(p.stdout) - size + 1, size)]
    diffs = [0.0] * len(frames)
    for i in range(LAG_FRAMES, len(frames)):
        a, b = frames[i], frames[i - LAG_FRAMES]
        diffs[i] = sum(abs(x - y) for x, y in zip(a, b)) / size
    return diffs


def change_times(diffs: list[float], floor: float = 14.0) -> list[float]:
    """Local peaks above max(floor, 2.5 x median); peaks closer than MIN_GAP_S keep the larger one."""
    if not diffs:
        return []
    thr = max(floor, 2.5 * statistics.median(diffs))
    peaks: list[tuple[float, float]] = []
    for i in range(1, len(diffs) - 1):
        if diffs[i] >= thr and diffs[i] >= diffs[i - 1] and diffs[i] >= diffs[i + 1]:
            t = round((i - LAG_FRAMES / 2) / SAMPLE_FPS, 2)
            if t < MIN_GAP_S:  # comparisons against the first frames are start-up noise, not cuts
                continue
            if peaks and t - peaks[-1][0] < MIN_GAP_S:
                if diffs[i] > peaks[-1][1]:
                    peaks[-1] = (t, diffs[i])
                continue
            peaks.append((t, diffs[i]))
    return [t for t, _ in peaks]


def shot_stats(cuts: list[float], duration: float) -> dict[str, Any]:
    bounds = [0.0, *[c for c in cuts if 0 < c < duration], duration]
    shots = [round(b - a, 3) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]
    first10 = sum(1 for c in cuts if c < 10)
    return {
        "cuts": len(shots) - 1,
        "shots": len(shots),
        "mean_shot_s": round(statistics.mean(shots), 2) if shots else None,
        "median_shot_s": round(statistics.median(shots), 2) if shots else None,
        "longest_shot_s": max(shots) if shots else None,
        "cuts_first_10s": first10,
        "cuts_per_10s_overall": round((len(shots) - 1) / duration * 10, 2) if duration else None,
        "shot_bounds": bounds,
    }


def parse_pauses(stderr: str) -> list[float]:
    return [float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", stderr)]


def speech_stats(srt_text: str) -> dict[str, Any]:
    cues = parse_srt(srt_text)
    words = sum(len(re.findall(r"\S+", c[2])) for c in cues)
    speech = sum(max(0.0, b - a) for a, b, _ in cues)
    first = cues[0][0] if cues else None
    return {"transcript_words": words, "transcribed_speech_s": round(speech, 1),
            "words_per_minute": round(words / speech * 60) if speech else None, "first_speech_at_s": first}


def _sheet(video: Path, times: list[float], out: Path, cols: int, width: int = 200) -> None:
    """Grid of stills with timestamp labels (Pillow), from frames extracted one by one with FFmpeg."""
    from PIL import Image, ImageDraw

    if not times:
        return
    tmp = out.parent / "_tmp_frames"
    tmp.mkdir(parents=True, exist_ok=True)
    tiles = []
    for i, t in enumerate(times):
        f = tmp / f"{i:03d}.jpg"
        _ff(["-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "5", str(f)])
        with Image.open(f) as im:
            tile = im.convert("RGB")
        d = ImageDraw.Draw(tile)
        d.rectangle([0, 0, 52, 16], fill=(0, 0, 0))
        d.text((3, 2), f"{t:.1f}s", fill=(255, 220, 0))
        tiles.append(tile)
        f.unlink()
    tmp.rmdir()
    tw, th = tiles[0].size
    rows = -(-len(tiles) // cols)
    sheet = Image.new("RGB", (cols * tw, rows * th))
    for i, tile in enumerate(tiles):
        sheet.paste(tile.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(out, quality=80)


def analyze_video(video: Path, out_root: Path, project_root: Path, model: Path | None) -> dict[str, Any]:
    out = out_root / slug(video.name)
    out.mkdir(parents=True, exist_ok=True)
    probe = summarize(run_ffprobe(video), video.name)
    dur = float(probe["duration_seconds"])
    fps_line = next((s.get("r_frame_rate") for s in run_ffprobe(video).get("streams", []) if s.get("codec_type") == "video"), None)

    cuts = change_times(frame_differences(video))
    shots = shot_stats(cuts, dur)
    ebur = _ff(["-i", str(video), "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"])
    lufs, peak = parse_loudness(ebur)
    lra_match = re.search(r"LRA:\s*([\d.]+)\s*LU", ebur[ebur.rfind("Summary:"):])
    lra_m = float(lra_match.group(1)) if lra_match else None
    pauses = parse_pauses(_ff(["-i", str(video), "-af", "silencedetect=noise=-35dB:d=0.25", "-vn", "-f", "null", "-"]))

    speech: dict[str, Any] = {}
    srt = out / "transcript.srt"
    if model and model.is_file():
        rel_model = model.resolve().relative_to(project_root).as_posix()
        rel_srt = srt.resolve().relative_to(project_root).as_posix()
        _ff(["-y", "-i", str(video.resolve()), "-vn", "-af",
             f"aresample=16000,whisper=model={rel_model}:language=auto:queue=10:destination={rel_srt}:format=srt",
             "-f", "null", "-"], cwd=project_root)
        if srt.is_file():
            speech = speech_stats(srt.read_text(encoding="utf-8", errors="replace"))

    opening = [i / 2 for i in range(OPENING_SECONDS * 2)]
    _sheet(video, opening, out / "opening_sheet.jpg", cols=6)
    b = shots["shot_bounds"]
    mids = [round((x + y) / 2, 2) for x, y in zip(b, b[1:])]
    if len(mids) > MAX_SHOT_FRAMES:
        step = len(mids) / MAX_SHOT_FRAMES
        mids = [mids[int(i * step)] for i in range(MAX_SHOT_FRAMES)]
    _sheet(video, mids, out / "shots_sheet.jpg", cols=6)

    summary = {
        "file": video.name, "duration_s": round(dur, 2), "width": probe["width"], "height": probe["height"],
        "fps": fps_line, "video_codec": probe["video_codec"], "audio_codec": probe["audio_codec"],
        "orientation": "vertical" if (probe["height"] or 0) > (probe["width"] or 0) else "horizontal",
        "shots": {k: v for k, v in shots.items() if k != "shot_bounds"},
        "cut_times_s": cuts,
        "loudness_lufs": lufs, "true_peak_dbfs": peak, "loudness_range_lu": lra_m,
        "pauses_over_0_25s": len(pauses), "mean_pause_s": round(statistics.mean(pauses), 2) if pauses else None,
        **speech,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary
