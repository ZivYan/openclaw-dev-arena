# arch-beta - 技术方案挑战者（破局）

对抗式研发流程中的**方案挑战者**。提供差异化技术方案，对 arch-alpha 的方案进行 rebuttal，通过对抗产出最优解。

## 在流程中的位置

```
coder 发需求 brief
    │
    ├─ → arch-alpha → 方案 A
    │
    ├─ → arch-beta（附方案 A）→ 方案 B + rebuttal    ← 本 Agent
    │
    ├─ → arch-alpha（附 rebuttal）→ 回应
    │
    └─ 对抗直到对齐
```

arch-beta 由 coder 通过 `sessions_send` 驱动，不需要用户直接交互。

## 快速部署

```bash
# 使用 create_agent.py 自动创建
python3 scripts/create_agent.py \
  --agent-id arch-beta --preset arch-beta \
  --app-id "cli_xxx" --app-secret "xxx" --user-open-id "ou_xxx"
```

## 文件说明

| 文件 | 用途 |
|------|------|
| SOUL.md | 差异化思考原则、双模式（独立提案/rebuttal+提案）、对抗规则 |
| IDENTITY.md | 身份标识（破局 ⚔️） |
| TOOLS.md | 工具权限、协作关系 |
| AGENTS.md | 接收 sessions_send 的处理流程 |

## 权限配置

```json
{
  "id": "arch-beta",
  "name": "破局",
  "workspace": "~/.openclaw/workspace-arch-beta",
  "tools": {
    "allow": ["read", "message", "web_search", "web_fetch", "session_status"]
  }
}
```

只读权限，不执行代码，只做技术方案设计和 rebuttal。

## 必须与以下 Agent 同时部署

- **coder** — 驱动对抗流程、接收方案、汇总裁决
- **arch-alpha** — 对抗方，提供基础方案
