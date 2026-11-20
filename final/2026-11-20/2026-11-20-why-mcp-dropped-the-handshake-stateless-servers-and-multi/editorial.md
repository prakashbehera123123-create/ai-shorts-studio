# Editorial review: 2026-11-20-why-mcp-dropped-the-handshake-stateless-servers-and-multi

Reviewer: video-reviewer agent (second pass after layout fixes). Inputs: script.md, storyboard.json, brief.md, fact_check.md, metadata.md, readiness.md, render/captions.srt, voiceover/takes.json, qa/technical.json, qa/contact_sheet.jpg, qa/frames/scene_02, plus one extra still extracted at 18.6 s (scene 5). Audio not heard and video not opened; voice quality, clone fidelity and pronunciation are unjudged (measurements only: -14.0 LUFS, -1.5 dBFS, full-mix whisper recall 95.6%, per-scene recall at least 85%, no long silences, runtime 52.13 s). Stills are single moments, so in-scene animation is judged from storyboard cues and the contact sheet.

Decision: PASS

Plain statement: re-reviewed after the re-render (fresh stills at 9.5, 18.6 and 36.5 s plus the regenerated contact sheet). Both earlier layout blockers are fixed, no blockers remain, every score is at least 3 and the average is 3.71 (26/7), above 3.5. Modest pass: sync and pacing sit at 3.

## Rubric

| item | score | evidence |
|---|---|---|
| Hook strength | 4 | "MCP deleted its own handshake" is a sourced broken-belief line (C1/S1), and the first frame shows "MCP deleted its handshake" with the accent word. It is a plain statement, so not a 5. |
| Mechanism clarity | 4 | Key card vs passport split, panel with the two _meta keys, version-error fork, handle flow, input_required then retry: one visual per spoken step. Scenes 5-9 are dense with identifiers for a general viewer. |
| Visual-narration sync | 3 | Each scene's visual matches its sentence and word cues exist. Scene 5 shows the panel while "capabilities." is captioned (consistent). In-scene timing of highlights is unverified from stills. |
| Visual variety | 4 | Contact sheet shows kinetic type, stack, split, panel, fork, flow, checklist, title across 12 scenes, with the signal-trace motif in scenes 1, 3 and 12. Same dark palette, and the lower third is empty on most scenes. |
| Pacing | 3 | About 135 words in 52.1 s (about 155 wpm, in range), no long silences. Longest static stretch 3.25 s misses the 1-3 s target, activity 46%. Audio not heard. |
| Payoff usefulness | 4 | Scene 11 recaps the three takeaways (request explains itself, explicit handles, retry loop), and the CTA "Miss the handshake?" ties back to the hook. Practical but a recap, not a new action. |
| Caption readability | 4 | Large bold white on dark pill with cyan active word, text matches script.md, 2-4 words per cue, reading-speed check passed. Single-word cue "handles." and "capabilities." are brief. |
| **Average** | **3.71** | 26/7. |

## Blockers
- none

## Blocker checks performed
- Re-verified scene 5 (still at 18.6 s): both full identifiers sit on their own line inside their row boxes and inside the panel; nothing crosses a border or the side margin. Text is about 30 px at 1080 wide (about 11 pt on a phone), small but legible with high contrast.
- Re-verified central-question overlay (contact sheet, scenes 2-9): now two short lines above the headline with clear space; no collision. It is small, so treated as a warning.
- Factual overstatement: none. Hook, handshake and session removal, _meta keys, UnsupportedProtocolVersionError, handles, input_required and inputResponses and the deprecation caveat map to S1 (fact_check.md: 11 claims supported or qualified). No load-balancer, scaling, SDK adoption or maintainer-reason claim in script.md or the storyboard, per the brief's NOT-to-claim list.
- Misleading hook or title: hook is accurate. metadata.md title is the folder slug, not a viewer-facing title (see warnings).
- Caption error: captions.srt text matches the script narration word for word.
- Illustrative labelling (scenes 8-9): both carry an ILLUSTRATIVE badge, the on-screen headlines read "Illustrative: input required" and "Illustrative: retry with answers", and the narration says "Illustrative:". They read as illustrative.
- Missing disclosure: synthetic cloned voice and original graphics are disclosed in metadata.md; the altered-content setting is flagged for a person.
- Unlicensed asset: no third-party footage or audio; text graphics only. Font terms (Segoe UI) remain a pre-publish check.

## Warnings
- Not heard: voice clone quality, per-scene take choice (scene 5 used take 2 after recalls of 75, 62.5, then 87.5), and pronunciation of "MCP" and "input required". A person must listen. Whisper missed 2026, hotel, logging, would, wrong, you.
- metadata.md title is the raw folder slug and the source line reads "(not stated)" for the date. Write a viewer-facing title before manual entry; the description is just the hook plus CTA.
- Central-question overlay and the scene 5 identifier text are small for a phone; consider a larger size if a human finds them hard to read.
- Scene 8: the connector line crosses the "Tool needs a user choice" node text slightly in the contact sheet; check after the re-render.
- Scene 5 headline says the request shows a "passport", the same metaphor as scene 4. Per fact_check.md C4 this must not be read as authentication; the narration keeps it as metaphor.
- "The July 2026 spec" is derived from revision id 2026-07-28 (qualified in fact_check.md). Optional storyboard wording tweaks 2-3 in fact_check.md are not applied.
- Visual cadence: longest static stretch 3.25 s against the 1-3 s target; the empty lower third and small low-contrast "Source: Model Context Protocol" line are weak on mobile.
- readiness.md Edit and render items are still unticked; complete them after the re-render.
- No music or SFX by design.

## Pass items
- One central question, tension before the fix, an explicit illustrative example, a caveat from the source, and a CTA tied to the hook.
- Claim map: 11 claims, all supported or qualified by the single primary source S1; the full identifier spelling correction from fact_check.md is applied in scene 5.
- Technical: 1080x1920, h264/aac, 52.13 s, -14.0 LUFS, true peak -1.5 dBFS, captions contiguous, render report clean. Measurements only; no audio heard.
- Voice is the owner's cloned voice, disclosed as synthetic.

State: blockers present; not ready to proceed until the layout is fixed and re-rendered. This review does not approve publishing; a person must watch and listen to the draft before any decision.
