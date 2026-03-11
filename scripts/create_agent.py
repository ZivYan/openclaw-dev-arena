#!/usr/bin/env python3
"""
创建对抗式研发流子 Agent 的完整脚本。

用法:
  python3 create_agent.py \
    --agent-id coder \
    --agent-name "Coder" \
    --role "代码开发助手" \
    --emoji "💻" \
    --user-name "YourName" \
    --preset coder

  python3 create_agent.py \
    --agent-id myagent \
    --agent-name "MyAgent" \
    --role "自定义角色描述" \
    --emoji "🤖" \
    --user-name "YourName" \
    --tools exec,read,write,edit,message,web_search

可选参数:
  --app-id        飞书 App ID（创建群聊用，不传则跳过）
  --app-secret    飞书 App Secret
  --user-open-id  用户的飞书 open_id（拉入群聊用）
  --model         模型 ID（默认用配置中的 defaults）
  --workspace-base  workspace 基础目录（默认 ~/.openclaw）
  --preset        预设角色（momo/orchestrator/coder/arch-alpha/arch-beta）
                  有 examples/ 模板的 preset（如 coder）会优先复制完整模板文件
  --tools         逗号分隔的工具列表（覆盖 preset）
  --skip-chat     跳过创建飞书群聊
  --skip-config   跳过修改 openclaw.json（只创建 workspace）
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ============================================================
# 预设角色配置
# ============================================================
# examples/ 目录中有完整模板的 preset，脚本会优先复制模板文件
# 没有模板的 preset 使用下面的配置自动生成
PRESETS = {
    "momo": {
        "tools": ["exec", "read", "write", "edit", "message",
                  "web_search", "web_fetch", "session_status", "cron", "browser",
                  "sessions_list", "sessions_history", "sessions_send",
                  "feishu_doc", "feishu_perm", "tts"],
        "template": "momo-agent",  # 指向 examples/momo-agent/
        "soul_core": "你是用户的私人 AI 助手。日常对话、信息查询、轻量任务由你直接完成；研发类任务委派给 orchestrator。",
        "soul_principles": [
            "用户优先 — 快速响应，简洁有用",
            "能自己做的不委派 — 查资料、聊天、轻量任务直接完成",
            "研发任务交给 orchestrator — 涉及编码、方案设计、MR 的任务委派",
            "三次失败就停，换方案或上报",
        ],
    },
    "orchestrator": {
        "tools": ["exec", "read", "write", "edit", "message",
                  "web_search", "web_fetch", "session_status", "cron", "browser",
                  "gateway", "sessions_list", "sessions_history", "sessions_send",
                  "sessions_spawn", "feishu_doc", "feishu_perm"],
        "template": "orchestrator-agent",  # 指向 examples/orchestrator-agent/
        "soul_core": "你是对抗式研发流的协调者。你的核心价值是任务拆解、派发和进度跟踪，不是执行。",
        "soul_principles": [
            "最大化委托，最小化亲力亲为",
            "绝不代替子 Agent 执行任务",
            "异步派发，立刻响应，心跳跟进",
            "三次失败就停，换方案或上报",
        ],
    },
    "coder": {
        "tools": ["exec", "read", "write", "edit", "message",
                  "web_search", "web_fetch", "session_status", "browser",
                  "sessions_list", "sessions_history", "sessions_send",
                  "feishu_doc", "feishu_perm"],
        "template": "coder-agent",  # 指向 examples/coder-agent/
        "soul_core": "你是研发流程的主驱动者。负责从需求到交付的全流程：需求理解、驱动对抗式方案设计、编码实现、自测、Code Review、提交 MR、提测归档。",
        "soul_principles": [
            "流程不可跳过，8 个 Phase 按顺序推进",
            "技术方案通过 arch-alpha 和 arch-beta 对抗产出",
            "原子化开发，每个任务 ≤ 2h，一个任务一个 commit",
            "进度透明，每完成一个任务群聊通知详细进度",
        ],
    },
    "arch-alpha": {
        "tools": ["read", "message", "web_search", "web_fetch", "session_status"],
        "template": "arch-alpha-agent",  # 指向 examples/arch-alpha-agent/
        "soul_core": "你是技术方案架构师 A（守正）。为每个研发需求提供独立的技术方案，与 arch-beta 对抗产出最优解。",
        "soul_principles": [
            "稳健优先，选择经过验证的技术路径",
            "方案必须涵盖接口设计、数据流、错误处理、兼容性",
            "承认合理质疑，补充遗漏，用数据反驳不合理部分",
            "目标是收敛到最优解，不是无限争论",
        ],
    },
    "arch-beta": {
        "tools": ["read", "message", "web_search", "web_fetch", "session_status"],
        "template": "arch-beta-agent",  # 指向 examples/arch-beta-agent/
        "soul_core": "你是技术方案挑战者 B（破局）。提供差异化技术方案，对 arch-alpha 的方案进行 rebuttal，通过对抗产出最优解。",
        "soul_principles": [
            "差异化思考，故意选择不同技术路径",
            "挑战假设，质疑理所当然的选择",
            "质疑有依据，每个 rebuttal 点有具体技术论据",
            "目标是收敛到最优解，可以妥协和承认对方优势",
        ],
    },
}


def create_workspace(base_dir: Path, agent_id: str) -> Path:
    """创建 Agent workspace 目录结构"""
    ws = base_dir / f"workspace-{agent_id}"
    (ws / "memory").mkdir(parents=True, exist_ok=True)
    (ws / "skills").mkdir(parents=True, exist_ok=True)
    print(f"✅ Workspace 创建: {ws}")
    return ws


def create_identity(ws: Path, agent_id: str, agent_name: str,
                     role: str, emoji: str, user_name: str):
    """生成 IDENTITY.md"""
    content = f"""# IDENTITY.md

- **Name:** {agent_id}
- **Creature:** {user_name}的{role}
- **Vibe:** 专业可靠
- **Emoji:** {emoji}
"""
    (ws / "IDENTITY.md").write_text(content, encoding="utf-8")
    print(f"✅ IDENTITY.md 创建")


def create_soul(ws: Path, agent_id: str, agent_name: str,
                role: str, user_name: str, preset: dict | None):
    """生成 SOUL.md"""
    if preset:
        core = preset["soul_core"]
        principles = "\n".join(f"- **{p.split('，')[0]}** — {'，'.join(p.split('，')[1:]) if '，' in p else p}"
                               for p in preset["soul_principles"])
    else:
        core = f"你是一位专业的{role}。为{user_name}提供高质量的服务。"
        principles = "- 简洁高效\n- 数据驱动\n- 安全第一"

    content = f"""# SOUL.md - {agent_name}

## 核心

{core}

## 原则

{principles}

## 工作目录

你的工作目录是 `{ws}`。所有文件操作在此目录下进行。
**严禁访问其他 Agent 的 workspace。**

## 风格

- 中文为主，技术术语可用英文
- 简洁直接，不废话
- 数据用列表呈现

## 消息限制

- 只在你的专属群聊里回复
- 不主动向其他群聊发消息

## 🔒 安全底线

- 严禁读取其他 Agent 的 workspace
- 禁止访问敏感目录（`~/.ssh/`、`~/.env`）
- 重大操作前告知用户

## 飞书消息格式

飞书消息使用富文本格式：**加粗**、*斜体*、`代码`、代码块、列表。
❌ 禁止使用：LaTeX 数学公式、Markdown 表格、Unicode 数学符号。
"""
    (ws / "SOUL.md").write_text(content, encoding="utf-8")
    print(f"✅ SOUL.md 创建")


def create_agents_md(ws: Path):
    """生成 AGENTS.md"""
    content = """# AGENTS.md

## 每次醒来

1. 读 `SOUL.md` — 你是谁
2. 读 `memory/` 最近的日记 — 最近发生了什么

## 记忆

- 日记写在 `memory/YYYY-MM-DD.md`
- 重要的事情写下来，不要靠"记住"

## 安全

- 不外泄私人数据
- 破坏性操作先确认
- `trash` > `rm`
"""
    (ws / "AGENTS.md").write_text(content, encoding="utf-8")
    print(f"✅ AGENTS.md 创建")


def create_feishu_chat(app_id: str, app_secret: str,
                        agent_name: str, user_open_id: str | None) -> str | None:
    """通过飞书 API 创建群聊，返回 chat_id"""
    # Step 1: 获取 token
    token_resp = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({"app_id": app_id, "app_secret": app_secret})],
        capture_output=True, text=True
    )
    try:
        token_data = json.loads(token_resp.stdout)
        token = token_data["tenant_access_token"]
    except (json.JSONDecodeError, KeyError):
        print(f"❌ 获取飞书 token 失败: {token_resp.stdout[:200]}")
        return None

    # Step 2: 创建群聊
    chat_resp = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "https://open.feishu.cn/open-apis/im/v1/chats",
         "-H", f"Authorization: Bearer {token}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({
             "name": f"{agent_name} 助手",
             "chat_mode": "group",
             "chat_type": "private"
         })],
        capture_output=True, text=True
    )
    try:
        chat_data = json.loads(chat_resp.stdout)
        if chat_data.get("code") != 0:
            print(f"❌ 创建群聊失败: {chat_data.get('msg', 'unknown error')}")
            return None
        chat_id = chat_data["data"]["chat_id"]
        print(f"✅ 飞书群聊创建: {chat_id}")
    except (json.JSONDecodeError, KeyError):
        print(f"❌ 解析群聊响应失败: {chat_resp.stdout[:200]}")
        return None

    # Step 3: 添加用户到群
    if user_open_id:
        add_resp = subprocess.run(
            ["curl", "-s", "-X", "POST",
             f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members",
             "-H", f"Authorization: Bearer {token}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps({"id_list": [user_open_id]})],
            capture_output=True, text=True
        )
        try:
            add_data = json.loads(add_resp.stdout)
            if add_data.get("code") == 0:
                print(f"✅ 用户 {user_open_id} 已加入群聊")
            else:
                print(f"⚠️ 添加用户失败: {add_data.get('msg')}")
        except json.JSONDecodeError:
            print(f"⚠️ 解析添加成员响应失败")

    return chat_id


def update_openclaw_config(config_path: Path, agent_id: str, agent_name: str,
                            workspace: Path, chat_id: str | None,
                            tools: list[str], model: str | None):
    """更新 openclaw.json，添加新 Agent 和 Binding"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 检查是否已存在
    existing_ids = [a["id"] for a in config["agents"]["list"]]
    if agent_id in existing_ids:
        print(f"⚠️ Agent '{agent_id}' 已存在于配置中，跳过")
        return

    # 构造 Agent 配置
    agent_config = {
        "id": agent_id,
        "name": agent_name,
        "workspace": str(workspace),
    }
    if model:
        agent_config["model"] = {"primary": model}
    if tools:
        agent_config["tools"] = {"allow": tools}

    config["agents"]["list"].append(agent_config)
    print(f"✅ Agent '{agent_id}' 已添加到 agents.list（共 {len(config['agents']['list'])} 个）")

    # 添加 Binding
    if chat_id:
        binding = {
            "agentId": agent_id,
            "match": {
                "channel": "feishu",
                "accountId": "default",
                "peer": {"kind": "group", "id": chat_id}
            }
        }
        config["bindings"].append(binding)
        print(f"✅ Binding 已添加: {agent_id} → {chat_id}")

        # 添加 groups 配置
        if "groups" not in config["channels"]["feishu"]:
            config["channels"]["feishu"]["groups"] = {}
        config["channels"]["feishu"]["groups"][chat_id] = {
            "enabled": True,
            "requireMention": False
        }
        print(f"✅ 群聊配置已添加")

    # 验证
    assert len(config["agents"]["list"]) >= 1, "agents.list 为空！"
    assert "bindings" in config, "bindings 缺失！"

    # 备份并写入
    backup_path = config_path.with_suffix(".json.bak")
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(json.loads(config_path.read_text()), f, indent=2, ensure_ascii=False)
    print(f"✅ 配置备份: {backup_path}")

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ 配置写入: {config_path}")
    print(f"⚡ 请运行 'openclaw gateway restart' 使配置生效")


def main():
    parser = argparse.ArgumentParser(description="创建对抗式研发流子 Agent")
    parser.add_argument("--agent-id", required=True, help="Agent ID（英文小写，如 coder）")
    parser.add_argument("--agent-name", help="Agent 显示名称（如 Coder），默认取 agent-id 首字母大写")
    parser.add_argument("--role", required=True, help="角色描述（如 '代码开发助手'）")
    parser.add_argument("--emoji", default="🤖", help="Agent emoji")
    parser.add_argument("--user-name", required=True, help="用户名称")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="预设角色")
    parser.add_argument("--tools", help="逗号分隔的工具列表（覆盖 preset）")
    parser.add_argument("--model", help="模型 ID")
    parser.add_argument("--app-id", help="飞书 App ID")
    parser.add_argument("--app-secret", help="飞书 App Secret")
    parser.add_argument("--user-open-id", help="用户飞书 open_id")
    parser.add_argument("--workspace-base", default=os.path.expanduser("~/.openclaw"),
                        help="workspace 基础目录")
    parser.add_argument("--skip-chat", action="store_true", help="跳过创建飞书群聊")
    parser.add_argument("--skip-config", action="store_true", help="跳过修改 openclaw.json")
    args = parser.parse_args()

    base_dir = Path(args.workspace_base)
    agent_name = args.agent_name or args.agent_id.capitalize()
    preset = PRESETS.get(args.preset) if args.preset else None

    # 解析工具列表
    if args.tools:
        tools = [t.strip() for t in args.tools.split(",")]
    elif preset:
        tools = preset["tools"]
    else:
        tools = ["read", "message", "web_search", "web_fetch", "session_status"]

    print(f"\n{'='*50}")
    print(f"创建 Agent: {agent_name} ({args.agent_id})")
    print(f"角色: {args.role}")
    print(f"工具: {', '.join(tools)}")
    print(f"{'='*50}\n")

    # Step 1: 创建 Workspace
    ws = create_workspace(base_dir, args.agent_id)

    # Step 2: 创建身份文件
    # 如果 preset 有 template，优先从 examples/ 复制完整模板
    template_dir = None
    if preset and preset.get("template"):
        # 查找 examples/ 目录（相对于脚本位置）
        script_dir = Path(__file__).resolve().parent
        template_dir = script_dir.parent / "examples" / preset["template"]
        if not template_dir.exists():
            template_dir = None  # 找不到就 fallback 到自动生成

    if template_dir:
        # 复制模板文件和子目录（不覆盖已存在的文件/目录）
        copied = []
        for src_item in template_dir.iterdir():
            if src_item.name == "README.md":
                continue  # README 是给项目看的，不需要复制到 workspace
            dst_item = ws / src_item.name
            if src_item.is_file() and src_item.suffix == ".md":
                if not dst_item.exists():
                    shutil.copy2(src_item, dst_item)
                    copied.append(src_item.name)
            elif src_item.is_dir():
                # 递归复制子目录（如 skills/）
                if not dst_item.exists():
                    shutil.copytree(src_item, dst_item)
                    copied.append(f"{src_item.name}/")
        print(f"✅ 从模板 {preset['template']} 复制: {', '.join(copied) or '(已存在，跳过)'}")
    else:
        create_identity(ws, args.agent_id, agent_name, args.role, args.emoji, args.user_name)
        create_soul(ws, args.agent_id, agent_name, args.role, args.user_name, preset)
        create_agents_md(ws)

    # Step 3: 创建飞书群聊
    chat_id = None
    if not args.skip_chat and args.app_id and args.app_secret:
        chat_id = create_feishu_chat(args.app_id, args.app_secret,
                                      agent_name, args.user_open_id)
    elif not args.skip_chat:
        print("⚠️ 未提供 --app-id 和 --app-secret，跳过创建飞书群聊")
        print("   你可以手动创建群聊，然后把 chat_id 填入 openclaw.json")

    # Step 4: 更新 OpenClaw 配置
    if not args.skip_config:
        config_path = base_dir / "openclaw.json"
        if config_path.exists():
            update_openclaw_config(config_path, args.agent_id, agent_name,
                                    ws, chat_id, tools, args.model)
        else:
            print(f"⚠️ 配置文件不存在: {config_path}")
            print("   请先安装并初始化 OpenClaw")

    # 汇总
    print(f"\n{'='*50}")
    print(f"✅ Agent '{args.agent_id}' 创建完成！")
    print(f"")
    print(f"Workspace: {ws}")
    if chat_id:
        print(f"群聊 ID:   {chat_id}")
    print(f"")
    print(f"下一步:")
    if not args.skip_config:
        print(f"  1. openclaw gateway restart")
        print(f"  2. 在飞书群聊中发送一条消息测试")
    else:
        print(f"  1. 将 Agent 配置添加到 openclaw.json")
        print(f"  2. openclaw gateway restart")
        print(f"  3. 在飞书群聊中发送一条消息测试")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
