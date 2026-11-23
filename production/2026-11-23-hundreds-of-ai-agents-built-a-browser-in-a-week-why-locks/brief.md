# Brief: Hundreds of AI agents built a browser in a week: why locks failed

- Video ID: 2026-11-23-hundreds-of-ai-agents-built-a-browser-in-a-week-why-locks
- Language: English
- Bucket: agentic-ai-mcp
- Type: evergreen
- Evidence confidence: medium
- Weighted score: 4.3 / 5 (freshness 4, relevance 5, usefulness 4, evidence 4, visual 5, distinctiveness 4)
- Research file: research/2026-11-23/approved/candidates.json (candidate C06)

## Central idea
Cursor ran hundreds of concurrent coding agents for close to a week on a from-scratch web browser: over 1M lines across 1,000 files. Equal agents sharing a lock file collapsed (20 agents worked like 2-3) and became risk-averse; splitting into planners, workers and a judge agent fixed most coordination problems.

## Why this audience should care
'Agent built a browser in 7 days' Short at ~21K views/day with 22K likes; we add the system-design lesson (coordination, locks, hierarchy) the viral clip skipped.

## Proposed hook (must not mislead)
Twenty AI agents did the work of three. Then one change let them build a browser in a week.

## Visual angle
Robot office world: 20 robots queue at one lock (traffic jam), then a planner robot hands task cards to workers and a judge robot stamps cycles.

## Editorial cautions
- Tension: before->after (flat swarm fails, hierarchy works).
- Worked example: Cursor's own numbers (20 agents ~ throughput of 2-3; 1M+ LoC, 1,000 files, ~1 week).
- Visual metaphor: kitchen with no head chef vs a brigade.
- Vendor-reported results (Jan 2026, not fresh). Reports quote the CEO saying it 'kind of works' - say the browser is a research project, not a usable Chrome rival.
- Do not repeat Cursor's model comparison (GPT-5.2 vs Opus 4.5) as fact - attribute or omit.

## Status (superseded by status.json)
RESEARCHED. Needs topic approval before scripting. Only claims listed in sources.md may be used.

## Owner direction (2026-11-23)
- Approved by owner in chat (C01 + C06). ENGLISH narration only, no Hindi. Cloned voice, best-of-3 takes, 165 wpm floor, no transition SFX.
- Professional structure: COLD-OPEN HOOK (0-2 s) -> short INTRO beat (2-5 s) -> body -> payoff -> OUTRO with CTA.
- Outro CTA: "For more AI concepts like this, follow."

## Hook reference (structure only; never copy wording or visuals)
From velocity_evidence.md row 8 (Brainy Byte, ~21K views/day, 22K likes): frame 0 states the OUTCOME + NUMBER as a headline
over a glowing agent graph; the payoff is promised immediately. Ours goes further: number + paradox ("20 agents, the work of 3").

## Central question
How do you get hundreds of AI agents to build one big thing without getting in each other's way?

## Tension
Before -> after: equal agents sharing one lock file jam (20 agents ~ the throughput of 2-3) and play it safe;
splitting roles into planners, workers and a judge let them run for close to a week on a browser (1M+ lines, ~1,000 files).

## Worked example (from Cursor's own report; attribute it)
Flat swarm with a lock file -> bottleneck and forgotten locks -> optimistic concurrency (better, still churn) -> planners create tasks, workers only finish
tasks, a judge decides whether to continue each cycle.

## Visual metaphor and world
- Metaphor: a kitchen with no head chef (everyone queues for one knife) vs a restaurant brigade.
- World (new): a robot construction site/workshop building a giant browser window; many small robots.
- Opening image: 20 robots jammed at one door marked LOCK. Callback ending: the browser window lights up, with the caption "research project, not a Chrome rival".
- B-roll: motion-text org chart Planner -> Workers -> Judge with Lucide icons (map, hammer, gavel/scale).

## Cautions (extra)
- Vendor-reported; Fortune quotes the CEO saying it "kind of works". Do not repeat Cursor's model-vs-model comparison.
