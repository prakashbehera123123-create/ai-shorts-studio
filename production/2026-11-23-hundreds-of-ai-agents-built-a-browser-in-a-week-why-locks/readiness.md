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
- [x] No `scene_3d` without justification and an installed tool
- [x] Source chip on every factual scene; toy numbers labelled illustrative
- [x] No real logos or vendor UI imitation

## Voice and sound (before render)
- [x] Pronunciation entries for every acronym/version [§3]
- [x] Emphasis and pauses directed per scene
- [x] Voice source decided (recorded / neural TTS / SAPI placeholder disclosed)
- [x] Music and SFX licensed and in the manifest, or deliberately none [§8]

## Edit and render
- [x] Speech starts ≤ 0.3 s; change cadence 1–3 s; no static scene ≥ 6 s [§6]
- [x] Captions word-timed, 2–4 words, active-word highlight, caption zone only [§7]
- [x] −14 LUFS ±1, true peak ≤ −1.5 dBFS [§1]
- [x] Last frame loops to the first

## Review
- [x] `python -m studio qa` PASS
- [x] Creative rubric: all ≥ 3, average ≥ 3.5 [§10]
- [x] Metadata lists every source URL and discloses synthetic voice
- [x] Status READY_FOR_HUMAN_REVIEW — a person uploads manually, never this project

## Notes (2026-11-23)
- Words: 113 (under the 120-145 guide). WAIVED: the owner wants tight English Shorts; the target length is ~40 s.
- Music: self-generated `pad` (no third-party rights) only under scenes 1, 2, 9 and 10 (`"music": true`); none under the explanation. No SFX (owner, 11-22 and 11-23).
- Voice: owner's cloned voice (English), best-of-3 takes, 165 wpm floor; disclosed in metadata.
- Anti-sameness verdict: PASS. A robot construction site with a swarm of small robots and a giant browser frame, unlike the 11-22 night office/desk and
  single robot. The opening is a jam at a LOCK door; the ending calls back to the browser window lighting up. The two B-roll scenes are an org chart and a lesson card.
