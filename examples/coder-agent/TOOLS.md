# TOOLS.md - Coder Agent

> 部署后根据实际环境填写

## 环境

- **OS:** macOS / Linux
- **Go:** 1.2x
- **Python:** 3.x
- **Node:** vXX.x

## 工作目录

主工作区：`~/.openclaw/workspace-coder/`

## 代码仓库

| 项目 | 路径 | 说明 |
|------|------|------|
| my-project | `~/projects/my-project` | 示例，替换为实际项目 |

## 多 Agent 协作

| Agent | 群聊 ID | 关系 |
|-------|---------|------|
| coder | `oc_你的群聊ID` | 本 agent（研发主驱动） |
| arch-alpha | `oc_你的群聊ID` | 方案架构师（守正） |
| arch-beta | `oc_你的群聊ID` | 方案挑战者（破局） |

## 飞书文档配置

| 配置项 | 值 |
|--------|-----|
| Wiki Space ID | `<YOUR_WIKI_SPACE_ID>` |
| 文档目录 Token | `<YOUR_WIKI_FOLDER_TOKEN>` |

> 安装时由用户提供个人 Wiki 目录信息。

## Codebase 配置

| 配置项 | 值 |
|--------|-----|
| 仓库 | `<YOUR_REPO>` |
| 默认 Base Branch | master |

## 注意事项

- Git commit 后不 push，除非进入 Phase 6
- 跨 workspace 访问需要在 SOUL.md 中明确授权
- MR 创建使用 Codebase MCP 工具

---

_环境变了就更新这里。_
