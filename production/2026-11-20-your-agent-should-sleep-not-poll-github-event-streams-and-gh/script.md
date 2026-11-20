# Script: Your agent should sleep, not poll

Language: English
Target duration: 48s

Central question: How should an agent wait for pull-request feedback without polling?
Payoff: Subscribe once and keep a connection open; the agent sleeps while there's no work and wakes as soon as there is. Caveat: preview, waitlist only, may change.
Running example: one agent waiting on one pull request, first asking again and again, then sleeping on an open wire that lights up when a review arrives.
Visual motif: the signal trace. A dot knocks and returns empty (poll); later one open wire stays dark until an event lights it (push).
Pronunciation: "G H event listen" is spoken for "gh event listen".

## Hook candidates
1. "Your agent keeps asking: is it done yet?" | pattern: consequence | curiosity 4, specificity 4, honesty 5 (polling is the usual way without a receiver, S1)
2. "Your coding agent checks your pull request constantly. It doesn't have to." | pattern: broken belief | curiosity 4, specificity 3, honesty 3 (constantly is not sourced; too long for 3 s)
3. "Poll often or poll late. Both lose." | pattern: paradox demo | curiosity 3, specificity 4, honesty 4
Chosen: 1 (consequence, directly supported by S1).

## Beats
| beat | seconds | content |
|---|---|---|
| hook | 0-3 | Your agent keeps asking: is it done yet? |
| tension | 3-12 | Obstacle: poll often and burn rate limit on mostly empty answers; poll less and feedback sits |
| context | 11-14 | Doorbell metaphor: stop knocking |
| explanation | 14-21 | Event Streams: subscribe to a pull request, keep a connection open, events arrive |
| example | 21-33 | gh event listen: PR link plus events; one JSON line per event; exits after first by default |
| payoff | 33-42 | Agent sleeps until there is work; no public webhook endpoint, works on a laptop |
| payoff (caveat) | 42-45 | Preview, waitlist only, may change |
| cta | 45-48 | Which agent loop would you fix first? |

## Hook
Your agent keeps asking: is it done yet?

## Narration
Poll often, and you burn rate limit on requests that mostly return nothing new. Wait longer between checks, and feedback sits until the next one. Think doorbell, not knocking again and again. GitHub Event Streams lets an agent subscribe to a pull request. It keeps a connection open, and events arrive. In the CLI, G H event listen takes a pull request link. Add the events you want, like a submitted review. It prints each event as one line of JSON, then, by default, exits after the first. Your agent sleeps while there's no work, and wakes as soon as there is. No public webhook endpoint, so it works on a laptop. It's preview, waitlist only, and may change.

## On-screen text
- Done yet?
- Mostly nothing new
- Poll less: feedback waits
- Doorbell, not knocking
- Subscribe once
- gh event listen
- One JSON line per event
- Sleeps, then wakes
- No webhook endpoint
- Preview, waitlist only
- Which loop first?

## CTA
Which agent loop would you fix first? Tell me below.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| C1 | Without a webhook receiver, the usual way to get PR feedback is polling; the agent keeps asking | S1 | fact |
| C2 | Poll often and you burn rate-limit budget on requests that mostly return nothing new | S1 | fact |
| C3 | Poll less often and review feedback sits until the next check | S1 | fact |
| C4 | Doorbell vs knocking repeatedly is a metaphor for push vs poll | S1 | interpretation |
| C5 | GitHub Event Streams lets an agent subscribe to a pull request and keep a connection open to receive events | S1 | fact |
| C6 | gh event listen takes a PR URL and the events you care about, e.g. a submitted review | S2 | fact |
| C7 | It creates the subscription, opens the stream and prints each event as one line of JSON | S2 | fact |
| C8 | By default it exits after the first event; flags --count, --follow, --timeout, --jq | S2 | fact |
| C9 | Your agent sleeps while there's no work and wakes as soon as there is | S1 | fact |
| C10 | No public webhook endpoint is needed, so an agent can receive events while running on a laptop | S1 | fact |
| C11 | Event Streams is a preview with a waitlist; gh event commands may change | S1, S2 | fact |
| C12 | How should an agent wait for PR feedback without polling (central question) | S1, S2 | interpretation |
