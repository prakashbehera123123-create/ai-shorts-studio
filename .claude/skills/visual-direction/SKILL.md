---
name: visual-direction
description: Plan each scene's visual — choose the visual form per beat, layout, motif, transitions and complexity level — producing a schema-v2 storyboard where every visual shows what is being said.
---

# Visual direction

## Purpose
Use after the script is fact-checked. Decides *what the viewer sees* for each sentence and how complex it needs to be
(text, 2D diagram, chart, 2.5D, 3D). Standards: `docs/CREATIVE_PRODUCTION_STANDARD.md` §4–6.

## Inputs
- `script.md` (beats, narration, claim map), `sources.md`
- `templates/storyboard.example.json` (schema v2 reference)
- Asset availability: own UI mocks, self-recorded screen captures, licensed stock

## Workflow
1. Split narration into scenes at beat boundaries and at each new idea (hook scenes 2–3 s; explanation scenes may build 4–12 s).
2. For each scene pick `visual_form` with the selection table in standard §5 — the **least complex** form that shows the sentence.
3. Write `visual_description` (what is on screen, in which zone of the layout grid) and `motion` (what changes every 1–3 s).
4. Place the motif: where it enters (hook), what it does in flows, how it returns resolved (payoff, `match_cut`).
5. Choose `transition_in` per scene (cut on beat changes, crossfade on calm beats, push/zoom_through into diagrams).
6. Add a source chip to every factual scene (`source_ids`); mark toy numbers *illustrative* in `on_screen_text`.
6b. Give every scene a structured `visual` object (template + content + `cues`) using the motion-graphics template list;
   labels must use only words from the narration/sources; set `"illustrative": true` for any made-up example content.
7. Set `schema_version: 2`; run `python -m studio script <folder>`; fix errors.

## Tools
Storyboard JSON; the motion-graphics and depth-and-3d skills for execution; Pillow/FFmpeg previews for layout checks.

## Decision rules
- If the narration names a process → `architecture_flow`; parts → `diagram_2d`; numbers → `chart`; options → `split_screen`.
- Never three `kinetic_type` scenes in a row; never a scene ≥ 6 s without described motion.
- `creative.central_question` ≤ 72 chars: it is drawn as a two-line overlay above every context/explanation headline
  (the script check rejects longer ones; 2026-11-20 a 3-line question collided with headlines).
- Long identifiers (namespaced spec keys, URLs) belong in `panel` fields; the engine wraps them onto their own line after
  `/` or `.` — still check a still at phone size, and prefer the shortest exact spelling the source uses.
- 3D is optional and decided per scene from the script: only for a physical object, a place/scale in space, or a
  spatial mechanism 2D cannot show (depth-and-3d skill gate). Most videos have 0 such scenes. Then use
  `visual.template: "scene3d"` + `visual.project`; the renderer builds it only for those scenes.
- `scene_3d` only with `visual_justification` and an installed tool; otherwise `parallax_2_5d`.
- Generic atmosphere (`still_motion`, `broll_video`) never carries the explanation and never exceeds 20% of runtime.
- No real logos or vendor UI imitations.

## Outputs
`storyboard.json` (schema v2: `beat`, `visual_form`, `transition_in`, `motion`, `visual_description`, `sfx`, `voice`, `source_ids`).

## Quality checklist
- [ ] Every scene's visual depicts its own sentence
- [ ] Hero visual fills ≥ 40% of frame; captions in caption zone only
- [ ] Motif enters in hook and returns in payoff
- [ ] Visual form varies; complexity justified
- [ ] Storyboard validates (schema v2)

## Failure handling
- A concept has no honest visual → use a labelled diagram of the claim itself, not decorative imagery.
- Required asset unavailable (e.g. 3D) → downgrade one complexity level and note it in the storyboard.
