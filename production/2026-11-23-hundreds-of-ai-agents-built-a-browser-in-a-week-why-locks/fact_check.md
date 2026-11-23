# Fact check

Sources re-opened 2026-11-23: S1 Cursor blog (2026-01-14), S2 Fortune (2026-01-23).

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| C1 | 20 agents ~ throughput of 2-3 | qualified | S1 | Source says "two or three". Hook and on-screen "did the work of three" / "= 3" overstated; fixed to "worked like two or three" and "20 agents ~ 2-3". |
| C2 | Equal agents + lock file; locks held too long or forgotten; risk-averse | supported | S1 | "Cursor says" attribution kept. |
| C3 | Optimistic concurrency better, still churn | qualified | S1 | Source: "simpler and more robust, but deeper problems"; churn is tied to the flat structure, not OCC. Reworded to "Simpler, but deeper problems remained". |
| C4 | Planners create tasks, workers finish, judge decides each cycle | supported | S1 | Judge decides whether to continue; added "whether to continue". |
| C5 | Close to a week, over 1M lines, ~1,000 files | supported | S1 | Matches "close to a week", "over 1 million lines ... 1,000 files". "Hundreds of agents" is not claimed in narration. |
| C6 | Research project; CEO "kind of works"; not a Chrome rival | qualified | S1, S2 | "kind of works" is from CEO Michael Truell (Fortune): supported. "Research project" phrase not in S1, changed to "experiment". Chrome remark was by Cursor engineer Jonas Nelle ("wouldn't download it and delete Chrome today"); narration now attributes it. |
| C7 | Structure beats more agents | supported | S1 | Interpretation, labelled as the lesson drawn from the report. |
| C8 | Visual metaphors (robots, LOCK door) | supported | S1 | Interpretation only; no factual claim. |

## Unmapped statements
- "Then one change built a browser in a week": overstated (not a single change; "close to a week"). Fixed to "Then new roles helped build a browser in about a week."
- "A browser from scratch": supported by S1.
- "Agents played it safe": supported (risk-averse).

## On-screen and chart values
- "20 agents = 3": corrected to "20 agents ~ 2-3".
- "One change. One week.": corrected to "New roles. ~1 week."
- "Attempt 2: better, still churn": corrected to "Attempt 2: simpler, deeper problems".
- "~1 week · 1M+ lines · ~1,000 files": supported.
- "Research project, not a Chrome rival": corrected to "Experiment, not a Chrome swap".
- Source chip dates correct. No charts, no toy numbers. No model comparison; no production-ready claim.

## Required corrections
All applied to script.md and storyboard.json (wording only). Residual: storyboard tag "one change" in lines ~73/86 is a visual tag; confirm it is not rendered text.

## Orchestrator follow-up (2026-11-23)
- Removed the Cursor-engineer Chrome remark: it was not recorded in sources.md (seen only via Fortune), so it was dropped instead of adding a thin source. On-screen text is now: An experiment that "kind of works" (S2).
- 2026-11-23 voice fix: scene 2 reworded "new roles" -> "a clear team structure" (the clone said "rules" in all 3 takes); same claim (S1: roles/hierarchy). Scene 1 uses take 2 (clean "Twenty AI agents..."); original take 0 kept in voiceover/replaced_takes/.
