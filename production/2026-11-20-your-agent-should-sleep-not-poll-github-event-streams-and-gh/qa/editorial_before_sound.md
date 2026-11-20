# Editorial review: 2026-11-20-your-agent-should-sleep-not-poll-github-event-streams-and-gh

Reviewer: video-reviewer agent · Inputs: script.md, storyboard.json, brief.md (story angle, NOT-to-claim list), fact_check.md, metadata.md, readiness.md, assets/manifest.csv, render/captions.srt, qa/technical.json, qa/transcript.srt, qa/contact_sheet.jpg, qa/frames/, voiceover/takes.json. Audio not heard and video not opened; voice quality and pronunciation are judged only from whisper transcripts and measurements (-14.0 LUFS, -1.5 dBFS, no long silences). Stills are single moments, so in-scene animation is judged from the contact sheet and storyboard only.

Decision: PASS

Plain statement: no blockers, every score is at least 3, and the average is 3.57 (25/7), above 3.5. It is a modest pass: sync, pacing and caption readability sit at 3.

## Rubric

| item | score | evidence |
|---|---|---|
| Hook strength | 4 | "Your agent keeps asking: is it done yet?" (sourced consequence framing, C1) with "Done yet?" hero text and the signal-trace wire in frame 1. Not 5: no concrete stake or number, and nothing visibly "asks" yet. |
| Mechanism clarity | 4 | Clear before/after: scene 2-3 poll often (rate limit burned) vs poll less (feedback waits), then doorbell, subscribe once, gh event listen panel (PR URL, event, flags), checklist, sleeps/wakes. Sparse: scene 5 and scene 8 show a single chip/node, so the open-connection mechanism is mostly carried by narration. |
| Visual-narration sync | 3 | Headlines track their sentences (e.g. "Poll often" tile at "Poll often,", "then, by default," with the checklist). But the scene 10 still shows "Preview" and "Waitlist only" boxes unticked while "waitlist only" is being said, and scene 7 shows two of four items ticked at its sampled moment; landing on cue words is unverified. |
| Visual variety | 4 | Contact sheet: wire + hero text, agent chip, split poll tiles, doorbell hero, subscribe chip, terminal panel, checklist, open-wire node, no-webhook hero, tag checklist, CTA; layouts differ across most scenes. Same dark palette, big empty lower-middle in several stills; longest static stretch 3.00 s, activity 50%. |
| Pacing | 3 | 137 words in 48.87 s (about 168 wpm, upper end of the standard's range) and no long silences. Technical QA flags three cues of 0.44-0.49 s and one at 35 chars/s in the fast stretch of scene 2. Longest static stretch 3.00 s is at the edge of the 1-3 s target. Audio not heard. |
| Payoff usefulness | 4 | Actionable: subscribe once, keep the connection open, sleep until work, no public webhook so it works on a laptop, plus the preview/waitlist/may-change caveat on screen and in narration. Not 5: no explicit "replace your poll loop with this" step. |
| Caption readability | 3 | Large bold white on a dark pill, cyan active word, correct text matching script.md word for word, no mid-word breaks. Weak spots: "and you burn rate / limit on requests / that mostly return" cues flash at 0.49 s each (35 chars/s on one), "you want," at 0.44 s, and a 3.1 s cue "Poll often," holds across a pause. |
| **Average** | **3.57** | 25/7. |

## Blockers
- none

## Blocker checks performed
- Factual overstatement: none. Spoken and on-screen claims map to S1/S2 (fact_check: 0 unsupported). Nothing from the NOT-to-claim list appears: no SSE/WebSocket transport, latency, cost, token or poll-count figures, no gh v2.105.0 requirement. "By default" correction (C8) is in the narration; the checklist screen reads "Exits after first event (default)" per fact_check, but the sampled still did not reach that row.
- Misleading hook/title: no. Title "Your agent should sleep, not poll" and the hook are sourced framing; the rejected "constantly" claim is not used.
- Caption error: render/captions.srt matches script.md narration. "G H event listen" is the intended spoken spelling for "gh event listen" (script pronunciation note).
- Pronunciation of "GitHub Event Streams": the targeted 11-22 s re-transcription heard it as "Get her ribbon strings", while the same window caught "doorbell not knocking again and again... subscribe to a pull request. It keeps the connection open and events arrive". The scene-level takes were chosen at 100% (scene 4) and 89.5% (scene 5) recall, and the on-screen caption (taken from the script) shows the correct name. This is a whisper ASR miss on a cloned voice, not evidence that a viewer cannot understand the phrase, and the caption/hero text carries the correct name, so it is not a blocker. It is a warning that a person must verify by ear.
- Unreadable text: none. Headlines and captions are large and high contrast. The "Source: GitHub Changelog" line is small (see warnings).
- Missing disclosure: synthetic cloned narration, original graphics and both source URLs are in metadata.md; YouTube altered/synthetic setting flagged for a person.
- Unlicensed asset: 3 manifest rows valid (generated graphic, owner's cloned voice with consent, Chatterbox MIT). Only the Segoe UI font terms are flagged (T001).

## Warnings
- Accepted limit: audio not heard by this review. Voice delivery, naturalness and the pronunciation of "GitHub Event Streams" and "G H event listen" are unjudged; whisper full-mix recall is 80% (skipped 11-22 s), and per-scene chosen takes are at least 85%. A person must listen, especially 14-22 s.
- Pronunciation: whisper misheard "GitHub Event Streams" ("Get her ribbon strings") and full-mix also missed "again", "an", "arrive", "connection", "doorbell", "endpoint", "g", "github". The scene 4-5 content was heard in the targeted pass; confirm the phrase by ear and re-take scene 5 if it is slurred.
- Caption pacing: three cues at 0.44-0.49 s and one at 35 chars/s in scene 2 ("and you burn rate", "limit on requests", "that mostly return", "you want,"). Text is correct but hard to read at that speed; consider merging into 2-3 longer cues. The 3.1 s "Poll often," cue is long for two words.
- Sync: scene 10 boxes are unticked at the spoken "waitlist only", and scene 7 is part-ticked at its sampled moment. A person should scrub scenes 7 and 10 to confirm ticks land on their words.
- Scene 5 and scene 8 are visually thin (one chip or node on a large empty frame); scenes 2-3 still show an empty lower third.
- The "Source: GitHub Changelog" line is small and low contrast for mobile.
- Longest static stretch 3.00 s (edge of the 1-3 s target); activity 50%.
- Technical QA also warns on render/voice-clone informational notes (PerthNet clone, motion renderer) and the Segoe UI font terms (T001): verify Microsoft font terms for video use before publishing.
- Claim nuances accepted in fact_check.md: "keeps a connection open" (no "one"), "Waitlist only" as shorthand, "agent sleeps/wakes" is the source's own wording.
- readiness.md edit/render and review boxes remain unticked pending this QA; orchestrator to tick them.

## Pass items
- One central question (how should an agent wait for PR feedback without polling?), tension before the fix, real worked example from S2 (gh event listen), a doorbell metaphor, an actionable payoff and a CTA tied to the hook.
- Claim map: 12 claims, all supported or qualified; fact-check corrections applied; metadata links both primary sources.
- Technical: 1080x1920, h264/aac, 48.87 s, -14.0 LUFS, true peak -1.5 dBFS, captions contiguous 0 to end, render report clean, visual cadence check passes.
- Recurring signal-trace motif (wire in the hook and doorbell scenes, open wire at the payoff) and word-timed caption highlight.
- Preview/waitlist/may-change caveat is present in narration and on screen.

State: no blockers; QA may proceed toward READY_FOR_HUMAN_REVIEW. This review does not approve publishing; a person must watch and listen to the draft and decide.
