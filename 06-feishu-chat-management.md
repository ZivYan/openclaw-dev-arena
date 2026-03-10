# 06 - Phase 4：自测验证

## 目标

先用最小成本建立信心，再逐步扩大验证范围。

## 默认执行角色

- 主执行：`rd-coder`
- 复核：`rd-ship`
- 推荐模型：Codex + GPT-5.4

## 验证顺序

1. 最小相关验证
2. 当前目录验证
3. 更大范围验证
4. 构建 / 测试 / lint / 格式检查

## 当前仓库常用命令

```bash
python3 -m py_compile scripts/create_agent.py
python3 -m json.tool examples/openclaw-config.json
git diff --stat
git status --short
```

## 通用代码仓库验证模板

```bash
# 先最小范围
<test command for changed dir>

# 再扩大
<build command>
<lint command>
```

## 失败规则

- 同一问题最多尝试 3 次
- 超过 3 次必须停下并说明：
  - 已尝试方案
  - 错误信息
  - 失败原因
  - 备选方案

## 输出模板

```markdown
## 验证结果
- 命令：
- 结果：
- 结论：
```
