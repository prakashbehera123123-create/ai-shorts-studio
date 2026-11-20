# Script: Why MCP dropped the handshake

Language: English
Target duration: 50s

Central question: No handshake, no session: how does an MCP server know who is asking?
Payoff: Each request explains itself; cross-call state becomes explicit server-minted handles passed as tool arguments; server questions become a retry loop.
Running example (illustrative): a tool needs the user to choose, so the server returns an input required result and the client retries the same request with answers attached.
Visual motif: the signal trace as a passport stamp. One request dot carries its passport (protocol version, capabilities) through each scene; in the payoff it returns resolved.
Metaphor (interpretation): hotel key card (good for one room) vs passport shown at every checkpoint.

## Hook candidates
1. "MCP deleted its own handshake." | pattern: broken belief | curiosity 5, specificity 4, honesty 5 (S1 shows the spec removes it)
2. "How does a server know you, with no session?" | pattern: black box | curiosity 4, specificity 3, honesty 5
3. "Your MCP server just lost its session." | pattern: consequence | curiosity 4, specificity 3, honesty 2 (implies it happens to your server now; adoption is not sourced)
Chosen: 1 (broken belief, directly supported by S1).

## Beats
| beat | seconds | content |
|---|---|---|
| hook | 0-2.5 | MCP deleted its own handshake |
| tension | 2.5-10.5 | Spec removes handshake and session ID; so how does a server know who is asking? (obstacle) |
| explanation | 10.5-29.7 | 1. Key card vs passport: every request carries protocol version and capabilities; 2. wrong version returns an error; 3. state becomes explicit handles |
| example | 29.7-38.7 | Illustrative: tool needs a user choice; input required result; client retries with answers |
| caveat | 38.7-42.1 | Roots, sampling and logging deprecated but still work |
| payoff | 42.1-47.1 | Request explains itself; explicit handles; retry loop |
| cta | 47.1-49.6 | Would you miss the handshake? |

## Hook
MCP deleted its own handshake.

## Narration
The July 2026 spec removes the handshake. It also removes the session ID. So how does a server know who's asking? A session works like a hotel key card, good for one room. Now every request shows a passport. Inside are its protocol version and client capabilities. A wrong version gets an unsupported version error. Need state across calls? The server creates a handle. The client passes it as a normal tool argument. Illustrative: a tool needs the user to choose. The server returns an input required result. Then the client sends the same request again, with the answers. Roots, sampling and logging are deprecated, but still work. So each request explains itself. State becomes explicit handles. Questions become a retry loop.

## On-screen text
- MCP deleted its handshake
- Handshake and session: removed
- Who is asking?
- Key card vs passport
- Every request shows its passport
- Wrong version = error
- State = explicit handles
- Illustrative: input required
- Illustrative: retry with answers
- Deprecated, still work
- Each request explains itself
- Miss the handshake?

## CTA
Would you miss the handshake? Tell me below.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| C1 | The 2026-07-28 MCP spec removes the initialize handshake | S1 | fact |
| C2 | The spec removes sessions (Mcp-Session-Id) | S1 | fact |
| C3 | Central question: how does a server know who is asking without handshake or session | S1 | interpretation |
| C4 | A session is like a hotel key card for one room; each request shows a passport (metaphor) | S1 | interpretation |
| C5 | Every request carries its protocol version and client capabilities in a metadata block | S1 | fact |
| C6 | A version mismatch returns UnsupportedProtocolVersionError | S1 | fact |
| C7 | Servers needing cross-call state use explicit server-minted handles passed as ordinary tool arguments | S1 | fact |
| C8 | A tool needing a user choice returns resultType input_required with inputRequests (example scenario illustrative) | S1 | fact |
| C9 | The client retries the original request with inputResponses | S1 | fact |
| C10 | Roots, Sampling and Logging are deprecated but still functional during the deprecation window | S1 | fact |
| C11 | Payoff: each request explains itself; state is explicit handles; server questions are a retry loop | S1 | interpretation |
