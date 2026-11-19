---
name: research-topics
description: Research and score current AI engineering and technology topics for YouTube Shorts.
---

# Research topics
Contract: `templates/research-candidates.example.json`. Rules: `config/research.json`, `config/content-strategy.md`.

1. Read `config/channel-brand.md` and `config/content-strategy.md` only.
2. Run `.venv\Scripts\python.exe -m studio research init` (creates `research/YYYY-MM-DD/candidates.json`). Window: last 7 days for news; evergreen topics allowed but set `"evergreen": true`.
3. Skim the last ~20 rows of `content/topic-backlog.md` and pass their titles to the research-analyst so it avoids repeats.
4. Ask research-analyst (one agent, one pass) for 8–12 candidates in the contract format. Every source needs url, publisher, published (YYYY-MM-DD or null if the page states none), accessed, kind (primary/secondary) and the exact claim it supports. News topics need a dated primary source inside the window.
5. Spot-check at least one primary URL per likely winner yourself. Remove or correct anything the page does not state. Never invent a source, date, number or quote; if research tools are unavailable, stop and report.
6. Write the file, then run `.venv\Scripts\python.exe -m studio research check research/YYYY-MM-DD/candidates.json`. Fix contract errors (do not change scores to force a selection).
7. Run `... research apply <file>`. This scores with the configured weights, rejects low-evidence/duplicate/out-of-window topics, selects at most 2, creates `production/YYYY-MM-DD-slug/` with `brief.md` and `sources.md` (status RESEARCHED), appends every decision to `content/topic-backlog.md`, and writes `shortlist.md` + `selection.json`.
8. Return the ranked table from `shortlist.md`, the selected folders, and any warnings. If fewer than 2 topics qualified, say so and ask; do not force a second topic.
Do not download footage, write scripts, or produce videos in this skill. Never publish or upload anything.
