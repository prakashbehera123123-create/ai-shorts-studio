# Editorial review: 2026-11-20-your-agent-should-sleep-not-poll-github-event-streams-and-gh (re-render with icons and sound design)

Reviewer: video-reviewer agent. Inputs: script.md, storyboard/spec, fact_check.md, metadata.md, assets/manifest.csv, render/captions.srt, render/render_report.json, qa/technical.json, qa/contact_sheet.jpg, qa/editorial_before_sound.md. The video and audio were not opened and no audio was heard. The sound plan is judged only from cue timing against captions and scene boundaries, and from the loudness numbers (-14.0 LUFS, -1.5 dBFS true peak, no long silences). Script and cached voice are unchanged from the previous review.

Decision: PASS

No blockers, every score is at least 3, average 3.57 (25/7). Still a modest pass: sync, pacing and captions sit at 3.

## Rubric

| item | score | evidence |
|---|---|---|
| Hook strength | 4 | "Your agent keeps asking: is it done yet?" (sourced consequence, C1) now has a refresh-arrows hero icon above "Done yet?" plus the signal-trace wire, and a knock SFX at 0 s that matches the "knocking" idea. Not 5: no concrete stake or number. |
| Mechanism clarity | 4 | Unchanged structure: poll often vs poll less, doorbell, subscribe once, gh event listen panel (PR URL, event, flags), checklist, sleeps/wakes. Icons (agent bot, rate-limit refresh, hourglass, subscribe) label nodes; scenes 5 and 8 still carry the open-connection idea mostly through narration. |
| Visual-narration sync | 3 | Headlines track their sentences. Scene 10 boxes are unticked at the spoken "waitlist only" and scene 7 is part-ticked at its sampled moment, so tick timing is unverified. SFX cues land on scene boundaries and caption starts (see warnings). |
| Visual variety | 4 | Contact sheet: hero icon + wire, agent chip, split tiles, bell hero, chip, terminal panel, checklist, node, laptop hero, tag checklist, CTA. The icons make the hero scenes (1, 4, 9) distinct. Lower-middle is still empty in scenes 2, 3, 5, 8. |
| Pacing | 3 | 137 words in 48.87 s (about 168 wpm, upper end), no long silences, longest static stretch 3.00 s (edge of target). SFX density is within limits (below). Audio not heard. |
| Payoff usefulness | 4 | Subscribe once, connection stays open, agent sleeps and wakes, no public webhook so it works on a laptop, plus the preview/waitlist/may-change caveat on screen and in narration. Not 5: no explicit "replace your poll loop" step. |
| Caption readability | 3 | Large white text on dark pills, cyan active word, text matches script. Same pacing weak spots: cues "and you burn rate", "limit on requests" (0.49 s), "you want," (0.44 s), "that mostly return" (35 chars/s), and a 3.1 s "Poll often," cue. Icons did not collide with captions in the sampled stills. |

## Blockers
- none

## Blocker checks performed
- Factual overstatement: script, claims and caveat unchanged; fact_check.md covers 12 claims, all supported or qualified. Icons and sound add no claims.
- Misleading hook/title: hook is the sourced polling consequence; metadata links both primary sources.
- Caption error: captions.srt is contiguous 0 to end and matches script wording.
- Unreadable text: headlines and captions are large and high contrast in the sampled stills. The source line is small (warning).
- Missing disclosure: synthetic cloned narration and generated graphics are disclosed in metadata/manifest. The generated bed and SFX are self-generated, so no third-party audio licence is involved.
- Unlicensed asset: Lucide icons are ISC (permissive; noted in studio/motion_spec.py), so licensed, but not yet recorded in the manifest (warning).
- Sound-plan check from timing: no SFX sits under a key spoken term. knock@0 s is on "Your agent"; tick@12.1 on "Think", ahead of "doorbell"; tick@42.4 on the start of "It's preview"; tick@45.73 on "Which". Density: five cues in 0-30 s (0, 2.45, 12.1, 14.55, 21.58), at most 5 per 30 s, and three in 30-48.87 s.

## Warnings
- Audio not heard by this review. Voice delivery, bed balance, SFX character and the roughly 15 dB ducking are unjudged. A person must listen end to end, especially 14-22 s, and confirm "GitHub Event Streams" and "G H event listen" are clear (whisper full-mix recall 81%; missed "github", "doorbell", "endpoint", "connection" etc.).
- SFX edge overlaps to check by ear: whoosh@2.45 s runs under the tail of "yet?" (caption ends 2.8 s); whoosh@14.55 s begins before "again and again." ends (14.9 s) and may reach "GitHub"; whoosh@21.58 s overlaps "arrive" (ends 21.93 s); rise@34.42 s overlaps "first" (ends 34.77 s). Not key terms by cue timing, but confirm they do not mask words. Tick@12.1 s is very close to "doorbell".
- Manifest gap: Lucide icons (scenes 1, 2, 3, 4, 5, 8, 9) have no manifest row. Add one (source lucide-static, ISC licence, no attribution required) so rights records match the render. Technical QA's "8 manifest rows valid" does not cover them.
- Caption pacing: three cues at 0.44-0.49 s and one at 35 chars/s in scene 2; merge into 2-3 longer cues. The 3.1 s "Poll often," cue is long.
- Sync: scenes 7 and 10 tick timing against spoken words is unverified; scrub them.
- Scenes 5 and 8 are still thin (one chip/node on a large empty frame); scenes 2-3 have an empty lower third.
- "Source: GitHub Changelog" line is small and low contrast for mobile.
- Technical QA warns on informational items (voice clone PerthNet, motion renderer) and Segoe UI font terms (T001): verify Microsoft font terms for video use before publishing.
- Longest static stretch 3.00 s; visual activity 52%.
- Claim nuances accepted in fact_check.md: "keeps a connection open" (no "one"), "waitlist only" as shorthand, "sleeps/wakes" is the source's wording.

## Pass items
- One central question, tension before the fix, worked example (gh event listen), doorbell metaphor, actionable payoff, CTA tied to the hook.
- Technical: 1080x1920, h264/aac, 48.87 s, -14.0 LUFS, -1.5 dBFS true peak, no long silences, captions contiguous, render report clean, cadence check passes.
- Recurring signal-trace motif, word-timed caption highlight, preview/waitlist/may-change caveat on screen and in narration.
- Sound design uses only self-generated bed and SFX, listed in render_report.json and manifest (A001-A005); cue density and placement are sensible on paper.

State: no blockers; QA may proceed toward READY_FOR_HUMAN_REVIEW. This review does not approve publishing; a person must watch and listen to the draft and decide.
