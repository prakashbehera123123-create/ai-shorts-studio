"""Deterministic metadata.md draft and its checks. Text for a human to paste into YouTube Studio; nothing is uploaded."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .manifest import read_manifest
from .script import parse_sections

MAX_TITLE = 100
MAX_DESCRIPTION = 5000
MAX_TAG_CHARS = 500
MAX_HASHTAGS = 3
HYPE_WORDS = ("insane", "shocking", "game changer", "game-changer", "you won't believe", "destroys", "killer", "secret")
DISCLOSURE_VOICE = "Narration uses a synthetic text-to-speech voice."
DISCLOSURE_CLONE = "Narration is an AI-generated clone of the creator's own voice (synthetic speech)."
BUCKET_TAGS = {
    "agentic-ai-mcp": ["agentic ai", "mcp", "ai agents"],
    "llm-engineering": ["llm engineering", "openai api", "ai engineering"],
    "ai-tools-releases": ["ai tools", "developer tools"],
    "cloud-ai": ["cloud ai"],
    "developer-workflows": ["developer workflow", "github copilot", "ai engineering"],
    "career-concepts": ["ai engineering career"],
    "responsible-ai": ["responsible ai", "ai safety"],
}


def cited_source_ids(folder: Path) -> set[str] | None:
    """S ids the video actually uses (claim map + storyboard source_ids); None if they cannot be determined."""
    ids: set[str] = set()
    script = folder / "script.md"
    if script.is_file():
        claims = parse_sections(script.read_text(encoding="utf-8")).get("claim-to-source map", "")
        ids.update(re.findall(r"\bS\d+\b", claims))
    board = folder / "storyboard.json"
    if board.is_file():
        try:
            for s in json.loads(board.read_text(encoding="utf-8")).get("scenes", []):
                ids.update(x for x in s.get("source_ids", []) if isinstance(x, str))
        except json.JSONDecodeError:
            return None
    return ids or None


def source_rows(sources_md: str, only: set[str] | None = None) -> list[tuple[str, str, str]]:
    """Unique (url, publisher, published) in table order, optionally restricted to cited S ids."""
    seen, out = set(), []
    for line in sources_md.splitlines():
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if (len(cells) >= 5 and re.fullmatch(r"S\d+", cells[0]) and cells[1] not in seen
                and (only is None or cells[0] in only)):
            seen.add(cells[1])
            out.append((cells[1], cells[2], cells[3]))
    return out


def _field(text: str, name: str) -> str:
    m = re.search(rf"^-\s*{name}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def uses_synthetic_voice(folder: Path) -> bool:
    try:
        rows = read_manifest(folder / "assets" / "manifest.csv")
    except Exception:  # noqa: BLE001 - absence is reported by other checks
        return False
    return any(r["asset_type"] == "generated_audio" for r in rows)


def uses_cloned_voice(folder: Path) -> bool:
    try:
        rows = read_manifest(folder / "assets" / "manifest.csv")
    except Exception:  # noqa: BLE001
        return False
    return any(r["asset_type"] == "generated_audio" and "clon" in r["notes"].lower() for r in rows)


def voice_disclosure(folder: Path) -> str:
    return DISCLOSURE_CLONE if uses_cloned_voice(folder) else DISCLOSURE_VOICE


def build_metadata(folder: Path) -> str:
    script = (folder / "script.md").read_text(encoding="utf-8")
    brief = (folder / "brief.md").read_text(encoding="utf-8")
    sections = parse_sections(script)
    title_m = re.search(r"^# Script:\s*(.+)$", script, re.M)
    title = (title_m.group(1).strip() if title_m else folder.name)[:MAX_TITLE]
    hook = " ".join(sections.get("hook", "").split())
    cta = " ".join(sections.get("cta", "").split())
    bucket = _field(brief, "Bucket")
    tags = BUCKET_TAGS.get(bucket, ["ai engineering"]) + ["youtube shorts"]
    srcs = source_rows((folder / "sources.md").read_text(encoding="utf-8"), cited_source_ids(folder))
    disclosures = ["Visuals are original text graphics made for this video; no third-party footage."]
    if uses_synthetic_voice(folder):
        disclosures.insert(0, voice_disclosure(folder))
    lines = [
        f"# Metadata: {folder.name}", "",
        "Draft text for manual entry in YouTube Studio. Not uploaded by this project.", "",
        "## Title", title, "",
        "## Description", hook, "", cta, "",
        "Sources:",
        *[f"- {pub} ({date}): {url}" for url, pub, date in srcs],
        "", " ".join(disclosures), "",
        "#Shorts #AIEngineering", "",
        "## Tags", ", ".join(dict.fromkeys(tags)), "",
        "## Disclosures", *[f"- {d}" for d in disclosures],
        "- Altered or synthetic content setting: review in YouTube Studio (TTS narration of factual content).", "",
    ]
    return "\n".join(lines)


def metadata_problems(folder: Path) -> list[str]:
    path = folder / "metadata.md"
    if not path.is_file():
        return ["missing metadata.md"]
    text = path.read_text(encoding="utf-8")
    sec = parse_sections(text)
    problems: list[str] = []
    title = sec.get("title", "").strip()
    if not 10 <= len(title) <= MAX_TITLE:
        problems.append(f"title length {len(title)} not within 10-{MAX_TITLE}")
    if title == folder.name or re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9-]+", title):
        problems.append("title is the folder slug; write a human title")
    if any(w in title.lower() for w in HYPE_WORDS):
        problems.append("title uses hype wording")
    desc = sec.get("description", "")
    if not desc.strip():
        problems.append("description is empty")
    if len(desc) > MAX_DESCRIPTION:
        problems.append(f"description over {MAX_DESCRIPTION} chars")
    for url, _pub, _date in source_rows((folder / "sources.md").read_text(encoding="utf-8"), cited_source_ids(folder)):
        if url not in desc:
            problems.append(f"description is missing source URL {url}")
    hashtags = re.findall(r"#\w+", desc)
    if len(hashtags) > MAX_HASHTAGS:
        problems.append(f"{len(hashtags)} hashtags; max {MAX_HASHTAGS}")
    tags = sec.get("tags", "")
    if not tags.strip() or len(tags) > MAX_TAG_CHARS:
        problems.append(f"tags must be 1-{MAX_TAG_CHARS} chars")
    if uses_synthetic_voice(folder) and voice_disclosure(folder) not in text:
        problems.append("synthetic voice used but not disclosed")
    return problems
