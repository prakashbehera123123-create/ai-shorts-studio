---
name: review-short
description: Review a produced Short for editorial, factual, rights, creative and technical quality using automated QA plus a scored creative rubric; never publishes.
---

# Review a Short

## Purpose
Final quality gate before human review. Combines `python -m studio qa` (technical) with the video-reviewer's creative rubric
(`docs/CREATIVE_PRODUCTION_STANDARD.md` §10).

## Inputs
- Production folder at RENDERED: script, storyboard, sources, fact check, manifest, metadata, `render/captions.srt`
- `qa/technical.json`, `qa/contact_sheet.jpg`, `qa/frames/` (sampled stills; never the full video)

## Workflow
1. `python -m studio metadata <folder>` (if not yet written) and `python -m studio qa <folder>`.
2. Optionally `python -m studio reference render/draft.mp4 --out qa/cadence` to measure change cadence against the standard.
3. video-reviewer scores the rubric (1–5): hook strength, mechanism clarity, visual–narration sync, visual variety, pacing,
   payoff usefulness, caption readability; lists blockers (factual overstatement, misleading hook/title, caption error,
   unreadable text, missing disclosure, unlicensed asset) and warnings; writes `qa/editorial.md` with `Decision: PASS|FAIL`.
4. Fix blockers once; re-render and re-run `python -m studio qa`.
5. Advance QA_PASSED → READY_FOR_HUMAN_REVIEW through the gates.

## Tools
`python -m studio qa|metadata|status`, video-reviewer agent (sonnet), sampled stills.

## Decision rules
- PASS requires: no blockers, every rubric score ≥ 3, average ≥ 3.5.
- Audio is judged only from measurements unless a human listened; say so.
- Known accepted downgrades (e.g. placeholder voice) are warnings, not blockers, but must appear in the report.

## Outputs
`qa/technical.json`, `qa/editorial.md`, `qa_report.md` (with human review checklist), `metadata.md`, status READY_FOR_HUMAN_REVIEW.

## Quality checklist
- [ ] Technical PASS; creative rubric recorded with scores
- [ ] Every claim (spoken, on screen, metadata) maps to sources
- [ ] Every asset has a rights record
- [ ] Human checklist present

## Failure handling
- Blockers remain after one fix → stop at QA_PASSED denied and report.
- Missing stills/captions → re-run `python -m studio qa` before reviewing.
Do not publish, upload or change public platforms.
