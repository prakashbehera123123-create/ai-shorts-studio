# Editorial review (v2): 2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp

Reviewer: video-reviewer agent · Dry run 2 · Inputs: script.md, storyboard.json (schema v2), sources.md, fact_check.md, metadata.md, readiness.md, render/captions.srt, qa/technical.json, qa/contact_sheet.jpg, qa/frames/scene_03.jpg and scene_06.jpg; v1 baseline: captions.srt, contact_sheet.jpg, editorial.md. Audio not heard and video not opened; voice, pronunciation and caption-to-speech sync are unjudged. Visual scores describe the rendered text cards as they are.

Decision: FAIL

Plain statement: there are no blockers, but v2 fails the numeric gate (visual variety 2 is below 3, and the v2 average of 3.29 is below 3.5). Both shortfalls come from the accepted text-card limit (motion renderer is Phase 5), not from script, facts or captions. The visual-variety score is deliberately not inflated. Under the rules this is FAIL, and the content layer (script, story, sourcing) is ready to carry the Phase 5 visuals.

## Rubric
Scored 1-5 with the same rubric on both versions. v1 is re-scored against §2/§6 of the standard, so it is stricter than the archived v1 editorial, which was a PASS under a looser pass.

| item | v1 | v2 | evidence |
|---|---|---|---|
| Hook strength | 2 | 4 | v1 opened "GitHub just added a way to..." (banned "X just launched" opener with no tension), on-screen card "Test your Copilot skills" was flat. v2 opens "One good answer doesn't prove your skill works." (broken belief, S3-backed), card "One good answer isn't proof" matches it, and it is under 3 s. |
| Mechanism clarity | 3 | 4 | v1 packed definition, /eval, "path" check, approval and plans into one run. v2 states the obstacle first (script lines 2-5), defines an eval, and gives numbered steps with on-screen 1./2./3. cards. Cards show labels only, no diagram, so not 5. |
| Visual-narration sync | 3 | 3 | Both: the headline roughly matches the spoken chunk (v2 scene 3 "Illustrative: did it help?" lands at "So how do you know your change helped?"; scenes 5-7 cards 1./2./3. under the step captions). No in-scene events to land on words, and caption timing is proportional, so tight sync cannot be judged. |
| Visual variety | 2 | 2 | Both are ten identical text cards (headline, source line, caption pill) with about half the frame empty gradient; no hero visual, no motif, no diagram. v2 adds a progress bar and clearer headline copy but not a different look. Accepted limit, scored honestly. |
| Pacing | 2 | 3 | v1: 130 words, 50.1 s, no beat after the hook. v2: 127 words in 51.87 s (about 147 wpm by arithmetic, slightly under the standard's 150 floor, so pauses exist), with a 3-beat rhythm (tension, steps, example). Still about 5 s per card with no change inside, against the 1-3 s cadence. Audio not heard. |
| Payoff usefulness | 3 | 4 | v1 ended on availability and plan list. v2 payoff is an action: rerun the same eval after every change and compare runs, plus the public-preview caveat (spoken) and a CTA tied to the hook. Caveat chip is not on screen (see Planned but not rendered). |
| Caption readability | 3 | 3 | Large white bold text on a dark pill, good contrast, correct spelling, cue speed check passed, caption zone only. Both still break phrases and end on dangling words (v2: "So how do you know your", "So rerun the same eval after", "Which skill would you test"), 4-5 words per cue vs 2-4, and no active-word highlight. |
| **Average** | **2.57** | **3.29** | v1 = 18/7, v2 = 23/7. |

## Blockers
- none. Checked: factual overstatement (none; hook, steps, caveat all map to S1-S4, no Vally/install/plan claims), misleading hook/title (hook is a sourced framing; title "GitHub Copilot Evals" is generic and accurate), caption error (spelling and wording match script.md), unreadable text (headline and caption text are large and high contrast), missing disclosure (synthetic TTS and original graphics disclosed in metadata), unlicensed asset (3 manifest rows valid; only the Segoe UI font is flagged).

## Warnings
- Accepted limits: SAPI placeholder voice (disclosed; audio not heard, so "MCP" pronunciation and delivery are unjudged), text-card visuals, no music/SFX by design, proportional caption timing, Segoe UI font terms (T001) to verify before any publish.
- Visual variety 2: ten near-identical cards, a large empty middle, no motif. This is what fails the gate.
- Pacing: roughly 147 wpm by arithmetic and about 5 s static cards; the standard's 150-165 wpm range and 1-3 s change cadence are not met. Check the delivered rate by ear.
- "Source: GitHub · 2026-11-17" under each headline is small and low contrast on mobile. It is not essential content but may be hard to read. Consider a larger or brighter chip.
- Captions: phrase-breaking and dangling words; 5-word cues ("give an agent a realistic"); the 4-word "Illustrative: your edit passed" cue splits mid-clause; no active-word highlight.
- Caveat "public preview" is spoken but has no on-screen chip, so a muted viewer misses it. The scene 9 card reads "Rerun after every change" only.
- "Rerun after every change" is slightly stronger than the source's "after you change"; the fact check accepted it.
- Scene 10 has no source chip. Fine for a CTA card.
- "Step one/two/three" is the script's own simplification of the source's capability list (flagged in fact_check.md). The on-screen header "How an eval works" avoids implying an official count. Acceptable.
- Metadata title "GitHub Copilot Evals" is plain; a curiosity-led title could be considered. It is not misleading. The YouTube altered-content setting is flagged for a person to review.
- Readiness.md Review items are unticked (to be done after this review); four items are WAIVED for Phase 5 reasons (hero visual, cadence, word timing, loop ending).

## Pass items
- Script is on one central question ("how do you know your change helped?"), stated in the first 15 s and answered in the payoff; the obstacle comes before the fix; a caveat is included; beats are complete.
- The worked example is labelled illustrative on screen in scenes 2, 3 and 8 and in the spoken line; fact_check corrections were applied and visible in the stills.
- Claim-to-source map: 10 claims mapped, 0 unsupported; no unsourced numbers, no vendor logos or UI imitation.
- Metadata lists the primary source URL and discloses synthetic voice and original graphics.
- Technical: 1080x1920, h264/aac, 51.87 s, -14.0 LUFS, true peak -1.4 dBFS (within the checker's limit), no long silences, captions contiguous, rights rows valid. Measurements only; no audio heard.
- CTA is one natural question tied to the hook.
- v2 is a clear content improvement over v1: stronger hook, tension before explanation, an actionable payoff.

## Planned but not rendered
Storyboard v2 plans these, but the renderer (text cards only) did not draw them; none is judged in the scores above.
- Scene 1: headline words punching in on stress; cyan trace dot landing on a mint check; 3% push-in.
- Scene 2: Task, Agent, Output node flow with a travelling trace dot; output node label changing across runs.
- Scene 3: split Run 1 and Run 2; left mint check, right forks to a coral cross; pulsing question mark.
- Scene 4: traces merging into a loop; step pips 1/3, 2/3, 3/3 drawing on.
- Scene 5: Task and Good-result nodes joined by an arrow, drawn on as each is named.
- Scene 6: own unbranded Approve button and four check rows resolving to mint and coral (note: this mock needs the planned on-screen "Illustrative" label when drawn).
- Scene 7: Eval, Edit, Eval loop with before/after result tiles.
- Scene 8: before/after halves with an ILLUSTRATIVE badge and a pulsing coral fail.
- Scene 9: parallax before/after tiles, trace callback to the hook, coral "Public preview" caveat chip and source chip.
- Scene 10: typed-on question and the trace dot circling to loop into scene 1.
- Also not done: word-timed captions with active-word highlight, loop ending, music/SFX.

State: remains below QA_PASSED for this version. Never approve publishing; a person decides next steps. Final status must stay short of READY_FOR_HUMAN_REVIEW until the rubric passes.
