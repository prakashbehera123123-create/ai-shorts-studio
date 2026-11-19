# AI Shorts Studio — Project Operating Rules

## Mission
Produce up to two high-quality, faceless, vertical YouTube Shorts per day in AI engineering, Agentic AI, practical AI tools/experiments, and relevant technology developments. One language per video: English OR Hinglish. Do not randomly mix languages.

## Non-negotiable rules
1. Never publish, schedule, delete, or modify a public YouTube video. Prepare deliverables and stop for explicit human approval.
2. Never fabricate sources, dates, product capabilities, statistics, quotes, benchmark results, or licensing rights.
3. For news/current claims, cite primary sources first (official release notes, docs, papers, company announcements); use reputable secondary sources for context.
4. Store source URL, publisher, publication date (if available), access date, claim supported, and confidence in `sources.md`.
5. Distinguish confirmed facts, interpretation, and speculation. Avoid presenting speculation as fact.
6. Do not download copyrighted video/audio from YouTube or other platforms without permission. Use self-created visuals, properly licensed assets, or user-provided assets. Record asset source and license.
7. Respect robots.txt, site terms, rate limits, privacy, and paywalls. Do not bypass anti-bot controls or authentication.
8. No paid API calls, cloud infrastructure, database, or external upload without explicit approval.
9. Do not expose secrets. Never read or print `.env` values. Never commit credentials.
10. Do not inspect large raw media files by loading them into the model. Use FFprobe/metadata, sampled frames, audio transcription, and short targeted excerpts.

## Model routing policy
- Routine classification, formatting, metadata, simple QA: Haiku-class model.
- Research synthesis, scripts, storyboards, asset planning, ordinary code: Sonnet-class model.
- Complex architecture, persistent debugging after a failed Sonnet attempt, high-stakes factual synthesis, final difficult creative arbitration: Opus-class model only when explicitly justified.
- Never default every subagent to Opus. Use model aliases (`haiku`, `sonnet`, `opus`) supported by the installed Claude Code version; do not hardcode dated model version strings in repository configuration.
- Main session should normally use Sonnet. Use Haiku for bounded low-risk tasks. Escalate only with a concise reason.
- Keep agent outputs compact: deliver structured artifacts, not long narrative explanations. Avoid duplicate research across agents.

## Token efficiency
- Read only relevant files. Use `find`/`grep` and metadata before opening large files.
- Do not re-read all of `CLAUDE.md` or the whole repository every task.
- Delegate only independent tasks with clear input/output contracts.
- Use at most 3 parallel research/review agents for a daily batch.
- Do not ask multiple agents to do the same research.
- Keep research briefs to 8–12 candidate topics; final selection to 2.
- Keep each script around 100–160 spoken words unless the target runtime requires otherwise.
- Store long-lived context in files; return concise summaries with file paths.
- Do not generate multiple variants unless requested or a decision is genuinely uncertain.

## Production target
- 9:16 vertical, 1080x1920 target, H.264 MP4, AAC audio.
- Target 25–55 seconds by default; validate actual duration and readability.
- Strong first 1–2 second hook; one central idea; clear payoff; one natural CTA.
- Captions readable on mobile, safe margins, no tiny text.
- Voice and visuals must support the same narrative.
- Avoid generic AI hype, exaggerated claims, misleading hooks, and repetitive templates.

## Daily batch workflow
1. Research 8–12 candidate topics with primary sources.
2. Score: relevance to audience, freshness, usefulness, evidence quality, visual potential, distinctiveness.
3. Select two topics that are not near-duplicates. If evidence is weak, return fewer topics and ask.
4. Draft scripts and source notes. Fact-check every concrete claim.
5. Build storyboard and asset manifest. Label each scene as generated graphic, self-created screen capture, licensed stock, or user asset.
6. Generate voice and captions using available local tools. If no suitable local TTS is configured, create a narration script and stop for user-recorded voice; do not silently substitute paid services.
7. Render draft using local scripts and FFmpeg.
8. Run technical and editorial QA.
9. Write a review report and mark `READY_FOR_HUMAN_REVIEW`. Never publish.

## File contracts
Every production folder must contain:
- `brief.md`
- `script.md`
- `sources.md`
- `storyboard.json`
- `assets/manifest.csv`
- `metadata.md`
- `qa_report.md`
- `render/` (draft MP4 when rendering prerequisites exist)
- `status.json`

## Status lifecycle
`RESEARCHED` -> `APPROVED_TOPIC` -> `SCRIPT_READY` -> `ASSETS_READY` -> `RENDERED` -> `QA_PASSED` -> `READY_FOR_HUMAN_REVIEW`.
No status named `PUBLISHED` may be set by this project.

## Safety and approvals
Ask before installing software, enabling new MCP servers, authenticating a service, creating a public repository, uploading assets, or taking external side effects. Use private GitHub repos by default. Do not interact with YouTube Studio except read-only metadata if explicitly requested.
