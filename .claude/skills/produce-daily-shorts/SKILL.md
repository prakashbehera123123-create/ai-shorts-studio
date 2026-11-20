---
name: produce-daily-shorts
description: Orchestrate a daily batch of up to two source-backed faceless Shorts — research, approval, per-video production via produce-short, and stop for human review.
---

# Produce daily Shorts

## Purpose
Daily entry point. Runs research once, then produce-short for up to two approved topics, and presents both for human review.

## Inputs
- Passing `.venv\Scripts\python.exe scripts\check_environment.py`
- Channel config; `docs/CREATIVE_PRODUCTION_STANDARD.md`

## Workflow
1. Run the research-topics workflow end to end.
2. Present the shortlist; ask for approval only if < 2 topics qualified, evidence is medium, or the choice is ambiguous.
   Record approval: `python -m studio status <folder> --set APPROVED_TOPIC --note "<who/why>"`.
3. For each approved folder run produce-short. The two videos are independent: scriptwriters, fact-checkers and reviewers
   may run in parallel across videos (max 3 agents at once), never duplicating research.
4. Present both folders: `qa_report.md` summaries, warnings (e.g. placeholder voice), source list, review checklist.

## Tools
`python -m studio` commands; subagents per `docs/MODEL_ROUTING.md`.

## Decision rules
- Quality over quota: one strong Short beats two weak ones.
- Never mix languages within a video; each video picks English or Hinglish.

## Outputs
Up to two production folders at READY_FOR_HUMAN_REVIEW (each auto-copied to `final/YYYY-MM-DD/<video_id>/`; re-renders keep old drafts in `render/versions/`) and a short batch summary. Never delete or overwrite older drafts.

## Quality checklist
- [ ] Research run recorded in `research/YYYY-MM-DD/`
- [ ] Each video passed every gate
- [ ] Warnings surfaced, nothing hidden

## Failure handling
- A video fails QA twice → stop that video, report blockers, continue with the other.
- Research unavailable → stop and report.
Never upload or publish.
