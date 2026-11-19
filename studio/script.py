"""script.md + fact_check.md contract and script/storyboard consistency checks.

script.md layout (headings are required, in any order):
    Language: English|Hinglish
    ## Hook / ## Narration / ## On-screen text / ## CTA / ## Claim-to-source map
Spoken text = Hook + Narration + CTA. The storyboard's scene narration, joined
in order, must contain exactly the same words.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import ProductionConfig
from .errors import ContractError
from .storyboard import load_storyboard

SPOKEN_SECTIONS = ("hook", "narration", "cta")
REQUIRED_SECTIONS = ("hook", "narration", "on-screen text", "cta", "claim-to-source map")
CLAIM_TYPES = ("fact", "interpretation", "speculation")
VERDICTS = ("supported", "qualified", "unsupported")
HINGLISH_MARKERS = frozenset(
    "hai hain kya nahi nahin aur toh ki ka ke mein yeh ye woh bhai kaise kyun matlab abhi sirf bhi apna apne "
    "karo karna karta karte dekho samjho chahiye wala wali".split()
)
DEVANAGARI = re.compile(r"[ऀ-ॿ]")
NUMBER = re.compile(r"\d+(?:\.\d+)?")
SOURCE_ROW = re.compile(r"^\|\s*(S\d+)\s*\|", re.M)


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:['.][a-z0-9]+)*", text.lower())


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current, buf = m.group(1).strip().lower(), []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def parse_table(text: str) -> list[list[str]]:
    """Data rows of the first markdown table in `text` (header and separator removed)."""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    out = []
    for ln in rows[2:]:
        out.append([c.strip() for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))])
    return out


def source_ids(sources_md: str) -> set[str]:
    return set(SOURCE_ROW.findall(sources_md))


@dataclass
class ScriptReport:
    language: str = ""
    spoken_words: int = 0
    estimated_seconds: float = 0.0
    storyboard_seconds: float = 0.0
    claims: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "language": self.language,
            "spoken_words": self.spoken_words,
            "estimated_seconds": self.estimated_seconds,
            "storyboard_seconds": self.storyboard_seconds,
            "claims": len(self.claims),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def check_language(spoken: str, language: str) -> list[str]:
    toks = words(spoken)
    if DEVANAGARI.search(spoken):
        return ["spoken text contains Devanagari; use English or romanized Hinglish only"]
    markers = sum(t in HINGLISH_MARKERS for t in toks)
    if language == "English" and markers >= 3:
        return [f"English script contains {markers} Hinglish words; do not mix languages"]
    if language == "Hinglish" and toks and markers / len(toks) < 0.05:
        return ["Hinglish script has too few Hindi words; it reads as English"]
    return []


def check_script(folder: Path, cfg: ProductionConfig) -> ScriptReport:
    rep = ScriptReport()
    script_md = (folder / "script.md").read_text(encoding="utf-8")
    sources_md = (folder / "sources.md").read_text(encoding="utf-8")
    sections = parse_sections(script_md)
    missing = [s for s in REQUIRED_SECTIONS if not sections.get(s)]
    if missing:
        rep.errors.append(f"script.md sections missing or empty: {missing}")
        return rep

    m = re.search(r"^Language:\s*(\S+)", script_md, re.M)
    rep.language = m.group(1) if m else ""
    if rep.language not in cfg.languages:
        rep.errors.append(f"script.md Language must be one of {list(cfg.languages)}")

    spoken = "\n".join(sections[s] for s in SPOKEN_SECTIONS)
    spoken_words = words(spoken)
    rep.spoken_words = len(spoken_words)
    rep.estimated_seconds = round(rep.spoken_words / cfg.target_wpm * 60, 1)
    if not cfg.min_words <= rep.spoken_words <= cfg.max_words:
        rep.errors.append(f"spoken words {rep.spoken_words} outside {cfg.min_words}-{cfg.max_words}")
    if not cfg.min_duration <= rep.estimated_seconds <= cfg.max_duration:
        rep.errors.append(f"estimated {rep.estimated_seconds}s at {cfg.target_wpm:g} wpm outside {cfg.min_duration:g}-{cfg.max_duration:g}s")
    if len(words(sections["hook"])) > 20:
        rep.warnings.append("hook is over 20 words; it should land in 1-2 seconds")
    if rep.language in cfg.languages:
        rep.errors.extend(check_language(spoken, rep.language))

    known = source_ids(sources_md)
    if not known:
        rep.errors.append("sources.md has no S# source rows")
    claim_text = ""
    for row in parse_table(sections["claim-to-source map"]):
        if len(row) < 4:
            rep.errors.append(f"claim row needs 4 columns (id | claim | sources | type): {row}")
            continue
        cid, claim, srcs, ctype = row[:4]
        rep.claims.append(cid)
        claim_text += " " + claim
        refs = re.findall(r"S\d+", srcs)
        if not refs:
            rep.errors.append(f"claim {cid} has no source id")
        for ref in refs:
            if ref not in known:
                rep.errors.append(f"claim {cid} cites {ref}, not in sources.md")
        if ctype.lower() not in CLAIM_TYPES:
            rep.errors.append(f"claim {cid} type '{ctype}' not in {list(CLAIM_TYPES)}")
        elif ctype.lower() == "speculation":
            rep.warnings.append(f"claim {cid} is speculation; narration must say so explicitly")
    if not rep.claims:
        rep.errors.append("claim-to-source map has no claims")
    if len(set(rep.claims)) != len(rep.claims):
        rep.errors.append("duplicate claim ids")

    mapped_numbers = set(NUMBER.findall(claim_text))
    for num in sorted(set(NUMBER.findall(spoken)) - mapped_numbers):
        rep.errors.append(f"number '{num}' is spoken but appears in no mapped claim")

    try:
        board = load_storyboard(folder / "storyboard.json", cfg, require_scenes=True)
    except ContractError as exc:
        rep.errors.extend(exc.problems)
        return rep
    if board.get("language") != rep.language:
        rep.errors.append(f"storyboard language '{board.get('language')}' != script '{rep.language}'")
    scenes = board["scenes"]
    rep.storyboard_seconds = float(scenes[-1]["end_seconds"])
    if not cfg.min_duration <= rep.storyboard_seconds <= cfg.max_duration:
        rep.errors.append(f"storyboard total {rep.storyboard_seconds}s outside {cfg.min_duration:g}-{cfg.max_duration:g}s")
    board_words = [w for s in scenes for w in words(str(s["narration"]))]
    if board_words != spoken_words:
        first = next((i for i, (a, b) in enumerate(zip(board_words, spoken_words)) if a != b), min(len(board_words), len(spoken_words)))
        rep.errors.append(
            f"storyboard narration differs from script spoken text at word {first + 1} "
            f"({len(board_words)} vs {len(spoken_words)} words)"
        )
    for s in scenes:
        dur = float(s["end_seconds"]) - float(s["start_seconds"])
        n = len(words(str(s["narration"])))
        if n and n / dur * 60 > cfg.max_wpm:
            rep.errors.append(f"scene {s['id']}: {n} words in {dur:g}s is faster than {cfg.max_wpm:g} wpm")
        if len(words(str(s["on_screen_text"]))) > 12:
            rep.warnings.append(f"scene {s['id']}: on-screen text over 12 words may be unreadable on mobile")
        for ref in s["source_ids"]:
            if ref not in known:
                rep.errors.append(f"scene {s['id']} cites {ref}, not in sources.md")
    total_wpm = len(spoken_words) / rep.storyboard_seconds * 60 if rep.storyboard_seconds else 0
    if total_wpm and not cfg.min_wpm <= total_wpm <= cfg.max_wpm:
        rep.errors.append(f"overall pace {total_wpm:.0f} wpm outside {cfg.min_wpm:g}-{cfg.max_wpm:g}")
    return rep


def check_fact_check(folder: Path, claim_ids: list[str]) -> list[str]:
    """fact_check.md must give every claim a verdict, and none may be unsupported."""
    path = folder / "fact_check.md"
    if not path.is_file():
        return ["missing fact_check.md"]
    problems: list[str] = []
    verdicts: dict[str, str] = {}
    for row in parse_table(path.read_text(encoding="utf-8")):
        if len(row) >= 3:
            verdicts[row[0]] = row[2].lower()
    for cid in claim_ids:
        v = verdicts.get(cid)
        if v is None:
            problems.append(f"fact_check.md has no verdict for claim {cid}")
        elif v not in VERDICTS:
            problems.append(f"fact_check.md verdict for {cid} '{v}' not in {list(VERDICTS)}")
        elif v == "unsupported":
            problems.append(f"claim {cid} is unsupported; fix or remove it")
    return problems


def script_gate_problems(folder: Path, cfg: ProductionConfig) -> list[str]:
    rep = check_script(folder, cfg)
    return rep.errors + (check_fact_check(folder, rep.claims) if rep.claims else [])
