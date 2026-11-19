---
name: produce-daily-shorts
description: Orchestrate a daily batch of up to two source-backed faceless Shorts and stop for human review.
---

# Produce daily Shorts
Preconditions: `.venv\Scripts\python.exe scripts\check_environment.py` passes; channel config present.
1. Run the research-topics skill workflow end to end. It produces `research/YYYY-MM-DD/shortlist.md` and up to two `production/YYYY-MM-DD-slug/` folders at status RESEARCHED.
2. Present the shortlist (ranked table, selected folders, warnings). Ask for approval only if fewer than two topics qualified, evidence is medium, or the choice is genuinely ambiguous; otherwise proceed with the selection. Record approval with `python -m studio status <folder> --set APPROVED_TOPIC --note "<who/why>"`.
3. For each approved folder, use scriptwriter with only `brief.md` + `sources.md` to create script and storyboard.
4. Use fact-checker to audit every concrete claim against `sources.md`. Resolve unsupported claims before production.
5. Create `assets/manifest.csv`; label each asset generated_graphic, screen_capture, licensed_stock or user_asset. Do not download unlicensed media.
6. Generate voiceover only if an approved local TTS engine is installed; otherwise create a clean narration file and stop for voice recording.
7. Generate captions and local graphics. Render using project scripts.
8. Run technical QA and video-reviewer. Fix blockers once, rerun QA.
9. Write `metadata.md`, `qa_report.md`; advance `status.json` only through `python -m studio status` (stage gates enforce required files).
10. Stop at `READY_FOR_HUMAN_REVIEW`. Present file paths, source summary, warnings, and review checklist.
Steps 3–10 depend on Milestones 3–5; until those exist, stop after step 2 and report.
Never upload or publish.
