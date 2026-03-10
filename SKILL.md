---
name: single-agent-multi-role-rd
description: |
  单Agent多职责研发流。用户要求按规范研发、先出方案再编码、
  修 Bug、做代码评审、补测试、输出交付报告时激活。
  触发词：研发规范、按流程做、先给方案、双方案对比、代码评审、最高代码质量。
---

# 单Agent多职责研发流

## 目标

让一个 `coder` 在单 Agent 场景下，仍然按高质量研发流程工作：

1. 先锁定需求
2. 再做双方案对抗
3. 再拆原子任务
4. 再实现与验证
5. 最后做对抗评审和交付

## 强制身份

同一个 `coder` 必须依次切换三种身份：

- **开发者**：理解需求、实现代码、补测试
- **反对者**：反驳方案、挑边界、找风险
- **验收者**：按标准裁决是否通过

禁止跳过“反对者”与“验收者”阶段。

## 读取顺序

### 第一步：理解总流程
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
