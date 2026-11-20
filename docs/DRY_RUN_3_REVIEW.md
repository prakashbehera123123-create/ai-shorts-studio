# Dry run 3 review — Phase 5 motion renderer

Date: 2026-11-20 · Same two topics and v2 scripts as dry run 2; only the production pipeline changed.
Both folders: **READY_FOR_HUMAN_REVIEW** (all gates passed). Nothing published.

## What Phase 5 built
| Piece | Files | Notes |
|---|---|---|
| Motion engine | `studio/motion/engine.html` | Deterministic HTML/SVG: every frame is a pure function of (spec, t). 9 templates: kinetic, title, fork, flow, split, checklist, stack, panel, chart. Signal-trace motif, transitions (cut, crossfade, push, zoom_through), ≤3% push-in, step tag, pinned question, source chip, ILLUSTRATIVE badge, karaoke captions. |
| Frame renderer | `scripts/render_motion.cjs` | Headless system Chrome via the Playwright bundled in the global `@playwright/cli` (no new installs); JPEG frames piped to FFmpeg; `--still` mode for quick layout checks. ~2 min per 50 s video. |
| Spec builder | `studio/motion_spec.py` | Storyboard `visual` objects + word timings → spec; cues sync each build step to a narration word; phrase-aware karaoke chunks (≤4 words, never end on a weak word, flashes < 0.8 s merged). |
| Word timing | `studio/tts.py` | SAPI `SpeakProgress` word boundaries, mapped back through pronunciation rewrites. Found and corrected SAPI's 16 kHz position time base (positions were 1.5× late at 24 kHz). |
| Assembly | `studio/compose.py` | `"renderer": "motion"` path; directed pauses; two-pass loudness to −14 LUFS; base TTS rate +2. Text cards kept as fallback. |
| QA | `studio/qa.py` | Visual-cadence check on the visual zone only (blocker > 6 s static, warning > 3 s); whisper recall of the script (warning < 90%); caption rules updated for word-timed captions. |
| Metadata | `studio/metadata.py` | Lists only sources the video cites. |
| Contracts | `studio/storyboard.py` | Optional `visual` object validated against the template list. |
Tests: 137 passing, including a determinism test (two renders of the same spec give byte-identical frames).

## Results across the three dry runs

| Metric | Copilot v1 | v2 | **v3** | GPT v1 | v2 | **v3** |
|---|---:|---:|---:|---:|---:|---:|
| Hook | 2 | 4 | **4** | 3 | 3 | **3** |
| Mechanism clarity | 3 | 4 | **4** | 3 | 4 | **4** |
| Visual–narration sync | 3 | 3 | **3** | 3 | 3 | **4** |
| Visual variety | 2 | 2 | **4** | 2 | 2 | **4** |
| Pacing | 2 | 3 | **3** | 3 | 3 | **3** |
| Payoff usefulness | 3 | 4 | **4** | 3 | 4 | **4** |
| Caption readability | 3 | 3 | **4** | 3 | 3 | **3** |
| **Rubric average** | 2.57 | 3.29 | **3.71** | 2.86 | 3.14 | **3.57** |
| Creative gate (≥3 each, avg ≥3.5) | — | FAIL | **PASS** | — | FAIL | **PASS** |
| Duration (s) | 50.07 | 51.87 | 47.17 | 50.30 | 49.87 | 49.87 |
| Loudness (LUFS) | −16.4 | −14.0 | −14.0 | −16.3 | −14.0 | −14.0 |
| Longest static visual zone (s) | 6.75 | — | **3.5** | — | — | **4.25** |
| Visual zone active (%) | 9 | — | **49** | — | — | **41** |
| Whisper recall of script | — | 98% | 99% | — | 94% | 97% |
| Caption chunks | 30 | 32 | 35 (word-timed) | 33 | 31 | 39 (word-timed) |

## Issues found and fixed during this run
- SAPI word positions 1.5× late at 24 kHz → time-base correction (`parse_marks`), verified at 16/22.05/24/48 kHz.
- Cadence metric could not tell text cards from motion (captions counted as change) → measure the visual zone only.
- Caption coverage rule assumed gapless proportional captions → allows ≤ 0.75 s pauses, requires start ≤ 0.3 s.
- Flashing 0.3–0.45 s caption chunks → merged into neighbours (≤ 5 words).
- Layout: fork branch outside the safe margin; split panels too tall; stack tag overlapping; tags wrapping; "GPT-6.2" breaking at its hyphen; ILLUSTRATIVE badge touching a node; checklist ticks landing late — all fixed and re-verified on stills.
- Missing ILLUSTRATIVE label on the GPT message stack (reviewer catch) → added.

## Remaining gaps (next priorities)
1. **Voice** — the SAPI placeholder is the weakest element; GPT runs at rate +3 to fit 55 s, which also drives the caption reading-speed warnings. Options: Piper neural TTS (needs install approval) or a recorded voice.
2. **Hooks for news topics** — GPT hook still 3/5; research should prefer topics with a real paradox or stake.
3. **Cadence** — longest static stretches 3.5–4.25 s vs the 3 s target; add mid-scene motion for long scenes (e.g. motif dot loops, highlight sweeps).
4. **Sound design** — no music bed or SFX yet (needs a licensed track); ducking is designed but not wired.
5. **Loop ending** and **2.5D/3D** — not implemented; not needed for these topics.
6. Engine template coverage is deliberately small; new visual forms need a template + test.

## Your review
```
production/2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp/render/draft.mp4
production/2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job/render/draft.mp4
```
Compare with `baseline_v1/draft.mp4` in each folder. Review checklist: `qa_report.md` in each folder.
