"""Production status lifecycle.

RESEARCHED -> APPROVED_TOPIC -> SCRIPT_READY -> ASSETS_READY -> RENDERED
-> QA_PASSED -> READY_FOR_HUMAN_REVIEW

Forward moves go one step at a time. Moving back to any earlier stage is allowed
(rework) but requires a note. There is deliberately no PUBLISHED state.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from .errors import ContractError, TransitionError


class Status(str, Enum):
    RESEARCHED = "RESEARCHED"
    APPROVED_TOPIC = "APPROVED_TOPIC"
    SCRIPT_READY = "SCRIPT_READY"
    ASSETS_READY = "ASSETS_READY"
    RENDERED = "RENDERED"
    QA_PASSED = "QA_PASSED"
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"

    @property
    def rank(self) -> int:
        return LIFECYCLE.index(self)


LIFECYCLE: tuple[Status, ...] = tuple(Status)
FORBIDDEN_STATUSES = frozenset({"PUBLISHED", "SCHEDULED", "UPLOADED"})


def parse_status(value: str) -> Status:
    if value.upper() in FORBIDDEN_STATUSES:
        raise TransitionError(f"Status '{value}' is forbidden: publishing is manual only")
    try:
        return Status(value)
    except ValueError as exc:
        raise TransitionError(f"Unknown status '{value}'. Valid: {[s.value for s in LIFECYCLE]}") from exc


def check_transition(current: Status, target: Status, note: str = "") -> None:
    if target == current:
        raise TransitionError(f"Already at {current.value}")
    if target.rank == current.rank + 1:
        return
    if target.rank > current.rank:
        nxt = LIFECYCLE[current.rank + 1].value
        raise TransitionError(f"Cannot skip from {current.value} to {target.value}; next is {nxt}")
    if not note.strip():
        raise TransitionError(f"Moving back from {current.value} to {target.value} requires a note")


def _iso(now: datetime | None) -> str:
    return (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0).isoformat()


def new_status(video_id: str, now: datetime | None = None) -> dict[str, Any]:
    ts = _iso(now)
    return {
        "video_id": video_id,
        "status": Status.RESEARCHED.value,
        "updated_at": ts,
        "human_review_required": True,
        "published": False,
        "history": [{"status": Status.RESEARCHED.value, "at": ts, "note": "created"}],
    }


def validate_status_data(data: Any) -> list[str]:
    problems: list[str] = []
    if not isinstance(data, dict):
        return ["status.json root must be an object"]
    for key in ("video_id", "status", "updated_at", "history"):
        if key not in data:
            problems.append(f"status.json missing '{key}'")
    raw = data.get("status")
    if isinstance(raw, str):
        try:
            parse_status(raw)
        except TransitionError as exc:
            problems.append(str(exc))
    elif raw is not None:
        problems.append("status must be a string")
    if data.get("published") is not False:
        problems.append("published must be false; this project never publishes")
    if data.get("human_review_required") is not True:
        problems.append("human_review_required must be true")
    history = data.get("history")
    if history is not None and (not isinstance(history, list) or not history):
        problems.append("history must be a non-empty list")
    return problems


def load_status(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError([f"Missing {path}"]) from exc
    except json.JSONDecodeError as exc:
        raise ContractError([f"Invalid JSON in {path}: {exc}"]) from exc
    problems = validate_status_data(data)
    if problems:
        raise ContractError(problems)
    return data


def save_status(path: Path, data: dict[str, Any]) -> None:
    problems = validate_status_data(data)
    if problems:
        raise ContractError(problems)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def apply_transition(data: dict[str, Any], target: Status, note: str = "", now: datetime | None = None) -> dict[str, Any]:
    """Return a new status dict moved to `target`. Does not touch disk."""
    current = parse_status(data["status"])
    check_transition(current, target, note)
    ts = _iso(now)
    updated = dict(data)
    updated["status"] = target.value
    updated["updated_at"] = ts
    updated["history"] = [*data.get("history", []), {"status": target.value, "at": ts, "note": note}]
    return updated
