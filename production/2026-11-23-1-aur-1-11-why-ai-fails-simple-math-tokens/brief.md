# Brief: 1 aur 1 = 11? Why AI fails simple math: tokens

- Video ID: 2026-11-23-1-aur-1-11-why-ai-fails-simple-math-tokens
- Language: English
- Bucket: llm-engineering
- Type: evergreen
- Evidence confidence: high
- Weighted score: 4.7 / 5 (freshness 5, relevance 5, usefulness 4, evidence 5, visual 5, distinctiveness 4)
- Research file: research/2026-11-23/approved/candidates.json (candidate C01)

## Central idea
LLMs read numbers as tokens, not digits. GPT-3.5/4 tokenize up to 3-digit chunks left-to-right; Singh & Strouse (2024) found forcing right-to-left grouping with commas largely improved arithmetic, and errors followed stereotyped patterns. Counting letters is hurt the same way (Zhang et al. 2024).

## Why this audience should care
Fastest niche pattern this week (TechAkshay 'AI fails' Shorts at 77K-280K views/day) only shows the failure; we explain the mechanism every AI user and engineer should know.

## Proposed hook (must not mislead)
This AI writes code. So why can't it add two numbers? It's not the brain. It's the eyes.

## Visual angle
Robot at a desk reading a number that gets chopped into token blocks [2 0 2][4 1 1]; the same number re-chunked with commas lines up and the sum lights green.

## Editorial cautions
- Tension: broken belief - an AI that writes code stumbles on primary-school arithmetic.
- Worked example: illustrative number shown in left-to-right 3-digit chunks vs comma-separated right-to-left chunks (label as illustrative, not a real tokenizer dump unless we capture one ourselves).
- Visual metaphor: reading glasses that cut text into wrong-size pieces.
- Findings are on GPT-3.5/GPT-4 (2024); the paper says the gap shrinks with scale. Say 'many models' and do not claim today's reasoning models always fail.
- Do not reproduce TechAkshay's prompts or clips.

## Status (superseded by status.json)
RESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.

## Owner direction (2026-11-23)
- Approved by owner in chat (C01 + C06). ENGLISH narration only, no Hindi. Cloned voice, best-of-3 takes, 165 wpm floor, no transition SFX.
- Professional structure: COLD-OPEN HOOK (0-2 s) -> short INTRO beat that names the question (2-5 s) -> body -> payoff -> OUTRO with CTA.
- Outro CTA: "For more AI concepts like this, follow."

## Hook reference (structure only; never copy wording or visuals)
From velocity_evidence.md rows 1-5 (TechAkshay 2.0, 77K-280K views/day): second 0 shows one big subject word plus an
on-camera challenge to the AI; the "failure" lands within about 1 s; no greeting or logo first. Ours: the impossible sum on screen at
frame 0 ("1 + 1 = 11?"), then a promise of the reason, not just the fail.

## Central question
Why does an AI that writes code stumble on simple arithmetic and letter counting?

## Tension
Broken belief: "smart enough to code = smart enough to add." The model never sees digits, only chunks (tokens).

## Worked example (ILLUSTRATIVE, labelled on screen)
A long number such as 8302447 split left-to-right into 3-digit chunks [830][244][7] vs comma grouping 8,302,447 ->
[8][302][447] that lines up with place value. State the paper's finding in words ("forcing right-to-left grouping with commas
largely improved accuracy in GPT-3.5 and GPT-4"). No invented percentages.

## Visual metaphor and world
- Metaphor: the robot reads through glasses that slice text into the wrong-size pieces.
- World (new, not the 11-22 office): a classroom chalkboard plus a robot student at a school desk; token blocks as physical tiles on the desk.
- Opening image: the chalkboard shows "1 + 1 = 11?" and the robot raises its hand. Callback ending: same board, the commas added, the robot gives a green tick.
- B-roll: motion-text panel "text -> tokens -> model" with Lucide icons (type, scissors, cpu).
