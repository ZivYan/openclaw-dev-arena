# TOOLS.md - MOMO (私人助手 Agent)

> 部署后根据实际环境填写

## 环境

- **OS:** macOS / Linux
- **Python:** 3.x

## 多 Agent 系统

| Agent | 群聊 ID | 用途 |
|-------|---------|------|
| momo | — | 私人助手（DM 入口） |
| orchestrator | `oc_你的群聊ID` | 研发流协调者 |
| coder | `oc_你的群聊ID` | 开发助手 |

## 工具权限矩阵

| 工具 | momo | orchestrator | coder | arch-* |
|------|------|-------------|-------|--------|
| exec | ✅ | ✅ | ✅ | ❌ |
| read/write/edit | ✅ | ✅ | ✅ | read |
| message | ✅ | ✅ | ✅ | ✅ |
| web_search | ✅ | ✅ | ✅ | ✅ |
| feishu_doc | ✅ | ✅ | ✅ | ❌ |
| browser | ✅ | ✅ | ✅ | ❌ |
| sessions_* | ✅ | ✅ | ✅ | ❌ |
| gateway | ❌ | ✅ | ❌ | ❌ |

> 设计原则：gateway 仅 orchestrator 可用；momo 专注用户服务；coder 专注编码

## 定时任务

| 任务 | Agent | 时间 | 说明 |
|------|-------|------|------|
| 心跳 | momo | 每 30min | 检查委派任务进度 |
| 示例 cron | — | — | 按需添加 |

---

_环境变了就更新这里。_
