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

## Milestone 3 — Script and storyboard
Generate concise scripts and scene-level storyboard JSON.
Acceptance: script fits target runtime; language is consistently English or Hinglish; every factual claim has source mapping.

## Milestone 4 — Deterministic render
Create local voiceover, captions, graphics and FFmpeg composition.
Acceptance: output MP4 is 1080x1920, H.264/AAC, within configured duration, readable captions.
If no local TTS selected, allow a manual voiceover file and report it as a prerequisite.

## Milestone 5 — QA and human approval
Run technical checks and produce editorial QA report.
Acceptance: status is READY_FOR_HUMAN_REVIEW; no upload/publish action exists.

## Milestone 6 — Optional integrations
Only after successful manual use: Playwright CLI, GitHub automation, Drive asset retrieval, YouTube API research. Each integration must be justified and permission-reviewed.
