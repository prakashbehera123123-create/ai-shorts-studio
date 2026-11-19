# AI Shorts Studio — Claude Code Edition

A local-first, human-approved production workflow for two faceless YouTube Shorts per day.

## Design principles
- Claude Code orchestrates; Python/FFmpeg perform deterministic media work.
- Cheap/default models handle routine work. Use a stronger model only for difficult reasoning or final creative arbitration.
- No paid API is required for the initial workflow.
- No public upload happens automatically. Human approval is mandatory.
- Research is source-backed; never fabricate trends, statistics, quotes, or footage rights.
- Start with a vertical-video template and stock/local assets. Do not add a database, web server, queue, or multi-agent framework until there is a demonstrated need.

## 1. Prerequisites (Windows 10/11)
Install:
1. Claude Code (already installed if `claude --version` works).
2. Git for Windows.
3. Python 3.11 or 3.12.
4. FFmpeg (ensure `ffmpeg.exe` is on PATH).
5. Node.js 20+ only if you want Playwright CLI browser research.

Verify in PowerShell:
```powershell
claude --version
git --version
python --version
ffmpeg -version
node --version
```
Node is optional. Python + FFmpeg are enough for the first milestone.

## 2. Create the project
Extract this ZIP to a development folder, for example `D:\Projects\ai-shorts-studio`.
Open PowerShell in that folder:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
git init
git add .
git commit -m "chore: initialize AI Shorts Studio"
claude
```
If PowerShell blocks activation, use:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Only do this for your current Windows user. Alternatively run `.venv\Scripts\python.exe` directly.

## 3. First Claude Code session
Inside Claude Code, run:
```text
/init
```
Review the generated CLAUDE.md; preserve the project rules in this kit. Then ask:
```text
Read CLAUDE.md and docs/SETUP.md. Inspect the repository, verify the local tools,
and implement only Milestone 1 from docs/BUILD_PLAN.md. Do not add paid APIs,
cloud services, a database, or a web backend. Run the tests and report exact
commands and any missing prerequisites.
```

## 4. Daily production
Once Milestones 1–4 work, use:
```text
/produce-daily-shorts
```
Claude should research a shortlist, select two distinct topics, prepare scripts and storyboards, produce local assets/render drafts, run QA, and stop at `READY_FOR_HUMAN_REVIEW`. It must not publish.

Useful commands:
- `/research-topics` — research and score a topic shortlist.
- `/produce-short` — produce one approved topic.
- `/review-short` — review a rendered video and production metadata.
- `/produce-daily-shorts` — orchestrate the daily two-video batch.

## 5. Browser research
Preferred low-context option: Playwright CLI (not a huge always-on MCP toolset).
Install after Node.js 20+:
```powershell
npm install -g @playwright/cli
playwright-cli --version
playwright-cli install
```
If the package command differs on your machine, consult the current Playwright CLI docs. Claude can also use its configured web-search/browser tools if available. Browser automation is optional: do not make the pipeline depend on scraping websites that block automation.

Use browser automation for public pages and research only. Respect robots.txt, site terms, rate limits, copyright, paywalls, and personal-data restrictions. Prefer official blogs, release notes, RSS feeds, public datasets, and direct source pages. Do not scrape YouTube comments or private/social accounts.

## 6. GitHub
Optional but recommended:
```powershell
gh --version
gh auth login
```
Create a private repository:
```powershell
gh repo create ai-shorts-studio --private --source . --remote origin --push
```
Do not commit `.env`, API keys, cookies, OAuth tokens, raw personal files, or large video assets. Keep rendered media out of Git; use `.gitignore`.

## 7. Human workflow
- You approve topics before production if the research shortlist is weak.
- You review every final MP4 and metadata package.
- You manually upload in YouTube Studio.
- Only consider YouTube API upload after a separate OAuth/security review and explicit approval.

## 8. Cost expectations
The target is ₹0 incremental spend, not guaranteed zero cost under every configuration. Claude Code usage is subject to your plan's usage limits. Free stock media, local TTS, Python and FFmpeg have their own license/usage conditions. Paid image/video/voice APIs are deliberately excluded.

## 9. Troubleshooting
- `ffmpeg not recognized`: install FFmpeg and add its `bin` directory to PATH; reopen PowerShell.
- `python not found`: use `py -3.11`; verify `py --list`.
- Claude consumes too much context: ask it to inspect only named files, use the skills, return concise status, avoid loading raw video/binary files, and delegate only independent bounded tasks.
- Research sources unavailable: return a source-gap report; do not invent claims.
- Rendering fails: inspect `logs/render.log`, run the exact FFmpeg command manually, and fix the deterministic script before retrying.

See `docs/SETUP.md`, `docs/MODEL_ROUTING.md`, and `docs/BUILD_PLAN.md`.
