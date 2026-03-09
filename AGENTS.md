# Repository Guidelines

## Project Structure & Module Organization

This repository is documentation-first. Root files `01-architecture.md` through `11-troubleshooting.md` are the main reference set, and `INDEX.md` is the entry point for navigation. Reusable agent templates live in `examples/` (for example `examples/coder-agent/` and `examples/momo-agent/`). Reusable OpenClaw skills live in `skills/`, each in its own folder with a `SKILL.md`. Automation is intentionally small: `scripts/create_agent.py` is the primary helper script. Treat `log/` as runtime output, not source.

## Build, Test, and Development Commands

There is no full build pipeline in this repo. Use small, targeted checks:

- `python3 scripts/create_agent.py --help` — verify the CLI entrypoint and arguments.
- `python3 -m py_compile scripts/create_agent.py` — catch Python syntax errors.
- `python3 scripts/create_agent.py --agent-id demo --preset coder --workspace-base /tmp/fma --skip-chat --skip-config` — smoke-test template generation without Feishu or config writes.
- `grep -R "old text" --include="*.md" .` — locate related docs before editing cross-file terminology.

## Coding Style & Naming Conventions

Follow the existing style instead of introducing new patterns. Python uses 4-space indentation, `snake_case`, and straightforward standard-library code. Markdown files use concise sections, explicit paths, and command examples. Keep numbered root docs in the current `NN-topic.md` format. Preserve the language of the surrounding file; most root docs and templates are Chinese.

## Testing Guidelines

This repo does not currently ship a formal test suite. Validate the smallest affected surface: syntax-check Python changes, smoke-test `create_agent.py` for script changes, and manually verify links, paths, and examples for Markdown changes. When changing templates or presets, test both a template-backed preset such as `coder` and a generated preset path.

## Commit & Pull Request Guidelines

Recent history follows Conventional Commit prefixes such as `feat:` and `fix:`. Keep commits focused and descriptive, for example `docs: clarify agent template setup`. PRs should explain the user-facing impact, list touched docs/examples/skills, and include sample commands or screenshots when behavior or rendered content changes.

## Security & Configuration Tips

Redact all secrets and identifiers. Never commit real `appId`, `appSecret`, Feishu chat IDs, personal paths, or internal model names. Use placeholders such as `<APP_ID>`, `<provider/model_id>`, and `/path/to/.openclaw/...`. Keep examples generic and reusable for external OpenClaw users.
