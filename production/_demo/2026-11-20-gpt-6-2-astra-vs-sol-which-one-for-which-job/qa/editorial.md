# Editorial review (v3, dry run 3, Phase 5 motion renderer): 2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job

Reviewer: video-reviewer agent. Inputs: script, storyboard (structured visual objects), sources, fact_check, metadata, render/captions.srt (word-timed chunks), qa/technical.json, qa/contact_sheet.jpg, qa/frames/scene_02, scene_05, scene_06, qa/editorial_dryrun2.md. Audio was not heard and is not judged; loudness, silence and whisper recall come from technical.json only. The video file was not opened. Stills are single sampled frames, so mid-animation states are not fully visible.

Decision: PASS

Why: no blockers, every v3 score is 3 or higher, and the v3 average is 3.57 (v1 2.86, v2 3.14). Margin over 3.5 is thin and rests on the motion renderer delivering distinct visual forms. This is not publish approval. The final state is READY_FOR_HUMAN_REVIEW and a human must listen and watch.

## Rubric

| item | v1 | v2 | v3 | evidence |
|---|---|---|---|---|
| Hook strength | 3 | 3 | 3 | "Switching to GPT-6.2? Check these three things first." is still a plain, honest question with no stakes or failure case. The big kinetic headline with an accent word (contact sheet, scene 1) helps a little, but the hook text itself is unchanged. |
| Mechanism clarity | 3 | 4 | 4 | Context, "we picked three", then 1/2/3, with a labelled illustrative example and a closing "1 requirement, 2 changes". The visuals now carry the steps: a flow for tool calling, a stack for edited history and a request panel for the instructions field. No direction of change is invented for checks 2 and 3. |
| Visual-narration sync | 3 | 3 | 4 | Each scene draws what is being said: Astra/Sol cards for "two models", a flow into a Responses API node for "requires", a Chat Completions box next to a "GPT-6.2 tools" box for the example, an edit stack for "edit earlier messages", and an instructions field for "instructions". Word cues are in the storyboard and the active word is highlighted in the pill. The last frame of each animation was not seen. |
| Visual variety | 2 | 2 | 4 | Seven templates across ten scenes: kinetic, split, checklist, flow, stack, panel, title (contact sheet). Same dark palette and pinned-question layout throughout. Roughly half of each frame is still empty. Technical cadence: visual zone active 43% of the time and longest static stretch 4.0 s, above the 3 s target (warning). |
| Pacing | 3 | 3 | 3 | 126 words in 49.87 s at SAPI rate +3, so it is dense. The first check starts at about 14 s. The technical visual cadence check is a warning (4.0 s vs 3 s). Delivery speed is unknown because audio was not heard. |
| Payoff usefulness | 3 | 4 | 4 | "Test the three, then read OpenAI's migration guide", then a requirement-vs-change split, then a CTA tied to the hook. Nothing claims anything breaks. |
| Caption readability | 3 | 3 | 3 | Large white text on a dark pill, active word in cyan, clear of the edges, no spelling errors, and the pill text matches the script. Technical.json flags 13 cues at 23 to 36 chars/s and one 0.43 s cue ("The other two"). The SRT has single-word cues ("first.", "One.", "Two."). This is a speech-pace artefact, but it is still real for a viewer. |
| Average | 2.86 | 3.14 | 3.57 | v1 20/7, v2 22/7, v3 25/7. v1 and v2 are copied from editorial_dryrun2.md. |

## Blockers
- none

## Blocker checks performed
- Factual: every spoken, caption and on-screen label maps to S1-S3 or is marked. "Tool calling" and "GPT-6.2 tools / Via Responses API" map to S2 (C5, C6), "Message 2 (edited)" and "changed in GPT-6.2" map to S3 (C7), "top-level field" maps to S3 (C8), and "our pick" and "1 requirement, 2 changes" are framed as interpretation (C1, C4, C10). Nothing says anything breaks.
- Astra/Sol: scene 2 uses two equal-sized cards with identical lane lists and no ranking, highlight or positioning text. The S1 vs S5 conflict is not used anywhere. The still of scene 2 shows Sol's card empty while Astra's items are drawn (a sampled animation moment, equal sizing); see Warnings.
- Title and hook: "What to check before you switch to GPT-6.2" matches the angle. The description repeats the hook and CTA and has no Astra/Sol positioning.
- Captions: SRT text matches script.md word for word (GPT-6.2, Astra, Sol, Responses API, Chat Completions, OpenAI's).
- Disclosure: metadata states synthetic TTS voice, original graphics and the altered-content setting to review in Studio. The Illustrative pill is present in scene 5.
- Rights: manifest has 3 rows (generated graphics, SAPI voice, Segoe UI). No third-party footage, music or logos. The request panel is labelled "(generic)" and carries no vendor UI.
- Text legibility: headline, labels and caption pills are large and readable on the stills. The only small text is the pinned question and the source chip.

## Warnings
- Accepted limits: SAPI placeholder voice (not judged, pace dense at rate +3), no music or SFX by design, Segoe UI font terms (T001, verify before publishing).
- Caption reading-speed warning (13 cues) and the visual cadence target miss (4.0 s static vs 3 s). Both come from the speech pace and from layout holds, not from a content defect.
- The message stack (scene 6) and the "reasoning preservation" visual are an invented illustration of four messages but are not marked ILLUSTRATIVE. The text claims are sourced, so this is not a blocker. Consider adding the same Illustrative pill, or "example" in the tag.
- Scenes 6 and 9 stills show only the first element (Message 1) and unchecked boxes. I could not confirm the final state: the edit mark, the "changed in GPT-6.2" tag, and the requirement/behaviour tags in scene 9. A human should watch those scenes through.
- The scene 2 still shows Astra's lane items drawn while Sol's card is empty. If this lasts long, the "equals" read is weakened. Draw both cards' items simultaneously or in a symmetric beat.
- The pinned question wraps as "GPT-/6.2" across two lines in every frame, splitting the model name. Use a non-breaking hyphen or shorten the question.
- Hook is plain. A concrete stake, such as "tool calling needs the Responses API", would raise the score. "Three things" could be read as a complete list; the "our pick" tag mitigates this.
- Source chip is small (about 30 px) and absent on scenes 1 and 10. Visual hero area is still under 40% of the frame in several scenes.
- Whisper recall is 97%. The missed words (changelog, openais, picked, sol) suggest the SAPI voice slurs or the check mispronounces them. A human must listen to those words, since the captions and cues depend on them.
- metadata.md lists no GitHub source, which is correct. The folder slug is stale (cosmetic).

## Pass items
- Format and loudness (technical.json, not re-measured): 1080x1920, H.264/AAC, 49.87 s, -14.0 LUFS, true peak -1.5 dBFS, no long silences, captions contiguous.
- Script contract: 126 words, 10 mapped claims, fact check clean, all earlier corrections applied.
- Story: one central question, stated in the hook and answered in the payoff, with numbered steps, a labelled illustrative example and one CTA.
- Visual forms now carry the mechanism rather than repeating a text card (v2 variety 2 to v3 4, sync 3 to 4).
- Astra/Sol shown as equals with no ranking.
- Rights: all assets recorded; voice and font flagged as placeholders.
- This review does not approve publishing. Status moves to READY_FOR_HUMAN_REVIEW only.

## Post-review fixes (main session, 2026-11-20; re-rendered, technical QA re-run, verified on stills)
- Message stack (scene 6) now carries the ILLUSTRATIVE badge.
- Non-breaking hyphens keep 'GPT-6.2' on one line in the pinned question and labels.
- Checklist ticks now land as each row is spoken.
