---
name: dev-workflow
description: 标准研发流程。当用户说"开发"、"做个需求"、"写个功能"、"新需求"、"帮我实现"、"start dev"时触发。
---

# 标准研发流程（8 Phase）

## 总览

```
Phase 0  需求理解      ← 用户确认 ✋
Phase 1  技术方案（对抗） ← 用户确认 ✋
Phase 2  分支创建 + 任务拆分
Phase 3  原子开发
Phase 4  自测验证
Phase 5  Code Review
Phase 6  提交 MR      ← 用户确认 ✋
Phase 7  提测交付
```

Phase 0 & 1 需要用户确认，确认后 Phase 2-5 全自动推进，Phase 6 提交 MR 前再次确认。

---

## Phase 0: 需求理解

**目标**：与用户对齐需求，明确边界和验收标准。

**执行步骤**：
1. 分析用户描述，提炼核心诉求
2. 阅读相关代码，了解现有实现
3. 输出结构化需求摘要：

```
📋 需求理解

**目标**：[做什么]
**背景**：[为什么要做]
**约束**：
  - [不能动什么]
  - [性能/兼容性要求]
**影响面**：
  - [涉及的模块/服务]
  - [上下游依赖]
**验收标准**：
  1. [可测试的条件]
  2. [可测试的条件]

请确认以上理解是否正确？确认后进入技术方案阶段。
```

4. **等待用户回复「确认」后**进入 Phase 1

---

## Phase 1: 技术方案（对抗式设计）

**目标**：通过双方案对抗产出最优技术方案。

**执行步骤**：

### 1.1 准备需求 brief

将 Phase 0 确认的需求整理为结构化 brief，包含：目标、约束、影响面、验收标准、相关代码路径。

### 1.2 发起对抗

```
1. sessions_list → 找到 arch-alpha 和 arch-beta 的 sessionKey
2. sessions_send → arch-alpha：发送需求 brief，要求独立出方案 A
3. 等待 arch-alpha 返回方案 A
4. sessions_send → arch-beta：发送需求 brief + 方案 A，要求出方案 B + rebuttal A
5. 等待 arch-beta 返回方案 B + rebuttal
6. sessions_send → arch-alpha：转发 rebuttal，要求回应
7. 等待 arch-alpha 回应
```

### 1.3 对抗收敛

检查双方是否已对齐（核心分歧是否消除）：
- **已对齐** → 进入 1.4
- **未对齐** → 将回应转发给 arch-beta，继续对抗（最多 3 轮额外对抗）

对齐判断标准：
- 核心架构选择达成共识
- 剩余分歧仅为实现细节层面
- 双方承认对方的主要论点

### 1.4 方案裁决 + 飞书归档

1. 汇总对比，输出推荐方案：

```
🏗️ 技术方案裁决

**方案 A**（守正）：[一句话摘要]
  ✅ [优势1] ✅ [优势2]
  ❌ [劣势1]

**方案 B**（破局）：[一句话摘要]
  ✅ [优势1] ✅ [优势2]
  ❌ [劣势1]

**推荐**：方案 [A/B]
**理由**：[为什么选这个]
**综合方案**：[如果需要融合两个方案的优点，说明如何融合]

技术方案文档已归档 → [飞书文档链接]
请确认后开始开发。
```

2. 写入飞书文档（个人 Wiki 目录下），内容包含：
   - 需求背景
   - 方案 A 完整内容
   - 方案 B 完整内容
   - 对抗记录（rebuttal + 回应）
   - 裁决结论

3. **等待用户确认后**进入 Phase 2

---

## Phase 2: 分支创建 + 任务拆分

**目标**：创建开发分支，拆解原子任务。

### 2.1 创建分支

检查用户是否指定了分支：
- **已指定** → 切换到该分支
- **未指定** → 从 master 拉新分支

分支命名规则：`feat/<关键词>-<MMDD>`
- 关键词从需求中自动提取，2-4 个英文单词，kebab-case
- 示例：`feat/user-profile-refactor-0310`

```bash
git fetch origin master
git checkout -b feat/<name>-<MMDD> origin/master
```

### 2.2 任务拆分

将技术方案拆解为原子任务，每个任务 ≤ 2h：

```
📋 任务拆分完成（共 N 个）

1. [ ] [任务描述] — 涉及文件：[文件列表]
2. [ ] [任务描述] — 涉及文件：[文件列表]
3. [ ] [任务描述] — 涉及文件：[文件列表]
...

依赖关系：1 → 2 → 3（顺序执行）/ 2,3 可并行
预估总耗时：Xh

开始执行 →
```

---

## Phase 3: 原子开发

**目标**：逐个完成任务，每个任务包含接口定义 → 实现 → 单测。

**每个任务的执行流程**：
1. 定义/修改接口
2. 编写实现代码
3. 编写对应单测
4. 运行单测确认通过
5. git commit（一个任务一个 commit）

**每完成一个任务，群聊通知进度**：

```
✅ [2/5] 实现 GetProfile 方法

📁 修改文件：
  - service/user.go (+45 -3)
  - dal/user.go (+30 -0)
  - service/user_test.go (+60 -0)
🧪 单测：3 passed, 0 failed
💬 commit: feat: implement GetProfile with cache support
⏱️ 耗时：8min
──────────────────
⏭️ 下一个：[3/5] 实现 UpdateProfile 方法
```

**失败处理**：
- 单测未通过 → 修复后重试，最多 3 次
- 3 次失败 → 群聊通知用户，说明卡点，等待指示

---

## Phase 4: 自测验证

**目标**：全量编译、测试、竞态检测、lint 检查。

### 技术栈自动识别

根据项目根目录文件自动选择命令：

| 标识文件 | 语言 | 编译 | 测试 | Lint |
|---------|------|------|------|------|
| `go.mod` | Go | `go build ./...` | `go test -gcflags="all=-N -l" -v ./...` | `golangci-lint run ./...` |
| `package.json` | Node.js | `npm run build` | `npm test` | `npm run lint` |
| `pyproject.toml` | Python | — | `pytest -v` | `ruff check .` |
| `Cargo.toml` | Rust | `cargo build` | `cargo test` | `cargo clippy` |
| `pom.xml` | Java | `mvn compile` | `mvn test` | — |

Go 项目额外执行：`go test -race ./...`

### 自测报告

```
🔬 自测报告

├─ 编译：✅ passed
├─ 单测：✅ 18 passed, 0 failed（覆盖率 85%）
├─ 竞态：✅ 无 data race
└─ Lint：✅ 无警告

全部通过，进入 Code Review →
```

**有失败项时**：
- 修复问题，重新执行自测
- 修复过程在群聊同步通知

---

## Phase 5: Code Review

**目标**：自审代码，按优先级检查问题。

### 审查维度

**P0 安全性（一票否决）**：
- SQL 注入：是否参数化查询？
- 敏感信息：是否泄露到日志或响应？
- 权限校验：是否有租户隔离？

**P1 稳定性**：
- 空指针：RPC 返回、指针、Map 是否先检查 nil？
- 资源泄漏：defer 释放？
- 并发安全：goroutine 安全启动？共享变量加锁？
- 错误处理：错误是否正确传播？

**P2 正确性**：
- 逻辑完备：Happy Path 和 Error Path 覆盖？
- 边界条件：空 slice、零值、类型断言？

**P3 性能**：
- N+1 查询：循环内是否可批量？
- 冗余操作：多余的数据库查询或序列化？

### Review 报告

```
🔍 Code Review 完成

├─ P0 安全性：✅ 0 issues
├─ P1 稳定性：⚠️ 1 issue → 已修复
│   └─ dal/user.go:42 — defer rows.Close() 遗漏，已补充
├─ P2 正确性：✅ 0 issues
└─ P3 性能：✅ 0 issues

所有问题已修复，准备提交 MR →
```

---

## Phase 6: 提交 MR

**目标**：push 代码，自动创建 Codebase MR。

**执行步骤**：

1. rebase master：
```bash
git fetch origin master
git rebase origin/master
```

2. 解决冲突（如有），重新执行 Phase 4 自测

3. push 分支：
```bash
git push origin feat/<branch-name>
```

4. 创建 Codebase MR（使用 Codebase MCP 工具）：
   - 标题：`feat: [需求一句话描述]`
   - 描述：包含需求背景、变更摘要、技术方案文档链接、测试结果
   - Base branch: master

5. 群聊通知：

```
🚀 MR 已创建

📎 MR 链接：[Codebase MR URL]
📄 技术方案：[飞书文档链接]

变更摘要：
  - [文件1] (+X -Y): [改了什么]
  - [文件2] (+X -Y): [改了什么]

测试结果：18 passed, 0 failed
──────────────────
请 review 后确认合并。
```

6. **等待用户确认后**合并 MR

---

## Phase 7: 提测交付

**目标**：生成提测报告，归档到飞书文档。

**提测报告内容**：

```markdown
# 提测报告：[需求标题]

## 需求背景
[Phase 0 的需求摘要]

## 变更内容
| 文件 | 变更行数 | 说明 |
|------|---------|------|
| service/user.go | +120 -15 | 用户资料接口重构 |
| ... | ... | ... |

## 技术方案
[飞书文档链接]

## 测试覆盖
- 单测用例数：X
- 覆盖率：X%
- 竞态检测：通过

## 自测结果
- 编译：✅
- 单测：✅
- Lint：✅

## MR 信息
- 分支：feat/xxx
- MR 链接：[URL]
- Commit 数：X

## 风险说明
[已知风险和缓解措施，无则写"无"]
```

**写入飞书文档**（个人 Wiki 目录下），群聊通知：

```
📦 提测交付完成

📄 提测报告：[飞书文档链接]
📎 MR：[MR 链接]
🏗️ 技术方案：[飞书文档链接]

✅ 全流程结束
```
