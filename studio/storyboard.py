"""storyboard.json contract."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import ContractError
from .manifest import VISUAL_TYPES as _VISUAL_TYPES

VISUAL_TYPES = _VISUAL_TYPES
REQUIRED_SCENE_KEYS = ("id", "start_seconds", "end_seconds", "narration", "on_screen_text", "visual_type", "source_ids")
EPSILON = 1e-6


def _num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_storyboard_data(data: Any, cfg: ProductionConfig, require_scenes: bool = False) -> list[str]:
    if not isinstance(data, dict):
        return ["storyboard root must be an object"]
    problems: list[str] = []
    if not str(data.get("video_id", "")).strip():
        problems.append("storyboard video_id is empty")
    language = data.get("language")
    if language not in cfg.languages:
        problems.append(f"storyboard language '{language}' not in {list(cfg.languages)}")
    if data.get("format") != "9:16":
        problems.append("storyboard format must be '9:16'")
    target = data.get("target_duration_seconds")
    if not _num(target) or not cfg.min_duration <= target <= cfg.max_duration:
        problems.append(f"target_duration_seconds must be within {cfg.min_duration}-{cfg.max_duration}")

    scenes = data.get("scenes")
    if not isinstance(scenes, list):
        return problems + ["scenes must be a list"]
    if require_scenes and not scenes:
        problems.append("storyboard has no scenes")

    prev_end = 0.0
    ids: set[Any] = set()
    for idx, scene in enumerate(scenes):
        where = f"scene[{idx}]"
        if not isinstance(scene, dict):
            problems.append(f"{where} must be an object")
            continue
        missing = [k for k in REQUIRED_SCENE_KEYS if k not in scene]
        if missing:
            problems.append(f"{where} missing keys {missing}")
            continue
        if scene["id"] in ids:
            problems.append(f"{where} duplicate id {scene['id']}")
        ids.add(scene["id"])
        start, end = scene["start_seconds"], scene["end_seconds"]
        if not (_num(start) and _num(end)) or end <= start:
            problems.append(f"{where} needs numeric start < end")
            continue
        if abs(start - prev_end) > EPSILON:
            kind = "overlaps previous scene" if start < prev_end else "leaves a gap after previous scene"
            problems.append(f"{where} starts at {start}s, {kind} (expected {prev_end}s)")
        prev_end = float(end)
        if scene["visual_type"] not in VISUAL_TYPES:
            problems.append(f"{where} visual_type '{scene['visual_type']}' not in {sorted(VISUAL_TYPES)}")
        if not isinstance(scene["source_ids"], list):
            problems.append(f"{where} source_ids must be a list")
        problems.extend(_creative_problems(scene, where, strict=data.get("schema_version", 1) >= 2))
    if scenes and prev_end > cfg.max_duration + EPSILON:
        problems.append(f"storyboard runs {prev_end}s, above max {cfg.max_duration}s")
    if scenes and data.get("schema_version", 1) >= 2:
        problems.extend(_creative_structure_problems(scenes))
        question = str((data.get("creative") or {}).get("central_question", ""))
        if len(question) > MAX_QUESTION_CHARS:
            problems.append(f"creative.central_question is {len(question)} chars; the on-screen overlay fits "
                            f"{MAX_QUESTION_CHARS} (two lines) - shorten it")
    return problems


# ---- creative fields (schema_version 2; see docs/CREATIVE_PRODUCTION_STANDARD.md) ----
BEATS = frozenset({"hook", "context", "tension", "explanation", "example", "reveal", "payoff", "cta"})
VISUAL_FORMS = frozenset({
    "kinetic_type", "diagram_2d", "architecture_flow", "chart", "ui_mock", "screen_capture",
    "still_motion", "broll_video", "split_screen", "parallax_2_5d", "scene_3d", "title_card",
})
TRANSITIONS = frozenset({"cut", "crossfade", "push", "zoom_through", "match_cut", "morph", "wipe"})
CREATIVE_KEYS = ("beat", "visual_form", "transition_in", "motion")
# Structured content for the motion engine (studio/motion/engine.html); optional per scene.
VISUAL_TEMPLATES = frozenset({"kinetic", "fork", "flow", "split", "checklist", "stack", "panel", "chart", "title", "scene3d", "hyperframes"})
MAX_HOOK_SECONDS = 3.0
MAX_QUESTION_CHARS = 72  # central question overlay: two lines at 34px in the 860px question zone
MAX_STATIC_SECONDS = 6.0  # longest a scene may hold without an internal visual change


def _creative_problems(scene: dict[str, Any], where: str, strict: bool) -> list[str]:
    problems: list[str] = []
    if strict:
        missing = [k for k in CREATIVE_KEYS if k not in scene]
        if missing:
            return [f"{where} missing creative keys {missing}"]
    for key, allowed in (("beat", BEATS), ("visual_form", VISUAL_FORMS), ("transition_in", TRANSITIONS)):
        if key in scene and scene[key] not in allowed:
            problems.append(f"{where} {key} '{scene[key]}' not in {sorted(allowed)}")
    if "motion" in scene and (not isinstance(scene["motion"], str) or not scene["motion"].strip()):
        problems.append(f"{where} motion must describe the movement inside the scene")
    if "sfx" in scene and not (isinstance(scene["sfx"], list) and all(isinstance(x, str) for x in scene["sfx"])):
        problems.append(f"{where} sfx must be a list of cue names")
    voice = scene.get("voice")
    if voice is not None:
        if not isinstance(voice, dict):
            problems.append(f"{where} voice must be an object")
        else:
            if not isinstance(voice.get("emphasis", []), list):
                problems.append(f"{where} voice.emphasis must be a list of words")
            pause = voice.get("pause_after_ms", 0)
            if not isinstance(pause, int) or not 0 <= pause <= 1200:
                problems.append(f"{where} voice.pause_after_ms must be an int 0-1200")
    visual = scene.get("visual")
    if visual is not None:
        if not isinstance(visual, dict) or visual.get("template") not in VISUAL_TEMPLATES:
            problems.append(f"{where} visual.template must be one of {sorted(VISUAL_TEMPLATES)}")
        elif "cues" in visual and not (isinstance(visual["cues"], list) and all(isinstance(c, str) for c in visual["cues"])):
            problems.append(f"{where} visual.cues must be a list of words from the narration")
    if strict and scene.get("visual_form") == "scene_3d" and not str(scene.get("visual_justification", "")).strip():
        problems.append(f"{where} uses scene_3d without visual_justification")
    if isinstance(visual, dict) and visual.get("template") == "scene3d":
        # 3D is opt-in per scene: only when the script needs a physical object/place in space (see depth-and-3d skill)
        if scene.get("visual_form") != "scene_3d":
            problems.append(f"{where} visual.template 'scene3d' needs visual_form 'scene_3d'")
        if not str(visual.get("project", "")).strip():
            problems.append(f"{where} scene3d needs visual.project (a HyperFrames project folder, e.g. assets/3d/scene_04)")
    if isinstance(visual, dict) and visual.get("template") == "hyperframes" and not str(visual.get("project", "")).strip():
        problems.append(f"{where} hyperframes needs visual.project (a HyperFrames project folder, e.g. assets/hf/scene_04)")
    return problems


def _creative_structure_problems(scenes: list[dict[str, Any]]) -> list[str]:
    problems: list[str] = []
    first, last = scenes[0], scenes[-1]
    if first.get("beat") != "hook":
        problems.append("first scene beat must be 'hook'")
    elif float(first["end_seconds"]) - float(first["start_seconds"]) > MAX_HOOK_SECONDS:
        problems.append(f"hook scene is longer than {MAX_HOOK_SECONDS}s")
    if last.get("beat") not in ("cta", "payoff"):
        problems.append("last scene beat must be 'payoff' or 'cta'")
    if not any(s.get("beat") == "payoff" for s in scenes):
        problems.append("storyboard has no 'payoff' beat")
    for s in scenes:
        dur = float(s["end_seconds"]) - float(s["start_seconds"])
        if dur > MAX_STATIC_SECONDS and not str(s.get("motion", "")).strip():
            problems.append(f"scene {s['id']} holds {dur:.1f}s with no motion described")
    forms = [s.get("visual_form") for s in scenes]
    for a, b, c in zip(forms, forms[1:], forms[2:]):
        if a == b == c == "kinetic_type":
            problems.append("three kinetic_type scenes in a row; vary the visual form")
            break
    return problems


def load_storyboard(path: Path, cfg: ProductionConfig, require_scenes: bool = False) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError([f"Missing {path}"]) from exc
    except json.JSONDecodeError as exc:
        raise ContractError([f"Invalid JSON in {path}: {exc}"]) from exc
    problems = validate_storyboard_data(data, cfg, require_scenes)
    if problems:
        raise ContractError(problems)
    return data
