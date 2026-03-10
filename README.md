# 🛠️ 单Agent多职责研发流

> 对外单入口、对内多模型多职责的高质量研发流程，可直接作为仓库安装到 OpenClaw 中使用。

## 项目定位

这个仓库的目标不是再提供多 Agent 编排模板，而是提供一套**单入口 + 多职责路由**的研发规范：

- 用户只面对一个研发入口
- 内部按阶段把任务路由给最适合的模型
- 先方案、后实现，强制保留对抗审查
- 输出结果可验证、可复盘、可归档

适合场景：

- 修 Bug
- 加功能
- 补测试
- 做代码评审
- 按固定 SOP 交付研发结果

## 核心流程

```text
Phase 0 需求锁定
Phase 1 方案对抗
Phase 2 任务拆分
Phase 3 原子开发
Phase 4 自测验证
Phase 5 对抗评审
Phase 6 提交交付
```

## 推荐角色与模型

| 角色 | 职责 | 推荐模型 |
|------|------|---------|
| `rd-lead` | 需求锁定、方案对抗、任务拆分、对抗评审 | Claude Opus |
| `rd-coder` | 编码实现、自测执行、问题修复 | Codex |
| `rd-ship` | 验证复核、提交交付、报告整理 | GPT-5.4 |

> 推荐把 `rd-lead` 作为对外唯一入口；`rd-coder` 和 `rd-ship` 作为内部执行角色。

## 安装到 OpenClaw

将整个仓库放到 OpenClaw 的 skills 目录下，例如：

```bash
cp -r feishu-multi-agent ~/.openclaw/skills/single-agent-multi-role-rd
```

或直接把仓库克隆到目标目录：

```bash
git clone git@github.com:ZivYan/feishu-multi-agent.git ~/.openclaw/skills/single-agent-multi-role-rd
```

根目录 `SKILL.md` 就是 Skill 入口。

## 如何触发

可以直接对 OpenClaw 说：

```text
按研发规范处理这个需求
```

```text
先给我两个方案，再开始编码
```

```text
按最高代码质量流程修这个 Bug
```

```text
先做对抗评审，再决定是否提交
```

## 阶段路由

```text
用户 → rd-lead(Claude Opus)
        ├─ Phase 0-2：锁需求、做方案、拆任务
        ├─ Phase 3-4：派给 rd-coder(Codex) 编码和自测
        ├─ Phase 4：交给 rd-ship(GPT-5.4) 复核验证结果
        ├─ Phase 5：回到 rd-lead 做对抗评审
        └─ Phase 6：由 rd-ship 输出提交与交付材料
```

## OpenClaw 中怎么实现

- **最优实现**：配置 `rd-lead`、`rd-coder`、`rd-ship` 三个 agent，各自单独配置 `model.primary`
- **默认入口**：只把 `rd-lead` 暴露给用户
- **内部通信**：`rd-lead` 通过 `sessions_send` / `sessions_history` 调用内部角色
- **冷启动优化**：如果运行时稳定支持 `sessions_spawn`，优先用它拉起内部 session
- **兼容做法**：如果 `sessions_spawn` 不稳定，就给 `rd-coder`、`rd-ship` 各保留一个内部群聊

## 阅读顺序

1. `INDEX.md`：文档索引
2. `01-architecture.md`：Skill 架构与三重身份
3. `02-feishu-setup.md`：Phase 0 需求锁定
4. `03-agent-binding.md`：Phase 1 方案对抗
5. `04-agent-communication.md`：Phase 2 任务拆分
6. `05-feishu-doc.md`：Phase 3 原子开发
7. `06-feishu-chat-management.md`：Phase 4 自测验证
8. `07-feishu-message-format.md`：Phase 5 对抗评审
9. `10-setup-wizard.md`：端到端执行清单与角色路由

## 当前仓库结构

```text
feishu-multi-agent/
├── SKILL.md                  Skill 入口
├── INDEX.md                  文档索引
├── 01-11 *.md                研发流程与规范文档
├── AGENTS.md                 维护者指引
├── scripts/                  辅助脚本
├── examples/                 历史参考与示例素材
└── skills/                   兼容保留的子技能资料
```

> `examples/` 与 `skills/` 目前保留为兼容参考；本仓库的主入口是根目录 `SKILL.md` 和 `01-11` 文档。

## 示例配置

参考 `examples/openclaw-config.json`：

- `rd-lead`：绑定用户 DM，负责对外沟通与裁决
- `rd-coder`：绑定内部编码群聊，负责执行与自测
- `rd-ship`：绑定内部交付群聊，负责复核与交付产物

## 最小验证命令

针对代码仓库任务，优先执行最小范围验证；针对本仓库自身，常用命令是：

```bash
python3 -m py_compile scripts/create_agent.py
python3 -m json.tool examples/openclaw-config.json
git diff --stat
git status --short
```

## 设计原则

- **少角色，强流程**
- **先确认，后编码**
- **先验收，后实现**
- **优先最小改动**
- **必须给出验证结果**
- **允许质疑当前方案**

## License

MIT
