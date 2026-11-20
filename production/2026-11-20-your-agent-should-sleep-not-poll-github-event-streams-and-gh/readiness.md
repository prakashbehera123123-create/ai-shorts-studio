# Production readiness checklist

Copy into the production folder as `readiness.md` before assets/rendering. Tick each item or write `WAIVED: <reason>`.
Standard: `docs/CREATIVE_PRODUCTION_STANDARD.md` (section numbers in brackets).

## Research (before scripting)
- [x] Every claim needed for hook, steps, example and payoff is in `sources.md` with a primary source [§9]
- [x] Source conflicts recorded; script does not resolve them
- [x] Brief names the tension (paradox / broken belief / black box / before→after) [§2.2]
- [x] Brief names one worked example (real, or marked illustrative) and one visual metaphor

## Story and script (before storyboard)
- [x] Three hook candidates written and scored; chosen hook ≤ 3 s, no banned opener [§2.2]
- [x] Central question stated in the hook and answered in the payoff [§2.3]
- [x] Beats present: hook → context/tension → explanation → example → payoff → CTA [§2.1]
- [x] Obstacle/failure shown before the fix; caveat included if sourced
- [x] 120–145 words, one language, sentences ≤ 14 words, jargon defined [§3]
- [x] `python -m studio script` clean; fact check 0 unsupported

## Visual plan (before assets)
- [x] Storyboard is schema v2 and validates
- [x] Each scene's visual depicts its own sentence; least-complex form chosen [§5]
- [x] Hero visual ≥ 40% of frame; layout zones respected [§4.3]
- [x] Motif enters in hook and returns in payoff [§4.2]
- [x] No `scene_3d` without justification and an installed tool (none used)
- [x] Source chip on every factual scene; toy numbers labelled illustrative
- [x] No real logos or vendor UI imitation

## Voice and sound (before render)
- [x] Pronunciation entries for every acronym/version [§3] (MCP, CLI mapped; 'G H' spelled in narration)
- [x] Emphasis and pauses directed per scene
- [x] Voice source decided: owner's cloned voice (Chatterbox, Demucs-cleaned reference), disclosed as synthetic in metadata
- [x] Music and SFX: deliberately none (voice-only; no licensed bed on file)

## Edit and render
- [x] Speech starts ≤ 0.3 s; change cadence 1–3 s; no static scene ≥ 6 s [§6] (QA: captions from 0 s; longest static ≤ 3.25 s)
- [x] Captions word-timed, 2–4 words, active-word highlight, caption zone only [§7]
- [x] −14 LUFS ±1, true peak ≤ −1.5 dBFS [§1]
- WAIVED: Last frame loops to the first — ends on a CTA title card, not a loop; acceptable for this format

## Review
- [x] `python -m studio qa` PASS
- [x] Creative rubric: all ≥ 3, average ≥ 3.5 [§10]
- [x] Metadata lists every source URL and discloses synthetic voice
- [x] Status READY_FOR_HUMAN_REVIEW — a person uploads manually, never this project (set by gate after editorial PASS)

Orchestrator notes (2026-11-20, run 2): research/script/visual items checked against `python -m studio script` (ok), fact_check.md (0 unsupported) and the brief's NOT-to-claim list. Edit/render and review items are ticked after render and QA.
