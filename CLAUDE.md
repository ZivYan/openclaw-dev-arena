# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**openclaw-dev-arena** is an open-source adversarial development workflow template built on the OpenClaw framework. It provides configuration templates, utility scripts, AI-optimized documentation, and preset Agent personas (momo + orchestrator + coder + arch-alpha + arch-beta) for deploying multi-agent AI systems on Feishu (Lark).

Core concept: One Feishu Bot → multiple independent AI Agents, each bound to a dedicated group chat with isolated context, tools, and permissions.

## Architecture

```
Feishu Bot (1 app) ──WebSocket──▶ OpenClaw Gateway
                                      │
                          Binding Rules (channel + peer → Agent)
                                      │
          ┌──────────┬─────────┬──┴──────┬──────────┬──────────┐
        Agent A    Agent B   Agent C   Agent D    Agent E
        (momo)  (orchestrator) (coder) (arch-alpha) (arch-beta)

  momo (DM入口/私人助手) ──委派──▶ orchestrator (研发协调) ──派发──▶ coder/arch-*
```

- **Binding**: Routes a chat/DM to an Agent via `[channel + peer_id]` mapping
- **Session**: Each Agent + chat combo = independent session (`agent:{id}:{channel}:{peer_kind}:{peer_id}`)
- **Cross-agent comms**: Orchestrator uses `sessions_send(sessionKey, message)` to delegate tasks

## Key Files

| File | Purpose |
|------|---------|
| `INDEX.md` | Documentation roadmap with reading order |
| `01-architecture.md` | System design |
| `examples/openclaw-config.json` | Annotated config template with placeholders |
| `examples/PLACEHOLDERS.md` | All 24+ placeholder values and their sources |
| `scripts/create_agent.py` | Auto-creates Agent workspace + Feishu group chat + updates config |
| `examples/coder-agent/` | Full coder Agent template (SOUL.md, TOOLS.md, skills/) |
| `examples/momo-agent/` | Personal assistant Agent template |
| `examples/orchestrator-agent/` | Dev workflow coordinator Agent template |
| `skills/` | Shared skill modules (agent-comm, feishu-chat, feishu-doc-writer, config-update, etc.) |

## Common Commands

### Create a new Agent
```bash
python3 scripts/create_agent.py \
  --agent-id coder \
  --agent-name "Coder" \
  --role "Code development assistant" \
  --preset coder \
  --app-id "<FEISHU_APP_ID>" \
  --app-secret "<FEISHU_APP_SECRET>" \
  --user-open-id "ou_<USER_OPEN_ID>"
```

### Validate config (no hardcoded secrets)
```bash
python3 scripts/check_sensitive.py
```

### Edit config safely
```bash
python3 skills/config-update/script/config_edit.py --validate
```

## Critical Constraints

- **`config.patch` on `agents.list`** does **array replacement**, not append — always include ALL agents when patching
- For array fields, use `config.apply` with full config instead of `config.patch`
- Agents must NOT access other agents' workspaces or `~/.openclaw/openclaw.json` directly
- **Feishu message format**: No LaTeX, no Markdown tables — use bold/code/lists only
- All documentation changes must go through deidentification before commit (replace model IDs, API keys, paths, open_ids with placeholders)

## Preset System

Presets define both tool permissions AND hand-crafted SOUL.md content:
- `momo` — Personal assistant: daily chat, info lookup, lightweight tasks. Delegates dev tasks to orchestrator.
- `orchestrator` — Dev workflow coordinator: task decomposition, dispatch to coder/arch-*, progress tracking. Has gateway + sessions_spawn.
- `coder` — Dev workflow driver (8 Phase): requirement → adversarial design → implement → test → MR → delivery. Tools: exec, read, write, edit, browser, sessions_*, feishu_doc
- `arch-alpha` — Architecture proposer (守正): generates stable, proven technical proposals. Tools: read, web_search (read-only)
- `arch-beta` — Architecture challenger (破局): generates alternative proposals + rebuttals. Tools: read, web_search (read-only)

## Dev Workflow (coder preset)

The coder agent drives an 8-phase adversarial development workflow:
- Phase 0: Requirement understanding (user confirms)
- Phase 1: Technical design via arch-alpha vs arch-beta adversarial debate (user confirms)
- Phase 2: Branch creation (`feat/<keyword>-<MMDD>`) + task breakdown
- Phase 3-5: Atomic development → self-test → code review (auto, with progress updates)
- Phase 6: Auto-create Codebase MR (user confirms merge)
- Phase 7: Delivery report archived to Feishu Wiki

## Language & Documentation

- All documentation is in Chinese, structured as AI-friendly directives
- SKILL.md files define trigger keywords and action instructions for each module
- Documentation follows sequential numbering (01- through 11-)
