# Script: Moving to GPT-6.2? Check these first

Language: English
Target duration: 45s

## Hook
Moving your app to GPT-6.2? Check these before you switch.

## Narration
OpenAI says GPT-6.2 Astra is for demanding reasoning and coding tasks, and GPT-6.2 Sol is for everyday coding and agent workflows. That's positioning, not a ranking. Now, three checks from OpenAI's changelog. First, OpenAI says tool calling requires the Responses API. Both models also support Chat Completions, but anything that calls tools needs Responses. Second, OpenAI says GPT-6.2 changes how the Responses API preserves reasoning when you edit a conversation's prefix. If your app rewrites earlier messages, test that. Third, it changes how the top-level instructions field is handled. OpenAI points to a GPT-6.2 migration guide for recommended integration updates. Worth reading before you ship.

## On-screen text
- Moving to GPT-6.2?
- OpenAI's own positioning
- Check 1: Tool calling
- Needs the Responses API
- Check 2: Reasoning and edited prefixes
- Check 3: The instructions field
- Read the migration guide
- Which check matters most?

## CTA
Which of these checks matters most for your app? Tell me below.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| K1 | OpenAI says GPT-6.2 Astra is for demanding reasoning and coding tasks. | S1 | fact |
| K2 | OpenAI says GPT-6.2 Sol is for everyday coding and agent workflows. | S1 | fact |
| K3 | That is OpenAI's positioning of the two GPT-6.2 models, not a ranking; GitHub describes the two models in different terms. | S1, S5 | interpretation |
| K4 | Tool calling requires the Responses API for GPT-6.2 Astra and GPT-6.2 Sol. | S2 | fact |
| K5 | Both GPT-6.2 models also support Chat Completions. | S2 | fact |
| K6 | Anything that calls tools needs the Responses API with GPT-6.2 (restates tool calling requiring Responses). | S2 | interpretation |
| K7 | GPT-6.2 changes how the Responses API preserves reasoning when you edit a conversation's prefix. | S3 | fact |
| K8 | If your app rewrites earlier messages in a conversation, test that behavior on GPT-6.2 (advice built on the prefix-editing change). | S3 | interpretation |
| K9 | GPT-6.2 changes how the Responses API handles the top-level instructions field. | S3 | fact |
| K10 | OpenAI points to a GPT-6.2 migration guide for recommended integration updates. | S3 | fact |
| K11 | The GPT-6.2 migration guide is worth reading before shipping a migration (advice built on OpenAI pointing to it). | S3 | interpretation |
