# Model routing and token budget

## Principle
Model choice should follow task difficulty, not prestige. Use aliases supported by the installed Claude Code version rather than freezing a dated model ID in the project.

## Routing matrix
| Task | Suggested model class | Effort | Reason |
|---|---|---|---|
| File naming, metadata, CSV cleanup, simple classification | Haiku | Low/default | Low ambiguity |
| Topic shortlist extraction and deduplication | Haiku, then Sonnet for synthesis | Low/default | Cheap filtering, stronger final judgment |
| Research synthesis with sources | Sonnet | Default/medium | Balance of evidence handling and cost |
| Scriptwriting/storyboard | Sonnet | Default/medium | Creative quality without routine Opus use |
| Python/FFmpeg implementation | Sonnet | Default/medium | Coding and test iteration |
| Captions and metadata formatting | Haiku | Low/default | Structured transformation |
| Editorial QA and factual conflict resolution | Sonnet | Medium | Needs judgment |
| Reference-video analysis synthesis, creative direction, skill development | Sonnet | Default/medium | Creative judgment from sampled evidence |

Current agent assignments (2026-11-20): research-analyst, scriptwriter, fact-checker, video-reviewer all `sonnet`.
research-analyst moved from `haiku` to `sonnet` because candidates now need story judgement (tension, worked example,
metaphor) and the dry-run review found research quality was a main gap. Use Haiku for bounded transforms (metadata,
CSV/JSON clean-up, simple classification) invoked ad hoc, not as a standing agent.
| Architecture redesign or persistent hard bug | Opus, only after escalation | High if needed | Reserve for genuinely difficult cases |

## Practical Claude Code controls
- Start with `/model` and select Sonnet (or the current Sonnet alias shown by your installed CLI).
- Use `/effort` if your version exposes it; keep the default for routine work.
- Subagents can declare `model: haiku` or `model: sonnet` in their frontmatter. Use `model: opus` only for a rare escalation agent.
- Do not hardcode a model version such as an old Opus 5.5 identifier. Anthropic changes available model names and aliases; verify the current options in `/model` or the official Claude Code docs.
- If the selected model is not available on your account, use the current alias exposed by Claude Code.

## Token-saving operating rules
1. Keep `CLAUDE.md` short and stable.
2. Put long workflow instructions in skills; they load when invoked.
3. Ask agents to return JSON/short Markdown with exact file paths.
4. Do not pass full research to every agent. Pass the selected 2–3 source excerpts/URLs.
5. Do not attach full videos. Use `ffprobe`, waveform, transcript, and sampled frames.
6. Run scripts/tests locally rather than asking the model to mentally simulate them.
7. Use one research pass, one script pass, one fact-check pass, one render pass, one QA pass.
8. Limit parallel agents to independent work; parallelism can multiply context use.
9. Do not repeatedly ask Opus to rewrite the same script. Use one Sonnet draft and one targeted revision.
10. Treat Claude Code plan usage as a budget; avoid unattended loops and repeated retries.

## Escalation rule
Escalate from Haiku to Sonnet when output is ambiguous, incomplete, or requires synthesis. Escalate from Sonnet to Opus only if:
- two focused Sonnet attempts fail on the same complex issue, OR
- conflicting primary sources materially affect a factual claim, OR
- an architecture/security decision has significant consequences.

Record the escalation reason in the task summary.
