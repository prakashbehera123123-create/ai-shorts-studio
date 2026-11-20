# Reference video analysis

Analysed: 2026-11-20 · Inputs: 8 user-provided reference videos in `reference/` (git-ignored, third-party).
These are learning references, not templates. This document records techniques only; it does not reproduce
scripts, graphics, branding or sequences. Any technique adopted must be re-expressed in our own visual identity
(see `docs/CREATIVE_PRODUCTION_STANDARD.md`).

## Method

Tool: `python -m studio reference <videos>` (`studio/reference.py`), all local, outputs in `reference/_analysis/<slug>/`.

| Evidence | How it was produced | Known limits |
|---|---|---|
| Technical metadata | ffprobe | — |
| Shot changes | 32x56 grey frames at 4 fps, mean abs difference vs the frame 0.5 s earlier, local peaks above max(14, 2.5×median), min gap 0.75 s | Catches cuts and dissolves. Misses changes on near-black UI-only animation (LLM video registered 1 shot). FFmpeg `scdet` was tried first and missed all dissolves. |
| Loudness / LRA / true peak | FFmpeg `ebur128` | — |
| Pauses | `silencedetect` −35 dB, ≥0.25 s | Music beds hide pauses (several videos show ~0–1 pauses). |
| Transcript, wpm, first-speech time | FFmpeg `whisper` filter + whisper.cpp `ggml-base` (multilingual), language=auto | Auto-detect labelled 5 Hinglish tracks as Urdu → garbled text and unreliable wpm. Force `language=hi` or `en` next time. |
| Visuals | `opening_sheet.jpg` (0–6 s at 2 fps), `shots_sheet.jpg` (one still per shot) + up to 6 targeted stills per video | Audio was never listened to; music/SFX/voice character are **inferences** from LRA, pauses and transcript gaps. |

Synthesis: three Sonnet analysts in parallel (independent video batches), then consolidation here. No video was loaded into a model.

## Measured overview

| Video | Dur (s) | Res | Shots | Median shot (s) | Cuts first 10 s | LUFS | True peak | LRA | wpm* | Lang |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| AI Discovers New Planet | 135.9 | 720x1280 | 29 | 2.50 | 5 | −14.1 | −0.2 | 3.0 | 188 | Hinglish |
| AI Models in Space | 148.7 | 720x1280 | 39 | 2.75 | 4 | −13.7 | +0.1 | 2.8 | 184 | Hinglish |
| Design ChatGPT (RAG) | 117.1 | 720x1280 | 17 | 4.75 | 3 | −14.2 | −0.4 | 3.6 | ~170 | Hinglish |
| Uber batched matching (teaser) | 42.6 | 1080x1920 | 2 | 21.3 | 0 | −13.3 | −1.3 | 5.0 | ~193 | Hinglish |
| How Google Authenticator works | 140.6 | 1080x1920 | 15 | 5.50 | 2 | −13.9 | −0.8 | 3.0 | ~172 | Hinglish |
| How LLMs Actually Work | 116.1 | 720x1280 (60 fps) | 1† | — | 0 | −11.2 | +0.1 | 3.9 | 132 | English |
| Incognito is not safe | 124.7 | 720x1280 | 17 | 3.25 | 2 | −14.0 | −0.5 | 3.5 | ~161 | Hinglish |
| What is Databricks | 42.5 | 720x1280 | 8 | 5.62 | 2 | −16.0 | −1.6 | 4.9 | 131 | English |
| **Our dry run (both)** | 50.1 / 50.3 | 1080x1920 | 30 / 33 card swaps | ~1.6 | ~6 | −16.4 / −16.3 | −4.4 | — | 168 / 129 | English |

\* Whisper-derived; "~" = unreliable because of Hinglish mis-detection. † Continuous animation; detector limit.
All videos start speaking at 0.0 s. Six of eight run 117–149 s, well beyond our 25–55 s target.

## Per-video analyses

### 1. AI Discovers New Planet (135.9 s)
- **Narrative:** hook on the viewer's own behaviour, then a surprising fact (0–5 s) → "no real photo exists, so how?" open loop (5–12 s) → data source context (12–22 s) → star brightness as a line over time, transit = dip (22–40 s) → obstacles named one by one, each labelled "fake" before the fix (40–68 s) → the model pipeline (68–100 s) → reveal of discoveries in old data (100–118 s) → payoff "AI isn't just chat" (118–129 s) → CTA that calls back to the opening character (129–136 s).
- **Research:** one ML concept (classification on time series) taught through analogy. On-screen and spoken numbers conflict (star counts); dating of events is ambiguous; no sources on screen.
- **Visual / motion:** low-poly 3D office characters + near-black data-viz world; cyan line charts with a circled dip; sliding window over data; block-diagram network; pill-shaped 2–4 word labels top-centre. One 22 s held diagram that builds progressively.
- **Audio (inferred):** fast, energetic voice (~188 wpm), almost no pauses, likely music bed; true peak −0.2 dBFS is too hot.
- **Editing:** quick cuts early (0.75–1.5 s), then long holds with in-scene animation.
- **Strongest:** relatable opener + callback ending; obstacles named before solutions; one reused visual metaphor (line with a dip).
- **Transfer:** reveal the surprising fact within 5 s; build one diagram progressively and hold it; show failure cases before the fix; close the loop on the opening image.
- **Do not adopt:** 136 s length, 188 wpm, hot peaks, unsourced numbers, mixed scripts.

### 2. AI Models in Space (148.7 s)
- **Narrative:** familiar chat UI → zoom from the viewer's city into orbit (hook, 0–14 s) → evidence cards (14–36 s) → "why a rocket?" question card (43 s) → numbered problems: power, cooling, radiation, cost (43–100 s) → downlink-bottleneck example (100–118 s) → scale reveal + CTA (118–149 s).
- **Research:** strong attribution habit — a small caps "kicker" above each title names the source type (vendor test, estimate, filing). But many future-dated claims are stated flatly and could not be verified.
- **Visual / motion:** photoreal Earth, consistent 3D satellite hero asset, dolly/orbit camera, leader-line callouts on the hero object, kicker + title + subline cards.
- **Audio (inferred):** fast near-continuous narration, likely ambient bed; true peak +0.1 dBFS (clipping risk).
- **Editing:** 2–15 s scenes with slow camera motion inside, crossfades between topics.
- **Strongest:** zoom-out from familiar to new context; attributed fact cards; numbered problems then a scale reveal.
- **Transfer:** source/date kicker above every factual card; numbered problem framing; one hero asset with leader-line callouts.
- **Do not adopt:** claim density, flat future dates, tiny kicker text, language mixing, clipping.

### 3. Design ChatGPT — RAG in 6 steps (117.1 s)
- **Narrative:** concrete before/after number as hook (a huge document answered in seconds, with a page reference) → "it didn't read it all" reveal → names the technique and shows a 6-step overview card (~19 s) → six steps with a worked example → failure mode (wrong chunk = confident wrong answer) → CTA.
- **Research:** one idea via one running example; simplified numbers are labelled "illustrative" (good); one spoken/on-screen number mismatch.
- **Visual / motion:** dark navy, three accent colours, monospace step tags; counter-driven document stack, highlighted chunk overlap, query arrow snapping to nearest neighbours in a vector cloud, prompt assembling, red error callout. Alternates 3D hero props with flat 2D diagram cards.
- **Editing:** few cuts, long holds (up to 23 s) with in-scene animation; bold per-step titles instead of word captions; progress dots.
- **Strongest:** measurable hook; overview card then progress tracker; ending on a limitation.
- **Transfer:** show the step list once, then a persistent n/N tracker; label simplified numbers "illustrative"; end with a limitation before the CTA.
- **Do not adopt:** small monospace text, number mismatches, generic CTA.

### 4. Uber batched matching — teaser (42.6 s)
- **Narrative:** counter-intuitive question pinned as a headline for the whole video (0–2.5 s on) → "the obvious answer is wrong" (2.5–6 s) → mechanism (6–11 s) → two-driver toy example with minute counts, greedy vs batched (11–29 s) → named reveal with a big before→after number and a source chip (~29–39 s) → single-action end card (39.5 s).
- **Research:** one idea, one tiny example. Flags: "most engineers get this wrong" is unsupported; toy numbers not labelled illustrative.
- **Visual / motion:** navy gradient; headline top third, thin-line diagram strip middle, reserved caption zone bottom; dots pop in, curved path arcs with labels, large "before → after" number.
- **Editing:** one continuous 39.5 s shot with progressive build, hard cut to end card. Karaoke captions: 3–5 words, white with the active word highlighted.
- **Strongest:** permanent question headline; toy example with before/after metric; one-action end card. Closest in length to our format.
- **Transfer:** pin the hook question; reserve a caption zone under the diagram; active-word highlight; two-actor toy example with a before→after number.
- **Do not adopt:** unsupported "most people get it wrong" framing, unlabelled invented numbers, "full video below" CTA without a long video.

### 5. How Google Authenticator works (140.6 s)
- **Narrative:** "should be impossible" paradox demo in the first 2 s (offline device still produces a valid code) → proof → five labelled steps (secret via QR, time counter, keyed hash, truncation, server repeats with tolerance) → comparison with an alternative → late twist (a phishing trap) → CTA tied to the topic.
- **Research:** one idea (shared secret + shared clock); mostly accurate; one oversimplification (truncation); one unsourced security claim.
- **Visual / motion:** navy base, own UI mockups, success/failure colour semantics, arrows from two inputs into a labelled function box, dashed device↔server connectors, countdown ring, digit cross-fades. Also real-brand mockups and a mascot.
- **Editing:** one cut per step (15 shots), step tag top-left every scene, headline box doubles as caption.
- **Strongest:** paradox hook; one diagram per labelled step; caveat as final reveal.
- **Transfer:** "impossible" demo hooks; inputs→box→output diagrams; consistent step-tag corner; caveat before CTA.
- **Do not adopt:** 140 s length, real brand UIs, mascot clutter, overlong digit-by-digit explanation.

### 6. How LLMs Actually Work (116.1 s)
- **Narrative:** viewer's own action (typing a prompt, answer appears) then a "? ? ?" box for the hidden middle (0–8 s) → tokens → embeddings → attention with one running pronoun example → layers → "the part most people miss": prediction, not lookup (open loop before reveal) → generation loop → recap pipeline diagram → series CTA.
- **Research:** clear and mostly accurate; illustrative numbers not labelled as such; attention simplified to a single link.
- **Visual / motion:** flat 2D, near-black, monospace; three semantic colours (input, new concept, loop); token chips, vector as coloured cells, stacked layer boxes, travelling dot on a loop arrow, thin progress bar. No camera moves, no cuts.
- **Audio (inferred):** calm, slow (132 wpm), longer pauses at step changes; −11.2 LUFS and +0.1 dBFS peak = over-limited.
- **Strongest:** per-step template (tag + 2-line headline + one diagram); abstractions drawn as literal data shapes; final recap diagram highlighting nodes as they are named.
- **Transfer:** "? ? ?" black-box opener; semantic three-colour palette; recap diagram synced to a one-sentence recap.
- **Do not adopt:** flat static frames with no depth, no muted-viewing captions, slow pace, silent tail, clipping.

### 7. Incognito is not safe (124.7 s)
- **Narrative:** myth contradiction in the first 3 s → "N steps" promise → six numbered stops along the path of one request (device memory, DNS cache, OS screen-time, router, ISP, website + trackers) → late legal-case reveal → two-label verdict → share CTA.
- **Research:** strong myth-buster structure; legal and date specifics unverified; some simplification of caching.
- **Visual / motion:** one physical metaphor — the request is a vehicle on a glowing road; the camera flies stop to stop in a low-poly city; 2D proof cards (terminal output) dissolve in; green/red verdict chip per stop; fixed n/6 tag top-left.
- **Editing:** fast first 20 s (7 changes), a 36 s uninterrupted block, then 5–10 s scenes; dissolves bridge 2D and 3D.
- **Strongest:** spatial metaphor for a network journey; numbered stops; belief-flipping verdict.
- **Transfer:** one physical metaphor for system flows with the camera travelling along it; proof card + flow scene pairing; verdict chips.
- **Do not adopt:** real carrier/brand logos, legal case used as spectacle, fear-leaning framing, mid-sentence language mixing.

### 8. What is Databricks (42.5 s)
- **Narrative:** generic "ever wondered" hook → feature list (platform, engine, clouds, storage layer, notebooks) → generic praise. No tension, example, payoff or CTA. **This is the closest to our dry run, and it is the anti-pattern.**
- **Visual / motion:** AI-generated cinematic stills with slow push-ins and 3–4 s dissolves; single teal/orange grade; one-word centred captions in the lower third. Visuals often do not match the word on screen.
- **Strongest:** compact length; consistent grade; big readable one-word captions.
- **Transfer:** single colour grade; large captions in a fixed zone; dissolves on calm beats.
- **Do not adopt:** generic hook, feature-list structure, unexplained jargon, promotional adjectives, generic imagery, no payoff.

## Cross-video patterns

1. **Hook = contradiction or paradox, made visual, in ≤3 s.** Belief contradiction (Incognito), impossible demo (Authenticator), counter-intuitive question (Uber), black box between action and result (LLMs), before/after number (RAG). The weakest video uses "ever wondered".
2. **One question carries the whole video.** It is pinned (Uber), re-asked as a card (Space) or held as a "? ? ?" box (LLMs) until the reveal.
3. **Numbered structure with a visible tracker.** n/N tags, progress dots or bars appear in 6 of 8 videos.
4. **One running example, one visual metaphor.** A line with a dip; a packet on a road; one PDF; one pronoun. Abstractions become literal shapes.
5. **Build, don't cut.** Median shots are 2.5–5.6 s, but the explanatory core is long held diagrams (15–40 s) that change every 1–3 s inside (element pops, arrows, highlights, counters).
6. **Obstacle before solution, caveat before CTA.** Fakes, problems, failure modes or traps appear before the payoff, and a limitation often closes the story.
7. **Before → after numbers** are the visual climax (14→7 min, 500 pages→seconds).
8. **Attribution on screen** (kicker/source chips) appears in the stronger videos.
9. **Three semantic colours** on a dark navy/near-black base: input, active concept, success/failure.
10. **Captions:** either karaoke 3–5 words with active-word highlight in a reserved zone, or headline-as-caption. All use large bold sans type.
11. **Audio:** speech starts at 0.0 s in every video; dense delivery (160–190 wpm); loudness −14 LUFS; low LRA (≈3) implies a compressed voice over a music bed. Several clip (peak ≥ −0.5 dBFS) — a defect, not a target.
12. **CTA:** one action, often tied back to the hook ("send to the friend who…").

## Gap analysis: first dry run vs references

| Area | Current implementation (2026-11-20 dry run) | Reference observations | Required improvement |
|---|---|---|---|
| Research | Primary sources, verified claims, fact-check gate; candidates scored on six criteria | Strong videos pick topics with a paradox or a broken belief and a worked example; weak ones list features | Add mandatory research fields: `paradox_or_tension`, `worked_example` (with real or clearly illustrative numbers), `visual_metaphor`; reject candidates with none (research-topics skill, content strategy) |
| Topic selection | Highest weighted score; "GPT-6.2 Astra vs Sol" chosen though thin | Each reference teaches one mechanism with a "how does that even work?" angle | Prefer "how/why does X work" mechanisms over announcements; announcements only if they change what the viewer does; require an explainable mechanism |
| Storytelling | Feature walk-through (what it is → what it does → availability → CTA); no tension, no example | Hook → open loop → numbered steps → obstacle → reveal/before-after → caveat → callback CTA | Beat sheet with required beats `hook`, `tension`, `explanation`, `example`, `payoff`; storyboard schema v2 enforces hook ≤3 s and a payoff beat |
| Scriptwriting | 130 words, accurate, neutral; hooks are statements of news ("GitHub just added…") | Hooks are questions/paradoxes tied to the viewer; one running example; obstacle named before fix | Write 3 hook candidates, score them (curiosity, specificity, honesty), pick 1; write narration per beat; one running example; spoken numbers only from mapped claims |
| Voiceover | Windows SAPI placeholder; 168/129 wpm via rate stepping; no emphasis, no designed pauses | Energetic 160–190 wpm, emphasis on key words, pauses at step changes, speech from 0.0 s | Voice direction per scene (`voice.emphasis`, `pause_after_ms`); target 165–180 wpm; neural local TTS (Piper) or recorded voice; SSML emphasis/breaks where engine supports it |
| Visual design | Pillow text cards: headline + caption box; ~50% of each frame empty | Dark base, one hero visual per scene, diagram fills the middle third, semantic colours, source kicker | Fixed layout grid: headline/question top, visual middle (≥40% of frame), caption zone bottom; three semantic colours; visual must depict the sentence being spoken |
| 2D motion graphics | None (static cards; only a progress bar moves) | Progressive diagram builds, arrows with travelling dots, pop-in chips, counters, highlights | HTML/SVG/CSS scene templates rendered frame-accurately (Playwright) for diagram build, flow, chart, compare, step-tracker; in-scene change every 1–3 s |
| 3D animation | None | Used for hero objects and spatial metaphors (satellite, city road), never for text | Default to 2D; allow `parallax_2_5d` (layered stills) for depth; `scene_3d` only with written justification and an available tool; no tool installed yet |
| Data visualisation | None | Before→after numbers, line with highlighted dip, bars | Chart template with units, source and date on screen; animate from zero; "illustrative" tag for toy numbers |
| Editing | Hard switch at every caption chunk (~1.6 s), no transitions, no camera moves | Long builds with internal motion; cuts on beat changes; dissolves on calm beats; slow push-ins | Change cadence: scene per beat (4–12 s) with internal motion every 1–3 s; `transition_in` per scene; subtle push-in (≤5%) on held frames |
| Sound design | Voice only | Inferred music bed under voice, LRA ≈3 | Licensed/self-made music bed ducked 12–18 dB under voice (`sidechaincompress`); sparse SFX on reveals only; every audio asset in the manifest |
| Captions | 6-word chunks, 68 px, centred box, no word highlight, timed proportionally (not word-synced) | 3–5 word karaoke with active-word highlight in a reserved zone, or headline-as-caption | Word-level timing (SAPI/Piper word boundaries or whisper on the final voice); 2–4 words per caption, active-word accent; ASS subtitles via FFmpeg or rendered in the HTML layer |
| Loudness | −16.4 LUFS, peak −4.4 dBFS | ≈ −14 LUFS, several clip | Target −14 LUFS integrated, true peak ≤ −1.5 dBFS (render config + QA range) |
| Length | 50 s | 42–149 s; the two ~42 s videos are teasers/overviews | Keep 35–55 s for single-mechanism Shorts (current rule). A 60–90 s "deep explainer" format would need a CLAUDE.md change — decision for the channel owner |

## Tooling lessons from this analysis

- The frame-difference detector is reusable QA for our own renders (scene-change cadence).
- Whisper must be run with a forced language for Hinglish; auto-detect produced Urdu script.
- Whisper on our own final render can confirm that audio matches `script.md` (a new QA check to add).
