# Production readiness checklist

Dry run 2 (2026-11-20). Filled by the main session after fact check; QA items are ticked after review. Voice: Windows SAPI placeholder (disclosed). Music/SFX: deliberately none for this dry run.
Updated for dry run 3 (motion renderer).

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
- [x] Hero visual ≥ 40% of frame (motion engine templates)
- [x] Motif enters in hook and returns in payoff [§4.2]
- [x] No `scene_3d` without justification and an installed tool
- [x] Source chip on every factual scene; toy numbers labelled illustrative
- [x] No real logos or vendor UI imitation

## Voice and sound (before render)
- [x] Pronunciation entries for every acronym/version [§3]
- [x] Emphasis and pauses directed per scene
- [x] Voice source decided (recorded / neural TTS / SAPI placeholder disclosed)
- [x] Music and SFX licensed and in the manifest, or deliberately none [§8]

## Edit and render
- [ ] WAIVED: Speech starts ≤ 0.3 s; change cadence 1–3 s — speech starts ≤ 0.1 s; longest static visual-zone stretch is 3.5–4.25 s (target 3 s, limit 6 s)
- [x] Captions word-timed (SAPI word boundaries), 2–5 words, active-word highlight
- [x] −14 LUFS ±1, true peak ≤ −1.5 dBFS [§1]
- [ ] WAIVED: Last frame loops to the first — loop ending needs the motif renderer (Phase 5)

## Review
- [x] `python -m studio qa` PASS
- [x] Creative rubric
- [x] Metadata lists every cited source URL
- [ ] Status READY_FOR_HUMAN_REVIEW — a person uploads manually, never this project
