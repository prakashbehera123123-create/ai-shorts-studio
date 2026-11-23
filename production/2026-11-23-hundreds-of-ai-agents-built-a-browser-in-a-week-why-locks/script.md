# Script: Hundreds of AI agents built a browser in a week: why locks failed

Language: English
Target duration: 48s
Central question: How do hundreds of AI agents build one big thing without getting in each other's way?
Payoff: Structure beats more agents: planners create tasks, workers finish them, a judge decides each cycle.
Running example: Cursor's browser experiment (reported by Cursor).
Visual motif: the LOCK door, jammed at frame 0, open at the end.
Voice: owner's cloned voice, English, energetic, short sentences.

## Hook candidates
1. "Twenty AI agents worked like two or three." | pattern: paradox + number | curiosity 5, specificity 5, honesty 4
2. "How do hundreds of AI agents build one thing without colliding?" | pattern: question | curiosity 4, specificity 3, honesty 5
3. "One lock file nearly sank Cursor's agent swarm." | pattern: stakes | curiosity 3, specificity 4, honesty 3 (overstates "nearly sank")
Chosen: 1, followed by "Then one change let them build a browser in a week. " as the intro question.

## Beats
| beat | seconds | content |
|---|---|---|
| hook | 0-2.5 | 20 robots jammed at LOCK; "did the work of three" |
| context | 2.5-6 | one change, one week; question |
| explanation | 6-13 | attempt 1: equal agents + shared lock file, forgotten locks |
| explanation | 13-17 | 20 agents ~ 2-3, risk-averse |
| explanation | 17-21 | attempt 2: optimistic concurrency, better, still churn |
| explanation | 21-29 | fix: planners, workers, judge (B-roll org chart) |
| example | 29-35 | result: ~1 week, 1M+ lines, ~1,000 files (Cursor reports) |
| caveat | 35-40 | research project, CEO "kind of works", an experiment |
| payoff | 40-43 | structure beats more agents (B-roll) |
| cta | 43-48 | outro, door now open |

## Hook
Twenty AI agents worked like two or three.

## Narration
Then a clear team structure helped build a browser in about a week. Cursor says it began with equal agents and one shared lock file. Agents held locks too long, or forgot them. So twenty agents moved like two or three. They played it safe. Next: optimistic concurrency. Simpler, but flawed. The fix: roles. Planners create tasks. Workers only finish them. A judge decides each cycle whether to continue. Cursor reports close to a week, over a million lines, about a thousand files. A browser from scratch. It's an experiment. Cursor's CEO said it kind of works. Lesson: structure beats more agents.

## On-screen text
- 20 agents ~ 2-3
- Structure. ~1 week.
- Equal agents + lock file
- 20 agents ~ 2-3
- Attempt 2: simpler, deeper problems
- Planner > Workers > Judge
- ~1 week · 1M+ lines · ~1,000 files
- An experiment that "kind of works"
- Structure > more agents
- Follow for more AI concepts
- Source chip: Source: Cursor blog (Jan 2026), Fortune (Jan 2026)

## CTA
For more AI concepts like this, follow.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| C1 | Twenty agents achieved the throughput of about two to three (lock-file coordination bottleneck); vendor-reported, attributed to Cursor | S1 | fact |
| C2 | First attempt: equal agents sharing a lock file; locks held too long or forgotten; agents became risk-averse | S1 | fact |
| C3 | Second attempt: optimistic concurrency was better but still had churn | S1 | fact |
| C4 | Fix: planners create tasks, workers only complete tasks, a judge decides whether to continue each cycle | S1 | fact |
| C5 | Result: browser from scratch, close to a week, over a million lines, about 1,000 files | S1 | fact |
| C6 | (fact: CEO quote; interpretation: not a rival) It is a research project; Cursor's CEO said it "kind of works"; an experiment | S1, S2 | fact |
| C7 | "Structure beats more agents" is the lesson drawn from the report | S1 | interpretation |
| C8 | Robot construction site, LOCK door, scaffolding and icons are visual metaphors | S1 | interpretation |
