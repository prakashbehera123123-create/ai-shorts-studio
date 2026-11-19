"""Research candidate contract, deterministic scoring and topic selection.

Agents gather evidence and propose 0-5 sub-scores; this module enforces the
evidence rules, computes the weighted score, rejects weak/duplicate topics and
selects at most `max_selected`. It never invents or fetches sources.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .config import PROJECT_ROOT
from .errors import ConfigError, ContractError

DEFAULT_RESEARCH_CONFIG = PROJECT_ROOT / "config" / "research.json"
SCORE_KEYS = ("freshness", "relevance", "usefulness", "evidence", "visual", "distinctiveness")
EVIDENCE_LEVELS = ("high", "medium", "low")
SOURCE_KINDS = ("primary", "secondary")
LIMIT_REASON = "daily limit reached by higher-scoring topics"
STOPWORDS = frozenset(
    "a an and are as at be by for from how in into is it its new of on or the this to vs what why with your you".split()
)


@dataclass(frozen=True)
class ResearchConfig:
    window_days: int
    min_candidates: int
    max_candidates: int
    max_selected: int
    min_selection_score: float
    min_evidence_score: int
    duplicate_similarity: float
    weights: dict[str, float]
    buckets: tuple[str, ...]


def load_research_config(path: Path | None = None) -> ResearchConfig:
    path = path or DEFAULT_RESEARCH_CONFIG
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        cfg = ResearchConfig(
            window_days=int(d["window_days"]),
            min_candidates=int(d["min_candidates"]),
            max_candidates=int(d["max_candidates"]),
            max_selected=int(d["max_selected"]),
            min_selection_score=float(d["min_selection_score"]),
            min_evidence_score=int(d["min_evidence_score"]),
            duplicate_similarity=float(d["duplicate_similarity"]),
            weights={k: float(d["weights"][k]) for k in SCORE_KEYS},
            buckets=tuple(d["buckets"]),
        )
    except FileNotFoundError as exc:
        raise ConfigError(f"Research config not found: {path}") from exc
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ConfigError(f"Invalid research config {path}: {exc}") from exc
    if abs(sum(cfg.weights.values()) - 1.0) > 1e-9:
        raise ConfigError("Research score weights must sum to 1.0")
    if not 0 < cfg.min_candidates <= cfg.max_candidates or cfg.max_selected < 1:
        raise ConfigError("Invalid candidate/selection counts")
    return cfg


# ---------------------------------------------------------------- validation

def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def validate_candidate(c: Any, rcfg: ResearchConfig, languages: tuple[str, ...], today: date) -> list[str]:
    """Structural and evidence problems for one candidate (empty = well-formed)."""
    if not isinstance(c, dict):
        return ["candidate must be an object"]
    cid = c.get("id", "?")
    where = f"candidate {cid}"
    problems: list[str] = []
    for key in ("id", "title", "summary", "audience_why", "visual_angle", "hook"):
        if not isinstance(c.get(key), str) or not c[key].strip():
            problems.append(f"{where}: '{key}' must be a non-empty string")
    if c.get("bucket") not in rcfg.buckets:
        problems.append(f"{where}: bucket '{c.get('bucket')}' not in {list(rcfg.buckets)}")
    if c.get("language") not in languages:
        problems.append(f"{where}: language must be one of {list(languages)}")
    if c.get("evidence") not in EVIDENCE_LEVELS:
        problems.append(f"{where}: evidence must be one of {list(EVIDENCE_LEVELS)}")
    if not isinstance(c.get("evergreen"), bool):
        problems.append(f"{where}: evergreen must be true/false")
    for key in ("reject_flags", "cautions"):
        value = c.get(key, [])
        if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
            problems.append(f"{where}: {key} must be a list of non-empty strings")

    scores = c.get("scores")
    if not isinstance(scores, dict):
        problems.append(f"{where}: scores must be an object")
    else:
        for k in SCORE_KEYS:
            v = scores.get(k)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 5:
                problems.append(f"{where}: scores.{k} must be a number 0-5")

    sources = c.get("sources")
    if not isinstance(sources, list) or not sources:
        problems.append(f"{where}: at least one source is required")
        return problems
    for i, s in enumerate(sources):
        sw = f"{where} source[{i}]"
        if not isinstance(s, dict):
            problems.append(f"{sw} must be an object")
            continue
        if not _valid_url(s.get("url")):
            problems.append(f"{sw}: url must be an absolute http(s) URL")
        if not isinstance(s.get("publisher"), str) or not s["publisher"].strip():
            problems.append(f"{sw}: publisher is required")
        if not isinstance(s.get("claim"), str) or not s["claim"].strip():
            problems.append(f"{sw}: claim supported is required")
        if s.get("kind") not in SOURCE_KINDS:
            problems.append(f"{sw}: kind must be primary or secondary")
        accessed = _parse_date(s.get("accessed"))
        if accessed is None:
            problems.append(f"{sw}: accessed must be YYYY-MM-DD")
        elif accessed > today:
            problems.append(f"{sw}: accessed date {accessed} is in the future")
        published_raw = s.get("published")
        if published_raw is not None:
            published = _parse_date(published_raw)
            if published is None:
                problems.append(f"{sw}: published must be YYYY-MM-DD or null")
            elif published > today:
                problems.append(f"{sw}: published date {published} is in the future")
            elif accessed and published > accessed:
                problems.append(f"{sw}: published after accessed date")
    return problems


def validate_research(data: Any, rcfg: ResearchConfig, languages: tuple[str, ...], today: date) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a candidates file."""
    if not isinstance(data, dict) or not isinstance(data.get("candidates"), list):
        return ["research file must be an object with a 'candidates' list"], []
    errors: list[str] = []
    warnings: list[str] = []
    cands = data["candidates"]
    if len(cands) > rcfg.max_candidates:
        errors.append(f"{len(cands)} candidates; maximum is {rcfg.max_candidates}")
    if len(cands) < rcfg.min_candidates:
        warnings.append(f"only {len(cands)} candidates; target is {rcfg.min_candidates}-{rcfg.max_candidates}")
    if _parse_date(data.get("research_date")) != today:
        errors.append(f"research_date must equal {today.isoformat()}")
    ids = [c.get("id") for c in cands if isinstance(c, dict)]
    dupes = sorted({str(i) for i in ids if ids.count(i) > 1})
    if dupes:
        errors.append(f"duplicate candidate ids: {dupes}")
    for c in cands:
        errors.extend(validate_candidate(c, rcfg, languages, today))
    return errors, warnings


# ------------------------------------------------------------------- scoring

def weighted_score(scores: dict[str, float], rcfg: ResearchConfig) -> float:
    return round(sum(float(scores[k]) * rcfg.weights[k] for k in SCORE_KEYS), 2)


def tokens(text: str) -> frozenset[str]:
    return frozenset(w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS and len(w) > 1)


def similarity(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def slugify(title: str, max_len: int = 60) -> str:
    words = re.findall(r"[a-z0-9]+", title.lower())
    slug = ""
    for w in words:
        candidate = f"{slug}-{w}" if slug else w
        if len(candidate) > max_len:
            break
        slug = candidate
    return slug or "topic"


def evidence_rejections(c: dict[str, Any], rcfg: ResearchConfig, today: date) -> list[str]:
    """Editorial rejection reasons per config/content-strategy.md."""
    reasons: list[str] = []
    sources = c["sources"]
    primaries = [s for s in sources if s["kind"] == "primary"]
    if not primaries:
        reasons.append("no primary source for the main claim")
    if c["evidence"] == "low":
        reasons.append("low evidence confidence")
    if c["scores"]["evidence"] < rcfg.min_evidence_score:
        reasons.append(f"evidence score below {rcfg.min_evidence_score}")
    if not c["evergreen"]:
        dated = [d for d in (_parse_date(s.get("published")) for s in primaries) if d]
        if not dated:
            reasons.append("news topic has no dated primary source")
        elif (today - max(dated)).days > rcfg.window_days:
            reasons.append(f"newest primary source older than {rcfg.window_days}-day window; label evergreen or drop")
    for flag in c.get("reject_flags", []) or []:
        reasons.append(f"flagged: {flag}")
    return reasons


@dataclass
class Decision:
    candidate: dict[str, Any]
    score: float
    selected: bool = False
    reasons: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.candidate["id"])

    @property
    def title(self) -> str:
        return str(self.candidate["title"])


def select_topics(
    data: dict[str, Any],
    rcfg: ResearchConfig,
    today: date,
    prior_titles: list[str] | None = None,
) -> list[Decision]:
    """Score, reject and select. Deterministic: ties break on candidate id.

    Assumes `data` already passed validate_research.
    """
    prior_titles = prior_titles or []
    decisions = [Decision(c, weighted_score(c["scores"], rcfg)) for c in data["candidates"]]
    for d in decisions:
        d.reasons.extend(evidence_rejections(d.candidate, rcfg, today))
        for prior in prior_titles:
            if similarity(d.title, prior) >= rcfg.duplicate_similarity:
                d.reasons.append(f"near-duplicate of earlier topic '{prior}'")
                break
        if d.score < rcfg.min_selection_score:
            d.reasons.append(f"score {d.score} below {rcfg.min_selection_score}")

    selected: list[Decision] = []
    for d in sorted(decisions, key=lambda x: (-x.score, x.id)):
        if d.reasons:
            continue
        if len(selected) >= rcfg.max_selected:
            d.reasons.append(LIMIT_REASON)
            continue
        twin = next((s for s in selected if similarity(d.title, s.title) >= rcfg.duplicate_similarity), None)
        if twin:
            d.reasons.append(f"near-duplicate of selected '{twin.id}'")
            continue
        d.selected = True
        selected.append(d)
    return decisions


def load_research_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContractError([f"Missing {path}"]) from exc
    except json.JSONDecodeError as exc:
        raise ContractError([f"Invalid JSON in {path}: {exc}"]) from exc
    return data
