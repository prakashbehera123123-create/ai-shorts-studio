# Fact check: Your agent should sleep, not poll (GitHub Event Streams and gh event listen)

Primary sources re-opened 2026-11-20: S1 https://github.blog/changelog/2026-11-17-github-event-streams-is-now-in-preview (dated 2026-11-17) and S2 https://github.blog/changelog/2026-11-18-wait-for-pull-request-events-with-github-cli (dated 2026-11-18, gh v2.105.0 or later). Both match sources.md. Neither page names a transport, latency, cost or token figures; the script claims none.

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| C1 | Without a webhook receiver, the usual way to get PR feedback is polling; the agent keeps asking | qualified | S1 | Page frames polling as the alternative that forces a trade-off, not as a "usual way". Narration only uses the hook "keeps asking: is it done yet?", a fair framing of polling. No "usual/most people" claim is spoken. |
| C2 | Poll often and you burn rate-limit budget on requests that mostly return nothing new | supported | S1 | Page wording is near-identical. |
| C3 | Poll less often and review feedback sits until the next check | supported | S1 | Page: feedback sits until your next check. |
| C4 | Doorbell vs knocking is a metaphor for push vs poll | supported | S1 | Interpretation, correctly typed; no factual content. |
| C5 | Event Streams lets an agent subscribe to a pull request and hold one open connection to receive events | qualified | S1 | Page: keep the connection open to receive events. "One" is not stated; harmless but not sourced, and no protocol is named (none claimed). |
| C6 | gh event listen takes a PR URL and the events you care about, e.g. a submitted review | supported | S2 | Matches the page. |
| C7 | It creates the subscription, opens the stream and prints each event as one line of JSON | supported | S2 | Matches the page. |
| C8 | By default it exits after the first event; flags --count, --follow, --timeout, --jq | qualified | S2 | Flags and default are correct. Narration "then exits after the first" and scene 7 "Exits after first event" omit "by default"; --count/--follow change that. Page also lists --template (not required). |
| C9 | Your agent sleeps while there's no work and wakes as soon as there is | supported | S1 | Direct page sentence. |
| C10 | No public webhook endpoint is needed, so an agent can receive events while running on a laptop | supported | S1 | Direct page sentence. |
| C11 | Event Streams is a preview with a waitlist; gh event commands may change | supported | S1, S2 | S1: preview, waitlist, all plans once approved. S2: gh event commands in preview and may change. "Waitlist only" is acceptable shorthand. |
| C12 | How should an agent wait for PR feedback without polling (central question) | supported | S1, S2 | Framing question, not an assertion. |

## Unmapped statements
- "Your agent keeps asking: is it done yet?" (hook): framing of polling (C1). No invented "most people get this wrong" or statistic. Acceptable; hook candidate 2's "constantly" was correctly rejected.
- "Check less, and feedback sits waiting": C3.
- "Think doorbell, not knocking again and again": C4, metaphor.
- "In the CLI": C6. "Add the events you want, like a submitted review": C6.
- "Which agent loop would you fix first? Tell me below.": CTA, no claim.
- Not claimed, correctly: transport (SSE/WebSocket), latency, cost, token savings, poll counts, the gh v2.105.0 requirement, event list beyond submitted review.
- Scene 8 "Open wire", scene 2 loop and rate-limit chip filling: metaphorical visuals, no numbers.

## On-screen and chart values
No numbers or charts.
- "Done yet?": OK (hook framing).
- "Mostly nothing new" / "Agent asks / Nothing new / Burns rate limit": OK (C2).
- "Poll often / Rate limit burned" vs "Check less / Feedback sits": OK (C2, C3).
- "Doorbell, not knocking": OK (metaphor).
- "Subscribe to a pull request / One open connection / Events arrive", tag "preview": OK, "One" mildly beyond source (C5).
- "gh event listen", PR / submitted review / flags "--count --follow --timeout --jq": OK (C6, C8). UI panel is self-created, not real output.
- Checklist "Creates the subscription / Opens the stream / One JSON line per event / Exits after first event": qualified, add "by default" (C8).
- "Sleeps: no work" / "Wakes: event arrives": OK (C9).
- "No public webhook endpoint" / "Works on a laptop": OK (C10).
- "Preview / Waitlist only / May change" with amber tags: OK (C11). Preview and waitlist caveat is present in narration (scene 10) and on screen.
- "Which loop first?" / "Tell me below": CTA.

## Required corrections
1. Scene 7 narration: "then exits after the first." -> "then, by default, exits after the first." (C8). Script.md narration and its spoken copy must match.
2. Scene 7 checklist item (visual.items[3]) and its mirror in script/on-screen: "Exits after first event" -> "Exits after first event (default)" (C8).
3. Optional: scene 5 row "One open connection" -> "Open connection" and narration "It holds one open connection" -> "It keeps a connection open" (C5, "one" not sourced). If kept, treat as accepted simplification.
No unsupported claims found.
