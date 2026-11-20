# Fact check: GitHub Copilot Evals (dry run 2 remake)

Primary source re-opened 2026-11-20: https://github.blog/changelog/2026-11-17-github-copilot-evals-is-now-in-public-preview (dated 2026-11-17). S1 to S6 in sources.md are all this one page; each row's quoted claim matches the page.

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| C1 | One good answer does not show a customization works | supported | S3 | Page: a single good result does not show a skill, agent or MCP tool works well. |
| C2 | AI output can change from one run to the next | supported | S3 | Page: output can differ between runs. |
| C3 | Edit passes once, rerun fails (illustrative) | qualified | S3 | Interpretation, not sourced as an event. Only OK if labelled illustrative on screen; scene 8 does, scenes 2 and 3 only partly (see below). |
| C4 | Copilot Evals is a repeatable test for AI behavior | qualified | S1, S2 | Page defines "an eval" as the repeatable test; Copilot Evals is the tool that creates and runs them. Prefer "An eval is a repeatable test". |
| C5 | Step one: give an agent a realistic task and describe a good result | supported | S2 | Matches the definition. The page also says it checks the path the agent took, not only the result (omission, not an error). |
| C6 | Step two: approve the run and see which checks passed and failed | supported | S4 | Page: you approve each run before it starts; review which checks passed and failed. |
| C7 | Step three: change a skill, agent or MCP tool and compare before/after | supported | S4 | Page: compare runs from before and after a customization change. Wording "3 steps" is ours (see corrections). |
| C8 | Rerun the same eval after a change to catch regressions | supported | S3, S4 | Page says exactly this. |
| C9 | Copilot Evals is in public preview | supported | S1 | Page title and body. Plans: Copilot Individual, Business, Enterprise. Narration makes no availability claim beyond "public preview". |
| C10 | How do you know your change helped (central question) | supported | S3 | Framing question, not a factual assertion. Page: compare runs to see whether it helped. |

## Unmapped statements
- "You edit a skill, try it once, and it passes. Rerun it, and it fails." (scene 2/3): covered by C3, interpretation; must be read as hypothetical. Needs on-screen illustrative label where it first appears (scene 2).
- "Copilot Evals is a repeatable test for AI behavior": mapped C4 (qualified, wording).
- "Step one / two / three": the numbered structure is the script's own simplification. The page lists capabilities (create, run and approve, investigate failure, compare), not a three-step procedure; it also omits "investigate a failed check".
- "Tell me below" and "Which skill would you test first?": CTA, no claim.
- Hook: "One good answer doesn't prove your skill works": source-backed (C1). No "most people get this wrong" or invented stat. Framing is acceptable.
- Not claimed, correctly: Vally (S5), install routes (S6), pricing, models.

## On-screen and chart values
No numbers or charts.
- "One good answer isn't proof": OK (C1).
- "AI output varies per run": OK (C2).
- "Did your edit help?": OK (question).
- "Copilot Evals: 3 steps": qualified. Reads as an official three-step flow. Source has no such count.
- "1. Realistic task" / "2. Approve, then check" / "3. Compare before/after": OK (C5 to C7).
- "Illustrative example": OK, present in scene 8; badge persists.
- "Rerun after every change": OK (C8). Source says "after you change" one, so "every" is mild but fair; keep as is.
- "Public preview" chip (scene 9): OK (C9).
- "Which skill first?": CTA.
- Scene 6 visual: "four check rows ... one coral fail" is a made-up mock result with no illustrative label in on_screen_text. Qualified.
- Scene 2 visual: output node changes label across runs, then mint pass; scene 3 "Run 1 / Run 2 (illustrative)" is labelled only in visual_description, not on_screen_text. Qualified.
- Scene 8: "no real numbers", "Illustrative" badge: supported.
- Scene 9 source chip: ensure it names GitHub changelog, 2026-11-17.

## Required corrections
1. Scene 6 on_screen_text or an on-screen chip: add "Illustrative mock" (or similar) so the four rows with one fail are not read as real Copilot output. Scene 6 narration is fine.
2. Scene 3 (and scene 2): make "Illustrative" visible on screen, not only in visual_description, since the pass-then-fail scenario first appears there.
3. Change "Copilot Evals: 3 steps" to something non-official, e.g. "Evals, simplified" or "How an eval works"; and/or narration "Here's the flow" instead of "Step one/two/three" if you want to avoid implying a documented three-step process. Minimum: keep as is only if accepted as our simplification.
4. Narration scene 4: change to "An eval is a repeatable test for AI behavior." (C4).
5. Optional: scene 9 source chip text should read "GitHub changelog, 17 Nov 2026".
No unsupported claims found.

## Corrections applied (main session, 2026-11-20)
- Scene 4 narration "Copilot Evals is a repeatable test..." -> "An eval is a repeatable test for AI behavior." (C4; the source defines an eval, not the product).
- Scene 4 on-screen "Copilot Evals: 3 steps" -> "How an eval works" (the 3-step structure is our simplification, not the source's).
- Scenes 2-3 on-screen now carry "illustrative"; scene 6 result mock labelled Illustrative.
- Scene 9 source chip is generated from sources.md (GitHub, 2026-11-17).
