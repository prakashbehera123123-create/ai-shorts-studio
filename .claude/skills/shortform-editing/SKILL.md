---
name: shortform-editing
description: Assemble scenes into the final Short — pacing, transitions, word-synced captions, audio-visual sync, B-roll placement, loop ending — and run the pre-QA edit check.
---

# Short-form editing

## Purpose
Use after scenes and audio exist. Turns rendered scenes + voice + music into `render/draft.mp4` that holds attention without
visual noise. Standards: `docs/CREATIVE_PRODUCTION_STANDARD.md` §6–8.

## Inputs
- Scene clips/frames (motion-graphics, depth-and-3d), `storyboard.json` (schema v2)
- Narration audio with word timings; music bed and SFX with licences
- `config/render.json`

## Workflow
1. **Conform timing:** set each scene to its voiced duration (+ pause_after_ms); hook scenes stay ≤ 3 s total.
2. **Transitions:** apply `transition_in` per scene (FFmpeg `xfade` for crossfade/push/wipe; hard cut otherwise), 6–12 frames.
3. **Camera:** subtle push-in (≤ 5%) on any held frame without internal motion.
4. **Captions:** 2–4 words, word-timed, active word in Signal cyan, caption zone only; export `captions.srt` too.
5. **Audio:** voice + ducked music + SFX on their cue words; normalise to −14 LUFS, true peak ≤ −1.5 dBFS.
6. **Loop:** end on the motif/question so the last frame cuts cleanly to the first.
7. **Edit check:** watch at phone size via sampled stills + caption file: is the screen changing every 1–3 s? does each visual match its words?
8. Render, then hand to review-short.

## Tools
`python -m studio render` — with `"renderer": "motion"` it assembles schema-v2 storyboards in the motion engine: transitions
(cut, crossfade, push, zoom_through, match_cut), ≤3% push-in per scene, word-timed karaoke captions from SAPI word boundaries
(phrase-aware, never ending on a weak word), directed pauses, two-pass loudness to −14 LUFS. FFmpeg (`sidechaincompress`
for music ducking — not wired yet, no licensed bed). `python -m studio qa` measures visual cadence (visual zone only) and
whisper recall of the script.

## Decision rules
- Cut on beat changes; dissolve only on calm beats; never transition mid-sentence unless it is a match cut.
- B-roll/atmosphere ≤ 20% of runtime and never during the explanation of the mechanism.
- If a visual and a word disagree, fix the visual timing, not the voice.
- Remove anything that moves without meaning (spinning icons, random particles).

## Outputs
`render/draft.mp4`, `render/captions.srt`, `render/render_report.json`, updated manifest.

## Quality checklist
- [ ] Speech starts ≤ 0.3 s; hook ≤ 3 s
- [ ] Visual change cadence 1–3 s; no scene ≥ 6 s without motion
- [ ] Captions word-synced, ≤ 4 words, readable, inside zone
- [ ] Music ducked; −14 LUFS; no clipping
- [ ] Last frame loops to the first

## Failure handling
- Over length → trim pauses first, then the least important step (story-architecture), never the payoff.
- Word timings unavailable → fall back to proportional caption timing and flag it in QA.
- Transition artefacts → replace with a hard cut.
