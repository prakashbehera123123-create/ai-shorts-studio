# Brief: Why MCP dropped the handshake: stateless servers and multi round-trip requests

- Video ID: 2026-11-20-why-mcp-dropped-the-handshake-stateless-servers-and-multi
- Language: English
- Bucket: agentic-ai-mcp
- Type: evergreen
- Evidence confidence: high
- Weighted score: 4.5 / 5 (freshness 3, relevance 5, usefulness 5, evidence 5, visual 5, distinctiveness 4)
- Research file: research/2026-11-20-run2/candidates.json (candidate C06)

## Central idea
MCP spec 2026-07-28 removes protocol sessions (Mcp-Session-Id) and the initialize handshake; each request carries protocol version and client capabilities in _meta, and a server/discover RPC replaces up-front negotiation. Server-initiated requests become Multi Round-Trip Requests (input_required result, client retries with inputResponses).

## Why this audience should care
Anyone building or hosting MCP servers must understand why statelessness makes them scale behind load balancers and how elicitation/sampling now work.

## Proposed hook (must not mislead)
MCP deleted its own handshake. Here's what broke, and what got easier.

## Visual angle
Before: client and server tethered by a session cord to one pod; after: each request carries its own 'passport' (_meta) and can hit any pod behind a load balancer; then a two-step input_required retry loop.

## Editorial cautions
- tension: broken belief - 'a protocol needs a handshake and a session' vs the official spec removing both (MCP 2026-07-28 changelog); server state moves into explicit server-minted handles passed as tool arguments.
- example: real spec detail - a request carries io.modelcontextprotocol/protocolVersion and clientCapabilities in _meta; mismatch returns UnsupportedProtocolVersionError; a tool needing a user choice returns resultType 'input_required' with inputRequests, client retries with inputResponses.
- metaphor: a hotel key card (session tied to one room) vs a passport shown at every checkpoint (each request self-describing).
- evergreen: spec dated 2026-07-28, outside the 7-day window. Changelog page shows no date, so published is null. Previously deferred; URL re-verified. Do not assert SDK adoption levels.

## Status
RESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.

## Story angle (orchestrator, from sources.md only; primary page re-opened 2026-11-20)
- Tension (broken belief): "a protocol starts with a handshake and keeps a session" — the 2026-07-28 spec removes both the initialize handshake and Mcp-Session-Id (S1).
- Central question: with no handshake and no session, how does an MCP server know who it is talking to, and how does it ask the user anything?
- Worked example (real spec detail, S1): every request carries `io.modelcontextprotocol/protocolVersion` and `clientCapabilities` in `_meta`; a version mismatch returns UnsupportedProtocolVersionError; a tool that needs a user choice returns `resultType: "input_required"` with `inputRequests`, and the client retries the same request with `inputResponses`.
- Visual metaphor: hotel key card (works only for one room/session) vs passport shown at every checkpoint (each request self-describing).
- Payoff: each request explains itself; cross-call state becomes explicit server-minted handles passed as ordinary tool arguments; server questions become a retry loop (S1).
- Caveats from S1: Roots, Sampling and Logging are deprecated (still functional during the deprecation window); SSE resumability removed (a broken stream loses the in-flight request; client re-issues it).
- NOT in sources — do not say: that statelessness was done "to scale behind load balancers", any SDK adoption level, any reason the maintainers gave. The "Why this audience should care" line above overstates S1; the script may only say what changed, not why.
