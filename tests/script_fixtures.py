"""Builds a contract-valid script.md / storyboard.json / sources.md / fact_check.md set."""
import json
from pathlib import Path

HOOK = "Your agent passed the demo yesterday, but did your last prompt change quietly break it today?"
NARRATION = (
    "Here is a simple habit that fixes this problem for most teams. Write a small set of repeatable tests "
    "for the behaviour you care about, and run them before and after every change you make. "
    "Compare the two runs side by side. If the new version is worse on the cases that matter, you catch it "
    "before your users do. Keep the cases short, keep them focused on real tasks, and add a new case every "
    "time something breaks in production."
)
CTA = "Which agent behaviour would you test first? Tell me in the comments."
SPOKEN = f"{HOOK} {NARRATION} {CTA}"

SOURCES = """# Sources

| id | url | publisher | published | accessed | claim supported | type | confidence |
|---|---|---|---|---|---|---|---|
| S1 | https://example.com/a | Example | 2026-11-17 | 2026-11-20 | Repeatable evals compare runs before and after a change. | primary | high |
"""


def script_md(language: str = "English", hook: str = HOOK, narration: str = NARRATION, cta: str = CTA,
              claims: str = "| K1 | Repeatable evals compare runs before and after a change | S1 | fact |") -> str:
    return (
        f"# Script: Demo\n\nLanguage: {language}\n\n## Hook\n{hook}\n\n## Narration\n{narration}\n\n"
        f"## On-screen text\n- Test before and after\n\n## CTA\n{cta}\n\n"
        f"## Claim-to-source map\n| id | claim | sources | type |\n|---|---|---|---|\n{claims}\n"
    )


def storyboard(video_id: str, spoken: str = SPOKEN, total: float = 44.0, language: str = "English", n: int = 4) -> dict:
    toks = spoken.split()
    size = -(-len(toks) // n)
    chunks = [" ".join(toks[i:i + size]) for i in range(0, len(toks), size)]
    step = total / len(chunks)
    scenes = []
    for i, chunk in enumerate(chunks):
        scenes.append({"id": i + 1, "start_seconds": round(i * step, 3), "end_seconds": round((i + 1) * step, 3) if i < len(chunks) - 1 else total,
                       "narration": chunk, "on_screen_text": "Test before and after", "visual_type": "generated_graphic",
                       "visual_description": "diagram", "source_ids": ["S1"]})
    return {"video_id": video_id, "language": language, "target_duration_seconds": 40, "format": "9:16", "scenes": scenes}


FACT_CHECK = """# Fact check

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| K1 | Repeatable evals compare runs | supported | S1 | matches page |
"""


def write_valid(folder: Path, **script_kw: str) -> None:
    (folder / "sources.md").write_text(SOURCES, encoding="utf-8")
    (folder / "script.md").write_text(script_md(**script_kw), encoding="utf-8")
    (folder / "storyboard.json").write_text(json.dumps(storyboard(folder.name)), encoding="utf-8")
    (folder / "fact_check.md").write_text(FACT_CHECK, encoding="utf-8")
