# Dry run 2 review — upgraded workflow on the same two topics

Date: 2026-11-20 · Topics: Copilot Evals, GPT-6.2 checks (same as dry run 1, for a like-for-like comparison).
v1 deliverables are archived in each production folder under `baseline_v1/` (the v1 MP4 there is git-ignored).
Status of both folders: **RENDERED** — the creative gate correctly refused QA_PASSED (see verdict).

## Workflow actually executed
1. Research validation gate: story angle (tension, central question, illustrative example, motif, payoff) added to each `brief.md` from `sources.md` only.
2. Two scriptwriter agents in parallel (story-architecture + visual-direction skills) → `script.md` with 3 scored hook candidates and beats, schema-v2 `storyboard.json`.
3. Two fact-checker agents in parallel, primary URLs re-opened → corrections applied by the main session, logged in `fact_check.md`.
4. `readiness.md` filled from `templates/production-readiness-checklist.md` (4 items honestly WAIVED: hero visual, change cadence, word-timed captions, loop ending — all need the Phase 5 renderer).
5. `python -m studio render` → `metadata` → `qa`; two video-reviewer agents scored the 7-item rubric for **both v1 and v2**.
6. Objective comparison with `python -m studio reference` on all four drafts + whisper transcript vs script.

## Results

| Metric | Copilot v1 | Copilot v2 | GPT v1 | GPT v2 |
|---|---:|---:|---:|---:|
| Duration (s) | 50.07 | 51.87 | 50.30 | 49.87 |
| Spoken words | 130 | 127 | 133 | 126 |
| Delivered pace (wpm) | ~156 | ~147 | ~159 | ~152 |
| Integrated loudness (LUFS) | −16.4 | **−14.0** | −16.3 | **−14.0** |
| True peak (dBFS) | −4.4 | −1.4 | −4.5 | −1.5 |
| Whisper word recall vs script | — | 98% | — | 94% |
| Detected visual changes (frame-difference) | 0 | 0 | 0 | 0 |
| Fact check | 0 unsupported | 0 unsupported (2 qualified) | 0 unsupported | 1 unsupported → fixed |

Creative rubric (1–5; v1 re-scored by the reviewers against the new standard):

| Item | Copilot v1 | Copilot v2 | GPT v1 | GPT v2 |
|---|---:|---:|---:|---:|
| Hook strength | 2 | **4** | 3 | 3 |
| Mechanism clarity | 3 | **4** | 3 | **4** |
| Visual–narration sync | 3 | 3 | 3 | 3 |
| Visual variety | 2 | 2 | 2 | 2 |
| Pacing | 2 | **3** | 3 | 3 |
| Payoff usefulness | 3 | **4** | 3 | **4** |
| Caption readability | 3 | 3 | 3 | 3 |
| **Average** | 2.57 | **3.29** | 2.86 | **3.14** |
| Decision | — | FAIL (no blockers) | — | FAIL (no blockers) |
Pass bar: every item ≥ 3 and average ≥ 3.5.

## Verdict
- **Story, script and content improved measurably**: hooks use an approved pattern (Copilot moved from a banned "X just added" opener to a sourced broken-belief hook), mechanisms are numbered with obstacle-first structure, payoffs are actions, illustrative examples are labelled, and claim hygiene is stricter.
- **Visuals did not improve** (variety 2/5 in all four drafts; the frame-difference detector sees no visual change at all). This is the expected limit of the text-card renderer and is now the single biggest gap. Both v2 drafts fail the creative gate only because of it.
- The process caught more errors than dry run 1: an **unsupported claim** (GPT "three things the changelog lists" → now "we picked three"), a **wrong definition** (Copilot "Copilot Evals is a repeatable test" → "An eval is…"), a misleading card ("Same name, new behaviour"), and implied-failure styling.

## Pipeline defects found and fixed during this run
| Defect | Effect | Fix | Test |
|---|---|---|---|
| Single-pass loudnorm undershot the new −14 target | −15.5 LUFS, QA FAIL | Two-pass loudnorm (measure → linear) | `test_parse_loudnorm_json` |
| Mono SAPI measured vs stereo delivery | still −15.4 LUFS | Convert to stereo before both passes | verified: −14.0 / −14.0 |
| Stale v1 `qa/editorial.md` reused by `qa_report.md` | false "overall PASS" | Removed before review; baseline archived | process note below |
| Editorial parser counted "- none. Checked: …" as a blocker | false blockers | Any bullet starting with "none" = no blocker | `test_editorial_parsing` |
| Reviewer listed passed checks under Blockers | false blockers | Reformatted file; reviewer instruction now requires exactly `- none` | — |
| Directed pauses ignored by renderer | storyboard `pause_after_ms` had no effect | Pauses added to scene timing | `test_directed_pauses_extend_scenes` |

Process note: when re-producing a folder, archive and delete `qa/editorial.md` before rendering so QA cannot mix versions.

## Remaining gaps (priority order for Phase 5)
1. **Visual renderer** — diagrams, flows with the signal trace, split screens, charts and in-scene motion (variety 2 → target ≥ 4). Without this no video can pass the creative gate.
2. **Word-timed captions** — cues break mid-phrase ("So how do you know your"), 4–5 words, no active-word highlight. Needs word boundaries (SAPI `SpeakProgress` events or whisper alignment) and phrase-aware chunking.
3. **Voice pace and quality** — SAPI at rate +1 delivers ~147 wpm on Copilot (below the 150 floor). Quick fix: base rate +2. Real fix: Piper or recorded voice (needs approval). Possible mispronunciations to check by ear: "Sol", "picked".
4. **Hook craft for news topics** — GPT hook is honest but plain (3/5); the checklist pattern lacks stakes. The research skill should prefer topics with a real paradox.
5. **Metadata** — description lists every source in `sources.md`, including ones the script no longer uses (GPT lists the GitHub post). Should list only sources cited by the claim map.

## Your review
Watch both versions side by side:
```
production/2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp/baseline_v1/draft.mp4   (v1)
production/2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp/render/draft.mp4        (v2)
production/2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job/baseline_v1/draft.mp4              (v1)
production/2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job/render/draft.mp4                   (v2)
```
Read: `script.md`, `storyboard.json` (planned visuals), `fact_check.md`, `qa/editorial.md`, `qa_report.md`, `readiness.md` in each folder.
