# Tools in use, and alternatives (2026-11-20)

Machine: Intel i5-13420H (12 threads), 16 GB RAM, Intel UHD integrated graphics — **no NVIDIA GPU**, so anything
needing CUDA (most local image/video generation) runs on CPU only, slowly.

## What the pipeline uses today

| Task | Tool | Notes |
|---|---|---|
| Topic research | `research-analyst` agent (Sonnet) with web search/fetch; orchestrator re-opens primary pages in the built-in browser | ~4 min agent + ~2 min verification per run |
| Scoring, selection, folders | `python -m studio research check/apply` | deterministic, seconds |
| Script + storyboard | `scriptwriter` agent (Sonnet), story-architecture + visual-direction skills | ~2.5 min, both videos in parallel |
| Fact check | `fact-checker` agent (Sonnet) | ~45 s per video, parallel |
| Gates / contracts | `python -m studio script / status / validate` | |
| Voice | **Chatterbox 0.1.7** (MIT) cloning the owner's voice, reference cleaned with **Demucs 4.0.1** (MIT), FFmpeg denoise | ~10 min per video on CPU — the slowest step. Settings frozen (owner approved) |
| Voice QA | whisper.cpp `ggml-base` via the FFmpeg `whisper` filter | per-scene recall, retakes |
| Motion graphics | Own HTML/SVG engine (`studio/motion/engine.html`) rendered frame by frame in headless Chrome via Playwright | 9 templates: kinetic, fork, flow, split, checklist, stack, panel, chart, title |
| Captions | Word-timed chunks drawn by the same engine | |
| Encode / mix / loudness | FFmpeg 9 (two-pass loudnorm −14 LUFS) | |
| Technical QA | `python -m studio qa` (ffprobe, ebur128, silencedetect, frame-difference cadence, whisper recall) | |
| Creative review | `video-reviewer` agent on sampled stills | |
| Archive | `render/versions/<timestamp>/` on re-render; `final/<date>/<video>/` on READY_FOR_HUMAN_REVIEW | nothing is overwritten |

**HyperFrames** is used **only for optional 3D scenes** (since 2026-11-20: a storyboard scene with `scene_3d` + template
`scene3d` is rendered by `studio/scene3d.py`; videos without such a scene never call it). **Remotion** is not used. Our engine does the same job — deterministic HTML frames to FFmpeg — in a
much smaller form. Remotion is not installed.

## Better or additional tools we are not using

| Need | Candidate | Cost / licence | Fit for this PC | Recommendation |
|---|---|---|---|---|
| Richer motion, transitions, ready blocks | **HyperFrames** (installed) — registry of ~450 blocks (transitions, kinetic type, charts, captions, 3D, camera moves), Three.js/GSAP/Lottie runtimes, Studio preview editor | free CLI; check each block's licence | yes (Chrome-based like ours) | **Pilot next**: build one scene type (3D hero or chart) in HyperFrames and compare with our engine |
| Same, React-based | Remotion | free for individuals/small teams; company licence above that (check current terms) | yes | Not needed if HyperFrames works — two engines would be overhead |
| Math/mechanism animation | Manim (Community, MIT) / Motion Canvas (MIT) | free | yes, CPU | Optional for algorithm explainers |
| 3D hero objects, low-poly characters | **Three.js inside HyperFrames** (in-browser) or **Blender** (GPL, free; not installed) with CC0 model packs (e.g. Kenney, Quaternius — verify licence per pack) | free | Three.js: yes. Blender Eevee on integrated GPU: slow but workable for short shots | Three.js first; Blender only for hero shots that need it |
| AI-generated images | Local: ComfyUI + SDXL-Turbo / FLUX.1-schnell (Apache-2.0) | free, but **CPU-only here: minutes per image (untested)** | weak | Use only for atmosphere stills; or approve a paid/cloud image service (CLAUDE.md rule 8 needs your approval) |
| AI-generated video clips | Runway, Kling, Veo, Sora-class services | paid / credit-based, cloud | n/a locally | Not without explicit approval; never as the main explanation |
| Real-world imagery | NASA image library (most is public domain — check each item), Wikimedia Commons (per-file licence), Pexels/Pixabay (own licences) | free | yes | Good for space/science topics; record licence per asset |
| Music / SFX bed | YouTube Audio Library, Pixabay Music, freesound (per-file CC licence) | free | yes | Add a ducked bed — references use one; we are voice-only today |
| Manual polish | CapCut / DaVinci Resolve (free tier) | free | yes | Commonly used by creators for final touches; optional, outside this pipeline |

"Popular creators use X" is not measured here — the table names commonly used options; check current pricing/licences
before adopting any.

## How the reference-video looks map to buildable work

| Look in references | How we can make it | Status |
|---|---|---|
| Dark data-viz diagrams, flows, charts, UI mocks, step trackers | Our motion engine (or HyperFrames blocks) | **Done** |
| Low-poly 3D cartoon characters/offices | Three.js scene in HyperFrames with CC0 low-poly models, keyed poses; or Blender | Feasible, not built — needs a pilot |
| 3D hero object (satellite, phone, server) with leader-line callouts | Three.js hero + our callout labels | Feasible, not built |
| Photoreal Earth / zoom from city to orbit | NASA public-domain textures on a Three.js sphere, camera dolly | Feasible, not built |
| AI-generated illustrations | Local SDXL-Turbo/FLUX on CPU (slow) or an approved paid service | Needs your decision |
| Fully 3D-animated "what happens if" explainers | `faceless-shorts` skill styles (Deep Dive 3D, Inside Out, Paper Atlas…) made in code | Available as a separate style; would replace our look for that video |

## 3D pilot result (2026-11-20)

`pilots/3d-hero/` — HyperFrames 0.9.66 + Three.js r147 + GSAP (both loaded from jsDelivr at render time, so the render
needs network access). A procedural low-poly planet and satellite (no third-party assets), camera dive, three leader-line
callouts anchored to 3D points, our palette, 1080×1920.

- `hyperframes check`: 0 errors after fixes (contrast, safe zones, one-time label measurement); remaining warnings are
  TikTok-only edges and stars touching the frame edge (intended).
- Render: 7 s at 30 fps in **44 s** on this CPU (~6 s per video second; our 2D engine is ~2.5 s). Fine for one 5–8 s
  3D scene per Short.
- Learned: HyperFrames' YouTube Shorts safe zone flagged text above y≈250 px and right-rail overlap. Our standard's
  question zone starts at y=190 — worth re-checking our own layout against the Shorts top UI.
- Integration path (not built): render the 3D scene as its own clip, leave the visual zone empty for `scene_3d` scenes in
  our engine, and overlay the clip with FFmpeg for that scene's time range; captions/headline stay in our engine.

## What faceless / explainer creators commonly use (web search 2026-11-20; mostly vendor or affiliate guides — opinion, not usage data)

| Job | Commonly named tools | Our equivalent |
|---|---|---|
| Script | ChatGPT or similar LLMs | scriptwriter agent + fact-checker (sourced) |
| Voice | ElevenLabs (paid plans for commercial use / instant cloning) | Chatterbox local clone (free) |
| Editing, auto-captions, templates | CapCut (free, mobile-first), Descript | own engine + FFmpeg, word-timed captions |
| Clipping long videos to Shorts | OpusClip, AutoShorts AI | not needed (we make native Shorts) |
| Graphics | Canva Pro | own engine templates |
| Polished motion design | Adobe After Effects (paid) | own engine; HyperFrames registry for richer blocks |
| 3D | Blender (free), Cinema 4D (paid) | HyperFrames + Three.js (optional per scene) |
| Template animation | Vyond, Powtoon, Animaker (paid) | — |

Sources: github.com/sasharun/awesome-faceless; opus.pro blog (best AI tools for faceless channels); outlierkit.com
(best faceless video tools); metricool.com (faceless YouTube channel); creamyanimation.com (animation apps);
imagine.art (best tools for motion design).

## Free / open-source toolkit research (2026-11-20) and recommendation

Goal: more professional, eye-catching, engaging Shorts while staying free, local and automatable (Windows, CPU only).
Retention guides (vendor blogs — opinion) agree on: constant subtle motion (punch-ins, drifts), kinetic text on key words,
and **sound design** — whooshes on transitions, pops on text, a quiet music bed (about 3–5 SFX per 30 s; music well
under the voice). Our videos already have motion and kinetic text; **sound is the biggest gap**.

### Recommended (fits our automated pipeline)

| # | What | Why | Licence (verify per item) | Setup |
|---|---|---|---|---|
| 1 | **Sound design layer**: music bed + whoosh/pop/tick SFX on cue words, sidechain ducking | Biggest engagement gap; references use a bed | YouTube Audio Library (YouTube says it is copyright-safe for monetised videos); Pixabay sounds/music (Pixabay licence: commercial use, no attribution required); Freesound **CC0 only** | Owner downloads a small curated pack (~15 SFX + 3–5 beds); code: SFX cues from storyboard `sfx`, ducking in FFmpeg |
| 2 | **HyperFrames registry blocks** (already installed) | ~450 ready transitions, kinetic type, captions, charts, camera moves — fastest route to a "pro" look | per-block; check each | `hyperframes add <block>` (network); adapt our styles |
| 3 | **Icons**: Lucide (ISC) | Clean consistent icons in diagrams instead of text-only boxes | ISC (permissive) | `npm i lucide-static` (needs approval) |
| 4 | **Lottie micro-animations** via dotLottie runtime (MIT) | Animated checkmarks, loaders, arrows, emojis | LottieFiles free animations: Lottie Simple License per help centre, but some items carry creator terms — **check each** | runtime in HyperFrames; curated files only |
| 5 | **CC0 3D models**: Poly Haven (models/HDRIs/textures), Kenney, Quaternius | Better 3D scenes than primitives (characters, devices, offices) | CC0 | download packs on demand for a 3D scene |
| 6 | **Stock b-roll / photos**: Pexels, Pixabay | Atmosphere shots for science/space topics (never the main explanation) | own licences; record per file | on demand |

### Not recommended now

| Tool | Reason |
|---|---|
| Remotion | Source-available; companies need a licence; duplicates our engine + HyperFrames |
| Motion Canvas | Open source, but its generator timeline is harder to automate; good for hand-crafted work |
| Manim | Great for maths/algorithms only; slow renders — revisit for algorithm topics |
| Natron | Reported static since 2022 |
| Blender | Free and powerful but slow on integrated graphics and not automation-friendly; Three.js covers our 3D needs |
| DaVinci Resolve / Fusion, Pikimov, Synfig | Good free manual editors; not part of an automated daily pipeline (fine for your own polish) |
| ZapSplat | Its FAQ says use in YouTube videos counts as redistribution — licence risk |
| AI video/image generators (Runway, Kling, Veo...) | Paid/cloud; needs approval; CPU-only local generation too slow |

Sources: maxon.net (free motion graphics software), b2w.tv (15 free motion graphics tools), github.com/madjin/awesome-cc0,
pixabay.com/service/faq, support.google.com/youtube/answer/3376882, help.lottiefiles.com (commercial use / licensing),
remotion.dev/docs/compare/motion-canvas, beginnersinai.org (Remotion vs Motion Canvas vs Manim), opus.pro and
pixflow.net (retention editing), YouTube videos on Pikimov and TiXL.
