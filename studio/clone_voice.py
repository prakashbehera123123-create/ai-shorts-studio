"""Cloned-voice narration (channel owner's own voice) via scripts/clone_tts.py in the isolated .venv-voice.

The clone engine gives no word boundaries, so word timings are estimated from the generated audio itself:
speech start/end and internal pauses come from FFmpeg silencedetect; pauses are matched to punctuation;
words share each speech segment in proportion to their length.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT, ProductionConfig
from .errors import MediaToolError, StudioError
from .media import require_tool, run_ffprobe, summarize
from .render_config import RenderConfig
from .tts import WordTime, apply_pronunciations

CLONE_TIMEOUT_SECONDS = 3600
PAUSE_NOISE_DB = -40
PAUSE_MIN_SECONDS = 0.18
PUNCT = re.compile(r"[.,?!;:]$")


def detect_silences(wav: Path) -> list[tuple[float, float]]:
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-nostats", "-i", str(wav),
           "-af", f"silencedetect=noise={PAUSE_NOISE_DB}dB:d={PAUSE_MIN_SECONDS}", "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=False)
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    dur = float(summarize(run_ffprobe(wav))["duration_seconds"])
    if len(ends) < len(starts):
        ends.append(dur)
    return [(max(0.0, s), e) for s, e in zip(starts, ends)]


def estimate_word_times(words: list[str], silences: list[tuple[float, float]], duration: float) -> list[WordTime]:
    """Pause-aware word timing for audio without engine word boundaries."""
    if not words:
        return []
    speech_start, speech_end = 0.0, duration
    internal = []
    for s, e in silences:
        if s <= 0.05:
            speech_start = max(speech_start, e)
        elif e >= duration - 0.05:
            speech_end = min(speech_end, s)
        else:
            internal.append((s, e))
    internal = [(s, e) for s, e in internal if speech_start < s < speech_end]
    weights = [max(len(re.sub(r"[^\w]", "", w)), 1) + 1 for w in words]
    total_w = sum(weights)
    talk = max(speech_end - speech_start - sum(e - s for s, e in internal), 0.1)
    # nominal end time of each word if there were no pauses, to match pauses to punctuation boundaries
    acc, nominal = 0.0, []
    for w in weights:
        acc += w
        nominal.append(speech_start + talk * acc / total_w)
    boundaries = [i for i, w in enumerate(words[:-1]) if PUNCT.search(w)]
    assigned: dict[int, tuple[float, float]] = {}
    shift = 0.0
    for s, e in internal:
        cands = [b for b in boundaries if b not in assigned]
        if not cands:
            break
        b = min(cands, key=lambda i: abs(nominal[i] + shift - s))
        assigned[b] = (s, e)
        shift += e - s
    # build segments of words separated by assigned pauses
    out: list[WordTime] = []
    seg_start_t, seg_first = speech_start, 0
    cut_points = sorted(assigned)
    for idx, b in enumerate([*cut_points, len(words) - 1]):
        seg_end_t = assigned[b][0] if b in assigned else speech_end
        seg_words = range(seg_first, b + 1)
        seg_w = sum(weights[i] for i in seg_words) or 1
        t = seg_start_t
        for i in seg_words:
            d = (seg_end_t - seg_start_t) * weights[i] / seg_w
            out.append(WordTime(words[i], round(t, 3), round(t + d, 3)))
            t += d
        if b in assigned:
            seg_start_t = assigned[b][1]
        seg_first = b + 1
    return out


def _run_worker(jobs: list[dict[str, str]], rcfg: RenderConfig, work: Path, language: str) -> str:
    c = rcfg.clone
    py = PROJECT_ROOT / c.get("python", ".venv-voice/Scripts/python.exe")
    ref = PROJECT_ROOT / c.get("reference", "voice/reference.wav")
    if not py.is_file():
        raise StudioError(f"Voice-clone environment missing: {py} (see voice-and-sound skill)")
    if not ref.is_file():
        raise StudioError(f"Voice reference missing: {ref}")
    spec = {"reference": str(ref), "language": language, "exaggeration": c.get("exaggeration", 0.6),
            "cfg_weight": c.get("cfg_weight", 0.5), "seed": c.get("seed", 1234), "jobs": jobs}
    jf = work / "clone_jobs.json"
    jf.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    try:
        p = subprocess.run([str(py), str(PROJECT_ROOT / "scripts" / "clone_tts.py"), str(jf)], capture_output=True,
                           text=True, timeout=CLONE_TIMEOUT_SECONDS, shell=False, cwd=PROJECT_ROOT)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("voice clone timed out") from exc
    (work / "clone.log").write_text(p.stdout + "\n" + p.stderr[-6000:], encoding="utf-8")
    if p.returncode != 0:
        raise MediaToolError(f"voice clone failed: {p.stderr.strip()[-500:]}")
    return p.stdout.strip().splitlines()[0] if p.stdout.strip() else ""


def fit_tempo(total: float, limit: float, max_tempo: float) -> float:
    """Speed-up factor (>= 1) needed to fit `limit`; raises if it would exceed `max_tempo`."""
    if total <= limit:
        return 1.0
    factor = round(total / limit + 0.005, 3)
    if factor > max_tempo:
        raise StudioError(f"Cloned narration needs {total:.1f}s (> {limit:g}s even at {max_tempo}x); shorten the script")
    return factor


def cache_key(text: str, reference: Path, settings: dict[str, Any], seed: int, language: str) -> str:
    """Identity of one cloned take: same key -> reuse the cached WAV instead of re-cloning (~1 min per scene on CPU)."""
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    h.update(reference.read_bytes() if reference.is_file() else b"")
    h.update(json.dumps({k: settings.get(k) for k in ("exaggeration", "cfg_weight")}, sort_keys=True).encode())
    h.update(f"{seed}|{language}".encode())
    return h.hexdigest()[:16]


def pick_takes(recalls: dict[int, list[float]], min_recall: float) -> tuple[dict[int, int], list[int]]:
    """Best take index per scene (highest recall, earliest on ties) and the scenes still below `min_recall`."""
    best = {sid: max(range(len(r)), key=lambda i: (r[i], -i)) for sid, r in recalls.items()}
    weak = [sid for sid, r in recalls.items() if r[best[sid]] < min_recall]
    return best, weak


def prepare_reference(source: Path, out: Path, start: float, seconds: float, rcfg: RenderConfig) -> dict[str, Any]:
    """One-time reference clean-up: Demucs vocal isolation -> high-pass + light denoise -> trimmed mono clip.

    The clone reproduces whatever is in the reference (background music, hiss, rumble), so this runs before cloning.
    """
    from .audio_clean import noise_profile

    py = PROJECT_ROOT / rcfg.clone.get("python", ".venv-voice/Scripts/python.exe")
    work = out.parent / "demucs"
    cmd = [str(py), "-m", "demucs", "--two-stems=vocals", "-n", "htdemucs", "-o", str(work), str(source)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=CLONE_TIMEOUT_SECONDS, shell=False, cwd=PROJECT_ROOT)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("Demucs timed out") from exc
    if p.returncode != 0:
        raise MediaToolError(f"Demucs failed (is it installed in .venv-voice?): {p.stderr.strip()[-400:]}")
    vocals = work / "htdemucs" / source.stem / "vocals.wav"
    if not vocals.is_file():
        raise MediaToolError(f"Demucs produced no vocals stem at {vocals}")
    fade = max(seconds - 0.3, 0.0)
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-i", str(vocals),
           "-t", f"{seconds:.3f}", "-ac", "1", "-ar", "44100",
           "-af", f"highpass=f=90,afftdn=nr=10:nf=-45:tn=1,afade=t=out:st={fade:.3f}:d=0.3", str(out)]
    q = subprocess.run(cmd, capture_output=True, text=True, timeout=120, shell=False)
    if q.returncode != 0:
        raise MediaToolError(f"reference trim failed: {q.stderr[-300:]}")
    return {"reference": str(out), "before": noise_profile(source), "after": noise_profile(out)}


def synthesize_scenes(scenes: list[dict[str, Any]], vo_dir: Path, rcfg: RenderConfig, cfg: ProductionConfig,
                      language: str, scene_pauses: list[float], headroom: float) -> tuple[list[float], list[list[WordTime]], float, str]:
    """Clone-voice every scene; returns (speech durations, local word times, tempo, worker summary).

    Per scene: cached take reused when text/reference/settings match; every take is denoised; if a whisper model is
    available, takes whose script recall is below `min_recall` are re-cloned with a new seed (up to `retakes` times)
    and the best take is kept. Choices are written to voiceover/takes.json.
    """
    from .audio_clean import denoise
    from .compose import run_ffmpeg  # local import: compose imports this module lazily too
    from .qa import transcript_recall

    vo_dir.mkdir(parents=True, exist_ok=True)
    c = rcfg.clone
    ref = PROJECT_ROOT / c.get("reference", "voice/reference.wav")
    base_seed = int(c.get("seed", 1234))
    retakes = int(c.get("retakes", 0))
    min_recall = float(c.get("min_recall", 85))
    model = PROJECT_ROOT / "models" / "ggml-base.bin"
    check = retakes > 0 and model.is_file() and language == "en"
    texts = {int(s["id"]): apply_pronunciations(str(s["narration"]), rcfg.pronunciations) for s in scenes}
    takes: dict[int, list[Path]] = {int(s["id"]): [] for s in scenes}
    recalls: dict[int, list[float]] = {int(s["id"]): [] for s in scenes}
    summary, cached = "", 0
    pending = [int(s["id"]) for s in scenes]
    for attempt in range(retakes + 1):
        seed = base_seed + 1000 * attempt
        jobs = []
        for sid in pending:
            raw = vo_dir / f"scene_{sid:02d}_take{attempt}_raw.wav"
            key = cache_key(texts[sid], ref, c, seed + sid, language)
            keyfile = raw.with_suffix(".key")
            if raw.is_file() and keyfile.is_file() and keyfile.read_text(encoding="utf-8").strip() == key:
                cached += 1
            else:
                jobs.append({"text": texts[sid], "out": str(raw), "seed": seed + sid, "key": key})
        if jobs:
            summary = _run_worker([{"text": j["text"], "out": j["out"], "seed": j["seed"]} for j in jobs], rcfg, vo_dir, language)
            for j in jobs:
                Path(j["out"]).with_suffix(".key").write_text(j["key"], encoding="utf-8")
        for sid in pending:
            raw = vo_dir / f"scene_{sid:02d}_take{attempt}_raw.wav"
            clean = vo_dir / f"scene_{sid:02d}_take{attempt}_clean.wav"
            denoise(raw, clean)
            takes[sid].append(clean)
            narration = next(str(s["narration"]) for s in scenes if int(s["id"]) == sid)
            recalls[sid].append(transcript_recall(clean, narration, model, clean.with_suffix(".srt"))[0] if check else 100.0)
        _, pending = pick_takes(recalls, min_recall)
        if not check or not pending:
            break
    best, weak = pick_takes(recalls, min_recall)
    (vo_dir / "takes.json").write_text(json.dumps(
        {"min_recall": min_recall, "recall_checked": check, "cached_takes_reused": cached,
         "scenes": {str(sid): {"recalls": recalls[sid], "chosen_take": best[sid]} for sid in recalls},
         "below_min_recall": weak}, indent=2) + "\n", encoding="utf-8")
    chosen = [takes[int(s["id"])][best[int(s["id"])]] for s in scenes]
    summary = (summary or "all takes from cache") + f"; takes chosen by recall, {cached} cached" + (
        f"; scenes {weak} still below {min_recall:g}% recall" if weak else "")
    raw = chosen
    durs = [float(summarize(run_ffprobe(p))["duration_seconds"]) for p in raw]
    total = sum(durs) + rcfg.scene_padding * len(scenes) + sum(scene_pauses)
    tempo = fit_tempo(total, cfg.max_duration - headroom, float(rcfg.clone.get("max_tempo", 1.12)))
    log = vo_dir / "clone_ffmpeg.log"
    speech, words = [], []
    for s, src in zip(scenes, raw):
        out = vo_dir / f"scene_{int(s['id']):02d}.wav"
        # trim leading/trailing silence, apply tempo, mono 24 kHz (the padding step later resamples)
        af = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
        if tempo != 1.0:
            af += f",atempo={tempo}"
        run_ffmpeg(["-i", str(src), "-af", af, "-ac", "1", str(out)], log)
        d = float(summarize(run_ffprobe(out))["duration_seconds"])
        speech.append(d)
        words.append(estimate_word_times(str(s["narration"]).split(), detect_silences(out), d))
    return speech, words, tempo, summary
