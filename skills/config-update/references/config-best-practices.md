# 配置更新最佳实践

## 为什么需要专用工具

OpenClaw 的 `agents.list` 和 `bindings` 是数组字段：
- `config.patch` 对数组是**整体替换**，不是合并
- 手动编辑容易遗漏字段导致 Agent 丢失
- 使用专用脚本可以自动备份、验证、阻断危险操作

## 安全原则

1. **永远使用脚本** — 不手动编辑 JSON
2. **先预览后应用** — 不加 `--apply` 先看变化
3. **备份自动创建** — 脚本每次修改前自动备份
4. **验证再重启** — `--validate` 确认无误后再应用

## 常见操作

### 修改单个 Agent 模型

```bash
python3 scripts/config_edit.py --set-model <agent_id> <provider/model_id> --apply --restart
```

### 批量修改模型

```bash
python3 scripts/config_edit.py --set-model <agent1>,<agent2> <provider/model_id> --apply --restart
```

### 调整心跳频率

```bash
python3 scripts/config_edit.py --set-heartbeat <agent_id> 30m --apply --restart
```

### 回滚配置

```bash
cp ~/.openclaw/config-backups/<backup-file>.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 常见陷阱

| 操作 | 风险 | 正确做法 |
|------|------|---------|
| `config.patch` 修改 agents.list | 整体替换，未列出的 Agent 丢失 | 用 config_edit.py |
| 手动拼 JSON | 格式错误导致启动失败 | 用 Python json 模块 |
| 不验证就重启 | 配置损坏无法恢复 | 先 `--validate` |
| 忘记备份 | 出错后无法回滚 | 脚本自动备份 |
