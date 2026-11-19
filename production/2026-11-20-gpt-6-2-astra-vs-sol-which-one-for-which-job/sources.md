# Sources

Confidence: high / medium / low. Mark each claim as fact, interpretation, or speculation in script.md.
All rows verified by reading the page in the Claude Code browser pane on 2026-11-20.

SOURCE CONFLICT (do not resolve in the script): OpenAI (S1) positions Astra for "demanding reasoning and coding tasks" and Sol for "everyday coding and agent workflows". GitHub (S5) describes Astra as for "agentic coding and terminal work" and Sol for "complex agentic coding and in-depth code review". Do not claim either model is the heavier/better one. If positioning is mentioned, attribute it to OpenAI.

| id | url | publisher | published | accessed | claim supported | type | confidence |
|---|---|---|---|---|---|---|---|
| S1 | https://developers.openai.com/api/docs/changelog | OpenAI (API changelog, entry "Nov 17") | 2026-11-17 | 2026-11-20 | OpenAI says: use GPT-6.2 Astra for demanding reasoning and coding tasks, or GPT-6.2 Sol for everyday coding and agent workflows. | primary | high |
| S2 | https://developers.openai.com/api/docs/changelog | OpenAI (API changelog, entry "Nov 17") | 2026-11-17 | 2026-11-20 | Both models support the Responses API and Chat Completions. Tool calling requires the Responses API. | primary | high |
| S3 | https://developers.openai.com/api/docs/changelog | OpenAI (API changelog, entry "Nov 17") | 2026-11-17 | 2026-11-20 | GPT-6.2 changes how the Responses API preserves reasoning when you edit a conversation's prefix, and how it handles the top-level instructions field; OpenAI points to a GPT-6.2 migration guide for recommended integration updates. | primary | high |
| S4 | https://github.blog/changelog/2026-11-17-openais-gpt-6-2-astra-and-gpt-6-2-sol-now-available | GitHub (changelog) | 2026-11-17 | 2026-11-20 | GPT-6.2 Astra and GPT-6.2 Sol are generally available in GitHub Copilot for Copilot Pro+, Max, Business and Enterprise users; rollout is gradual. | primary | high |
| S5 | https://github.blog/changelog/2026-11-17-openais-gpt-6-2-astra-and-gpt-6-2-sol-now-available | GitHub (changelog) | 2026-11-17 | 2026-11-20 | GitHub describes Astra as for agentic coding and terminal work and Sol for complex agentic coding and in-depth code review; GitHub says that in early testing both caught significantly more real issues in code review than earlier GPT-6 models. | primary | medium |
