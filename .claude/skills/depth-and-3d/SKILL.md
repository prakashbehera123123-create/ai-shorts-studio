---
name: depth-and-3d
description: Decide whether a scene needs depth, then plan and produce 2.5D parallax or, only when the script calls for a physical object or place in space, a HyperFrames + Three.js 3D hero scene.
---

# Depth and 3D

## Purpose
3D is **opt-in per scene and never required**. Most Shorts use no 3D at all: the default is 2D motion graphics.
This skill decides, from the script, whether one scene genuinely needs depth, and if so builds it. Standard:
`docs/CREATIVE_PRODUCTION_STANDARD.md` §5–6.

## Inputs
- `script.md` (the sentence the scene must show) and the storyboard scene
- Template `templates/scene3d/` (1080×670 transparent HyperFrames + Three.js project: seeded low-poly model, camera move,
  leader-line callouts projected from 3D anchors)
- `config/render.json` → `hyperframes.launcher`

## Workflow
1. **Gate (decide from the script, before any build).** Use 3D only if the spoken sentence is about one of:
   - a **physical object** whose parts/shape matter (satellite, phone, chip, server rack, robot, car sensor);
   - a **place or scale in space** (orbit, a planet, a city to street zoom, inside a data centre);
   - a **spatial mechanism** 2D cannot show clearly (layers stacked in depth, an object rotating to reveal its back).
   Otherwise stop: abstract software ideas (protocols, APIs, prompts, agents, pricing, code) stay 2D
   (`flow`, `stack`, `panel`, `split`, `chart`...). Typical result: **0 scenes**; at most 1 (rarely 2) per video.
2. **Write the justification** in the scene's `visual_justification`: one sentence on what depth shows that 2D cannot.
3. **Storyboard:** `"visual_form": "scene_3d"`, `"visual": {"template": "scene3d", "project": "assets/3d/scene_NN",
   "illustrative": true}` when the model is a generic stand-in (it usually is). Keep `on_screen_text` and narration as
   for any scene — the engine still draws headline, captions, source chip and ILLUSTRATIVE badge around the 3D band.
4. **Build:** copy `templates/scene3d/` to `production/<id>/assets/3d/scene_NN/`; replace the model, anchors and labels
   (labels only use words from the narration); keep the root 1080×670, transparent, everything seeded. Animation should
   finish within ~4 s and then idle, because the clip's last frame is held for the rest of the scene.
5. **Check:** in that folder run the HyperFrames launcher `check --json` (0 errors) and `snapshot --at 1,3,5`; look at the
   frames. `python -m studio render` then renders the clip automatically (cached by content hash, so voice/caption
   re-renders reuse it), lays it into the visual zone for that scene only, and adds a manifest row.
6. **2.5D alternative** when an object has depth but no 3D model is worth building: 2–4 layers drifting at different
   speeds plus a ≤5% push-in, drawn in the HTML engine.

## Tools
- HyperFrames CLI 0.9.66 (installed) via the launcher in `config/render.json`; Three.js r147 + GSAP load from jsDelivr
  at render time (**needs network**). Renders ProRes 4444 with alpha. Cost: ~6 s per video second the first time
  (a 7 s clip ≈ 45–65 s on this PC), then cached.
- Integration: `studio/scene3d.py` (`render_3d_clips`, `apply_3d`), engine template `scene3d` leaves the band empty.
- Models: procedural (built from primitives in code) or CC0 packs with the licence recorded in the manifest. Never
  vendor logos or copied characters. Blender is not installed.

## Decision rules
- No justification, no 3D. When in doubt, choose 2D.
- One hero object, one camera move (push in to explain, pull out for scale). Labels stay 2D-readable (≥ 36 px).
- Never 3D for text, charts, code, UI or abstract concepts.
- Generic models are illustrative: say so with the badge; never imply a real product's exact design.

## Outputs
`assets/3d/scene_NN/` project, cached clip in its `renders/` (git-ignored), manifest row `G3DNN`.

## Quality checklist
- [ ] Gate passed and `visual_justification` written
- [ ] `check` 0 errors; snapshots looked at; labels inside the band and readable
- [ ] Illustrative badge when the model is a stand-in; licence recorded for any non-procedural model
- [ ] Rendered video: 3D visible only during its scene, no seam at the band edges

## Failure handling
- HyperFrames unavailable or no network → the render fails loudly for that scene; switch the scene to 2D
  (`visual_form` → `diagram_2d`, template `stack`/`flow`) rather than shipping an empty band.
- Render too slow → shorten the animation (it holds its last frame) or reuse a cached clip with the same motif.
