# Editorial review (v3, Phase 5 motion renderer): 2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp

Reviewer: video-reviewer agent · Dry run 3 · Inputs: script.md, storyboard.json (structured visuals), sources.md, fact_check.md, metadata.md, render/captions.srt, qa/technical.json, qa/contact_sheet.jpg, qa/frames/scene_03, 06, 08, 09; v1/v2 scores from qa/editorial_dryrun2.md. Audio not heard and video not opened; voice quality and pronunciation are unjudged (only measurements: -14.0 LUFS, -1.5 dBFS, whisper recall 99%, no long silences). Stills are single moments, so in-scene animation is judged only from the storyboard cues and the contact sheet.

Decision: PASS

Plain statement: no blockers, every v3 score is at least 3, and the v3 average is 3.71 (26/7), above 3.5. The gain over v2 comes from structured motion visuals (fork, flow, split, checklist, tiles), word-timed karaoke captions and a loop-able motif. It is a modest pass: sync and pacing sit at 3.

## Rubric

| item | v1 | v2 | v3 | evidence |
|---|---|---|---|---|
| Hook strength | 2 | 4 | 4 | Same sourced broken-belief line (C1/S3). Scene 1 now shows "Same task" forking to "Try 1 passes" (green) and "Try 2 fails" (red), so the claim is visible in the first frame. Not 5: hook text is a plain statement. |
| Mechanism clarity | 3 | 4 | 4 | Numbered 1/3, 2/3, 3/3 headers match spoken "Step one/two/three"; each step has its own diagram (task node, approve/check rows, before/after tile). Scene 4 "Eval = a repeatable test" is a clear definition card. Steps are sparse (one node on the step-1 still). |
| Visual-narration sync | 3 | 3 | 3 | Storyboard has word cues and the karaoke highlight tracks speech (srt is word-chunked, whisper recall 99%). But in scene 9 the still at the caption "and compare the runs." shows all three boxes still unchecked, and scene 6 shows "Check A" greyed at "which checks", so landing on words is unverified or late. |
| Visual variety | 2 | 2 | 4 | Contact sheet: fork diagram, flow, split tiles, hero text, node, checklists, before/after, node-and-curve; nine of ten scenes differ in layout. Same dark palette, and the lower third and the area below the caption are empty. |
| Pacing | 2 | 3 | 3 | 127 words in 47.17 s (about 161 wpm, in the standard's range) and no long silences. Longest static stretch 3.50 s misses the 1-3 s target and visual activity is 49%. Audio not heard. |
| Payoff usefulness | 3 | 4 | 4 | Scene 9 checklist "Rerun the same eval / After every change / Compare the runs" is an action. The "public preview" caveat is now a planned amber tag in scene 9 (storyboard), so muted viewers can see it (tag not visible in the sampled still, appears on the "preview" cue). |
| Caption readability | 3 | 3 | 4 | Large bold white on a dark pill with cyan active-word highlight, correct text, 2-4 words per cue and no mid-word breaks. Weak spots: 0.39 s "An eval" cue, the 2-line "hand, but the rerun shows" pill, and two dangling cues ("Which skill would", "your edit passed by"). |
| **Average** | **2.57** | **3.29** | **3.71** | v1 18/7, v2 23/7, v3 26/7. |

## Blockers
- none

## Blocker checks performed
- Factual overstatement: none. Hook, definition, steps, rerun advice and preview caveat map to S1-S4; no Vally, install-target or plan-list claims on screen or in audio.
- On-screen label audit: every stamped label is either supported by sources.md or marked ILLUSTRATIVE. Supported: "One good answer isn't proof", "Eval = a repeatable test", "Realistic task" (S2), "Approve, then check" (S4), "Compare before/after" (S4), "Rerun after every change" (S3/S4), "public preview" (S1). Illustrative and badged: "Same task / Try 1 passes / Try 2 fails", "Run 1: output A / Run 2: output B", "Tried once: Passed / Rerun: Failed", "You approve the run / Check A", "Before: Check A passed, Check B failed", "Your edit / Passed by hand". The scene 2 title carries "(illustrative)" in text.
- Misleading hook/title: no; the title "GitHub Copilot Evals" is accurate and the hook is a sourced framing.
- Caption error: srt text matches script.md word for word.
- Unreadable text: none; headlines, captions and badges are large and high contrast.
- Missing disclosure: synthetic TTS and original graphics disclosed in metadata.md; the YouTube altered-content setting is flagged for a person.
- Unlicensed asset: 3 manifest rows valid; only the Segoe UI font terms are flagged (T001).

## Warnings
- Accepted limits: SAPI placeholder voice (audio not heard, so delivery and the "MCP" pronunciation are unjudged), no music/SFX by design, Segoe UI font terms to verify before any publish.
- Sync: in the scene 9 and scene 6 stills the checkboxes and rows lag the caption. A person should scrub scenes 6 and 9 to confirm checks land on their cue words.
- Scene 8: the ILLUSTRATIVE badge overlaps the top-right corner of the "Your edit" node and its text is partly crossed by the node border. Still legible, but move the badge or the node.
- Scene 8 sample shows only the "Passed by hand" branch; the failed-rerun branch (storyboard: "Rerun: failed check") is not verified in the stills.
- "public preview" tag in scene 9 is not visible in the sampled still; confirm it appears when "preview" is spoken.
- Empty lower third and the small low-contrast "Source: GitHub · 2026-11-17" line; the source line is small for mobile.
- The technical caption reading-speed warning is driven by speech pace (e.g. "An eval" 0.39 s, "Which skill would" 31 chars/s). Judged from the stills and srt, text is readable, but the 0.39 s cue is hard to read.
- Visual cadence: longest static stretch 3.50 s against the 1-3 s target; activity 49%.
- Whisper did not hear "task" (99% recall); check by ear.
- "Rerun after every change" is slightly stronger than the source's "after you change" (accepted in fact_check.md). The "Step one/two/three" structure is the script's own simplification (flagged in fact_check.md).

## Pass items
- One central question ("how do you know your change helped?"), tension before the fix, a worked example labelled illustrative on screen and in speech, an actionable payoff, and a CTA tied to the hook.
- Claim map: 10 claims, all supported or qualified; metadata links the primary source and discloses synthetic voice.
- Technical: 1080x1920, h264/aac, 47.17 s, -14.0 LUFS, true peak -1.5 dBFS, captions contiguous, render report clean, whisper recall 99%. Measurements only; no audio heard.
- Word-timed karaoke captions with active-word highlight (a v2 gap) and a recurring signal-trace motif.
- Clear improvement over v2 in visual variety (2 to 4) with no loss on content scores.

State: no blockers; QA may proceed toward READY_FOR_HUMAN_REVIEW. This review does not approve publishing; a person must watch and listen to the draft and decide.

## Post-review fixes (main session, 2026-11-20; re-rendered, technical QA re-run, verified on stills)
- ILLUSTRATIVE badge moved up so it no longer touches the hook's 'Your edit' node.
- Checklist ticks now land as each row is spoken (scene 9 previously ticked all rows at the end).
