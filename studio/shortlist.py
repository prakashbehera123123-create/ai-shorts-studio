"""Turn a validated research run into briefs, sources, backlog rows and a report."""
from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT, ProductionConfig
from .errors import ContractError, StudioError
from .production import FOLDER_RE, create_production, folders_for_day, make_video_id
from .research import LIMIT_REASON, SCORE_KEYS, Decision, ResearchConfig, slugify

DEFAULT_BACKLOG = PROJECT_ROOT / "content" / "topic-backlog.md"
DEFAULT_RESEARCH_ROOT = PROJECT_ROOT / "research"
BACKLOG_HEADER = "| Date added | Topic | Bucket | Evidence | Score | Status | Production folder |"


def _cell(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text)).replace("|", "\\|").strip()


def prior_titles(backlog: Path, production_root: Path) -> list[str]:
    """Topics already produced: selected backlog rows and existing production folder slugs.

    Deferred/rejected candidates are not counted, so they can be reconsidered later.
    """
    titles: list[str] = []
    if backlog.is_file():
        for line in backlog.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if len(cells) >= 7 and cells[0][:4].isdigit() and cells[5] == "selected":
                titles.append(cells[1].replace("\\|", "|"))
    if production_root.is_dir():
        for p in sorted(production_root.iterdir()):
            m = FOLDER_RE.match(p.name)
            if p.is_dir() and m:
                titles.append(m.group(2).replace("-", " "))
    return titles


def render_brief(d: Decision, video_id: str, rcfg: ResearchConfig, research_file: str) -> str:
    c = d.candidate
    breakdown = ", ".join(f"{k} {c['scores'][k]}" for k in SCORE_KEYS)
    return (
        f"# Brief: {c['title']}\n\n"
        f"- Video ID: {video_id}\n"
        f"- Language: {c['language']}\n"
        f"- Bucket: {c['bucket']}\n"
        f"- Type: {'evergreen' if c['evergreen'] else 'news (last ' + str(rcfg.window_days) + ' days)'}\n"
        f"- Evidence confidence: {c['evidence']}\n"
        f"- Weighted score: {d.score} / 5 ({breakdown})\n"
        f"- Research file: {research_file} (candidate {c['id']})\n\n"
        f"## Central idea\n{c['summary']}\n\n"
        f"## Why this audience should care\n{c['audience_why']}\n\n"
        f"## Proposed hook (must not mislead)\n{c['hook']}\n\n"
        f"## Visual angle\n{c['visual_angle']}\n\n"
        "## Editorial cautions\n"
        + ("".join(f"- {x}\n" for x in c.get("cautions", [])) or "- none\n")
        + "\n"
        "## Status\nRESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.\n"
    )


def render_sources(c: dict[str, Any]) -> str:
    lines = [
        "# Sources",
        "",
        "Confidence: high / medium / low. Mark each claim as fact, interpretation, or speculation in script.md.",
        "",
        "| id | url | publisher | published | accessed | claim supported | type | confidence |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, s in enumerate(c["sources"], start=1):
        lines.append(
            f"| S{i} | {_cell(s['url'])} | {_cell(s['publisher'])} | {_cell(s.get('published') or 'not stated')} "
            f"| {_cell(s['accessed'])} | {_cell(s['claim'])} | {s['kind']} | {c['evidence']} |"
        )
    return "\n".join(lines) + "\n"


def render_report(decisions: list[Decision], today: date, warnings: list[str], folders: dict[str, str]) -> str:
    selected = [d for d in decisions if d.selected]
    lines = [f"# Research shortlist {today.isoformat()}", ""]
    if warnings:
        lines += ["## Warnings", *[f"- {w}" for w in warnings], ""]
    if len(selected) < 2:
        lines += ["## Action needed", f"- Only {len(selected)} topic(s) met the evidence bar. Review before forcing more.", ""]
    lines += ["## Ranked candidates", "", "| rank | id | score | decision | title | reason |", "|---:|---|---:|---|---|---|"]
    for rank, d in enumerate(sorted(decisions, key=lambda x: (-x.score, x.id)), start=1):
        decision = "SELECTED" if d.selected else "rejected"
        reason = folders.get(d.id, "") if d.selected else "; ".join(d.reasons)
        lines.append(f"| {rank} | {_cell(d.id)} | {d.score} | {decision} | {_cell(d.title)} | {_cell(reason)} |")
    lines += ["", "## Selected sources"]
    for d in selected:
        lines.append(f"### {d.title}")
        for s in d.candidate["sources"]:
            lines.append(f"- [{s['kind']}] {s['publisher']}, published {s.get('published') or 'not stated'}, accessed {s['accessed']}: {s['url']}")
    return "\n".join(lines) + "\n"


def backlog_rows(decisions: list[Decision], today: date, folders: dict[str, str]) -> list[str]:
    rows = []
    for d in sorted(decisions, key=lambda x: (-x.score, x.id)):
        if d.selected:
            status = "selected"
        elif d.reasons == [LIMIT_REASON]:
            status = "deferred: daily limit"
        else:
            status = "rejected: " + (d.reasons[0] if d.reasons else "")
        rows.append(
            f"| {today.isoformat()} | {_cell(d.title)} | {d.candidate['bucket']} | {d.candidate['evidence']} "
            f"| {d.score} | {_cell(status)} | {folders.get(d.id, '')} |"
        )
    return rows


def apply_selection(
    decisions: list[Decision],
    warnings: list[str],
    today: date,
    cfg: ProductionConfig,
    rcfg: ResearchConfig,
    research_file: Path,
    backlog: Path = DEFAULT_BACKLOG,
    production_root: Path | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Create production folders for selected topics and record every decision.

    Checks every precondition before writing anything, so a refused run leaves no partial output.
    """
    production_root = production_root or cfg.production_root
    selection_path = research_file.parent / "selection.json"
    if selection_path.exists():
        raise StudioError(f"Selection already applied: {selection_path}")
    if not backlog.is_file() or BACKLOG_HEADER not in backlog.read_text(encoding="utf-8"):
        raise ContractError([f"Backlog missing or lacks header row: {backlog}"])

    selected = [d for d in decisions if d.selected]
    planned: dict[str, str] = {}
    for d in selected:
        video_id = make_video_id(today, slugify(d.title))
        if (production_root / video_id).exists() or video_id in planned.values():
            raise StudioError(f"Production folder already exists or collides: {video_id}")
        planned[d.id] = video_id
    if len(folders_for_day(production_root, today)) + len(selected) > cfg.max_videos_per_day:
        raise StudioError(f"Selection would exceed {cfg.max_videos_per_day} productions for {today}")

    try:
        rel_research = research_file.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        rel_research = research_file.name
    for d in selected:
        video_id = planned[d.id]
        folder = create_production(cfg, today, slugify(d.title), d.title, d.candidate["language"], root=production_root, now=now)
        (folder / "brief.md").write_text(render_brief(d, video_id, rcfg, rel_research), encoding="utf-8")
        (folder / "sources.md").write_text(render_sources(d.candidate), encoding="utf-8")

    folder_labels = {cid: f"production/{vid}" for cid, vid in planned.items()}
    existing = backlog.read_text(encoding="utf-8")
    with backlog.open("a", encoding="utf-8", newline="\n") as fh:
        if not existing.endswith("\n"):
            fh.write("\n")
        fh.write("\n".join(backlog_rows(decisions, today, folder_labels)) + "\n")

    report_path = research_file.parent / "shortlist.md"
    report_path.write_text(render_report(decisions, today, warnings, folder_labels), encoding="utf-8")
    summary = {
        "research_date": today.isoformat(),
        "selected": [{"id": d.id, "title": d.title, "score": d.score, "folder": folder_labels[d.id]} for d in selected],
        "rejected": [{"id": d.id, "score": d.score, "reasons": d.reasons} for d in decisions if not d.selected],
        "warnings": warnings,
        "report": report_path.name,
    }
    selection_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary
