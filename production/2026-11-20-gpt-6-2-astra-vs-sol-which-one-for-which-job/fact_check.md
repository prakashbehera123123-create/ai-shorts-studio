# Fact check: 2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job

Checked: 2026-11-20 · Method: re-read primary source(s) via WebFetch (page converted to markdown, then answered by a small model with quote-extraction prompts; not a raw DOM read, so quotes below are as returned by that tool)

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| K1 | OpenAI says Astra is for demanding reasoning and coding tasks | supported | S1 | Nov 17 entry: "Use GPT-6.2 Astra for demanding reasoning and coding tasks" |
| K2 | OpenAI says Sol is for everyday coding and agent workflows | supported | S1 | Same sentence: "GPT-6.2 Sol for everyday coding and agent workflows." Attributed to OpenAI correctly. |
| K3 | Positioning, not a ranking; sources differ on which is heavier | qualified | S1, S5 | GitHub says Astra is for "agentic coding and terminal work", Sol for "complex agentic coding and in-depth code review". That is a different framing, not an explicit contradiction. "Not a ranking" is the script's own interpretation. Narration is fine because it attributes to OpenAI and never says which is heavier. Do not say "sources conflict" on screen or in narration. |
| K4 | Tool calling requires the Responses API | supported | S2 | "Tool calling requires the Responses API." The entry is about the two GPT-6.2 models. |
| K5 | Both models also support Chat Completions | supported | S2 | "Both models support the Responses API and Chat Completions." |
| K6 | Agents that call tools need Responses | qualified | S2 | The source says tool calling requires Responses. It never mentions "agents". The inference is sound (agents use tools), but the script should phrase it as the tool-calling rule. Chat Completions plus tool calling is not stated as impossible beyond that sentence. |
| K7 | GPT-6.2 changes how Responses API preserves reasoning when you edit a conversation's prefix | supported | S3 | "changes how the Responses API preserves reasoning when you edit a conversation's prefix." The direction of the change is not given. |
| K8 | If your app rewrites earlier messages, test that | qualified | S3 | Advice only. The source does not say what breaks. Fine as a "test it" suggestion, with no claim that it will break. |
| K9 | Changes how Responses API handles the top-level instructions field | supported | S3 | The entry says the release changes handling of the top-level `instructions` field. WebFetch paraphrased this one rather than quoting it. Re-confirm wording in the browser pane if exact phrasing matters. |
| K10 | OpenAI points to a GPT-6.2 migration guide for recommended integration updates | supported | S3 | Entry directs readers to "the GPT-6.2 migration guide". The guide's contents were not opened. |
| K11 | Read the migration guide before shipping | qualified | S3 | Advice, not a sourced fact. Acceptable if it is clearly the script's own recommendation. |

## Unmapped statements
- "That's positioning, not a ranking." — qualified. It is interpretation, mapped under K3. It is acceptable because the narration attributes the positioning to OpenAI.
- "Now, the migration checks." / "First... Second... Third..." — qualified. The wording implies a complete list of migration steps. The source only names three changes. The checks are the script's selection from the changelog entry.
- "tool calling requires the Responses API" stated bare (no "OpenAI says") — supported (K4). The attribution to OpenAI is only implicit. The on-screen "OpenAI's own positioning" covers only the first line.
- Hook "Moving your app to GPT-6.2? Check these before you switch." — supported as advice. No factual claim.
- On-screen text "Needs the Responses API" — qualified. Under "Check 1: Tool calling" it reads as true. Without that context it would overstate, since both models also support Chat Completions for non-tool use.
- CTA "Which of these would break your app first?" — supported. It is a question, not a factual claim. It does assume these changes might break apps, which the source does not say.
- On-screen "Which breaks first?" — qualified, same reason as the CTA.
- Not in script, do not add: GitHub availability, plans and review-quality claims (S4/S5). They are not used.

## Required corrections
- K6 and narration: change "agents that call tools need Responses" to "so anything that calls tools needs Responses" (the source says tool calling, not agents).
- Narration: change "Now, the migration checks." to "Now, three checks from OpenAI's changelog." Do not imply a complete checklist.
- Narration: change "First, tool calling requires the Responses API." to "First, OpenAI says tool calling requires the Responses API."
- Narration: change "Second, GPT-6.2 changes..." to "Second, OpenAI says GPT-6.2 changes..." so the whole list is attributed. Keep "If your app rewrites earlier messages, test that" as advice, with no claim that it breaks.
- Migration guide line: keep as is ("OpenAI points to a GPT-6.2 migration guide for recommended integration updates"). It says nothing about the guide's contents. Do not add anything about what the guide contains. Change "Read it before you ship" to "Worth reading before you ship" so it reads as advice.
- CTA and on-screen "Which breaks first?": soften to "Which of these affects your app?" because the source does not say these changes break anything.
- sources.md: S4/S5 are currently not used for any spoken claim. Keep S5 only for the conflict note.

## Corrections applied (main session, 2026-11-20)
- "the migration checks" -> "three checks from OpenAI's changelog"; added "OpenAI says" to checks 1 and 2.
- "agents that call tools need Responses" -> "anything that calls tools needs Responses" (K6 updated).
- "Read it before you ship" -> "Worth reading before you ship" (K11 updated).
- CTA/on-screen "Which breaks first?" -> "Which check matters most?" (source does not say anything breaks).
- K3 map text no longer says "sources conflict"; it says GitHub describes the models in different terms.
- Storyboard retimed to 47.0s so every scene stays under 200 wpm.
