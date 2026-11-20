# Fact check: 2026-11-20-github-copilot-evals-testing-your-skills-agents-and-mcp

Checked: 2026-11-20 · Method: re-read primary source(s) via WebFetch (S1-S6 are the same URL; the tool returned a paraphrase, not verbatim text, so quotes below are the few short phrases it marked as quotes or near-verbatim)

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| K1 | GitHub just added a way to test Copilot skills and MCP tools (Nov 17, 2026) | supported | S1 | Page dated Nov 17, 2026, "public preview"; covers skills, custom agents and MCP tools. Hook omits agents but is not false. |
| K2 | AI output can change from one run to the next | supported | S3 | Page: output varies between runs. |
| K3 | One good answer does not prove your skill, agent or MCP tool works | supported | S3 | Page: one good answer "doesn't prove a customization works"; skills, agents and MCP are the covered customizations. |
| K4 | An eval is a repeatable test for AI behavior | supported | S2 | Page: "An eval is a repeatable test for AI behavior." |
| K5 | Give an agent a realistic task, describe a good result, check the result and how the agent got there | supported | S2 | Page: realistic task, define good result, check result and the path taken. |
| K6 | Ask Copilot in your own words or use /eval to create an eval | supported | S4 | Page lists both routes; creation is for a skill, custom agent or MCP tool in your project. |
| K7 | Approve each run before it starts, then see which checks passed and failed | supported | S4 | Page: "You approve each run before it starts"; see passed/failed checks. |
| K8 | After changing a skill/agent/MCP tool, rerun the same eval and compare before/after runs | supported | S3, S4 | Page: rerun after a change to catch regressions; compare runs before and after. |
| K9 | Public preview for Copilot Individual, Business and Enterprise plans | supported | S1 | Page: public preview for Copilot Individual, Business and Enterprise plans. No mention of Free or other plans. |
| K10 | Because output varies, repeatable evals are a more reliable check than a single answer | qualified | S2, S3 | Reasonable inference from the page, not a page statement; labeled interpretation, keep it so. |

## Unmapped statements
- On-screen "One good answer proves nothing" — qualified: page says one good answer does not prove a customization works; "proves nothing" is stronger.
- On-screen "Rerun after every change" — qualified: page says rerun after changing a skill/agent/MCP; "every" is stronger than the page.
- On-screen "You approve every run" — supported: page says "each run".
- On-screen "Eval = repeatable AI test", "Task, then good result, then checks", "Ask Copilot, or use /eval", "Public preview" — supported (K4/K5/K6/K9).
- Narration "In Copilot Evals, you ask Copilot..." (framing as the tool's own feature) — supported; page describes these as what you can do with Evals.
- CTA "What would you test first?" — opinion/question, no factual claim.
- Not claimed in script: Vally engine, install routes, local execution — nothing to verify.

## Required corrections
- On-screen: change "One good answer proves nothing" to "One good answer isn't proof".
- On-screen: change "Rerun after every change" to "Rerun after you change a skill".
- Optional: hook could read "skills, agents and MCP tools" to match the page's scope; current wording is not wrong.

## Corrections applied (main session, 2026-11-20)
- On-screen: "One good answer proves nothing" -> "One good answer isn't proof" (script.md, storyboard.json scene 3)
- On-screen: "Rerun after every change" -> "Rerun after you change a skill" (script.md, storyboard.json scene 9)
- Optional hook widening not applied: current wording is accurate and changing it would alter the spoken text.
