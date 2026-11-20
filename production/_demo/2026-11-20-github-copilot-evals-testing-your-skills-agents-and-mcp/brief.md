# Brief: GitHub Copilot Evals: testing your skills, agents and MCP tools

- Video ID: 2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp
- Language: English
- Bucket: developer-workflows
- Type: news (last 7 days)
- Evidence confidence: high
- Weighted score: 4.3 / 5 (freshness 5, relevance 4, usefulness 4, evidence 5, visual 3, distinctiveness 4)
- Research file: research/2026-11-20/candidates.json (candidate C01)

## Central idea
GitHub changelog dated Nov 17, 2026: Copilot Evals is in public preview for Copilot Individual, Business and Enterprise plans. It lets users create repeatable evals for a skill, custom agent or MCP tool, and compare runs from before and after a customization change. Users approve each run before it starts.

## Why this audience should care
Developers building agent setups with skills and MCP tools need a way to check whether changes actually help; this is a concrete tool for that.

## Proposed hook (must not mislead)
GitHub just added a way to test your Copilot skills and MCP tools like code.

## Visual angle
Self-made diagram of the eval loop: create eval, approve run, compare before/after. No imitation of GitHub UI.

## Editorial cautions
- Page says to install it in VS Code, Copilot CLI or the Copilot app; do not claim more surfaces.
- Public preview: say so explicitly.

## Status
RESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.

## Story angle (added for dry run 2, from sources.md only)
- Tension (pattern: consequence / broken belief): one good answer does not show a customization works, because AI output can change from one run to the next (S3).
- Central question: how do you know a change to your skill, agent or MCP tool actually helped?
- Worked example (illustrative, must be labelled): a skill edit that passed once in a manual try, then a repeatable eval run before and after the edit shows which checks pass and fail (S2, S4).
- Visual motif: the signal trace — the same task sent through the agent twice; one trace reaches a green check, the rerun forks to a red one; later two eval runs (before/after) side by side.
- Payoff: rerun the same eval after every customization change and compare runs (S3, S4). Caveat: public preview (S1).
