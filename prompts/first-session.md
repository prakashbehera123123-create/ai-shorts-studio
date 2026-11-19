# First session prompt

Read CLAUDE.md and docs/SETUP.md. Do not build the entire system in one pass.
1. Inspect the current environment using `python scripts/check_environment.py`.
2. Identify missing required prerequisites and give exact Windows installation steps.
3. Inspect the project contracts and run `pytest -q`.
4. Implement only the next incomplete milestone in docs/BUILD_PLAN.md.
5. Keep the implementation minimal, modular, typed where useful, and tested.
6. Use Sonnet for implementation; use Haiku for simple file/metadata tasks. Do not use Opus unless you can state a concrete escalation reason.
7. Do not add paid APIs, cloud services, a database, a web backend, or auto-publishing.
8. Summarize changed files, tests, commands, remaining work, and estimated next step in under 20 bullets.
