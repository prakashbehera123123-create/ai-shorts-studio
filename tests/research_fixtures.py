from datetime import date
from typing import Any

TODAY = date(2026, 11, 20)

TITLES = [
    "Open protocol adds remote tool servers",
    "Vector database ships hybrid search",
    "Evaluation harness for agent trajectories",
    "Cloud provider launches managed agent runtime",
    "Prompt caching cuts repeated context cost",
    "Interview concept: retrieval versus fine tuning",
    "Guardrails library adds jailbreak tests",
    "Local model runner supports speculative decoding",
]
BUCKETS = ["agentic-ai-mcp", "llm-engineering", "llm-engineering", "cloud-ai",
           "developer-workflows", "career-concepts", "responsible-ai", "ai-tools-releases"]


def source(**kw: Any) -> dict[str, Any]:
    s = {"url": "https://example.com/notes", "publisher": "Example Vendor", "published": "2026-11-18",
         "accessed": "2026-11-20", "kind": "primary", "claim": "Feature X is generally available."}
    s.update(kw)
    return s


def candidate(i: int, score: float = 4, **kw: Any) -> dict[str, Any]:
    c = {
        "id": f"C{i:02d}", "title": TITLES[(i - 1) % len(TITLES)], "summary": "s", "bucket": BUCKETS[(i - 1) % len(BUCKETS)],
        "language": "English", "evergreen": False, "evidence": "high", "audience_why": "a", "visual_angle": "v", "hook": "h",
        "scores": {k: score for k in ("freshness", "relevance", "usefulness", "evidence", "visual", "distinctiveness")},
        "reject_flags": [], "sources": [source()],
    }
    c.update(kw)
    return c


def research(cands: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if cands is None:
        cands = [candidate(i, score=5 - i * 0.25) for i in range(1, 9)]
    return {"research_date": TODAY.isoformat(), "window_days": 7, "candidates": cands}
