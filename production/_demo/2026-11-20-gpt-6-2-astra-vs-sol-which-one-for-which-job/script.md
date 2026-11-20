# Script: What to check before you switch to GPT-6.2

Language: English
Target duration: 50s

Central question: What do you check before you switch an app to GPT-6.2?
Payoff: Test three things we picked from OpenAI's changelog (tool calling, edited conversation history, the instructions field), then read the migration guide.
Running example (illustrative): an app that calls tools through Chat Completions.
Visual motif: the signal trace, a request leaving the app and routing through an API lane.

## Hook candidates
1. "Switching to GPT-6.2? Check these three things first." Pattern: Consequence (practical checklist). Scores: curiosity 4, specificity 4, honesty 5 (total 13).
2. "Your model name is one line. Your app's behaviour is not." Pattern: Broken belief. Scores: curiosity 4, specificity 2, honesty 3 (total 9). Rejected: the model name does change.
3. "Request goes in, ? ? ?, answer comes out. Does GPT-6.2 change the middle?" Pattern: Black box. Scores: curiosity 3, specificity 3, honesty 4 (total 10).
Chosen: candidate 1. Revised after fact check: the first v2 hook overstated behaviour change for all apps.

## Beats
- hook: three checks before switching (our framing).
- context: two models, both on two APIs.
- tension: the changelog notes differences; we picked three.
- explanation 1: tool calling requires the Responses API.
- example: illustrative app calling tools through Chat Completions.
- explanation 2: Responses API reasoning preservation on edited earlier messages.
- explanation 3: Responses API handling of the instructions field.
- payoff: test the three, read the migration guide.
- payoff caveat: one requirement, two behaviour changes.
- cta: which check would your app hit first.

## Hook
Switching to GPT-6.2? Check these three things first.

## Narration
OpenAI released two models, Astra and Sol. Both support the Responses API and Chat Completions. The changelog notes differences. We picked three worth testing. One. Tool calling requires the Responses API. Illustrative: if your app calls tools through Chat Completions, tools on GPT-6.2 need the Responses API. Two. In the Responses API, GPT-6.2 changes how reasoning is preserved when you edit earlier messages. Three. It also changes how the Responses API handles the top-level instructions field. So test those three before you switch. Then read OpenAI's GPT-6.2 migration guide. The first is a requirement. The other two are behaviour changes worth testing.

## On-screen text
- 3 checks before GPT-6.2
- Two models, two APIs
- 3 checks (our pick)
- 1: Tool calling
- Illustrative: tools app
- 2: Edited history
- 3: Instructions field
- Test 3, then read the guide
- 1 requirement, 2 changes
- Which one first?

## CTA
Which of these three would your app hit first? Comment below.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| C1 | Before switching an app to GPT-6.2 there are things worth checking; the three chosen here are our selection from OpenAI's changelog, not a list the changelog gives. | S2, S3 | interpretation |
| C2 | OpenAI released two GPT-6.2 models, Astra and Sol (no ranking). | S1 | fact |
| C3 | Both GPT-6.2 models support the Responses API and Chat Completions. | S2 | fact |
| C4 | The changelog notes differences for GPT-6.2 (tool calling requirement; Responses API reasoning preservation; instructions field handling); picking three to test is our framing. | S2, S3 | interpretation |
| C5 | Tool calling requires the Responses API. | S2 | fact |
| C6 | Illustrative: an app that calls tools through Chat Completions would need the Responses API to use tools with GPT-6.2 (follows from C5). | S2 | interpretation |
| C7 | In the Responses API, GPT-6.2 changes how reasoning is preserved when you edit a conversation's earlier messages (its prefix). | S3 | fact |
| C8 | GPT-6.2 changes how the Responses API handles the top-level instructions field. | S3 | fact |
| C9 | OpenAI points to a GPT-6.2 migration guide for recommended integration updates; testing first is our suggestion. | S3 | fact |
| C10 | Of the three, tool calling is a stated requirement; the other two are stated behaviour changes worth testing. | S2, S3 | interpretation |
