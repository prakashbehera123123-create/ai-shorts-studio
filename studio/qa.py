"""Technical QA (code), editorial QA intake (agent-written qa/editorial.md) and qa_report.md assembly.

Nothing here uploads, schedules or publishes. The final state is READY_FOR_HUMAN_REVIEW.
"""
from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import ContractError, MediaToolError
from .manifest import read_manifest
from .media import check_summary, require_tool, run_ffprobe, summarize
from .script import check_fact_check, check_script, parse_sections

LOUDNESS_RANGE = (-15.0, -13.0)  # docs/CREATIVE_PRODUCTION_STANDARD.md §1: -14 LUFS ±1
MAX_TRUE_PEAK = -1.0
LONG_SILENCE_SECONDS = 1.5
MIN_CUE_SECONDS = 0.5
MAX_CHARS_PER_SECOND = 22.0
QA_TIMEOUT_SECONDS = 300
SRT_TIME = re.compile(r"(\d+):(\d+):(\d+),(\d+)")
VISUAL_BAND = (540 / 1920, 690 / 1920)  # visual zone of the layout grid
STATIC_DIFF = 1.0                       # mean luma change below this (0-255 scale, 0.5 s lag) counts as static
MAX_STATIC_BLOCKER = 6.0
MAX_STATIC_WARN = 3.0
MIN_RECALL = 90.0
MAX_CAPTION_START = 0.3
MAX_CAPTION_GAP = 0.75
MAX_CAPTION_TAIL = 1.0
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    severity: str = "blocker"  # blocker | warning


@dataclass
class TechnicalQA:
    video_id: str
    checks: list[Check] = field(default_factory=list)
    measurements: dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks if c.severity == "blocker")

    def add(self, name: str, passed: bool, detail: str, severity: str = "blocker") -> None:
        self.checks.append(Check(name, passed, detail, severity))


def _ffmpeg_stderr(args: list[str]) -> str:
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-nostats", *args]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=QA_TIMEOUT_SECONDS, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise MediaToolError("ffmpeg analysis timed out") from exc
    if p.returncode != 0:
        raise MediaToolError(f"ffmpeg analysis failed: {(p.stderr or '')[-300:]}")
    return p.stderr or ""


def parse_loudness(stderr: str) -> tuple[float, float]:
    """Integrated loudness (LUFS) and true peak (dBFS) from the ebur128 summary block."""
    summary = stderr[stderr.rfind("Summary:"):] if "Summary:" in stderr else stderr
    i = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", summary)
    pk = re.search(r"Peak:\s*(-?[\d.]+|-inf)\s*dBFS", summary)
    if not i or not pk:
        raise MediaToolError("could not parse ebur128 output")
    peak = float("-inf") if pk.group(1) == "-inf" else float(pk.group(1))
    return float(i.group(1)), peak


def parse_silences(stderr: str) -> list[float]:
    return [float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", stderr)]


def _srt_seconds(ts: str) -> float:
    m = SRT_TIME.match(ts.strip())
    if not m:
        raise ValueError(ts)
    h, mi, s, ms = (int(x) for x in m.groups())
    return h * 3600 + mi * 60 + s + ms / 1000


def parse_srt(text: str) -> list[tuple[float, float, str]]:
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = lines[1].split("-->")
            cues.append((_srt_seconds(a), _srt_seconds(b), " ".join(lines[2:])))
    return cues


def caption_problems(cues: list[tuple[float, float, str]], duration: float) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not cues:
        return ["captions.srt has no cues"], []
    # Word-timed captions may blank during real pauses; they must start with the speech and never leave long holes.
    if cues[0][0] > MAX_CAPTION_START:
        errors.append(f"captions start at {cues[0][0]}s (speech must be captioned from <= {MAX_CAPTION_START}s)")
    if cues[-1][1] < duration - MAX_CAPTION_TAIL:
        errors.append(f"captions end at {cues[-1][1]}s but video is {duration}s")
    for (a0, a1, _), (b0, _b1, _) in zip(cues, cues[1:]):
        if b0 - a1 > MAX_CAPTION_GAP:
            errors.append(f"caption gap {a1}s-{b0}s longer than {MAX_CAPTION_GAP}s")
    for start, end, text in cues:
        dur = end - start
        if dur < MIN_CUE_SECONDS:
            warnings.append(f"cue '{text}' shows for only {dur:.2f}s")
        elif len(text) / dur > MAX_CHARS_PER_SECOND:
            warnings.append(f"cue '{text}' needs {len(text) / dur:.0f} chars/s reading speed")
    return errors, warnings


def sample_frames(video: Path, scenes: list[dict[str, Any]], out_dir: Path) -> list[Path]:
    """One small JPEG per scene midpoint, plus a contact sheet. Only these stills are shown to reviewers."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for s in scenes:
        mid = (float(s["start"]) + float(s["end"])) / 2
        p = out_dir / f"scene_{int(s['id']):02d}.jpg"
        _ffmpeg_stderr(["-y", "-ss", f"{mid:.3f}", "-i", str(video), "-frames:v", "1", "-vf", "scale=540:960", "-q:v", "4", str(p)])
        paths.append(p)
    cols = min(5, len(paths))
    rows = -(-len(paths) // cols)
    sheet = out_dir.parent / "contact_sheet.jpg"
    inputs: list[str] = []
    for p in paths:
        inputs += ["-i", str(p)]
    pads = "".join(f"[{i}:v]scale=216:384[s{i}];" for i in range(len(paths)))
    labels = "".join(f"[s{i}]" for i in range(len(paths)))
    layout = "|".join(f"{(i % cols) * 216}_{(i // cols) * 384}" for i in range(len(paths)))
    _ffmpeg_stderr(["-y", *inputs, "-filter_complex", f"{pads}{labels}xstack=inputs={len(paths)}:layout={layout}:fill=black",
                    "-frames:v", "1", "-q:v", "4", str(sheet)])
    if rows < 1:
        raise MediaToolError("no frames sampled")
    return paths


def visual_cadence(video: Path) -> tuple[float, float]:
    """(longest stretch in s with no change in the visual zone, % of time the visual zone is changing).

    Measured on the visual zone only (docs/CREATIVE_PRODUCTION_STANDARD.md §4.3) so caption swaps do not count.
    """
    from .reference import SAMPLE_FPS, frame_differences

    diffs = frame_differences(video, VISUAL_BAND)[2:]
    run = best = active = 0
    for d in diffs:
        run = run + 1 if d < STATIC_DIFF else 0
        best = max(best, run)
        active += d >= STATIC_DIFF
    return round(best / SAMPLE_FPS, 2), round(100 * active / max(len(diffs), 1), 1)


NUMBER_WORDS = {str(i): w for i, w in enumerate("zero one two three four five six seven eight nine ten".split())}


def _speech_norm(w: str) -> str:
    w = re.sub(r"[^a-z0-9]", "", w.lower())
    w = NUMBER_WORDS.get(w, w)
    return re.sub(r"our$", "or", w)  # behaviour/behavior


def transcript_recall(video: Path, spoken_text: str, model: Path, out_srt: Path) -> tuple[float, list[str]]:
    """% of script words found in a local whisper transcript (adjacent transcript words are also joined, so
    'change log' matches 'changelog'). Advisory: catches missing or garbled narration."""
    out_srt.parent.mkdir(parents=True, exist_ok=True)
    rel_model = model.resolve().relative_to(PROJECT_ROOT).as_posix()
    rel_out = out_srt.resolve().relative_to(PROJECT_ROOT).as_posix()
    cmd = [require_tool("ffmpeg"), "-hide_banner", "-nostdin", "-y", "-i", str(video.resolve()), "-vn", "-af",
           f"aresample=16000,whisper=model={rel_model}:language=en:queue=10:destination={rel_out}:format=srt", "-f", "null", "-"]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=QA_TIMEOUT_SECONDS, cwd=PROJECT_ROOT, shell=False, check=True)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
        raise MediaToolError("whisper transcription failed") from exc
    heard_words = [_speech_norm(w) for c in parse_srt(out_srt.read_text(encoding="utf-8", errors="replace")) for w in c[2].split()]
    heard = set(heard_words) | {a + b for a, b in zip(heard_words, heard_words[1:])}
    script = [w for w in (_speech_norm(x) for x in spoken_text.split()) if w]
    missing = [w for w in script if w not in heard and not any(p in heard for p in re.findall(r"[a-z]+|\d+", w))]
    return round(100 * (1 - len(missing) / max(len(script), 1)), 1), sorted(set(missing))


def run_technical_qa(folder: Path, cfg: ProductionConfig) -> TechnicalQA:
    qa = TechnicalQA(video_id=folder.name)
    video = folder / "render" / "draft.mp4"
    if not video.is_file():
        qa.add("draft exists", False, "render/draft.mp4 missing")
        return qa
    summary = summarize(run_ffprobe(video), "render/draft.mp4")
    qa.measurements["probe"] = summary
    spec = check_summary(summary, cfg)
    qa.add("format spec (1080x1920, H.264/AAC, 25-55s)", not spec, "; ".join(spec) or
           f"{summary['width']}x{summary['height']} {summary['video_codec']}/{summary['audio_codec']} {summary['duration_seconds']}s")

    lufs, peak = parse_loudness(_ffmpeg_stderr(["-i", str(video), "-af", "ebur128=peak=true", "-f", "null", "-"]))
    qa.measurements.update(loudness_lufs=lufs, true_peak_dbfs=peak)
    qa.add("integrated loudness", LOUDNESS_RANGE[0] <= lufs <= LOUDNESS_RANGE[1], f"{lufs} LUFS (allowed {LOUDNESS_RANGE[0]} to {LOUDNESS_RANGE[1]})")
    qa.add("true peak / clipping", peak <= MAX_TRUE_PEAK, f"{peak} dBFS (max {MAX_TRUE_PEAK})")

    silences = parse_silences(_ffmpeg_stderr(["-i", str(video), "-af", f"silencedetect=noise=-45dB:d={LONG_SILENCE_SECONDS}", "-f", "null", "-"]))
    qa.measurements["long_silences"] = silences
    qa.add("no long silences", not silences, f"{len(silences)} silence(s) >= {LONG_SILENCE_SECONDS}s" if silences else "none")

    srt = folder / "render" / "captions.srt"
    if srt.is_file():
        errs, warns = caption_problems(parse_srt(srt.read_text(encoding="utf-8")), summary["duration_seconds"])
        qa.add("captions cover full timeline", not errs, "; ".join(errs) or "contiguous, 0 to end")
        qa.add("caption reading speed", not warns, "; ".join(warns) or f"all cues >= {MIN_CUE_SECONDS}s and <= {MAX_CHARS_PER_SECOND:g} chars/s", "warning")
    else:
        qa.add("captions present", False, "render/captions.srt missing")

    report_path = folder / "render" / "render_report.json"
    render_report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else {}
    qa.add("render report clean", report_path.is_file() and not render_report.get("errors"),
           "; ".join(render_report.get("errors", [])) or ("no errors" if report_path.is_file() else "missing"))
    for w in render_report.get("warnings", []):
        qa.add("render warning", False, w, "warning")
    if render_report.get("scenes"):
        frames = sample_frames(video, render_report["scenes"], folder / "qa" / "frames")
        qa.measurements["sampled_frames"] = [p.relative_to(folder).as_posix() for p in frames]

    longest, active = visual_cadence(video)
    qa.measurements.update(longest_static_s=longest, visual_activity_pct=active)
    qa.add("visual cadence (no static visual zone > 6 s)", longest <= MAX_STATIC_BLOCKER,
           f"longest static stretch {longest:.2f}s, visual zone active {active:.0f}% of the time")
    if MAX_STATIC_WARN < longest <= MAX_STATIC_BLOCKER:
        qa.add("visual cadence target (1-3 s)", False, f"longest static stretch {longest:.2f}s exceeds {MAX_STATIC_WARN:g}s", "warning")

    rep = check_script(folder, cfg)
    model = PROJECT_ROOT / "models" / "ggml-base.bin"
    if model.is_file() and rep.language == "English":
        sections = parse_sections((folder / "script.md").read_text(encoding="utf-8"))
        spoken = " ".join(sections.get(s, "") for s in ("hook", "narration", "cta"))
        recall, missing = transcript_recall(video, spoken, model, folder / "qa" / "transcript.srt")
        qa.measurements["transcript_recall_pct"] = recall
        qa.add("audio matches script (whisper recall >= 90%)", recall >= MIN_RECALL,
               f"{recall:.0f}% of script words heard" + (f"; not heard: {', '.join(missing[:8])}" if missing else ""), "warning")
    fact = check_fact_check(folder, rep.claims) if rep.claims else ["no claims"]
    qa.add("script/storyboard contract", not rep.errors, "; ".join(rep.errors) or f"{rep.spoken_words} words, {rep.claims and len(rep.claims)} mapped claims")
    qa.add("fact check (no unsupported claims)", not fact, "; ".join(fact) or "all claims supported/qualified")

    try:
        rows = read_manifest(folder / "assets" / "manifest.csv", require_rows=True)
        qa.add("asset rights recorded", True, f"{len(rows)} manifest rows valid")
        for r in rows:
            if "PLACEHOLDER" in r["notes"].upper() or "verify" in r["notes"].lower():
                qa.add("rights/quality note", False, f"{r['asset_id']} {r['filename']}: {r['notes']}", "warning")
    except ContractError as exc:
        qa.add("asset rights recorded", False, "; ".join(exc.problems))

    (folder / "qa").mkdir(exist_ok=True)
    (folder / "qa" / "technical.json").write_text(
        json.dumps({"video_id": qa.video_id, "passed": qa.passed, "measurements": qa.measurements,
                    "checks": [asdict(c) for c in qa.checks]}, indent=2) + "\n", encoding="utf-8")
    return qa


# ------------------------------------------------------------------ editorial

def parse_editorial(text: str) -> tuple[str, list[str], list[str]]:
    """qa/editorial.md -> (decision, blockers, warnings). Decision line: 'Decision: PASS' or 'Decision: FAIL'."""
    m = re.search(r"^Decision:\s*(PASS|FAIL)\s*$", text, re.M | re.I)
    decision = m.group(1).upper() if m else ""

    def bullets(heading: str) -> list[str]:
        sec = re.search(rf"^##\s+{heading}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
        items = re.findall(r"^\s*-\s+(.+)$", sec.group(1), re.M) if sec else []
        # "- none", "- None.", "- none. Checked: ..." all mean "nothing here"; reviewers often add their reasoning.
        return [i.strip() for i in items if not re.match(r"none\b", i.strip(), re.I)]

    return decision, bullets("Blockers"), bullets("Warnings")


def editorial_problems(folder: Path) -> list[str]:
    path = folder / "qa" / "editorial.md"
    if not path.is_file():
        return ["missing qa/editorial.md (run the video-reviewer)"]
    decision, blockers, _ = parse_editorial(path.read_text(encoding="utf-8"))
    problems = []
    if decision != "PASS":
        problems.append(f"editorial decision is '{decision or 'missing'}', not PASS")
    problems.extend(f"editorial blocker: {b}" for b in blockers)
    return problems


def technical_problems(folder: Path) -> list[str]:
    path = folder / "qa" / "technical.json"
    if not path.is_file():
        return ["missing qa/technical.json (run python -m studio qa)"]
    data = json.loads(path.read_text(encoding="utf-8"))
    return [f"technical: {c['name']}: {c['detail']}" for c in data["checks"] if c["severity"] == "blocker" and not c["passed"]]


def write_qa_report(folder: Path) -> str:
    tech = json.loads((folder / "qa" / "technical.json").read_text(encoding="utf-8"))
    ed_path = folder / "qa" / "editorial.md"
    decision, blockers, ed_warnings = parse_editorial(ed_path.read_text(encoding="utf-8")) if ed_path.is_file() else ("", [], [])
    tech_blockers = [c for c in tech["checks"] if c["severity"] == "blocker" and not c["passed"]]
    warnings = [c["detail"] for c in tech["checks"] if c["severity"] == "warning" and not c["passed"]] + ed_warnings
    overall = "PASS" if tech["passed"] and decision == "PASS" and not blockers else "FAIL"
    m = tech["measurements"]
    lines = [
        f"# QA report: {folder.name}", "",
        f"Overall: **{overall}** · Technical: {'PASS' if tech['passed'] else 'FAIL'} · Editorial: {decision or 'NOT RUN'}", "",
        "## Technical (generated by `python -m studio qa`)", "",
        "| check | result | detail |", "|---|---|---|",
        *[f"| {c['name']} | {'pass' if c['passed'] else ('WARN' if c['severity'] == 'warning' else 'FAIL')} | {c['detail'].replace('|', '/')} |"
          for c in tech["checks"]],
        "", f"Loudness {m.get('loudness_lufs')} LUFS, true peak {m.get('true_peak_dbfs')} dBFS. Sampled frames: `qa/frames/`, contact sheet: `qa/contact_sheet.jpg`.",
        "", "## Editorial (from `qa/editorial.md`)", "",
        "### Blockers", *([f"- {b}" for b in blockers] or ["- none"]),
        *[f"- {c['name']}: {c['detail']}" for c in tech_blockers],
        "", "### Warnings", *([f"- {w}" for w in warnings] or ["- none"]),
        "", "## Human review checklist (must be done by a person; this project never publishes)",
        "- [ ] Watch the full draft with sound on a phone",
        "- [ ] Open every URL in sources.md and confirm the claims",
        "- [ ] Decide on the voice (SAPI placeholder vs recorded) and font terms",
        "- [ ] Edit title/description in metadata.md if needed",
        "- [ ] Upload manually in YouTube Studio only if you approve",
        "",
    ]
    text = "\n".join(lines)
    (folder / "qa_report.md").write_text(text, encoding="utf-8")
    return overall
