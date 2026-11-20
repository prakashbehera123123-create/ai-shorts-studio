# Script: GitHub Copilot Evals

Language: English
Target duration: 48s

Central question: How do you know a change to your skill, agent or MCP tool actually helped?
Payoff: Rerun the same eval after every change and compare the runs. Caveat: public preview.
Running example (illustrative): a skill edit passes once by hand, but a rerun shows a failed check.
Visual motif: the signal trace. One task goes through the agent twice; the first trace ends in a green check, the rerun forks to a red one.

## Hook candidates
1. "One good answer doesn't prove your skill works." | pattern: broken belief | curiosity 4, specificity 4, honesty 5
2. "Your agent passed yesterday. Today the same task fails." | pattern: consequence | curiosity 5, specificity 3, honesty 3 (yesterday/today is invented, not sourced)
3. "Same task, same agent, different result. Which run do you trust?" | pattern: paradox demo | curiosity 4, specificity 3, honesty 4
Chosen: 1 (broken belief, directly supported by S3).

## Beats
| beat | seconds | content |
|---|---|---|
| hook | 0-3 | One good answer is not proof |
| tension | 3-15 | Output varies run to run; edit passes once, rerun fails; how do you know it helped? (obstacle) |
| explanation | 15-33 | Copilot Evals = repeatable test; 3 steps: task + good result, approve and see checks, compare before/after |
| example | 33-38 | Illustrative: edit passed by hand, rerun shows a failed check |
| payoff | 38-44 | Rerun the same eval after every change, compare runs; public preview |
| cta | 44-48 | Which skill would you test first? |

## Hook
One good answer doesn't prove your skill works.

## Narration
AI output can change from one run to the next. You edit a skill, try it once, and it passes. Rerun it, and it fails. So how do you know your change helped? An eval is a repeatable test for AI behavior. Step one: give an agent a realistic task, and describe a good result. Step two: approve the run and see which checks passed and failed. Step three: change your skill, agent or MCP tool, and compare before and after. Illustrative: your edit passed by hand, but the rerun shows a failed check. So rerun the same eval after every change, and compare the runs. It's in public preview.

## On-screen text
- One good answer isn't proof
- Varies per run (illustrative)
- Illustrative: did it help?
- How an eval works
- 1. Realistic task
- 2. Approve, then check
- 3. Compare before/after
- Illustrative example
- Rerun after every change
- Which skill first?

## CTA
Which skill would you test first? Tell me below.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| C1 | One good answer does not show a customization works | S3 | fact |
| C2 | AI output can change from one run to the next | S3 | fact |
| C3 | You edit a skill, try it once, it passes; rerun fails (worked example, labelled illustrative on screen) | S3 | interpretation |
| C4 | An eval is a repeatable test for AI behavior (Copilot Evals lets you create and run evals) | S1, S2 | fact |
| C5 | Step one: give an agent a realistic task and describe a good result | S2 | fact |
| C6 | Step two: approve the run and see which checks passed and failed | S4 | fact |
| C7 | Step three: change a skill, agent or MCP tool and compare runs from before and after | S4 | fact |
| C8 | Rerun the same eval after changing a skill, agent or MCP to catch regressions | S3, S4 | fact |
| C9 | Copilot Evals is in public preview | S1 | fact |
| C10 | How do you know your change helped (central question) | S3 | interpretation |
