# Brief: Your agent should sleep, not poll: GitHub Event Streams and gh event listen

- Video ID: 2026-11-20-your-agent-should-sleep-not-poll-github-event-streams-and-gh
- Language: English
- Bucket: agentic-ai-mcp
- Type: news (last 7 days)
- Evidence confidence: high
- Weighted score: 4.4 / 5 (freshness 5, relevance 5, usefulness 4, evidence 4, visual 4, distinctiveness 4)
- Research file: research/2026-11-20-run2/candidates.json (candidate C01)

## Central idea
GitHub Event Streams (preview, waitlist) lets an agent subscribe to a pull request and hold an open connection, receiving events (review submitted, new commits, merge conflict, merge/close, check-suite changes) instead of polling. gh event listen wraps it: one command, JSON line per event, exits after first event by default.

## Why this audience should care
Every CI-watching or PR-babysitting agent loop burns tokens and API calls polling; push-based wake-up is a core agent-architecture pattern a junior engineer can apply today.

## Proposed hook (must not mislead)
Your coding agent is checking your pull request every few seconds. It doesn't have to.

## Visual angle
Split diagram: left an agent repeatedly knocking 'done yet?' on a PR; right a sleeping agent with a single open wire that lights up when a review/check event arrives. Show the real gh event listen flags as terminal text (self-created).

## Editorial cautions
- tension: before->after - agents loop-poll PR state (the changelog says gh pr view/run watch now suggest gh event listen instead of polling), versus an open event stream where 'your agent sleeps while there's no work and wakes as soon as there is' (GitHub changelog 2026-11-17/18).
- example: worked example from sources - gh event listen takes a PR URL plus event types, creates a subscription, opens the stream, prints each event as one JSON line, exits after first event; --count, --follow, --timeout, --jq flags. No latency or cost numbers published, so any poll-vs-push cost comparison must be labelled illustrative.
- metaphor: doorbell vs. repeatedly opening the front door to check if the courier is there.
- Preview and waitlist-only; gh event commands 'may change' (v2.105.0+). Page does not state transport (SSE/WebSocket); do not claim one.

## Status
RESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.

## Story angle (orchestrator, from sources.md only; both primary pages re-opened 2026-11-20)
- Tension (before→after): polling forces a bad trade — poll often and burn rate-limit budget on requests that mostly return nothing new; poll less and review feedback sits until the next check (S1).
- Central question: how should an agent wait for pull-request feedback without polling?
- Worked example (real, S2): `gh event listen` with a PR URL and the events you care about (e.g. a submitted review) creates the subscription, opens the stream and prints each event as one JSON line; by default it exits after the first event, so it slots into scripts and agent loops; `--count`, `--follow`, `--timeout`, `--jq`/`--template`.
- Visual metaphor: doorbell vs opening the front door every few seconds to check for the courier (the signal trace = one open wire that lights when an event arrives).
- Payoff: subscribe once, keep the connection open, the agent "sleeps while there's no work and wakes as soon as there is"; no public webhook endpoint, so it works on a laptop (S1). gh pr view / run watch now suggest `gh event listen` instead of polling (S2).
- Caveats: preview, waitlist-only; gh event commands "may change"; requires gh v2.105.0+ (S1, S2).
- NOT in sources — do not say: transport (SSE/WebSocket), latency or cost numbers, token savings figures; any poll-count comparison must be labelled illustrative.
