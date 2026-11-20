# Fact check: Why MCP dropped the handshake

Primary source re-opened 2026-11-20: https://modelcontextprotocol.io/specification/2026-07-28/changelog (S1; changes relative to revision 2025-11-25; page carries no publication date, only the revision identifier 2026-07-28). Every claim below maps to this one page. Brief Story angle respected: no scaling/load-balancer claim, no SDK adoption, no maintainer reasons found in script.md or storyboard.json.

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| C1 | The 2026-07-28 MCP spec removes the initialize handshake | supported | S1 | Major change 2: "remove the initialize/notifications/initialized handshake". Narration says "The July 2026 spec": date is inferred from the revision id 2026-07-28 (see corrections, optional). |
| C2 | The spec removes sessions (Mcp-Session-Id) | supported | S1 | Major change 1: removes protocol-level sessions and the Mcp-Session-Id header from the Streamable HTTP transport. "Session ID" in narration is accurate. |
| C3 | Central question: how does a server know who is asking without handshake or session | supported | S1 | Interpretation/framing question, not a factual assertion. Note: clients SHOULD (optional) send clientInfo per request; script answers with version and capabilities only, which is what the page says is mandatory. |
| C4 | A session is like a hotel key card for one room; each request shows a passport (metaphor) | qualified | S1 | Interpretation only. Must stay labelled as metaphor; the scene 4 tiles are metaphor labels. Do not read "passport" as authentication or identity (spec does not say requests prove identity). |
| C5 | Every request carries its protocol version and client capabilities in a metadata block | supported | S1 | Major change 2: io.modelcontextprotocol/protocolVersion and io.modelcontextprotocol/clientCapabilities in _meta. |
| C6 | A version mismatch returns UnsupportedProtocolVersionError | supported | S1 | Spelled exactly as in the page (scene 6 label matches). |
| C7 | Servers needing cross-call state use explicit server-minted handles passed as ordinary tool arguments | supported | S1 | Major change 1 wording. Applies to servers that need cross-call state; narration "Need state across calls?" preserves that. |
| C8 | A tool needing a user choice returns resultType input_required with inputRequests (example scenario illustrative) | supported | S1 | Major change 7: InputRequiredResult (resultType: "input_required") with inputRequests. The "user choice" scenario is our illustration and is labelled. |
| C9 | The client retries the original request with inputResponses | supported | S1 | Major change 7: clients respond with inputResponses on a retry of the original request. |
| C10 | Roots, Sampling and Logging are deprecated but still functional during the deprecation window | supported | S1 | Deprecated section 1: remain fully functional during the deprecation window; new implementations should not add them. |
| C11 | Payoff: each request explains itself; state is explicit handles; server questions are a retry loop | qualified | S1 | Interpretation of C5, C7, C8, C9. "Questions become a retry loop" is true only for server-initiated requests (roots/sampling/elicitation replaced by MRTR); listener is not told which questions. Acceptable as a summary. |

## Unmapped statements
- "The July 2026 spec removes the handshake" (scene 2): C1, but "July 2026" comes from the revision id 2026-07-28, not from a dated page. Qualified, harmless.
- "So how does a server know who's asking?" (scene 3): C3 framing question.
- "Roots, sampling and logging are deprecated, but still work" (scene 10): C10; no removal date or window length is stated, correctly.
- "Tell me below" and "Would you miss the handshake?": CTA, no claim.
- Hook "MCP deleted its own handshake": supported by C1; "deleted" = removed. No "most people get this wrong" or invented stat.
- Script header lines (Central question, Payoff, Running example, Metaphor, hook candidates, beat table): consistent with the claim map; hook 3 note about unsourced adoption is correct.
- Not claimed, correctly: scaling behind load balancers, SDK adoption, maintainers' reasons, server/discover, subscriptions/listen, SSE resumability removal, ping removal.

## On-screen and chart values
No numbers or charts.
- "MCP deleted its handshake" / "Handshake and session: removed" (scenes 1-2): OK (C1, C2). Rows "initialize handshake" and "Mcp-Session-Id" match the spec spelling.
- "Who is asking?" (scene 3): OK (question).
- "Key card vs passport" / "Good for one room" / "Shown on every request" (scene 4): OK as metaphor (C4).
- "Every request shows its passport" (scene 5): OK. Visual fields "_meta / protocolVersion" and "_meta / clientCapabilities": qualified. Real keys are io.modelcontextprotocol/protocolVersion and io.modelcontextprotocol/clientCapabilities; bare names are a shortening not spelled as in the spec (correction 1).
- "Wrong version = error", fork labels "Version matches" and "UnsupportedProtocolVersionError" (scene 6): OK (C6). "Version matches" is our label for the non-error path.
- "State = explicit handles", flow nodes "Server mints a handle" / "Client passes it as an argument" / "Next tool call" (scene 7): OK (C7).
- "Illustrative: input required", node "resultType: input_required" (scene 8): OK (C8); illustrative flag set and in on_screen_text.
- "Retry with answers", panel "inputResponses" (scene 9): OK (C9). Field name matches spec. Illustrative flag is set (badge) though on_screen_text lacks the word; acceptable because the badge is on screen (optional correction 3).
- "Deprecated, still work", Roots/Sampling/Logging with "deprecated" tags (scene 10): OK (C10). Source chip should name MCP spec changelog 2026-07-28.
- "Each request explains itself", rows "Request explains itself" / "State: explicit handles" / "Questions: retry loop", tag "resolved" (scene 11): OK as interpretation (C11); "resolved" is the dot motif, not a spec term.
- "Miss the handshake?" / "Tell me below" (scene 12): CTA.
- Scene 12 source_ids is empty: fine, no claim.

## Required corrections
No unsupported claims found. Required (identifier spelling):
1. storyboard.json scene 5 visual.fields: change `["_meta", "protocolVersion"]` to `["_meta", "io.modelcontextprotocol/protocolVersion"]` and `["_meta", "clientCapabilities"]` to `["_meta", "io.modelcontextprotocol/clientCapabilities"]` (if too long for mobile, split across two lines; do not leave the bare names as if they were the keys).

Optional:
2. Narration scenes 2 (script.md and storyboard.json) "The July 2026 spec removes the handshake." -> "The 2026-07 spec revision removes the handshake." or keep as is (date derived from revision id 2026-07-28; page is undated). Keep consistent in both files.
3. storyboard.json scene 9 on_screen_text "Retry with answers" -> "Illustrative: retry with answers" (script.md On-screen text line "Retry with answers" likewise), so the label is in the text and not only the badge.
