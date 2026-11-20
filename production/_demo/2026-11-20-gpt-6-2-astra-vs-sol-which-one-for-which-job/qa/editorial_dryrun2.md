# Editorial review (v2, dry run 2): 2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job

Reviewer: video-reviewer agent. Inputs: script, storyboard (schema v2), sources, fact_check, metadata, readiness, render/captions.srt, qa/technical.json, qa/contact_sheet.jpg, baseline_v1 (script, storyboard, captions, contact sheet, editorial). Audio not heard and not judged; loudness and silence come from technical.json only. The video file was not opened.

Decision: FAIL

Why: no blockers, but visual variety scores 2 (below the 3 floor) and the v2 average is 3.14 (below 3.5). Both shortfalls come from the known accepted limit that the renderer draws text cards only (motion renderer is Phase 5). This is a rubric FAIL caused by accepted limits, not by a content or accuracy defect. Scores are not inflated to get around it. The status stays below READY_FOR_HUMAN_REVIEW until the Phase 5 render or a human waiver. This review does not approve publishing.

## Rubric

| item | v1 | v2 | evidence |
|---|---|---|---|
| Hook strength | 3 | 3 | Both are plain, honest questions with no banned opener. v2 adds a concrete count ("Check these three things first" over "3 checks before GPT-6.2"). Neither shows stakes or a failure case, so a count is the only gain. |
| Mechanism clarity | 3 | 4 | v1 spent about 15 s on Astra/Sol positioning before the checks. v2 goes context, "we picked three", then 1/2/3 with an illustrative tool-calling example and a closing split of "1 requirement, 2 changes". The sources give no direction of change for checks 2 and 3, and the script does not invent one. |
| Visual-narration sync | 3 | 3 | Each card headline matches its own sentence ("1: Tool calling", "2: Edited history", "3: Instructions field"). Cues are timed proportionally within scenes, and no visual shows the action described. Same score for both. |
| Visual variety | 2 | 2 | All 10 v2 cards share one layout: top-left headline, tiny source chip, empty middle, caption pill. Only the text changes (see contact sheet). Roughly 60% of each frame is empty. Scene 10 has no chip. v1 looked the same. |
| Pacing | 3 | 3 | v2 is 126 words in 49.87 s. The first check starts at about 14 s (v1: about 18 s). The v2 SRT has 31 cues of 0.8 to 2.7 s, so the caption text changes every 1 to 2 s. Nothing else moves in a scene, and delivery speed is unknown because audio was not heard. |
| Payoff usefulness | 3 | 4 | v2 ends with "test these three, then read OpenAI's migration guide", labels the first item a requirement and the other two behaviour changes, and makes no safety or breakage claim. The CTA is tied to the hook ("which would your app hit first"). v1's payoff was "worth reading the guide". |
| Caption readability | 3 | 3 | Large white text on a dark pill, no spelling errors (GPT-6.2, Astra, Sol, Responses API, Chat Completions, OpenAI's), clear of the edges. Cues break mid-phrase ("The changelog notes / differences. We picked three", "Tool calling requires the / Responses API"). There is no active-word highlight, and timing is proportional. |
| Average | 2.86 | 3.14 | v1: 20/7. v2: 22/7. Pass needs >= 3.5 with every score >= 3. |

v1 scores are my own re-scoring of the archived artifacts on the same rubric. The earlier v1 PASS applied a looser reading of the rubric and is not reused.

## Blockers
- none

## Blocker checks performed
(Reformatted by main session 2026-11-20: these bullets were passed checks written under Blockers; content unchanged.)
- Factual: all claims in script, on-screen text and metadata map to S1-S3 (primary, high confidence). The "our pick" framing (C1, C4) is applied, C6 is conditional, C7 and C8 are scoped to the Responses API, and nothing says anything breaks. The fact-check corrections are applied in script.md, the captions and the card text.
- Astra/Sol conflict: neither the script nor the cards rank them or give positioning. The S1 vs S5 conflict stays unresolved and unused.
- Title and hook: "What to check before you switch to GPT-6.2" matches the v2 angle. The metadata description repeats the hook and CTA and carries no stale v1 text such as "Moving to GPT-6.2" or the Astra/Sol positioning.
- Caption text matches the script word for word.
- Disclosure: metadata states synthetic TTS voice, original text graphics, and the Studio altered-content setting to review. Rights: the manifest has 3 rows (generated graphics, SAPI voice, Segoe UI), with no third-party footage, music or logos.

## Warnings
- Accepted limits: SAPI placeholder voice (not judged), text-card visuals, no music or SFX by design, proportional caption timing, Segoe UI font terms (T001, verify before publishing).
- The hook says "three things" before the script says they are "our pick". The cards read "3 checks (our pick)", but a viewer could take "three things" as a complete list. Consider "three checks worth running" in the spoken hook.
- Check 1 is narrated as "Tool calling requires the Responses API" with no "for GPT-6.2" on that line, which the source scopes it to. The next sentence says "tools on GPT-6.2", so this is low risk. Moving "GPT-6.2" into the first sentence is safer.
- metadata.md lists the GitHub changelog under Sources, but v2 uses no GitHub claim (fact_check: availability only). Drop it or label it "context".
- The folder slug (astra-vs-sol-which-one-for-which-job) does not match the v2 angle. This is cosmetic, and the metadata title is correct.
- Layout (readiness waivers): the hero visual is below 40% of the frame and the middle of every card is empty. The source chip is about 30 px, at the minimum size, and hard to read on a phone.
- readiness.md Review items are still unticked, so the main session should tick them after the human check.
- Audio and delivery speed were not judged. A human must listen for pace, pronunciation of "GPT-6.2" and the pauses.

## Planned but not rendered
The v2 storyboard describes the following. The renderer draws only the headline, a source chip and caption pills, so none of it is on screen.
- Hook: app box and GPT-6.2 box joined by the cyan signal trace.
- Scene 2: two equal Astra/Sol cards each linked to Responses API and Chat Completions lanes.
- Scene 3: large "3" with three amber check boxes.
- Scene 4: S-curve architecture flow with a travelling dot and a dimmed Chat Completions lane.
- Scene 5: split screen of Chat Completions (muted) vs Responses API with a tool-call arrow.
- Scene 6: four stacked message blocks with an amber edit mark and a "reasoning preservation changed" tag.
- Scene 7: generic request panel (model, instructions, input) with the instructions field highlighted.
- Scene 8: three mint ticks and a trace ending at a "migration guide" node.
- Scene 9: three rows tagged requirement (amber) vs behaviour change (cyan, x2).
- Scene 10: end card with three numbered chips, and the trace looping to the first frame.
- Also not delivered: in-scene change every 1 to 3 s, transitions, word-timed captions with a cyan active word, the loop ending, and the hero visual at 40% or more of the frame.
Most of the variety and some of the sync scores sit in this list. A Phase 5 render that delivers it should lift variety to 4 or more and the average above 3.5.

## Pass items
- Format and loudness (technical.json, not re-measured): 1080x1920, H.264/AAC, 49.87 s, -14.0 LUFS, true peak -1.5 dBFS, no long silences, captions contiguous across the timeline, reading speed within limits.
- Script contract: 126 words, 10 mapped claims, fact check shows no unsupported claims, and all three required corrections were applied.
- Story: one central question, stated in the hook and answered in the payoff. The numbered 1/2/3 structure is introduced before the steps, with a labelled illustrative example and a single CTA.
- Accuracy and wording on screen: the "Illustrative" label is present and "our pick" attribution is on card 3. The earlier unsupported "same name, new behaviour" text is gone.
- v1 to v2 gains: no positioning detour, a worked example, a requirement-vs-change summary, a sourced and framed payoff, and a cleaner fact-check trail.
- Rights: assets are all recorded, with the voice and font flagged as placeholders.
