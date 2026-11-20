"""Never lose a draft.

- `archive_previous_render`: before a re-render, move the existing draft (MP4, captions, report) into
  `render/versions/<YYYY-MM-DD_HHMMSS>/` named by the old draft's modification time.
- `deliver`: when a production reaches READY_FOR_HUMAN_REVIEW, copy its review package into
  `final/<YYYY-MM-DD>/<video_id>/`; an existing delivery is never overwritten (a `-v2`, `-v3`, ... folder is added).
Nothing here deletes files.
"""
from __future__ import annotations

import shutil
from datetime import date, datetime
from pathlib import Path

DRAFT_FILES = ("draft.mp4", "captions.srt", "render_report.json")
DELIVERY_FILES = ("render/draft.mp4", "render/captions.srt", "metadata.md", "qa_report.md", "script.md",
                  "sources.md", "fact_check.md", "status.json", "qa/editorial.md", "qa/contact_sheet.jpg")


def _free_dir(base: Path) -> Path:
    if not base.exists():
        return base
    n = 2
    while (candidate := base.with_name(f"{base.name}-v{n}")).exists():
        n += 1
    return candidate


def archive_previous_render(render_dir: Path) -> Path | None:
    """Move the current draft set into render/versions/<timestamp>/. Returns the new folder, or None."""
    draft = render_dir / "draft.mp4"
    if not draft.is_file():
        return None
    stamp = datetime.fromtimestamp(draft.stat().st_mtime).strftime("%Y-%m-%d_%H%M%S")
    dest = _free_dir(render_dir / "versions" / stamp)
    dest.mkdir(parents=True)
    for name in DRAFT_FILES:
        src = render_dir / name
        if src.is_file():
            shutil.move(str(src), str(dest / name))
    return dest


def deliver(folder: Path, root: Path, day: date | None = None) -> Path:
    """Copy the review package to root/<day>/<video_id>[-vN]/ and return that folder."""
    dest = _free_dir(root / (day or date.today()).isoformat() / folder.name)
    dest.mkdir(parents=True)
    for rel in DELIVERY_FILES:
        src = folder / rel
        if src.is_file():
            shutil.copy2(src, dest / Path(rel).name)
    return dest
