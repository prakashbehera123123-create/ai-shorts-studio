---
name: research-topics
description: Research and score current AI engineering and technology topics for YouTube Shorts, keeping only topics with primary sources and a real story angle (tension, worked example, visual metaphor).
---

# Research topics

## Purpose
Daily topic discovery. Produces 8–12 sourced candidates, scores them, selects ≤ 2 and creates their production folders at
RESEARCHED. Story requirements come from `docs/CREATIVE_PRODUCTION_STANDARD.md` §2; scoring from `config/content-strategy.md`.

## Inputs
- `config/channel-brand.md`, `config/content-strategy.md`, `config/research.json`
- Last ~20 backlog titles from `content/topic-backlog.md`
- Contract: `templates/research-candidates.example.json`

## Workflow
1. `python -m studio research init` → `research/YYYY-MM-DD/candidates.json`. News window 7 days; evergreen allowed when labelled.
2. Ask research-analyst (one pass) for 8–12 candidates in the contract, each with the story fields (in `cautions` until the
   contract gains dedicated fields): **tension** (paradox / broken belief / black box / before→after), **worked example**
   (real or clearly illustrative), **visual metaphor**. Pass it the recent titles.
3. Prefer mechanisms ("how/why does X work") over announcements; an announcement must change what the viewer does.
4. Spot-check the primary URL of every likely winner yourself (browser pane or fetch). Correct or remove unsupported claims.
5. `python -m studio research check <file>` → fix contract errors (never edit scores to force a pick).
6. `python -m studio research apply <file>` → folders, briefs, sources, backlog, `shortlist.md`.
7. Copy the story fields into each selected `brief.md` (tension, example, metaphor) for story-architecture.
8. Report ranked table, selections, warnings; if < 2 qualify, say so.

## Tools
Web search / fetch, Claude Code browser pane or Playwright CLI for primary pages, `python -m studio research`.

## Decision rules
- Reject: no primary source; speculative; duplicate; rights unclear; misleading hook; **no tension and no worked example**.
- Two primary sources that disagree → record the conflict in `sources.md`; the script must not resolve it.
- Do not force two topics.

## Outputs
`research/YYYY-MM-DD/{candidates.json,shortlist.md,selection.json}`, `production/<id>/{brief.md,sources.md,status.json}`, backlog rows.

## Quality checklist
- [ ] Every source has url, publisher, published (or null), accessed, kind, claim
- [ ] Winners' primary URLs opened by the orchestrator
- [ ] Each selected brief names tension, worked example and visual metaphor
- [ ] Backlog updated; deferred topics not blocked for future runs

## Failure handling
- Search tools unavailable → stop and report; never invent sources.
- Fewer than 8 candidates → proceed with a warning; fewer than 2 qualifying → ask the owner.
Do not download footage, write scripts or produce videos here. Never publish or upload anything.
