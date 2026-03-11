# HEARTBEAT.md - Orchestrator

心跳触发时执行以下检查：

## 检查项

1. **Agent 任务进度** — `sessions_history` 检查 coder 的任务状态
2. **Cron 任务** — 检查定时任务执行情况
3. **系统健康** — git 状态、workspace 完整性
4. **记忆维护** — 更新 memory/ 日记

## 静默规则

- 23:00-08:00 除非紧急不打扰
- 无事可做回复 `HEARTBEAT_OK`
