"""Optional HyperFrames scenes (3D, or any registry block) rendered only for storyboard scenes that ask for one.

Templates: `scene3d` (Three.js hero, needs visual_form scene_3d) and `hyperframes` (any block/project).

A scene opts in with `"visual_form": "scene_3d"`, a `visual_justification`, and
`"visual": {"template": "scene3d", "project": "assets/3d/scene_04"}` — a HyperFrames project whose root is
1080 x 670 (the visual zone, y 560-1230) with a transparent background. Scenes without it never touch HyperFrames.

Each clip is cached by a hash of the project's files, so re-renders (voice/caption fixes) reuse it. The clip is laid
over the engine's empty visual zone for the scene's time range; if it is shorter, its last frame is held.
Template to start from: `pilots/3d-hero/index.html` (see the depth-and-3d skill).
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .compose_types import SceneTiming
from .errors import MediaToolError, StudioError
from .render_config import RenderConfig

ZONE_TOP, ZONE_WIDTH, ZONE_HEIGHT = 560, 1080, 670  # must match VZ in studio/motion/engine.html
SKIP_DIRS = {"renders", ".hyperframes", "node_modules"}
HF_TEMPLATES = frozenset({"scene3d", "hyperframes"})  # 3D scenes and any HyperFrames block in the visual zone


@dataclass(frozen=True)
class Clip3D:
    scene_id: int
    start: float
    end: float
    path: Path
    cached: bool


def scenes_needing_3d(board: dict[str, Any]) -> list[dict[str, Any]]:
    return [s for s in board["scenes"] if (s.get("visual") or {}).get("template") in HF_TEMPLATES]


def project_hash(project: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in project.rglob("*") if p.is_file() and not (SKIP_DIRS & set(p.relative_to(project).parts))):
        h.update(f.relative_to(project).as_posix().encode())
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


def check_project(project: Path) -> list[str]:
    """Static checks before spending render time."""
    index = project / "index.html"
    if not index.is_file():
        return [f"{project} has no index.html (copy pilots/3d-hero/index.html as a starting point)"]
    html = index.read_text(encoding="utf-8")
    problems = []
    w = re.search(r'data-width="(\d+)"', html)
    h = re.search(r'data-height="(\d+)"', html)
    if not (w and h and int(w.group(1)) == ZONE_WIDTH and int(h.group(1)) == ZONE_HEIGHT):
        problems.append(f"{project.name}: root must be data-width=\"{ZONE_WIDTH}\" data-height=\"{ZONE_HEIGHT}\" (the visual zone)")
    if "Math.random(" in html or "Date.now(" in html:
        problems.append(f"{project.name}: non-deterministic Math.random/Date.now")
    return problems


def _hf(rcfg: RenderConfig) -> list[str]:
    import os

    launcher = rcfg.hyperframes.get("launcher") or os.environ.get("HYPERFRAMES_LAUNCHER", "")  # set the env var on your PC
    node = shutil.which("node")
    if launcher and Path(launcher).is_file() and node:
        return [node, launcher]
    exe = shutil.which("hyperframes")
    if exe:
        return [exe]
    raise MediaToolError("HyperFrames is not available (set hyperframes.launcher in config/render.json)")


def _run_hf(cmd: list[str], project: Path, log: Path, timeout: int) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=project, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    with log.open("a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd)}\n{proc.stdout[-4000:]}\n{proc.stderr[-4000:]}\n")
    return proc


def render_3d_clips(folder: Path, board: dict[str, Any], timings: list[SceneTiming], rcfg: RenderConfig,
                    log: Path) -> list[Clip3D]:
    wanted = scenes_needing_3d(board)
    if not wanted:
        return []
    by_id = {t.scene_id: t for t in timings}
    hf = _hf(rcfg)
    clips = []
    for scene in wanted:
        sid = int(scene["id"])
        project = (folder / scene["visual"]["project"]).resolve()
        if folder.resolve() not in project.parents:
            raise StudioError(f"scene {sid}: visual.project must be inside the production folder")
        problems = check_project(project)
        if problems:
            raise StudioError("; ".join(problems))
        ext = rcfg.hyperframes.get("format", "mov")
        out = project / "renders" / f"clip_{project_hash(project)}.{ext}"
        cached = out.is_file()
        if not cached:
            check = _run_hf(hf + ["check", "--json"], project, log, 600)
            errors = _check_errors(check.stdout)
            if errors:
                raise StudioError(f"scene {sid}: hyperframes check found errors: {errors[:3]}")
            out.parent.mkdir(parents=True, exist_ok=True)
            proc = _run_hf(hf + ["render", "-o", str(out), "--format", ext, "--fps", str(rcfg.fps)], project, log, 1800)
            if proc.returncode != 0 or not out.is_file():
                raise MediaToolError(f"scene {sid}: hyperframes render failed (see {log.name})")
        t = by_id[sid]
        clips.append(Clip3D(sid, t.start, t.end, out, cached))
    return clips


def _check_errors(stdout: str) -> list[str]:
    start = stdout.find("{")
    try:
        data = json.loads(stdout[start:stdout.rfind("}") + 1]) if start >= 0 else {}
    except json.JSONDecodeError:
        return []
    found: list[str] = []

    def walk(o: Any) -> None:
        if isinstance(o, dict):
            if o.get("severity") == "error":
                found.append(f"{o.get('code')}: {str(o.get('message'))[:120]}")
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(data)
    return found


def overlay_filter(clips: list[Clip3D]) -> tuple[str, str]:
    """filter_complex laying each clip (input i+1) on the base video (input 0) in the visual zone."""
    parts, last = [], "0:v"
    for i, c in enumerate(clips, start=1):
        dur = max(0.04, c.end - c.start)
        parts.append(f"[{i}:v]tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},"
                     f"setpts=PTS-STARTPTS+{c.start:.3f}/TB,scale={ZONE_WIDTH}:{ZONE_HEIGHT}[c{i}]")
        nxt = f"v{i}"
        parts.append(f"[{last}][c{i}]overlay=0:{ZONE_TOP}:eof_action=pass:"
                     f"enable='between(t,{c.start:.3f},{c.end:.3f})'[{nxt}]")
        last = nxt
    return ";".join(parts), last


def apply_3d(silent: Path, clips: list[Clip3D], rcfg: RenderConfig, log: Path) -> Path:
    from .compose import run_ffmpeg  # local import: compose imports this module

    if not clips:
        return silent
    out = silent.with_name("video_silent_3d.mp4")
    graph, last = overlay_filter(clips)
    args = ["-i", str(silent)]
    for c in clips:
        args += ["-i", str(c.path)]
    args += ["-filter_complex", graph, "-map", f"[{last}]", "-c:v", "libx264", "-crf", str(rcfg.crf),
             "-preset", rcfg.preset, "-pix_fmt", "yuv420p", "-r", str(rcfg.fps), str(out)]
    run_ffmpeg(args, log)
    silent.unlink(missing_ok=True)
    out.replace(silent)
    return silent
