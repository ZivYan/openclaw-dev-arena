---
name: single-agent-multi-role-rd
description: |
  单Agent多职责研发流。对外保持单入口，对内按多职责角色路由不同模型。
  用户要求按规范研发、先出方案再编码、
  修 Bug、做代码评审、补测试、输出交付报告时激活。
  触发词：研发规范、按流程做、先给方案、双方案对比、代码评审、最高代码质量。
---

# 单Agent多职责研发流

## 目标

对外保持一个研发入口，对内按阶段把工作路由给最适合的模型：

1. `rd-lead`：需求锁定、方案对抗、任务拆分、对抗评审
2. `rd-coder`：编码实现、自测执行、修复收口
3. `rd-ship`：验证复核、提交交付、报告整理

## 推荐模型映射

- `rd-lead` → Claude Opus
- `rd-coder` → Codex
- `rd-ship` → GPT-5.4

## 核心原则

- **对用户单入口**：默认只让用户与 `rd-lead` 交互
- **对系统多职责**：不同阶段路由到不同内部角色
- **对质量强约束**：Phase 0 / 1 先确认，P0 / P1 问题不交付

## 读取顺序

### 第一步：理解总流程与角色路由
```text
read("INDEX.md")
read("01-architecture.md")
read("10-setup-wizard.md")
```

### 第二步：锁定需求与方案
```text
read("02-feishu-setup.md")
read("03-agent-binding.md")
read("04-agent-communication.md")
```

### 第三步：执行实现与验证
```text
read("05-feishu-doc.md")
read("06-feishu-chat-management.md")
read("07-feishu-message-format.md")
read("09-best-practices.md")
```

### 第四步：按需补充
- 安装方式与目录约定 → `read("08-skill-organization.md")`
- 卡住或失败升级 → `read("11-troubleshooting.md")`

## 默认执行约束

1. **Phase 0 / 1 先确认**：需求和方案未确认，不进入开发
2. **优先最小改动**：只改与任务直接相关的文件
3. **先定义验收，再写实现**：没有验证标准不允许开工
4. **验证必须可复现**：列出命令、结果、结论
5. **已知 P0 / P1 问题未处理，不允许交付**

## 阶段路由

| Phase | 默认角色 | 推荐模型 |
|------|---------|---------|
| 0 需求锁定 | `rd-lead` | Claude Opus |
| 1 方案对抗 | `rd-lead` | Claude Opus |
| 2 任务拆分 | `rd-lead` | Claude Opus |
| 3 原子开发 | `rd-coder` | Codex |
| 4 自测验证 | `rd-coder` 主执行，`rd-ship` 复核 | Codex + GPT-5.4 |
| 5 对抗评审 | `rd-lead` | Claude Opus |
| 6 提交交付 | `rd-ship` 主输出，`rd-coder` 提供结果 | GPT-5.4 + Codex |

## 路由实现建议

优先方案：

- `rd-lead` 对外作为唯一入口
- 通过 `sessions_send` / `sessions_history` 调用 `rd-coder`、`rd-ship`
- 如果运行时支持，优先用 `sessions_spawn` 冷启动内部角色

兼容方案：

- 为 `rd-coder`、`rd-ship` 各保留一个内部专用群聊或固定 session
- 用户不直接进入这些群聊，只用于内部执行

## 输出格式

每次任务固定输出 6 段：

1. 任务定义
2. 方案对比
3. 任务拆分
4. 实现结果
5. 验证结果
6. 对抗审查结论

## 仓库维护

如果要修改本 Skill 自身，而不是用它做研发任务，先读：

```text
read("AGENTS.md")
```
