# Editorial review: 2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job

Reviewer: video-reviewer agent · Inputs: script, storyboard, sources, fact check, captions.srt, technical.json, 3 sampled stills (contact sheet + scene_02, scene_05) · Audio not heard

Decision: PASS

## Blockers
- none

## Warnings
- Known/accepted: SAPI placeholder voice (not judged; audio not heard), text-card visuals with no diagrams (storyboard diagram descriptions not drawn; large empty lower half on every card), Segoe UI font terms to verify (T001).
- Scene 5 on-screen text "Chat Completions: supported, no tools" is slightly stronger than the source. S2 says only that tool calling requires the Responses API. Suggested softer text: "Chat Completions: supported" or "Tools need Responses". Not a blocker because it restates the same rule, but it is an absolute phrasing.
- Scene 2 card "Astra: demanding reasoning, coding" does not show "OpenAI says" on screen (storyboard planned that caption). Attribution is only the small "Source: OpenAI" line and the narration. Safe because scene 3 says "Positioning, not a ranking", but adding "OpenAI says" on the card would be safer. The Sol card is not sampled; check it in the next render.
- Hook is a plain question ("Moving to GPT-6.2?") with no stakes or number. It is clear and honest, but moderate in strength for the first 2 s.
- Caption cues split mid-phrase (e.g. "Completions, but / anything that", "positioning, / not a ranking"). They are readable and within the tool's speed limits, but the phrase breaks are choppy.
- Actual runtime is 50.3 s against the 47 s storyboard and 45 s script target. It is within the 25-55 s spec; pacing is dense (133 words, three checks plus a positioning intro), so human review of the audio is needed.
- The metadata description lists the GitHub changelog as a source, but no spoken claim uses it (S5 is only the conflict note). Consider dropping it or labelling it "context", so the sources list matches the claims.
- Narration says "Both models also support Chat Completions" and "it changes how the top-level instructions field is handled". No direction of change is given, which matches the source. Keep it that way in any rewrite.
- Folder slug ("astra-vs-sol-which-one-for-which-job") does not match the video angle (migration checks). The metadata title matches the video, so this is cosmetic.
- Metadata flags the "Altered or synthetic content" setting for review in YouTube Studio. The human reviewer should set it.

## Pass items
- Format: 1080x1920, H.264/AAC, 50.3 s, loudness -16.3 LUFS, true peak -4.5 dBFS, no long silences, captions cover the full timeline (per technical.json; not independently re-measured).
- One central idea (three migration checks for GPT-6.2) with a clear payoff (read the migration guide). Intro positioning is attributed to OpenAI and explicitly "not a ranking"; nothing implies Astra or Sol is better or heavier. The GitHub framing is not used on screen, in the narration, or in the metadata.
- Claim alignment: all narration and on-screen claims map to S1-S3 (primary, high confidence). The fact-check corrections are applied: "OpenAI says" attribution on checks 1 and 2, "three checks from OpenAI's changelog" (no implied complete list), and the advice lines are framed as advice. No claim that anything breaks.
- Caption spelling is correct (GPT-6.2, Astra, Sol, Responses API, Chat Completions, OpenAI's). Captions are large white text on a dark pill, centred at about 70% of frame height. They are legible and clear of the edges and the progress bar.
- On-screen headlines are short, high-contrast, at most 3 lines, and inside safe margins. The "Source: OpenAI · 2026-11-17" line on each card is accurate. The title/headline "Moving to GPT-6.2?" is accurate.
- CTA ("Which of these checks matters most for your app? Tell me below.") is natural and not a leading or doom-framed question.
- Metadata title "Moving to GPT-6.2? Check these first" matches the actual video and is non-hype. The description repeats the hook and CTA, with dated source URLs and a synthetic-voice and original-graphics disclosure.
- Rights: manifest has 3 rows (generated graphics, SAPI TTS, system font). There is no third-party footage, music, or logos; the voice placeholder and font terms are flagged.
- State remains READY_FOR_HUMAN_REVIEW; this review does not approve publishing.

## Resolved after review (main session, 2026-11-20)
- Scene 5 on-screen text changed from "Chat Completions: supported, no tools" to "Tool calls: Responses API only" (matches S2 wording; re-rendered and re-QAd).
