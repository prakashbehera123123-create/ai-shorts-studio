"""storyboard.json contract."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import ContractError
from .manifest import ASSET_TYPES

VISUAL_TYPES = ASSET_TYPES
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
    if scenes and prev_end > cfg.max_duration + EPSILON:
        problems.append(f"storyboard runs {prev_end}s, above max {cfg.max_duration}s")
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
