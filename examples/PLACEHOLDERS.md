# 占位符替换清单

示例配置文件（`openclaw-config.json`）和 Agent 模板中使用占位符标记需要用户填入的字段。
**AI Agent 在帮用户配置时，必须逐个确认并替换以下占位符。**

## 必须替换的占位符

### 模型配置

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `<YOUR_API_KEY>` | LLM 模型 API Key | 模型提供商（如 OpenAI、Anthropic、火山引擎等） |
| `your-provider` | 模型提供商 ID | 自定义名称，如 `openai`、`anthropic`、`ark` |
| `your-model-id` | 模型 ID | 提供商的模型列表 |
| `your-model-name` | 模型显示名称 | 同上 |
| `your-api-endpoint` | 模型 API 地址 | 提供商文档 |
| `fallback-provider/fallback-model` | 备用模型（可选） | 可删除或替换为实际模型 |

### 飞书应用

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `<YOUR_FEISHU_APP_ID>` | 飞书应用 App ID | 飞书开放平台 → 应用详情 |
| `<YOUR_FEISHU_APP_SECRET>` | 飞书应用 App Secret | 飞书开放平台 → 应用凭证 |
| `your-bot-name` | Bot 名称 | 飞书应用 → 机器人设置 |
| `ou_YOUR_OPEN_ID` | 用户的飞书 open_id | 给 Bot 发私信 → 从日志获取 |

### 群聊 ID（部署 Agent 后自动获取）

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `oc_CODER_CHAT_ID` | Coder Agent 群聊 ID | `create_agent.py --preset coder` 创建后获取 |
| `oc_ARCH_ALPHA_CHAT_ID` | arch-alpha Agent 群聊 ID | `create_agent.py --preset arch-alpha` 创建后获取 |
| `oc_ARCH_BETA_CHAT_ID` | arch-beta Agent 群聊 ID | `create_agent.py --preset arch-beta` 创建后获取 |

### 飞书文档归档（coder Agent TOOLS.md 中使用）

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `<YOUR_WIKI_SPACE_ID>` | 飞书 Wiki 空间 ID | 飞书知识库 → 空间设置 → 空间 ID |
| `<YOUR_WIKI_FOLDER_TOKEN>` | Wiki 目录 Token | 飞书知识库 → 目录页面 URL 中的 token |

### Codebase 配置（coder Agent TOOLS.md 中使用）

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `<YOUR_REPO>` | 代码仓库标识 | Codebase 仓库设置页面 |

### 基础设施

| 占位符 | 说明 | 从哪里获取 |
|--------|------|-----------|
| `<YOUR_GATEWAY_TOKEN>` | Gateway 认证令牌 | 运行 `openssl rand -hex 24` 生成 |
| `<YOUR_BRAVE_API_KEY>` | Brave 搜索 API Key（可选） | https://brave.com/search/api/ |
| `/home/user/.openclaw/` | OpenClaw 目录路径 | 替换为你的实际路径（如 `~/.openclaw/`） |

## 替换规则

1. **尖括号占位符**（`<YOUR_xxx>`）— 必须替换为实际值
2. **描述性占位符**（`your-provider`、`your-model-id`）— 替换为实际的提供商/模型 ID
3. **路径占位符**（`/home/user/`）— 替换为实际的用户主目录
4. **群聊 ID**（`oc_xxx`）— 创建飞书群聊后获取，格式为 `oc_` + 32位字符
5. **open_id**（`ou_xxx`）— 从飞书 API 或 Bot 日志获取，格式为 `ou_` + 32位字符

## 验证

替换完成后，用以下命令验证配置中没有残留占位符：

```bash
grep -E '<YOUR_|your-provider|your-model|YOUR_OPEN_ID|_CHAT_ID|/home/user/' openclaw.json
# 如果没有输出，说明全部替换完成
```

## AI Agent 操作指引

当帮用户配置时：
1. 先问用户要上面表格中的所有信息
2. 用 Python 读取示例配置 → 替换占位符 → 写入实际配置
3. 替换后运行验证命令确认无残留
4. 通过 `config.apply` 写入并重启
