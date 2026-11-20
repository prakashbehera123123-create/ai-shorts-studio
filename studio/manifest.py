"""Asset manifest (assets/manifest.csv) contract.

Every scene asset must be labelled with its origin and license so rights can be
audited before human review.
"""
from __future__ import annotations

import csv
from pathlib import Path

from .errors import ContractError

COLUMNS: tuple[str, ...] = (
    "asset_id",
    "filename",
    "asset_type",
    "source_url",
    "creator",
    "license",
    "license_url",
    "attribution_required",
    "notes",
)

# Visual vocabulary is shared with storyboard visual_type (CLAUDE.md workflow step 5).
VISUAL_TYPES = frozenset({"generated_graphic", "screen_capture", "licensed_stock", "user_asset"})
ASSET_TYPES = VISUAL_TYPES | {"generated_audio", "font"}
YES_NO = frozenset({"yes", "no"})


def validate_rows(rows: list[dict[str, str]]) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):  # line 1 is the header
        where = f"manifest line {i}"
        asset_id = (row.get("asset_id") or "").strip()
        if not asset_id:
            problems.append(f"{where}: asset_id is empty")
        elif asset_id in seen:
            problems.append(f"{where}: duplicate asset_id '{asset_id}'")
        seen.add(asset_id)
        if not (row.get("filename") or "").strip():
            problems.append(f"{where}: filename is empty")
        asset_type = (row.get("asset_type") or "").strip()
        if asset_type not in ASSET_TYPES:
            problems.append(f"{where}: asset_type '{asset_type}' not in {sorted(ASSET_TYPES)}")
        if not (row.get("license") or "").strip():
            problems.append(f"{where}: license is empty")
        attribution = (row.get("attribution_required") or "").strip().lower()
        if attribution not in YES_NO:
            problems.append(f"{where}: attribution_required must be yes/no")
        if asset_type == "licensed_stock":
            for field in ("source_url", "license_url"):
                if not (row.get(field) or "").strip():
                    problems.append(f"{where}: licensed_stock requires {field}")
        if attribution == "yes" and not (row.get("creator") or "").strip():
            problems.append(f"{where}: attribution required but creator is empty")
    return problems


def read_manifest(path: Path, require_rows: bool = False) -> list[dict[str, str]]:
    """Read and validate a manifest. Raises ContractError listing every problem."""
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            header = tuple(h.strip() for h in (reader.fieldnames or ()))
            rows = [dict(r) for r in reader]
    except FileNotFoundError as exc:
        raise ContractError([f"Missing {path}"]) from exc

    problems: list[str] = []
    missing = [c for c in COLUMNS if c not in header]
    if missing:
        problems.append(f"manifest header missing columns: {missing}")
    else:
        problems.extend(validate_rows(rows))
    if require_rows and not rows:
        problems.append("manifest has no assets")
    if problems:
        raise ContractError(problems)
    return rows


def write_empty_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(COLUMNS)
