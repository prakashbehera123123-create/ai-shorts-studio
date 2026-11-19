---
name: produce-daily-shorts
description: Orchestrate a daily batch of up to two source-backed faceless Shorts and stop for human review.
---

# Produce daily Shorts
Preconditions: local tools verified; channel config present.
1. Run `/research-topics` or invoke the research-topics skill workflow.
2. Select up to two non-duplicate, high-evidence topics. Ask for approval only if topic evidence is weak or topic choice is genuinely ambiguous; otherwise proceed with best two.
3. For each topic, use scriptwriter to create script and storyboard.
4. Use fact-checker to audit every concrete claim. Resolve unsupported claims before production.
5. Create `assets/manifest.csv`; identify each asset as generated, user-provided, self-captured, or licensed stock. Do not download unlicensed media.
6. Generate voiceover only if an approved local TTS engine is installed; otherwise create a clean narration file and stop for voice recording.
7. Generate captions and local graphics. Render using project scripts.
8. Run technical QA and video-reviewer. Fix blockers once, rerun QA.
9. Write `metadata.md`, `qa_report.md`, and `status.json`.
10. Stop at `READY_FOR_HUMAN_REVIEW`. Present file paths, source summary, warnings, and review checklist.
Never upload or publish.
