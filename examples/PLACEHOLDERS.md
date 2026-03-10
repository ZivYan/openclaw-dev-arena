# 占位符替换清单

示例配置文件（`openclaw-config.json`）中使用占位符标记需要用户填入的字段。
**AI Agent 在帮用户配置时，必须逐个确认并替换以下占位符。**

## 必须替换的占位符

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `<YOUR_ANTHROPIC_API_KEY>` | Claude 评审模型 API Key | Anthropic 或对应代理提供商 |
| `<YOUR_OPENAI_API_KEY>` | Codex / GPT-5.4 API Key | OpenAI 或对应代理提供商 |
| `<CLAUDE_OPUS_MODEL_ID>` | Claude Opus 模型 ID | 提供商的模型列表 |
| `<CODEX_MODEL_ID>` | Codex 模型 ID | 提供商的模型列表 |
| `<GPT54_MODEL_ID>` | GPT-5.4 模型 ID | 提供商的模型列表 |
| `<YOUR_FEISHU_APP_ID>` | 飞书应用 App ID | 飞书开放平台 → 应用详情 |
| `<YOUR_FEISHU_APP_SECRET>` | 飞书应用 App Secret | 飞书开放平台 → 应用凭证 |
| `your-bot-name` | Bot 名称 | 飞书应用 → 机器人设置 |
| `ou_YOUR_OPEN_ID` | 用户的飞书 open_id | 给 Bot 发私信 → 从日志获取 |
| `oc_RD_CODER_CHAT_ID` | `rd-coder` 内部群聊 ID | 创建内部执行群聊后获取 |
| `oc_RD_SHIP_CHAT_ID` | `rd-ship` 内部群聊 ID | 创建内部交付群聊后获取 |
| `<YOUR_GATEWAY_TOKEN>` | Gateway 认证令牌 | 运行 `openssl rand -hex 24` 生成 |
| `<YOUR_BRAVE_API_KEY>` | Brave 搜索 API Key（可选） | https://brave.com/search/api/ |
| `/home/user/.openclaw/` | OpenClaw 目录路径 | 替换为你的实际路径（如 `~/.openclaw/`） |

## 替换规则

1. **尖括号占位符**（`<YOUR_xxx>`）— 必须替换为实际值
2. **模型占位符**（如 `<CLAUDE_OPUS_MODEL_ID>`）— 替换为实际模型 ID
3. **路径占位符**（`/home/user/`）— 替换为实际的用户主目录
4. **群聊 ID**（`oc_xxx`）— 创建飞书群聊后获取，格式为 `oc_` + 32位字符
5. **open_id**（`ou_xxx`）— 从飞书 API 或 Bot 日志获取，格式为 `ou_` + 32位字符
6. **默认 provider 与 baseUrl 可直接使用**：模板默认使用 `anthropic` / `openai` 和官方 API 地址；只有走代理时才需要改

## 验证

替换完成后，用以下命令验证配置中没有残留占位符：

```bash
grep -E '<YOUR_|<CLAUDE_OPUS_MODEL_ID>|<CODEX_MODEL_ID>|<GPT54_MODEL_ID>|YOUR_OPEN_ID|_CHAT_ID|/home/user/' openclaw.json
# 如果没有输出，说明全部替换完成
```

## AI Agent 操作指引

当帮用户配置时：
1. 先问用户要上面表格中的所有信息
2. 用 Python 读取示例配置 → 替换占位符 → 写入实际配置
3. 替换后运行验证命令确认无残留
4. 通过 `config.apply` 写入并重启
