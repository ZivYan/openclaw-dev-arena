# Config Update Skill

OpenClaw 配置安全更新指南。

## 用途

指导如何安全地更新 OpenClaw 配置（Agent 模型、心跳、权限等）。

## ⚠️ 核心原则

`agents.list` 和 `bindings` 是**数组字段**，`config.patch` 对数组执行**整体替换**而非合并。
传入不完整的数组 = 丢失未包含的 Agent。

### 绝对禁止

- ❌ 用 `config.patch` 修改 `agents.list` 或 `bindings`
- ❌ 手动拼接 JSON 字符串写入配置文件
- ❌ 不经验证就应用配置

## ✅ 推荐流程

### 使用 config_edit.py 脚本

```bash
# 查看当前配置
python3 script/config_edit.py --list

# 修改模型（预览）
python3 script/config_edit.py --set-model <agent_id> <provider/model_id>

# 修改模型（应用并重启）
python3 script/config_edit.py --set-model <agent_id> <provider/model_id> --apply --restart

# 批量修改
python3 script/config_edit.py --set-model <agent1>,<agent2> <provider/model_id> --apply --restart

# 修改心跳
python3 script/config_edit.py --set-heartbeat <agent_id> <interval> --apply --restart

# 验证配置
python3 script/config_edit.py --validate

# 查看变化
python3 script/config_edit.py --diff
```

### 安全机制

| 功能 | 说明 |
|------|------|
| 自动备份 | 修改前自动备份到 `~/.openclaw/config-backups/` |
| Agent 数量检查 | 数量减少时阻断并提示 |
| JSON 验证 | 修改前验证格式完整性 |
| Binding 引用检查 | 确保所有 binding 引用的 Agent 存在 |
| 模型验证 | 检查 provider 是否有效 |

### 回滚

```bash
cp ~/.openclaw/config-backups/<backup-file>.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 参考

- [配置更新最佳实践](./references/config-best-practices.md)
