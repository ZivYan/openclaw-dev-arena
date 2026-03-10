# 🦞 OpenClaw Dev Arena

> 对抗式研发工作流 — coder × arch-alpha × arch-beta，基于 [OpenClaw](https://github.com/openclaw/openclaw) 构建。

## 🎯 项目定位

**这个项目是为 AI 写的，也是由 AI 维护的，用于快速创建飞书多 Agent 系统。你可以直接将这个仓库喂给 OpenClaw（小龙虾 🦞），它会自动理解架构并帮你创建多 Agent 系统。**

### 如何使用本项目

1. **复制模板**：将 `examples/` 目录复制到你的 OpenClaw workspace
2. **修改配置**：修改 agent 名称、模型、工具权限等
3. **创建群聊**：使用 `scripts/create_agent.py` 或手动创建飞书群聊
4. **更新配置**：将 binding 添加到你的 openclaw.json

### 💬 试试对你的 AI 说

```
读一下 INDEX.md，了解这个项目的结构
```

```
帮我部署一套对抗式研发 Agent（coder + arch-alpha + arch-beta）
```

```
按照 10-setup-wizard.md 引导我完成飞书多 Agent 系统搭建
```

```
读一下 examples/coder-agent/，帮我创建一个研发助手
```

- **AI-first 文档**：结构化的提示词工程，而非给人看的散文
- **模型一致性**：明确的代码和 checklist 代替模糊描述，减少不同模型的理解偏差
- **自维护**：由 Agent 维护的项目，脚本化操作代替手动配置
- **强制脱敏**：所有示例经过脱敏处理，不含真实身份信息


## 这个项目做什么？

用**一个飞书 Bot** 驱动**多个独立 AI Agent**。每个 Agent 绑定一个飞书群聊，拥有独立的身份、记忆、工具权限，Agent 之间可以互相通信协作。

### 核心架构：对抗式研发流程

```
                    飞书 Bot（一个应用）
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     群聊「开发」   群聊「方案A」  群聊「方案B」
          │              │              │
      Coder Agent   arch-alpha     arch-beta
    (研发主驱动)     (守正/提案)    (破局/rebuttal)
```

**Coder** 是研发主驱动者，负责 8 Phase 全流程；**arch-alpha** 和 **arch-beta** 在技术方案阶段进行对抗式设计，通过双方案 + rebuttal 产出最优解。

### 8 Phase 标准研发流程

```
Phase 0  需求理解          ← 用户确认 ✋
Phase 1  技术方案（对抗式）   ← 用户确认 ✋
Phase 2  分支创建 + 任务拆分
Phase 3  原子开发（逐任务推进，群聊实时通知进度）
Phase 4  自测验证（编译 + 测试 + 竞态检测 + lint）
Phase 5  Code Review（P0-P3 优先级自审）
Phase 6  提交 MR           ← 用户确认 ✋
Phase 7  提测交付（飞书文档归档）
```

### 核心能力

- 🤖 **一 Bot 多 Agent** — 一个飞书应用，多个独立 AI 助手
- ⚔️ **对抗式方案设计** — 双架构师独立提案 + 互相 rebuttal，对抗直到对齐
- 💬 **群聊隔离** — 每个 Agent 专属群聊，独立上下文
- 📡 **Agent 间通信** — coder 通过 sessions_send 驱动 arch-alpha/beta 对抗
- 📝 **飞书文档归档** — 技术方案、提测报告自动写入个人 Wiki
- 🚀 **自动创建 MR** — 开发完成后自动创建 Codebase Merge Request
- 🌿 **自动分支管理** — 未指定分支时从 master 自动拉取 `feat/<关键词>-<日期>`

## 快速开始

> 假设已安装 OpenClaw 并完成基础配置。

### Step 1：创建飞书应用

1. [飞书开放平台](https://open.feishu.cn/app) → 创建企业自建应用
2. 记录 **App ID** 和 **App Secret**
3. 添加「机器人」能力
4. 申请权限（见下方权限清单）
5. 事件订阅：`im.message.receive_v1`，连接方式选 **WebSocket**
6. 发布应用版本

详细配置见 [02-feishu-setup.md](02-feishu-setup.md)。

### Step 2：配置 OpenClaw

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "connectionMode": "websocket",
      "accounts": {
        "default": {
          "appId": "<YOUR_APP_ID>",
          "appSecret": "<YOUR_APP_SECRET>"
        }
      },
      "dm": { "allowFrom": ["ou_<YOUR_OPEN_ID>"] }
    }
  },
  "bindings": [{
    "agentId": "main",
    "match": { "channel": "feishu", "peer": { "kind": "dm", "id": "ou_<YOUR_OPEN_ID>" } }
  }]
}
```

重启 Gateway，给 Bot 发消息验证。

### Step 3：部署对抗式研发 Agent

**一键创建三个 Agent：**

```bash
# 1. 创建 coder（研发主驱动）
python3 scripts/create_agent.py \
  --agent-id coder --preset coder \
  --app-id "<APP_ID>" --app-secret "<APP_SECRET>" \
  --user-open-id "ou_<YOUR_OPEN_ID>"

# 2. 创建 arch-alpha（技术方案/守正）
python3 scripts/create_agent.py \
  --agent-id arch-alpha --preset arch-alpha \
  --app-id "<APP_ID>" --app-secret "<APP_SECRET>" \
  --user-open-id "ou_<YOUR_OPEN_ID>"

# 3. 创建 arch-beta（技术方案/破局）
python3 scripts/create_agent.py \
  --agent-id arch-beta --preset arch-beta \
  --app-id "<APP_ID>" --app-secret "<APP_SECRET>" \
  --user-open-id "ou_<YOUR_OPEN_ID>"
```

每个脚本自动完成：创建工作目录 → 生成身份文件 → 建群 → 更新配置。

部署后编辑 coder 的 `TOOLS.md`，填入飞书 Wiki 目录 Token 和 Codebase 仓库信息。

手动方式见 [03-agent-binding.md](03-agent-binding.md)。

## 架构原理

### Binding（路由）

一条 binding = 一条路由规则：
```json
{ "agentId": "coder", "match": { "channel": "feishu", "peer": { "kind": "group", "id": "oc_xxx" } } }
```
来自该群聊的消息 → 全部交给 coder 处理。

### Session（会话隔离）

每个 Agent + 群聊组合 = 独立会话（独立上下文、工作目录、模型、工具）。

### Agent 间通信

coder 通过 `sessions_send` 驱动 arch-alpha/beta 的对抗式方案设计。详见 [04-agent-communication.md](04-agent-communication.md)。

### 对抗式方案设计流程

```
coder 发送需求 brief
    │
    ├─ sessions_send → arch-alpha → 方案 A
    │
    ├─ sessions_send → arch-beta（附方案 A）→ 方案 B + rebuttal
    │
    ├─ sessions_send → arch-alpha（附 rebuttal）→ 回应
    │
    ├─ 继续对抗直到核心架构对齐（最多 3 轮额外）
    │
    └─ coder 汇总裁决 → 飞书文档归档 → 用户确认
```

## 预设角色

| 角色 | 模板 | 工具权限 | 适合场景 |
|------|------|---------|---------|
| **coder** | `coder-agent` | exec, read, write, edit, sessions_*, feishu_doc | 研发主驱动（8 Phase 全流程） |
| **arch-alpha** | `arch-alpha-agent` | read, web_search（只读） | 技术方案架构师（守正） |
| **arch-beta** | `arch-beta-agent` | read, web_search（只读） | 技术方案挑战者（破局） |
| **momo** | `momo-agent` | 全部权限（sessions_*, gateway） | 协调者（可选，多 Agent 场景） |

> 有模板的 preset 使用 `create_agent.py --preset` 时会自动复制 `examples/` 中的完整配置文件。

## 飞书权限清单

| 功能 | 权限 |
|------|------|
| 基础消息 | `im:message` `im:message:send_as_bot` |
| 群聊管理 | `im:chat:create` `im:chat:update` `im:chat.members:write_only` |
| 文档读写 | `docs:doc` `docs:doc:create` `drive:drive` |
| 权限管理 | `drive:permission:member:create` |

## ⚠️ 安全注意

- `dm.allowFrom` 必须配置白名单
- `appSecret` 不要提交到 Git
- `agents.list` 修改是**整体替换**，漏掉 Agent 会丢失配置
- Bot 创建的文档只有 Bot 能看，需调用权限 API 授权

## 项目结构

```
openclaw-dev-arena/
├── README.md                     本文件
├── INDEX.md                      AI 文档索引
├── 01~11 *.md                    详细设计文档
├── scripts/create_agent.py       一键创建功能 Agent
├── examples/
│   ├── coder-agent/              研发主驱动 Agent 模板（8 Phase 全流程）
│   ├── arch-alpha-agent/         技术方案架构师模板（守正）
│   ├── arch-beta-agent/          技术方案挑战者模板（破局）
│   ├── momo-agent/               协调者 Agent 模板
│   └── openclaw-config.json      示例配置（脱敏）
└── skills/
    ├── dev-workflow/              标准研发流程（8 Phase）
    ├── agent-comm/                跨 Agent 通信
    ├── delegate-agent/            任务委派
    ├── feishu-chat/               群聊管理
    ├── feishu-doc-writer/         文档写作
    ├── config-update/             配置安全编辑
    └── maintenance/               项目维护
```

## 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) — AI Agent 运行时
- [飞书开放平台](https://open.feishu.cn/) — 消息、文档、群聊 API

## License

MIT
