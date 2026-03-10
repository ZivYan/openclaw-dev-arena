# arch-alpha - 技术方案架构师（守正）

对抗式研发流程中的**方案提出者**。为每个研发需求提供稳健、经过验证的技术方案，并在 rebuttal 中回应质疑。

## 在流程中的位置

```
coder 发需求 brief
    │
    ├─ → arch-alpha → 方案 A（本 Agent）
    │
    ├─ → arch-beta（附方案 A）→ 方案 B + rebuttal
    │
    ├─ → arch-alpha（附 rebuttal）→ 回应    ← 本 Agent
    │
    └─ 对抗直到对齐
```

arch-alpha 由 coder 通过 `sessions_send` 驱动，不需要用户直接交互。

## 快速部署

```bash
# 使用 create_agent.py 自动创建
python3 scripts/create_agent.py \
  --agent-id arch-alpha --preset arch-alpha \
  --role "技术方案架构师" --user-name "YourName" \
  --app-id "cli_xxx" --app-secret "xxx" --user-open-id "ou_xxx"
```

## 文件说明

| 文件 | 用途 |
|------|------|
| SOUL.md | 方案设计原则、输出格式、rebuttal 回应规则、对抗规则 |
| IDENTITY.md | 身份标识（守正 🏛️） |
| TOOLS.md | 工具权限、协作关系 |
| AGENTS.md | 接收 sessions_send 的处理流程 |

## 权限配置

```json
{
  "id": "arch-alpha",
  "name": "守正",
  "workspace": "~/.openclaw/workspace-arch-alpha",
  "tools": {
    "allow": ["read", "message", "web_search", "web_fetch", "session_status"]
  }
}
```

只读权限，不执行代码，只做技术方案设计。

## 必须与以下 Agent 同时部署

- **coder** — 驱动对抗流程、接收方案、汇总裁决
- **arch-beta** — 对抗方，提供差异化方案 + rebuttal
