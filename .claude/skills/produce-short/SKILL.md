---
name: produce-short
description: Orchestrate one Short from an approved topic — select the specialist skills and visual complexity, validate research before scripting and scripts before rendering, coordinate creative and technical QA, stop at READY_FOR_HUMAN_REVIEW.
---

# Produce one Short (orchestrator)

## Purpose
The main session's procedure for a single APPROVED_TOPIC folder. It decides which specialist skills to use and in what order,
and enforces the gates. Standards: `docs/CREATIVE_PRODUCTION_STANDARD.md`; pre-render checklist: `templates/production-readiness-checklist.md`.

## Inputs
- `production/<id>/` at APPROVED_TOPIC with `brief.md` (tension, example, metaphor) and `sources.md`
- `config/render.json`, channel config

## Workflow
1. **Validate research:** brief has tension + worked example + metaphor and every needed claim is in `sources.md`. If not → back to research-topics.
2. **Story:** story-architecture → `script.md`. Fact-checker audits; apply corrections; `python -m studio script` clean.
3. **Visual plan:** visual-direction → schema-v2 `storyboard.json`. Decide per scene: kinetic type / 2D diagram / chart / UI mock /
   2.5D / 3D (3D only with justification and tooling). Status → SCRIPT_READY (gate checks script, storyboard, fact check).
4. **Readiness review:** walk `templates/production-readiness-checklist.md`; every item must be ticked or explicitly waived.
5. **Voice and sound:** voice-and-sound (pronunciations, direction, music licence).
6. **Assets:** motion-graphics for 2D scenes; depth-and-3d **only if** the storyboard has a `scene_3d` scene that passed
   its gate (build `assets/3d/scene_NN/` from `templates/scene3d/`, check + snapshot; render picks it up automatically); manifest row per asset → ASSETS_READY.
7. **Edit:** shortform-editing → `render/draft.mp4` → RENDERED.
8. **QA:** `python -m studio metadata`, `python -m studio qa`, then review-short (creative rubric) → QA_PASSED → READY_FOR_HUMAN_REVIEW.

## Tools
`python -m studio {script,render,metadata,qa,status,validate}`; subagents: scriptwriter (sonnet), fact-checker (sonnet),
video-reviewer (sonnet), research-analyst (sonnet). Parallelise only across different videos, never inside one video's chain.

## Decision rules
- Complexity follows information: use the least complex visual that shows the sentence (standard §5).
- Voice and visuals must tell the same story; when they disagree, the script wins and visuals change.
- Fix blockers once and re-run QA; if they persist, stop and report rather than looping.
- Opus only with a written escalation reason (`docs/MODEL_ROUTING.md`).

## Outputs
A complete production folder (`brief.md`, `script.md`, `sources.md`, `fact_check.md`, `storyboard.json`, `assets/manifest.csv`,
`metadata.md`, `qa_report.md`, `qa/`, `render/`, `status.json`) at READY_FOR_HUMAN_REVIEW.

## Quality checklist
- [ ] Research validated before scripting; script validated before rendering
- [ ] Readiness checklist complete
- [ ] Technical QA PASS and creative rubric pass
- [ ] Status history shows every gate; never PUBLISHED

## Failure handling
- Missing tool (e.g. motion renderer, neural TTS) → use the documented fallback in that skill and record the downgrade in `qa_report.md`.
- Gate refuses a status → fix the listed problems; never edit `status.json` by hand.
Never publish, schedule or upload anything; a person uploads manually after review.
