---
name: story-architecture
description: Turn an approved, sourced topic into a retention-focused beat sheet and script — hook candidates, one central question, numbered mechanism, worked example, payoff and CTA.
---

# Story architecture

## Purpose
Use after a topic is APPROVED_TOPIC and before storyboarding. Replaces "feature walk-through" scripts with a story that
opens a question in ≤3 s and pays it off. Standards: `docs/CREATIVE_PRODUCTION_STANDARD.md` §2–3.

## Inputs
- `brief.md` (must contain paradox/tension, worked example, visual metaphor — see research-topics)
- `sources.md` (the only allowed evidence)
- Target language (English or Hinglish, never mixed) and target length (35–55 s)

## Workflow
1. Write the **central question** in one line; write the **payoff** in one line. If either cannot be sourced, stop and report.
2. Pick a hook pattern from standard §2.2. Write **three** hook candidates (≤ 14 words, spoken in ≤ 3 s).
   Score each 1–5 for curiosity, specificity, honesty; keep the best; record all three in `script.md` under `## Hook candidates`.
3. Beat sheet (in `script.md`, `## Beats`): hook → context/tension → explanation (1–3 numbered steps) → example → (reveal) → payoff → CTA,
   with target seconds per beat. Name the obstacle/failure before the fix.
4. Choose **one running example** and **one visual motif** (default: the signal trace) and note them.
5. Write narration per beat: sentences ≤ 14 words, jargon defined at first use, 120–145 words total.
6. Map every concrete claim (spoken or on-screen) in `## Claim-to-source map`; label toy numbers *illustrative*.
7. Run `python -m studio script <folder>`; fix all errors (fact check comes later).

## Tools
Text editing only; `python -m studio script` for word count, runtime, number mapping and language checks.

## Decision rules
- Prefer a mechanism ("how/why does it work") over an announcement; an announcement must change what the viewer does.
- If there is no real tension in the sources, use the black-box pattern rather than inventing drama.
- Write for the cloned voice: avoid tongue-twister clusters and rare verbs (2026-11-20: "Poll less often", "mints",
  "retries" were slurred and failed recall; "Wait longer between checks", "creates", "sends again" passed). Never speak raw
  identifiers or flags — show them on screen.
- Never claim "most people/engineers get this wrong" without a source.
- Hinglish: Hindi grammar with English technical terms, romanised; keep the same register for the whole video.

## Outputs
`script.md` with: Language, Target duration, `## Hook candidates`, `## Beats`, `## Hook`, `## Narration`, `## On-screen text`, `## CTA`,
`## Claim-to-source map` (layout the script checker parses).

## Quality checklist
- [ ] Hook ≤ 3 s, uses an approved pattern, no banned opener
- [ ] Central question stated in hook, answered in payoff
- [ ] One running example; obstacle before solution; caveat if sourced
- [ ] Every number mapped; toy numbers marked illustrative
- [ ] 120–145 words; one language; `python -m studio script` clean

## Failure handling
- Sources too thin for a payoff → return to research-topics with a "needs evidence" note; do not pad.
- Script too long → cut the weakest step, not the example or payoff.
- Hook only works with exaggeration → use the black-box pattern.
