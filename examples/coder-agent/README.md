# Coder Agent - 对抗式研发主驱动

研发流程的**主驱动者**。负责 8 Phase 全流程：需求理解 → 驱动对抗式方案设计 → 编码实现 → 自测 → Code Review → 提交 MR → 提测归档。

## 核心能力

- **8 Phase 研发流程** — 从需求到交付的全自动推进
- **对抗式方案设计** — 通过 sessions_send 驱动 arch-alpha/beta 双方案对抗
- **原子化开发** — 每个任务 ≤ 2h，一个任务一个 commit，群聊实时通知进度
- **技术栈自动识别** — 根据 go.mod/package.json/pyproject.toml 自动选择编译/测试/lint 命令
- **自动分支管理** — 未指定分支时从 master 拉取 `feat/<关键词>-<MMDD>`
- **飞书文档归档** — 技术方案、提测报告自动写入个人 Wiki
- **自动创建 MR** — 开发完成后自动创建 Codebase Merge Request

## 快速部署

```bash
# 1. 复制到 workspace
cp -r examples/coder-agent ~/.openclaw/workspace-coder

# 2. 创建记忆目录
mkdir -p ~/.openclaw/workspace-coder/memory

# 3. 编辑 TOOLS.md — 填入以下信息：
#    - 项目路径
#    - arch-alpha/arch-beta 的群聊 ID
#    - 飞书 Wiki Space ID 和目录 Token
#    - Codebase 仓库信息

# 4. 编辑 USER.md — 填入你的信息

# 5. 创建 Agent（或手动添加到 openclaw.json）
python3 scripts/create_agent.py \
  --agent-id coder --agent-name "Coder" --preset coder \
  --app-id "cli_xxx" --app-secret "xxx" --user-open-id "ou_xxx"

# 6. 同时创建 arch-alpha 和 arch-beta
python3 scripts/create_agent.py \
  --agent-id arch-alpha --preset arch-alpha \
  --app-id "cli_xxx" --app-secret "xxx" --user-open-id "ou_xxx"

python3 scripts/create_agent.py \
  --agent-id arch-beta --preset arch-beta \
  --app-id "cli_xxx" --app-secret "xxx" --user-open-id "ou_xxx"

# 7. 重启
openclaw gateway restart
```

## 文件说明

| 文件 | 用途 | 部署时修改 |
|------|------|-----------|
| SOUL.md | 8 Phase 研发流程、对抗驱动逻辑、进度通知格式 | 按需调整 |
| AGENTS.md | 职责、工具权限、协作关系 | 按需调整 |
| TOOLS.md | 环境信息、项目路径、飞书 Wiki 配置、Codebase 配置 | **必须填写** |
| USER.md | 用户偏好 | **必须填写** |
| IDENTITY.md | 身份标识 | 可选修改 |

## 协作 Agent

| Agent | 模板 | 关系 |
|-------|------|------|
| **arch-alpha**（守正） | `examples/arch-alpha-agent/` | Phase 1 由 coder 发送需求 brief，返回方案 A |
| **arch-beta**（破局） | `examples/arch-beta-agent/` | Phase 1 由 coder 发送 brief + 方案 A，返回方案 B + rebuttal |

三个 Agent 必须同时部署，否则 Phase 1 对抗流程无法运行。

## 内置 Skills

| Skill | 触发 | 用途 |
|-------|------|------|
| **dev-workflow** | `做个需求`、`新需求`、`帮我实现` | 8 Phase 标准研发流程 |
| **project-switcher** | `/repo` | 多项目管理，快速切换工作目录 |
| **code-review** | `/review` | 代码审查（安全/质量/架构 checklist） |
| **git-workflow** | `/git` | Git 分支/commit/PR 标准流程 |

## 权限配置

```json
{
  "id": "coder",
  "name": "Coder",
  "workspace": "~/.openclaw/workspace-coder",
  "tools": {
    "allow": [
      "exec", "read", "write", "edit",
      "message", "web_search", "web_fetch", "session_status",
      "browser", "feishu_doc", "feishu_perm",
      "sessions_list", "sessions_history", "sessions_send"
    ]
  }
}
```

## 使用示例

在「开发」群聊中发送需求：

> 帮我重构 UserService 的 GetProfile 方法，增加缓存支持

Coder 会自动启动 8 Phase 流程：
1. 输出需求摘要 → 等你确认
2. 驱动 arch-alpha/beta 对抗出技术方案 → 飞书文档归档 → 等你确认
3. 从 master 拉分支 `feat/user-profile-cache-0310` → 拆任务
4. 逐任务开发，每完成一个群聊通知进度
5. 全量自测 + Code Review
6. 自动创建 Codebase MR → 等你确认合并
7. 生成提测报告 → 飞书文档归档
