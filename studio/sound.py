"""Sound design: a quiet music bed ducked under the voice, and sparse SFX at scene changes.

Library: `assets/library/audio/`
- `generated/` — self-made with FFmpeg (whoosh, pop, tick, rise, knock, bed). No third-party rights; regenerated on demand.
- `music/` and `sfx/` — owner-downloaded files (YouTube Audio Library, Pixabay, Freesound CC0). A file is used only if it
  has a row in `LICENSES.csv` (file, source_url, creator, license). Downloaded music is preferred over the generated bed.

Standard: docs/CREATIVE_PRODUCTION_STANDARD.md §8 — voice ≥ 12 dB above the bed, at most one SFX per beat change.
"""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .compose_types import SceneTiming
from .config import PROJECT_ROOT
from .render_config import RenderConfig

LIBRARY = PROJECT_ROOT / "assets" / "library" / "audio"
SR = 48000

# name -> FFmpeg lavfi source graph (mono 48 kHz). Deterministic: anoisesrc uses a fixed seed.
GENERATORS: dict[str, str] = {
    "whoosh": "anoisesrc=d=0.7:c=pink:a=0.7:seed=11,highpass=f=300,lowpass=f=5000,"
              "afade=t=in:d=0.42:curve=exp,afade=t=out:st=0.42:d=0.28",
    "pop": "sine=f=740:d=0.14,afade=t=out:st=0.005:d=0.135:curve=exp,volume=0.9",
    "tick": "sine=f=2200:d=0.05,afade=t=out:st=0.002:d=0.048,volume=0.6",
    "rise": "aevalsrc='0.35*sin(2*PI*(180*t+260*t*t))':d=1.0,afade=t=in:d=0.8:curve=exp,afade=t=out:st=0.85:d=0.15",
    "knock": "aevalsrc='0.9*sin(2*PI*110*t)*exp(-38*t)+0.9*sin(2*PI*110*(t-0.18))*exp(-38*(t-0.18))*gte(t,0.18)':d=0.45",
    # ambient pad: A minor <-> F major every 4 s, slow swell; 64 s, looped by the mixer
    "bed": "aevalsrc='0.10*(sin(2*PI*110*t)+0.7*sin(2*PI*220*t)"
           "+0.5*sin(2*PI*if(lt(mod(t,8),4),261.63,349.23)*t)+0.5*sin(2*PI*if(lt(mod(t,8),4),329.63,440)*t))"
           "*(0.75+0.25*sin(2*PI*t/8))':d=64,lowpass=f=1800,afade=t=in:d=1.5",
}
# which cue a transition gets when the storyboard does not name one
TRANSITION_SFX = {"push": "whoosh", "zoom_through": "whoosh", "match_cut": "rise", "wipe": "whoosh", "crossfade": "tick"}
MAX_SFX_PER_30S = 5


@dataclass(frozen=True)
class SfxCue:
    time: float
    name: str
    path: Path


def generate_library(force: bool = False) -> dict[str, Path]:
    from .compose import run_ffmpeg

    out_dir = LIBRARY / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    log = out_dir / "generate.log"
    paths = {}
    for name, graph in GENERATORS.items():
        out = out_dir / f"{name}.wav"
        if force or not out.is_file():
            run_ffmpeg(["-f", "lavfi", "-i", f"{graph}", "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(out)], log)
        paths[name] = out
    return paths


def licensed_files(kind: str) -> list[Path]:
    """Owner-downloaded files of `kind` (music|sfx) that have a licence row."""
    folder, sheet = LIBRARY / kind, LIBRARY / "LICENSES.csv"
    if not folder.is_dir() or not sheet.is_file():
        return []
    with sheet.open(encoding="utf-8") as fh:
        ok = {row["file"].strip() for row in csv.DictReader(fh) if row.get("license", "").strip()}
    return sorted(p for p in folder.iterdir() if p.is_file() and f"{kind}/{p.name}" in ok)


def licence_row(path: Path) -> dict[str, str]:
    sheet = LIBRARY / "LICENSES.csv"
    rel = path.relative_to(LIBRARY).as_posix()
    if sheet.is_file():
        with sheet.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["file"].strip() == rel:
                    return row
    return {"file": rel, "source_url": "", "creator": "AI Shorts Studio (generated with FFmpeg)", "license": "self-generated"}


def pick_bed(video_id: str, generated: dict[str, Path]) -> Path:
    music = licensed_files("music")
    if not music:
        return generated["bed"]
    return music[int(hashlib.sha256(video_id.encode()).hexdigest(), 16) % len(music)]


def sfx_path(name: str, generated: dict[str, Path]) -> Path | None:
    for p in licensed_files("sfx"):
        if p.stem.lower().startswith(name.lower()):
            return p
    return generated.get(name)


def plan_sfx(board: dict[str, Any], timings: list[SceneTiming], generated: dict[str, Path], auto: bool) -> list[SfxCue]:
    """One cue at most per scene start: the storyboard's `sfx` name, else a transition default (when `auto`)."""
    by_id = {t.scene_id: t for t in timings}
    cues: list[SfxCue] = []
    prev_beat = None
    prev_speech_end = 0.0
    for i, s in enumerate(board["scenes"]):
        t = by_id[int(s["id"])]
        speech_end, prev_speech_end = prev_speech_end, t.start + t.speech
        names = [str(x) for x in (s.get("sfx") or [])]
        name = names[0] if names else None
        if name is None and auto and i > 0:
            name = TRANSITION_SFX.get(str(s.get("transition_in", "")))
            if name is None and s.get("beat") != prev_beat:
                name = "pop"
        prev_beat = s.get("beat")
        path = sfx_path(name, generated) if name else None
        if path is not None:
            # whoosh/rise lead into the cut; pops/ticks land on it
            # whoosh/rise lead into the cut, but only inside the pause: never over the previous scene's last word
            lead = 0.35 if name in ("whoosh", "rise") else 0.0
            start = max(t.start - lead, min(t.start, speech_end + 0.05))
            cues.append(SfxCue(max(0.0, round(start, 3)), name, path))
    return _thin(cues)


def _thin(cues: list[SfxCue]) -> list[SfxCue]:
    """Keep at most MAX_SFX_PER_30S in any 30 s window (earliest first)."""
    kept: list[SfxCue] = []
    for c in sorted(cues, key=lambda c: c.time):
        if sum(1 for k in kept if c.time - k.time < 30) < MAX_SFX_PER_30S:
            kept.append(c)
    return kept


def mix_filter(n_sfx: int, total: float, bed_db: float, sfx_db: float, cues: list[SfxCue]) -> str:
    """Inputs: 0 narration, 1 bed, 2.. sfx. Bed is looped, ducked by the voice (sidechain), SFX delayed to their cues."""
    parts = [
        f"[0:a]aresample={SR},aformat=channel_layouts=stereo,asplit=2[voice][key]",
        f"[1:a]aresample={SR},aformat=channel_layouts=stereo,aloop=loop=-1:size=2147483647,atrim=duration={total:.3f},"
        f"volume={bed_db}dB,afade=t=out:st={max(0.0, total - 1.5):.3f}:d=1.5[bedraw]",
        "[bedraw][key]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=500:makeup=1[bed]",
    ]
    labels = ["[voice]", "[bed]"]
    for i, c in enumerate(cues):
        ms = int(round(c.time * 1000))
        parts.append(f"[{i + 2}:a]aresample={SR},aformat=channel_layouts=stereo,volume={sfx_db}dB,adelay={ms}|{ms}[s{i}]")
        labels.append(f"[s{i}]")
    parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first[mix]")
    return ";".join(parts)


def build_mix(narration: Path, out: Path, board: dict[str, Any], timings: list[SceneTiming], total: float,
              video_id: str, rcfg: RenderConfig, log: Path) -> tuple[Path, list[SfxCue], Path]:
    from .compose import run_ffmpeg

    cfg = rcfg.sound
    generated = generate_library()
    bed = pick_bed(video_id, generated)
    cues = plan_sfx(board, timings, generated, bool(cfg.get("auto_sfx", True)))
    args = ["-i", str(narration), "-i", str(bed)]
    for c in cues:
        args += ["-i", str(c.path)]
    args += ["-filter_complex", mix_filter(len(cues), total, float(cfg.get("bed_db", -22)), float(cfg.get("sfx_db", -10)), cues),
             "-map", "[mix]", "-ar", str(SR), "-c:a", "pcm_s16le", str(out)]
    run_ffmpeg(args, log)
    return out, cues, bed
