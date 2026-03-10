# Repository Guidelines

## Project Structure & Module Organization

This repository is a root OpenClaw skill. `SKILL.md` is the entrypoint, `INDEX.md` is the reading map, and `01-11` documents define the研发规范 workflow. `scripts/` contains helper scripts used for minimal verification. `examples/` and `skills/` are kept as compatibility references and are not the primary entry path.

## Build, Test, and Development Commands

- `python3 -m py_compile scripts/create_agent.py` — syntax-check the bundled helper script.
- `python3 -m json.tool examples/openclaw-config.json` — validate the example JSON file.
- `git diff --stat` — review change scope before handoff.
- `git status --short` — confirm staged and unstaged changes.

Run the smallest relevant validation first, then expand only if needed.

## Coding Style & Naming Conventions

Keep changes minimal and consistent with existing repository style. Markdown should be concise, procedural, and explicit about file paths and commands. Python uses 4-space indentation and `snake_case`. Do not add new dependencies unless explicitly requested.

## Testing Guidelines

This repo is documentation-heavy, so validation is mostly command-based. For doc changes, verify internal consistency and command accuracy. For script changes, run syntax checks and the smallest realistic smoke test. If a task spans more than 5 files or changes structure, create `IMPLEMENTATION_PLAN.md` during execution and delete it when done.

## Commit & Pull Request Guidelines

Use focused commits with the repository’s emoji style, for example `♻️ 收敛 Skill 定位并同步流程文档`. Keep each commit to one logical change. PRs should summarize scope, verification commands, risks, and any files intentionally left unchanged.

## Security & Configuration Tips

Never commit secrets, real user identifiers, chat IDs, or private paths. Use placeholders such as `<YOUR_API_KEY>` and `/path/to/...`. Keep examples generic and reusable for public OpenClaw users.
