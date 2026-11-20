---
name: reference-analysis
description: Analyse reference videos (or our own drafts) locally into compact evidence — shot cadence, loudness, pacing, transcript, contact sheets — and turn findings into production rules without copying.
---

# Reference analysis

## Purpose
Use when the channel owner adds reference videos, or to benchmark our own render against the standard. Produces evidence
for `docs/REFERENCE_VIDEO_ANALYSIS.md` and proposed changes to `docs/CREATIVE_PRODUCTION_STANDARD.md`.

## Inputs
- Video files supplied by the user (default folder `reference/`, git-ignored) or `production/*/render/draft.mp4`
- Optional whisper model `models/ggml-base.bin` (git-ignored)

## Workflow
1. Locate files; never assume names. Confirm they are user-provided and keep them out of git.
2. Run `python -m studio reference <videos> --out reference/_analysis` (`studio/reference.py`).
   For Hinglish/Hindi audio, auto language detection may output Urdu script — re-run whisper with a forced language if text matters.
3. Per video read `summary.json`, `transcript.srt`, `opening_sheet.jpg`, `shots_sheet.jpg`; extract ≤ 6 extra stills at chosen timestamps.
   Never load the full video or audio into the model.
4. Write an 11-part analysis (technical, structure, hook, research, visual, motion, audio, editing, strongest, transferable, do-not-adopt).
   Parallelise across at most 3 analysts with disjoint video sets; they return text, the orchestrator saves it.
5. Consolidate cross-video patterns and a gap table versus our latest draft; convert each gap into a measurable rule.
6. Update the standard and the affected skills; add tests for any new contract.

## Tools
FFmpeg (frame sampling, `ebur128`, `silencedetect`, `whisper`), ffprobe, Pillow contact sheets, `studio/reference.py`.

## Decision rules
- Record techniques, never scripts, graphics, sequences or branding; ≤ 1 short quote per video.
- Label anything about audio as inference unless audio was actually reviewed by a human.
- Treat reference claims as unverified; never reuse their facts without our own primary sources.
- A technique becomes a rule only if it appears in ≥ 2 references or clearly fixes a gap in our draft.

## Outputs
`reference/_analysis/<slug>/` (git-ignored evidence), updated `docs/REFERENCE_VIDEO_ANALYSIS.md`, proposed standard/skill changes.

## Quality checklist
- [ ] Every accessible video has an individual analysis with real timestamps (estimates marked ~)
- [ ] Detector/transcript limitations stated
- [ ] Gap table compares against our actual draft, with actionable requirements
- [ ] Nothing copied; references not committed

## Failure handling
- Detector shows 1 shot for an animated video → sample extra stills at spread timestamps.
- No whisper model → analyse without transcripts and say so; ask before downloading a model.
- Unsupported container/codec → ffprobe error is reported; skip that file.
