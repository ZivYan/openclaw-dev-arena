# Orchestrator - 研发协调者 Agent

对抗式研发流的**协调者**。Orchestrator 不执行具体任务，而是将任务分发给专业子 Agent 并跟进结果。

## 核心职责

- **任务调度** — 理解需求，拆解并派发给 coder
- **进度跟进** — 通过心跳和 sessions_history 监控子 Agent 状态
- **系统运维** — 管理 Gateway 配置、cron 任务、Agent 健康度
- **记忆维护** — 记录决策和经验，维护长期记忆

## 快速部署

```bash
# 1. 复制到 workspace
cp -r examples/orchestrator-agent ~/.openclaw/workspace-orchestrator

# 2. 创建记忆目录
mkdir -p ~/.openclaw/workspace-orchestrator/memory

# 3. 编辑 TOOLS.md — 填入实际的 Agent 列表和群聊 ID

# 4. 在 openclaw.json 中添加 agent 配置
# 5. 重启 Gateway
```

## 文件说明

| 文件 | 用途 | 部署时修改 |
|------|------|-----------|
| SOUL.md | 协调原则、任务下发规则、安全边界 | 按需调整 |
| AGENTS.md | 记忆规范、安全规则、Git 规范 | 按需调整 |
| TOOLS.md | Agent 列表、权限矩阵、定时任务 | **必须填写** |
| HEARTBEAT.md | 心跳检查项 | 按需调整 |
| IDENTITY.md | 身份标识 | 可选修改 |

## 推荐 Skills

| Skill | 位置 | 用途 |
|-------|------|------|
| **delegate-agent** | `skills/delegate-agent/` | 异步任务派发（10s 超时 + 心跳跟进） |
| **agent-comm** | `skills/agent-comm/` | 跨 Agent 通信（sessions_send/list/history） |

## 权限配置

```json
{
  "id": "orchestrator",
  "name": "Orchestrator",
  "workspace": "~/.openclaw/workspace-orchestrator",
  "heartbeat": { "every": "30m", "target": "last" },
  "tools": {
    "allow": [
      "exec", "read", "write", "edit",
      "message", "web_search", "web_fetch", "session_status",
      "cron", "browser", "gateway",
      "sessions_list", "sessions_history", "sessions_send", "sessions_spawn",
      "feishu_doc", "feishu_perm"
    ]
  }
}
```

## 架构关系

```
  MOMO (私人助手)  ──委派研发任务──▶  Orchestrator (研发协调)
                                        ┌──┼──────────┐
                                      coder        arch-alpha
                                    (研发主驱动)     arch-beta
                                                   (对抗式方案设计)
```

- Orchestrator 是研发流程的中枢，负责跨 Agent 协调
- 编码任务派发给 coder，coder 再驱动 arch-alpha/beta 对抗式方案设计
- Orchestrator 只协调，不执行具体任务
- 子 Agent 失败 → Orchestrator 优化提示词重新派发，**不接手**
