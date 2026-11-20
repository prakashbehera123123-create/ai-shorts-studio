# Production readiness checklist

Copy into the production folder as `readiness.md` before assets/rendering. Tick each item or write `WAIVED: <reason>`.
Standard: `docs/CREATIVE_PRODUCTION_STANDARD.md` (section numbers in brackets).

## Research (before scripting)
- [ ] Every claim needed for hook, steps, example and payoff is in `sources.md` with a primary source [§9]
- [ ] Source conflicts recorded; script does not resolve them
- [ ] Brief names the tension (paradox / broken belief / black box / before→after) [§2.2]
- [ ] Brief names one worked example (real, or marked illustrative) and one visual metaphor

## Story and script (before storyboard)
- [ ] Three hook candidates written and scored; chosen hook ≤ 3 s, no banned opener [§2.2]
- [ ] Central question stated in the hook and answered in the payoff [§2.3]
- [ ] Beats present: hook → context/tension → explanation → example → payoff → CTA [§2.1]
- [ ] Obstacle/failure shown before the fix; caveat included if sourced
- [ ] 120–145 words, one language, sentences ≤ 14 words, jargon defined [§3]
- [ ] `python -m studio script` clean; fact check 0 unsupported

## Visual plan (before assets)
- [ ] Storyboard is schema v2 and validates
- [ ] Each scene's visual depicts its own sentence; least-complex form chosen [§5]
- [ ] Hero visual ≥ 40% of frame; layout zones respected [§4.3]
- [ ] Motif enters in hook and returns in payoff [§4.2]
- [ ] No `scene_3d` without justification and an installed tool
- [ ] Source chip on every factual scene; toy numbers labelled illustrative
- [ ] No real logos or vendor UI imitation

## Voice and sound (before render)
- [ ] Pronunciation entries for every acronym/version [§3]
- [ ] Emphasis and pauses directed per scene
- [ ] Voice source decided (recorded / neural TTS / SAPI placeholder disclosed)
- [ ] Music and SFX licensed and in the manifest, or deliberately none [§8]

## Edit and render
- [ ] Speech starts ≤ 0.3 s; change cadence 1–3 s; no static scene ≥ 6 s [§6]
- [ ] Captions word-timed, 2–4 words, active-word highlight, caption zone only [§7]
- [ ] −14 LUFS ±1, true peak ≤ −1.5 dBFS [§1]
- [ ] Last frame loops to the first

## Review
- [ ] `python -m studio qa` PASS
- [ ] Creative rubric: all ≥ 3, average ≥ 3.5 [§10]
- [ ] Metadata lists every source URL and discloses synthetic voice
- [ ] Status READY_FOR_HUMAN_REVIEW — a person uploads manually, never this project
