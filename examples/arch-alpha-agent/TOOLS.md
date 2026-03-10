# TOOLS.md - arch-alpha（守正）

> 部署后根据实际环境填写

## 工作目录

主工作区：`~/.openclaw/workspace-arch-alpha/`

## 工具权限

| 工具 | 说明 |
|------|------|
| read | 读取文件（只读，不执行代码） |
| message | 群聊消息回复 |
| web_search | 搜索技术文档和资料 |
| web_fetch | 获取网页内容 |
| session_status | 查看会话状态 |

⚠️ **无 exec/write/edit 权限** — 只做技术方案设计，不执行代码。

## 协作关系

| Agent | 关系 |
|-------|------|
| coder | 接收 coder 发来的需求 brief，返回方案 A |
| arch-beta | 对抗方，提供方案 B + rebuttal |

## 注意事项

- 收到 `sessions_send` 消息时，按 SOUL.md 中的格式输出方案
- 不主动发起通信，只响应 coder 的请求
- 方案中不包含硬编码的密钥、路径等敏感信息

---

_环境变了就更新这里。_
