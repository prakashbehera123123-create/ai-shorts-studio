# Creative production standard

Version 1 · 2026-11-20 · Applies to every production from Phase 5 onward.
Derived from `docs/REFERENCE_VIDEO_ANALYSIS.md`. This file holds the **standards** (what good looks like, with numbers).
Skills in `.claude/skills/` hold the **procedures** and link to the sections here instead of repeating them.
Project rules in `CLAUDE.md` (sources, one language, no publishing) always take precedence.

## 1. Format

| Item | Standard |
|---|---|
| Canvas | 1080x1920, 30 fps, H.264 + AAC 48 kHz stereo |
| Length | 35–55 s for a single-mechanism Short (config limit 25–55 s). Longer formats need an explicit CLAUDE.md change. |
| Speech start | ≤ 0.3 s. No silent intro, no logo sting. |
| Loudness | −14 LUFS integrated (±1), true peak ≤ −1.5 dBFS, voice always intelligible over music |
| Loop | Last frame should be able to cut back to the first (motif or question returns) |

## 2. Story

### 2.1 Required beats (storyboard schema v2 `beat` values)
`hook` (≤3 s) → `context` or `tension` → `explanation` (1–3 numbered steps) → `example` → `payoff` → `cta`.
`reveal` is optional and sits between example and payoff. A beat may span several scenes.

### 2.2 Hook patterns (choose one; write three candidates, keep the best)
| Pattern | Use when | Honesty rule |
|---|---|---|
| Paradox demo — "this should be impossible" | the mechanism produces a surprising observable effect | the effect must be real and sourced |
| Broken belief — "X doesn't do what you think" | a common misconception exists | the misconception must be common, not invented; no "most engineers get this wrong" without evidence |
| Black box — viewer's own action, then "? ? ?" for the hidden middle | explaining how a familiar tool works | — |
| Before → after number | there is a measurable change | number must be sourced, or labelled *illustrative* |
| Consequence — "your agent passed yesterday and fails today" | a practical risk | must follow from the source |
Banned openers: "Ever wondered…", "In this video…", "X just launched…" without a tension, rhetorical hype.

### 2.3 Story rules
1. One central question, stated in the hook and answered in the payoff. It stays visible (pinned headline or "? ? ?" element) until answered.
2. One running example and one visual motif for the whole video.
3. Name the obstacle or failure case before the solution. End with one caveat or limitation if the sources support one.
4. Numbered steps when there are 2+ steps; show the count early ("3 steps").
5. The payoff is something the viewer can do, check or now explain — not praise of a product.
6. CTA: one action, tied to the hook; no "full video below" unless one exists.
7. Toy numbers are labelled **illustrative** on screen; real numbers carry a source chip.

## 3. Script and voice

| Item | Standard |
|---|---|
| Words | 100–160 spoken (config); target 120–145 for 45–50 s |
| Pace | 165–180 wpm delivered; never below 150 or above 195 |
| Sentences | ≤ 14 words; one idea each; jargon defined in ≤ 6 words the first time |
| Emphasis | 1 emphasised word per sentence max (`voice.emphasis`) |
| Pauses | 150–300 ms before a reveal or step change (`voice.pause_after_ms`); none inside the hook |
| Pronunciation | every acronym and version string has an entry in `config/render.json` → `tts.pronunciations` |
| Voice | recorded human voice, or a neural local TTS; Windows SAPI is a placeholder only and must be disclosed |

## 4. Visual identity (original to this channel)

### 4.1 Palette (semantic, not decorative)
| Role | Hex | Use |
|---|---|---|
| Base | `#0B1020` → `#121A33` gradient | background |
| Text | `#FFFFFF` / muted `#AAB4CF` | headlines / labels, source chips |
| Active concept | Signal cyan `#4CC9F0` | the thing being explained right now, the motif |
| Input / user | Amber `#FFB703` | what the viewer or user provides |
| Success | Mint `#3DDC97` | correct path, pass, after-state |
| Failure / risk | Coral `#FF5D73` | wrong path, fail, before-state, caveat |
Never more than three accent colours in one frame.

### 4.2 Motif: the signal trace
A thin cyan line with a travelling dot represents data, a request or an agent action. It enters in the hook, carries every flow
diagram, and returns resolved in the payoff. It is our recurring identity element; keep it simple and original.

### 4.3 Layout grid (1080x1920)
| Zone | y range (px) | Content |
|---|---|---|
| Top bar | 90–170 | step tag `n/N` (left), progress line |
| Question / headline | 190–520 | pinned question or beat headline, ≤ 2 lines, 76–96 px bold |
| Visual | 540–1230 | one hero visual; must occupy ≥ 40% of the frame |
| Caption | 1250–1480 | 2–4 word captions, active word highlighted |
| Reserved | 1580–1920 | Shorts UI; nothing important. Source chip may sit at 1500–1560 |
Side margins 90 px; right 130 px kept clear of key content (Shorts action buttons).

### 4.4 Typography
Bold geometric sans for headlines/captions, monospace only for code/tokens. Minimum sizes: captions 64 px, headline 72 px,
labels 40 px, source chip 30 px. Until an OFL font is approved, Segoe UI is the placeholder (licence note in manifest).

## 5. Visual form selection

Choose the **least complex** form that shows the sentence being spoken. Storyboard field `visual_form`:
| Information | Form | Notes |
|---|---|---|
| A claim or question | `kinetic_type` | ≤ 6 words on screen; never three kinetic scenes in a row |
| Parts and relations | `diagram_2d` | nodes draw on in narration order |
| A process / request path | `architecture_flow` | motif dot travels each arrow as it is named; S-curve layout for 9:16 |
| Quantities | `chart` | animate from zero, units, source + date chip, "illustrative" when toy |
| A product behaviour | `ui_mock` (own, unbranded) or `screen_capture` (self-recorded, demo data) | never imitate a real vendor UI |
| Two options | `split_screen` | before/after or A/B, colour = failure/success |
| Physical/spatial metaphor | `parallax_2_5d` | layered stills drifting at different speeds |
| A hero object in space | `scene_3d` | only with `visual_justification` and an available 3D tool |
| Section or end card | `title_card` | — |
| Atmosphere only | `still_motion`, `broll_video` | licensed or generated, never as the main explanation |

## 6. Motion and editing

| Item | Standard |
|---|---|
| In-scene change | something meaningful changes every 1–3 s (node, arrow, highlight, counter) |
| Scene length | 2–3 s in the hook; 4–12 s for explanation scenes (they build); ≤ 6 s with no internal motion |
| Transitions | `cut` on beat changes and in the hook; `crossfade` on calm beats; `push`/`zoom_through` to enter a diagram; `match_cut` for the motif callback |
| Camera | push-in ≤ 5% over a held scene; pans follow the flow direction |
| Easing | ease-out for entrances (200–400 ms), ease-in-out for moves; no bounce |
| Sync | every visual event lands within ±120 ms of the word it illustrates |

## 7. Captions
2–4 words per caption, word-timed, active word in Signal cyan, white otherwise, black 70% rounded box, caption zone only.
No caption may cover the hero visual. Jargon shown exactly as spoken. Captions must also be exported as `captions.srt`.

## 8. Sound design
- Music bed: instrumental, licensed or self-made, recorded in the asset manifest with licence; ducked so voice sits ≥ 12 dB above it.
- SFX: at most one per beat change or reveal (soft pop, whoosh, rise). Never under a spoken key term.
- No audio clipping; QA enforces true peak.

## 9. Research and claims on screen
- Every factual card carries a source chip `Source: <publisher> · <date>`.
- On-screen numbers obey the same claim-to-source mapping as spoken numbers.
- No real brand logos or vendor UI imitations; use generic labelled shapes.

## 10. Quality gates (summary)
Automated: `python -m studio script`, `render`, `qa` (format, loudness, captions, contracts, rights).
Creative (video-reviewer rubric, 1–5 each, all ≥ 3 and average ≥ 3.5 to pass): hook strength, clarity of the mechanism,
visual–narration sync, visual variety, pacing, payoff usefulness, caption readability.
Full pre-render checklist: `templates/production-readiness-checklist.md`.

## 11. Tool policy
| Need | Tool | Status | Cost |
|---|---|---|---|
| Assembly, transitions (`xfade`), push-ins (`zoompan`), ducking (`sidechaincompress`), ASS captions | FFmpeg 9 | installed | free |
| Stills, layout, simple cards, 2.5D layers | Pillow | installed | free |
| 2D motion graphics (diagrams, flows, charts, kinetic type) | `studio/motion/engine.html` rendered frame-by-frame in headless system Chrome via the Playwright bundled with the global @playwright/cli (`scripts/render_motion.cjs`) | **built (Phase 5)**; ~2 min per 50 s video | free |
| Word timing, audio↔script QA | whisper.cpp via FFmpeg `whisper` filter, `models/ggml-base.bin` | installed | free (MIT) |
| Cloned voice of the owner | Chatterbox 0.1.7 (Resemble AI, MIT) in `.venv-voice`, CPU PyTorch 2.6 | **installed 2026-11-20**; ~10 min per 50 s video on CPU | free |
| Vocal isolation for the clone reference | Demucs 4.0.1 (Meta, MIT, htdemucs ~80 MB) in `.venv-voice` | **installed 2026-11-20** (by owner); ~75 s per minute of audio on CPU | free |
| Fast CPU cloning (alternative) | Pocket TTS (Kyutai, English + 5 EU languages) | not installed; consider if CPU time matters | free (check weights licence) |
| React motion graphics | Remotion | not installed; only if HTML scenes prove insufficient; licence requires a company licence for larger teams | free for individuals |
| Mathematical animation | Manim Community (MIT) | not installed; only for maths-heavy topics | free |
| 3D hero scenes | Blender (GPL) | not installed; ~1 GB, GPU recommended; only with justification | free |
