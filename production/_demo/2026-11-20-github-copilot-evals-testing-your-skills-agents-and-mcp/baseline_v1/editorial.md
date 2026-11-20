# Editorial review: 2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp

Reviewer: video-reviewer agent · Inputs: script, storyboard, sources, fact check, captions.srt, technical.json, 3 sampled stills (contact sheet, scene_01, scene_10) · Audio not heard

Decision: PASS

## Blockers
- none

## Warnings
- Voice is the Windows SAPI placeholder (accepted by user for this draft). Audio was not heard, so voice quality, pronunciation of "MCP" and "/eval", and sync of captions to speech are unjudged.
- Visuals are plain text cards with no diagrams (accepted for this draft). Roughly half of each frame is empty gradient between the headline and captions, so retention may be weak. The storyboard's visual_description entries are not drawn.
- Segoe UI font (T001) terms still need verifying before publishing.
- Hook: the on-screen text for the first seconds is "Test your Copilot skills", a flat imperative that is weaker than the spoken "GitHub just added a way to...". It also omits MCP tools, which the narration includes. Consider "New: test your Copilot skills and MCP tools" for the first card.
- CTA: "What would you test first?" is spoken and captioned but is not on screen. The storyboard promised "follow prompt text" in scene 10, and the still shows only "Public preview". The CTA is natural, but the last card could carry it.
- Caption line breaks split phrases and end on dangling words ("test your Copilot skills and", "In Copilot Evals," then "you ask Copilot in your own"; "for Individual," then "Business and Enterprise plans."). Spelling is correct and cue timings are within the reading-speed check. Phrase-aware breaks would read better.
- The "Source: GitHub · 2026-11-17" line under each headline is small and low-contrast on mobile. It is not essential, but it may be unreadable as it stands.
- The draft runs 50.07 s against a 48 s target. This is within the 25-55 s spec, but pacing is dense: 130 words with continuous narration and no beat after the hook. Check this by ear.
- The narration says "Individual, Business and Enterprise plans" without saying "Copilot". This is accurate in context.
- The 2026-11-17 announcement against "just added" on 2026-11-20 is acceptable, but it will age quickly.

## Pass items
- Hook is stated in the first ~2 s as a concrete, news-style claim (K1) and is not misleading. The first scene's on-screen text is accurate.
- One central idea (evals make non-deterministic AI behavior testable) with a clear payoff: create, run, approve, see passed and failed checks, rerun and compare, then availability.
- On-screen text is accurate against sources.md. The two fact-check corrections ("isn't proof", "Rerun after you change a skill") were applied and are visible in the stills.
- The metadata title ("GitHub Copilot Evals: testing your skills, agents and MCP tools") matches S1 scope, with no hype. The description repeats the hook and CTA and links the primary source. The description states no unsupported claim.
- Fact check shows K1-K9 supported, with K10 labeled as interpretation. Public preview and plan scope (K9) are stated correctly, with no claim about Free plans.
- Nothing in the script claims Vally, local execution or install routes, so there is nothing unsupported.
- The CTA is a natural, low-pressure question.
- Disclosures are present: synthetic TTS voice, original text graphics, no third-party footage, and a reminder to review the YouTube altered-content setting.
- assets/manifest.csv records source, license and notes for all 3 assets. The only third-party item is the Windows system font, which is already flagged. Frames are self-generated.
- The technical.json checks pass: 1080x1920, h264/aac, 50.07 s, -16.4 LUFS, -4.4 dBFS true peak, no long silences, captions contiguous.
- Caption text is readable in the stills: large bold white text on a dark pill, with good contrast and mid-lower placement. Headline text is large and high-contrast. Left margins are safe.
