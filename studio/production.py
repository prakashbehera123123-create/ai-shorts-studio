"""Production folder scaffolding and contract validation."""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import ContractError, StudioError
from .manifest import read_manifest, write_empty_manifest
from .status import Status, apply_transition, load_status, new_status, parse_status, save_status
from .storyboard import load_storyboard

REQUIRED_FILES: tuple[str, ...] = (
    "brief.md",
    "script.md",
    "sources.md",
    "storyboard.json",
    "assets/manifest.csv",
    "metadata.md",
    "qa_report.md",
    "status.json",
)
REQUIRED_DIRS: tuple[str, ...] = ("render",)
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FOLDER_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")

SOURCES_TEMPLATE = """# Sources

Confidence: high / medium / low. Mark each claim as fact, interpretation, or speculation.

| id | url | publisher | published | accessed | claim supported | type | confidence |
|---|---|---|---|---|---|---|---|
"""

MARKDOWN_TEMPLATES: dict[str, str] = {
    "brief.md": "# Brief: {title}\n\n- Video ID: {video_id}\n- Language: {language}\n- Bucket:\n- Audience angle:\n- Central idea:\n- Why now:\n",
    "script.md": "# Script: {title}\n\nLanguage: {language}\n\n## Hook\n\n## Narration\n\n## On-screen text\n\n## CTA\n\n## Claim-to-source map\n",
    "sources.md": SOURCES_TEMPLATE,
    "metadata.md": "# Metadata: {title}\n\n## Title\n\n## Description\n\n## Tags\n\n## Disclosures\n",
    "qa_report.md": "# QA report: {video_id}\n\n## Technical\n\n## Editorial\n\n## Rights\n\n## Decision\n",
}


def make_video_id(day: date, slug: str) -> str:
    if not SLUG_RE.match(slug):
        raise StudioError(f"Invalid slug '{slug}': use lowercase letters, digits and single hyphens")
    if len(slug) > 60:
        raise StudioError("Slug must be 60 characters or fewer")
    return f"{day.isoformat()}-{slug}"


def parse_day(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise StudioError(f"Invalid date '{value}': expected YYYY-MM-DD") from exc


def folders_for_day(root: Path, day: date) -> list[Path]:
    if not root.is_dir():
        return []
    prefix = day.isoformat() + "-"
    return sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith(prefix) and FOLDER_RE.match(p.name))


def create_production(
    cfg: ProductionConfig,
    day: date,
    slug: str,
    title: str,
    language: str,
    root: Path | None = None,
    now: datetime | None = None,
) -> Path:
    if language not in cfg.languages:
        raise StudioError(f"Language '{language}' not in {list(cfg.languages)}; pick exactly one")
    root = root or cfg.production_root
    video_id = make_video_id(day, slug)
    folder = root / video_id
    if folder.exists():
        raise StudioError(f"Production folder already exists: {folder}")
    existing = folders_for_day(root, day)
    if len(existing) >= cfg.max_videos_per_day:
        raise StudioError(f"Daily limit of {cfg.max_videos_per_day} reached for {day}: {[p.name for p in existing]}")

    folder.mkdir(parents=True)
    for d in REQUIRED_DIRS:
        (folder / d).mkdir()
        (folder / d / ".gitkeep").touch()
    values = {"title": title or slug, "video_id": video_id, "language": language}
    for name, template in MARKDOWN_TEMPLATES.items():
        (folder / name).write_text(template.format(**values), encoding="utf-8")
    storyboard: dict[str, Any] = {
        "video_id": video_id,
        "language": language,
        "target_duration_seconds": cfg.default_target_duration,
        "format": "9:16",
        "scenes": [],
    }
    (folder / "storyboard.json").write_text(json.dumps(storyboard, indent=2) + "\n", encoding="utf-8")
    write_empty_manifest(folder / "assets" / "manifest.csv")
    save_status(folder / "status.json", new_status(video_id, now))
    return folder


def _gate_problems(folder: Path, cfg: ProductionConfig, stage: Status) -> list[str]:
    problems: list[str] = []
    for name in REQUIRED_FILES:
        if not (folder / name).is_file():
            problems.append(f"missing {name}")
    for name in REQUIRED_DIRS:
        if not (folder / name).is_dir():
            problems.append(f"missing directory {name}/")
    if problems:
        return problems

    storyboard: dict[str, Any] | None = None
    try:
        storyboard = load_storyboard(folder / "storyboard.json", cfg, require_scenes=stage.rank >= Status.SCRIPT_READY.rank)
    except ContractError as exc:
        problems.extend(exc.problems)
    if storyboard is not None and storyboard.get("video_id") != folder.name:
        problems.append(f"storyboard video_id '{storyboard.get('video_id')}' != folder '{folder.name}'")
    if storyboard is not None and stage.rank >= Status.SCRIPT_READY.rank:
        from .script import script_gate_problems  # local import avoids a cycle

        problems.extend(script_gate_problems(folder, cfg))
    try:
        read_manifest(folder / "assets" / "manifest.csv", require_rows=stage.rank >= Status.ASSETS_READY.rank)
    except ContractError as exc:
        problems.extend(exc.problems)
    if stage.rank >= Status.RENDERED.rank and not any((folder / "render").glob("*.mp4")):
        problems.append("stage requires a draft MP4 in render/")
    return problems


def validate_production(folder: Path, cfg: ProductionConfig) -> list[str]:
    """Return all contract problems for the folder at its current status (empty = valid)."""
    if not folder.is_dir():
        return [f"Not a directory: {folder}"]
    if not FOLDER_RE.match(folder.name):
        return [f"Folder name '{folder.name}' must be YYYY-MM-DD-slug"]
    try:
        status_data = load_status(folder / "status.json")
    except ContractError as exc:
        return exc.problems
    problems = []
    if status_data["video_id"] != folder.name:
        problems.append(f"status video_id '{status_data['video_id']}' != folder '{folder.name}'")
    return problems + _gate_problems(folder, cfg, parse_status(status_data["status"]))


def set_status(folder: Path, cfg: ProductionConfig, target: str, note: str = "", now: datetime | None = None) -> dict[str, Any]:
    """Move a production to `target` only if the lifecycle and stage gates allow it."""
    target_status = parse_status(target)
    status_path = folder / "status.json"
    data = load_status(status_path)
    updated = apply_transition(data, target_status, note, now)
    if target_status.rank > parse_status(data["status"]).rank:
        problems = _gate_problems(folder, cfg, target_status)
        if problems:
            raise ContractError([f"cannot enter {target_status.value}: {p}" for p in problems])
    save_status(status_path, updated)
    return updated
