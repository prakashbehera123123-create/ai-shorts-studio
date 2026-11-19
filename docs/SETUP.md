# Setup and tool map

## Where to do what
| Work | Where | Why |
|---|---|---|
| Orchestration, planning, coding | Claude Code in this repository | Persistent project rules, local scripts, subagents |
| Web research | Claude Code web/search capability or Playwright CLI | Research public sources; no blanket scraping |
| Browser automation | Playwright CLI, invoked by Claude Code | Lower context overhead than a large browser MCP surface for many coding-agent tasks |
| Media processing | PowerShell + Python + FFmpeg | Deterministic local processing |
| Visual finishing | CapCut (optional) | Human polish, not a pipeline dependency |
| Source control | Git + private GitHub repo | Versioning and backup |
| Publishing | YouTube Studio manually | Human approval gate |

## Minimum install sequence
1. Git for Windows
2. Python 3.11/3.12
3. FFmpeg
4. Claude Code
5. Optional: Node.js 20+ and Playwright CLI
6. Optional: GitHub CLI (`gh`)

Avoid installing every MCP server at the beginning. MCP tools increase context and permission surface. Add one only when a real repeated workflow needs it.

## Recommended browser approach
Use Playwright CLI for agent browser tasks where supported. It is designed for coding agents and can be more token-efficient than a broad MCP tool schema. Use official documentation for current installation syntax. Do not scrape sites indiscriminately.

## Optional MCP integrations, in order
1. GitHub MCP or `gh` CLI: repository operations. CLI is enough for initial setup.
2. Browser/Playwright: only if built-in search is insufficient.
3. Google Drive: only if source assets live there and you need repeated access.
4. YouTube integration: defer; publishing remains manual.

Never install an unknown MCP server from an untrusted repository. Review its source, permissions, transport, and data handling. Prefer official/vendor-maintained integrations.

## Node.js role
Node is not needed for the first render pipeline. Add it for Playwright CLI or a future Remotion-based motion-graphics renderer. Do not introduce Remotion until FFmpeg templates prove insufficient.

## Local TTS strategy
Start with a manual voiceover or an offline TTS engine after evaluating voice quality and license. A local engine may sound less natural than commercial TTS. Keep the script and voiceover separate so the narration can be replaced without changing the storyboard.
