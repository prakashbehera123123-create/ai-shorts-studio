# Brief: GPT-6.2 Astra vs Sol: which one for which job

- Video ID: 2026-11-20-gpt-6-2-astra-vs-sol-which-one-for-which-job
- Language: English
- Bucket: llm-engineering
- Type: news (last 7 days)
- Evidence confidence: high
- Weighted score: 4.2 / 5 (freshness 5, relevance 5, usefulness 4, evidence 4, visual 3, distinctiveness 3)
- Research file: research/2026-11-20/candidates.json (candidate C02)

## Central idea
OpenAI API changelog entry dated Nov 17, 2026: use GPT-6.2 Astra for demanding reasoning and coding tasks, or GPT-6.2 Sol for everyday coding and agent workflows. The entry states tool calling requires the Responses API.

## Why this audience should care
Engineers choosing a model for coding agents need to know the split between the two variants and the API requirement for tool calling.

## Proposed hook (must not mislead)
OpenAI split GPT-6.2 into two models, and tool calling needs the Responses API.

## Visual angle
Two-column comparison card (Astra vs Sol) with the Responses API requirement shown as a flow arrow; no vendor logos.

## Editorial cautions
- No benchmark claims are sourced; do not state which model is better beyond OpenAI's stated use cases.
- Check pricing/availability on the model pages before scripting if mentioned.

## Status
RESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.

## Story angle (added for dry run 2, from sources.md only)
- Tension (pattern: black box / consequence): switching to GPT-6.2 looks like changing one model name, but OpenAI's changelog lists API behaviour changes (S2, S3).
- Central question: what do you check before you switch an app to GPT-6.2?
- Worked example (illustrative, must be labelled): an app that calls tools through Chat Completions, and an app that edits earlier messages in a conversation — the two places S2 and S3 say behaviour differs.
- Visual motif: the signal trace — a request leaving the app; tool-call requests can only route through the Responses API lane (S2).
- Payoff: three checks from OpenAI's changelog, then read the migration guide (S3). Positioning of Astra vs Sol is OpenAI's own wording (S1); GitHub describes them differently (S5) — never rank them.
