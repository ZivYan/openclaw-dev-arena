# TOOLS.md - MOMO (协调者 Agent)

> 部署后根据实际环境填写

## 环境

- **OS:** macOS / Linux
- **Python:** 3.x

## 多 Agent 系统

| Agent | 群聊 ID | 用途 |
|-------|---------|------|
| momo | — | 协调者 |
| coder | `oc_你的群聊ID` | 开发助手 |
| writer | `oc_你的群聊ID` | 写作助手 |
| analyst | `oc_你的群聊ID` | 分析助手 |

## 工具权限矩阵

| 工具 | momo | coder | writer | analyst |
|------|------|-------|--------|---------|
| exec | ✅ | ✅ | ❌ | ✅ |
| read/write/edit | ✅ | ✅ | ❌ | ✅ |
| message | ✅ | ✅ | ✅ | ✅ |
| web_search | ✅ | ✅ | ✅ | ✅ |
| cron | ✅ | ❌ | ❌ | ❌ |
| browser | ✅ | ✅ | ❌ | ❌ |
| feishu_doc | ✅ | ❌ | ✅ | ❌ |
| sessions_* | ✅ | ❌ | ❌ | ❌ |
| gateway | ✅ | ❌ | ❌ | ❌ |

> 设计原则：gateway/sessions 仅 main 可用；coder 专注编码；writer 专注文档；analyst 专注分析。

## 定时任务

| 任务 | Agent | 时间 | 说明 |
|------|-------|------|------|
| 心跳 | momo | 每 30min | 批量检查 |
| 示例 cron | — | — | 按需添加 |

---

_环境变了就更新这里。_
