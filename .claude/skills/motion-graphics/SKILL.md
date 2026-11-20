---
name: motion-graphics
description: Produce 2D motion graphics for a scene — progressive diagrams, architecture flows with a travelling signal dot, animated charts, kinetic type, callouts and step trackers — as deterministic, frame-accurate renders.
---

# Motion graphics (2D)

## Purpose
Use for scenes whose `visual_form` is `diagram_2d`, `architecture_flow`, `chart`, `kinetic_type`, `split_screen`, `ui_mock` or
`title_card`. Covers technical architecture visualisation and data-driven animation. Standards: `docs/CREATIVE_PRODUCTION_STANDARD.md` §4–7.

## Inputs
- One storyboard scene (schema v2) with timing, `motion`, `visual_description`, `source_ids`
- Word timings for the scene (from TTS boundaries or whisper) to sync builds to words
- Palette, layout grid and type sizes from the standard

## Workflow
1. Translate `motion` into a **build list**: element, appear time (word it syncs to), animation (draw-on, pop, travel, count-up), duration.
2. Lay out in the visual zone (y 540–1230). Flows wrap as a vertical S-curve; max 5 nodes visible.
3. Build the scene as an HTML/SVG/CSS template with all animations driven by a single time variable (no wall-clock timers).
4. Render frames deterministically at 30 fps in headless Chromium (Playwright), or Pillow for static layers; encode with FFmpeg.
5. Charts: axis labels, units, start at zero, source chip + date; *illustrative* tag for toy values; value labels count up.
6. Kinetic type: ≤ 6 words, one accent word in Signal cyan, entrance 200–400 ms ease-out.
7. Step tracker `n/N` top-left on every step scene; progress line in the top bar.
8. Check a mid-scene still and the last frame at phone size before handing to editing.

## Tools
Built (Phase 5): `studio/motion/engine.html` (deterministic HTML/SVG engine: every frame is a pure function of spec + t),
`scripts/render_motion.cjs` (headless system Chrome via the globally installed Playwright, frames piped to FFmpeg),
`studio/motion_spec.py` (storyboard + word timings → spec). Enabled by `"renderer": "motion"` in `config/render.json`.
Scene content comes from each storyboard scene's `visual` object; templates and their fields:
- `kinetic` {lines, accent, size} · `title` {text, sub} · `fork` {from, branches:[{label, tone}]}
- `flow` {nodes:[{label, tone}], side} · `split` {left/right:{title, tone, items}} · `checklist` {items, checked, tags:[{text,color}]}
- `stack` {rows, mark, tag} · `panel` {title, fields:[[key,value]], highlight} · `chart` {bars:[{label,value,color}], unit}
- common: `illustrative` (adds the ILLUSTRATIVE chip), `cues` (narration words that trigger each build step, in order).
- **Icons (Lucide, ISC, `vendor/node_modules/lucide-static`, 2,400+ ids — browse lucide.dev/icons):** `icon` on
  `kinetic` (220 px hero icon above the words), on `flow` nodes / `fork` branches / `split` sides; `icons:[...]` parallel
  to `stack.rows` or `checklist.items`. One icon per idea, literal not decorative (bell = notification, moon = idle);
  unknown ids fail the render. Prefer icons on 3–6 scenes per video, not all.
- **HyperFrames scene** (`template: "hyperframes"`, `project: "assets/hf/scene_NN"`): any registry block or Lottie
  animation rendered into the visual zone (1080×670, transparent) and overlaid only for that scene, cached by content.
  Starters: `templates/hf-scene/` (mounts a 1920×1080 registry block scaled to the band — enlarge the block's fonts
  first, desktop text is too small on a phone), `templates/lottie-scene/` (dotLottie runtime vendored, self-made check
  animation as an example), library `templates/hf-blocks/` (code-typing, code-diff, ai-chat-reveal, data-chart,
  terminal-simulator, chart-story; Apache-2.0). Never ship third-party logos bundled with a block. Use when a block is
  clearly better than our templates (typed code, chat exchange, real chart); otherwise stay with the engine.
Tones: input (amber), active (cyan), success (mint), failure (coral), muted. Pillow text cards remain as fallback
(`"renderer": "cards"`). Remotion or Manim only if a scene cannot be expressed in HTML/SVG (standard §11).

## Decision rules
- Animate meaning, not decoration: each element appears when it is named.
- One highlight colour per frame for the active element; inactive elements dim to muted.
- Never show more text than the narration says; never tiny labels (< 40 px).
- Before/after numbers get the largest type in the video.

## Outputs
`assets/scenes/<scene_id>/` (template + frames or clip), a manifest row per generated asset, frame-accurate clip per scene.

## Quality checklist
- [ ] Every build event within ±120 ms of its word
- [ ] Something changes every 1–3 s
- [ ] Text sizes ≥ standard minimums; safe zones respected
- [ ] Charts labelled, sourced, honest scale
- [ ] Same input renders identical frames (deterministic)

## Failure handling
- Chrome/Playwright unavailable → set `"browser_channel": "msedge"`, or `"renderer": "cards"` and record the downgrade in QA.
- Scene has no `visual` object → engine falls back to kinetic type and the render report warns; add the object.
- Quick layout check without a full render: `node scripts/render_motion.cjs assets/motion/spec.json x.mp4 --still 2.5,10 --still-dir <dir>`.
- Diagram too dense → split into two scenes or show only the active path.
