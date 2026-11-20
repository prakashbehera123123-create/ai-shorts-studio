# Build plan

## Milestone 0 — Environment
Verify Python, Git, FFmpeg, Claude Code. Node optional.
Acceptance: all required commands work from PowerShell.

## Milestone 1 — Repository and production contracts
Create directory structure, config, status schema, asset manifest, and tests.
Acceptance: `pytest -q` passes; no API credentials required.
Implemented in `studio/` (stdlib only) + `config/production.json`. CLI:
`python -m studio new <slug> --language English|Hinglish [--date YYYY-MM-DD]`,
`python -m studio validate <folder>`, `python -m studio status <folder> [--set STATUS --note "..."]`.
Status changes are gated: SCRIPT_READY needs storyboard scenes, ASSETS_READY needs manifest rows,
RENDERED needs `render/*.mp4`. No PUBLISHED/UPLOADED/SCHEDULED state exists.

## Milestone 2 — Research and editorial workflow
Implement `/research-topics` and `/produce-daily-shorts` skills. Research 8–12 candidates, cite primary sources, score them, select at most two.
Acceptance: no unsupported claims; output includes source URLs and publication/access dates.
Implemented in `studio/research.py` + `studio/shortlist.py`, rules in `config/research.json`, contract in
`templates/research-candidates.example.json`. CLI: `python -m studio research init|check <file>|apply <file>`.
Code enforces source fields/dates, primary-source + 7-day window for news, weighted scoring, duplicate and
low-evidence rejection, max 2 selections. Claim truthfulness still depends on the agent's spot-checks.

## Milestone 3 — Script and storyboard
Generate concise scripts and scene-level storyboard JSON.
Acceptance: script fits target runtime; language is consistently English or Hinglish; every factual claim has source mapping.
Implemented in `studio/script.py`; CLI `python -m studio script <folder>`. Checks: 100–160 spoken words,
estimated runtime at 165 wpm within 25–55s, single language, every claim row cites S ids that exist in
sources.md, every spoken number appears in a mapped claim, storyboard narration equals the spoken text
word-for-word, per-scene pace ≤ 200 wpm, and `fact_check.md` has a verdict for every claim with none
unsupported. The SCRIPT_READY gate enforces all of this.

## Milestone 4 — Deterministic render
Create local voiceover, captions, graphics and FFmpeg composition.
Acceptance: output MP4 is 1080x1920, H.264/AAC, within configured duration, readable captions.
If no local TTS selected, allow a manual voiceover file and report it as a prerequisite.
Implemented: `python -m studio render <folder> [--voice auto|sapi|manual]` (studio/compose.py, tts.py, visuals.py,
config/render.json). Voice: `voiceover/voiceover.wav` if present, else Windows SAPI as a labelled PLACEHOLDER.
Per-scene TTS is measured with ffprobe; captions are timed to real speech, wrapped evenly, checked for size and
safe area; SAPI rate steps up (max +4) to fit 55s, else the script must be shortened. Output: render/draft.mp4,
captions.srt, render_report.json, manifest rows. RENDERED gate requires a render report with zero errors.
Known draft limitation: scenes are text cards; storyboard diagram descriptions are not drawn yet.

## Milestone 5 — QA and human approval
Run technical checks and produce editorial QA report.
Acceptance: status is READY_FOR_HUMAN_REVIEW; no upload/publish action exists.
Implemented: `python -m studio metadata <folder>` (studio/metadata.py) and `python -m studio qa <folder>` (studio/qa.py).
Technical QA (code): spec, loudness -18..-13 LUFS, true peak <= -1 dBFS, no silence >= 1.5s, captions cover the
timeline and stay readable, render report clean, script/fact-check contracts, asset rights; samples one still per
scene to qa/frames + qa/contact_sheet.jpg. Editorial QA: video-reviewer writes qa/editorial.md (Decision, Blockers).
Gates: QA_PASSED needs technical PASS + editorial PASS; READY_FOR_HUMAN_REVIEW needs valid metadata (all source
URLs, synthetic-voice disclosure, no hype) and qa_report.md Overall PASS. A test forbids network/YouTube clients.

## Creative reverse-engineering (done 2026-11-20, awaiting owner review)
8 reference videos analysed locally (`studio/reference.py`, `python -m studio reference`), findings in
`docs/REFERENCE_VIDEO_ANALYSIS.md`, standard in `docs/CREATIVE_PRODUCTION_STANDARD.md`, 7 new skills + 4 rewritten,
agents updated, storyboard schema v2 validator, readiness checklist, loudness target −14 LUFS.

## Phase 5 — Creative production upgrade (IN PROGRESS, approved 2026-11-20)
Done: motion engine + renderer (1), SAPI word timing with 16 kHz time-base correction + karaoke captions (2), assembly
with transitions/push-ins/directed pauses/two-pass loudness (3, music ducking pending a licensed bed), base TTS rate +2 (4,
Piper still needs approval), QA visual-cadence + whisper-recall checks (5), cited-sources-only metadata. Benchmark (6): see
docs/DRY_RUN_3_REVIEW.md.
Voice (2026-11-20, after review): owner's voice cloned locally (Chatterbox, MIT) from a Demucs-cleaned reference;
per-scene denoise, whisper-recall retakes, clip cache; `python -m studio voice prepare`. Validated on test lines only
(owner asked to skip re-rendering today); first full render with the cloned voice is the next production run.
Goal: produce Shorts that meet the creative standard, not just the technical spec.
1. Scene renderer: HTML/SVG/CSS templates (diagram build, architecture flow with signal trace, chart, split screen,
   kinetic type, step tracker, title card) rendered frame-by-frame with Playwright → clips. Deterministic, tested.
2. Word-level timing: SAPI word-boundary events (and Piper/whisper when available) → karaoke captions (ASS) with
   active-word highlight.
3. Assembly v2: scene clips + `xfade` transitions + push-ins + music bed ducking (`sidechaincompress`) + SFX cues.
4. Voice: per-scene emphasis/pauses (SSML where supported); evaluate Piper (needs install approval).
5. QA additions: change-cadence check on our render, whisper transcript vs script, creative rubric parsing in gates.
6. Re-produce one existing topic end to end as the benchmark, compare against the dry run with the same metrics.
Acceptance: storyboard v2 + readiness checklist complete; render meets §1–8 of the standard; rubric average ≥ 3.5.

## Milestone 6 — Optional integrations
Only after successful manual use: Playwright CLI, GitHub automation, Drive asset retrieval, YouTube API research. Each integration must be justified and permission-reviewed.
