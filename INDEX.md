# 单Agent多职责研发流索引

## 这是什么

这是一个给 OpenClaw 使用的研发流程 Skill，目标是让用户只面对一个入口，但系统内部能按不同职责把工作路由给不同模型，完成需求、方案、实现、验证、评审和交付。

## 适合谁

- 想让 OpenClaw 按固定研发流程工作的开发者
- 想要“先方案、后编码”的单 Agent 工作流
- 希望把代码质量、验证和交付统一成 SOP 的团队

## 文档地图

| 文件 | 用途 |
|------|------|
| `01-architecture.md` | Skill 架构、角色路由、总流程 |
| `02-feishu-setup.md` | Phase 0：需求锁定 |
| `03-agent-binding.md` | Phase 1：方案对抗 |
| `04-agent-communication.md` | Phase 2：任务拆分 |
| `05-feishu-doc.md` | Phase 3：原子开发 |
| `06-feishu-chat-management.md` | Phase 4：自测验证 |
| `07-feishu-message-format.md` | Phase 5：对抗评审与输出格式 |
| `08-skill-organization.md` | 安装方式与目录组织 |
| `09-best-practices.md` | 质量红线与最佳实践 |
| `10-setup-wizard.md` | 端到端执行清单 |
| `11-troubleshooting.md` | 失败与受阻升级策略 |

## 推荐阅读顺序

1. `01-architecture.md`
2. `02-feishu-setup.md`
3. `03-agent-binding.md`
4. `10-setup-wizard.md`
5. 再按需进入 `04-11`

## 执行约束

- Phase 0 / 1 默认需要用户确认
- 单任务尽量控制在 2 小时以内
- 超过 5 个文件或涉及结构变化时，创建临时 `IMPLEMENTATION_PLAN.md`
- 每次任务都必须给出验证结果与对抗审查结论

## 关键结论

这个 Skill 不是“人人都能直接编码”，而是：

- 用户只进入一个入口
- `rd-lead` 负责锁需求、做方案、做评审
- `rd-coder` 负责真正改代码和执行验证
- `rd-ship` 负责复核和交付
