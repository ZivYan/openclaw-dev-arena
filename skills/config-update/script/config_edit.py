#!/usr/bin/env python3
"""
OpenClaw 配置安全编辑工具

用法:
  # 查看当前 agent 列表
  python3 config_edit.py --list

  # 修改单个 agent 的模型
  python3 config_edit.py --set-model trader <provider>/<model>

  # 批量修改多个 agent 的模型
  python3 config_edit.py --set-model trader,momo <provider>/<model>

  # 修改 agent 的心跳
  python3 config_edit.py --set-heartbeat momo 30m

  # 添加新 agent（交互式）
  python3 config_edit.py --add-agent new_agent

  # 对比当前配置与备份
  python3 config_edit.py --diff

  # 验证配置完整性（不修改）
  python3 config_edit.py --validate

  # 应用修改（写入文件，不重启）
  加 --apply 参数到任何修改命令

  # 应用修改并重启 gateway
  加 --apply --restart 参数

安全机制:
  1. 自动备份（带时间戳）
  2. 修改前后 agent 数量对比，减少则阻断
  3. JSON 格式验证
  4. 关键字段完整性检查
  5. 所有 binding 引用的 agent 必须存在
"""

import json
import sys
import os
import shutil
from datetime import datetime
from pathlib import Path

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
BACKUP_DIR = os.path.expanduser("~/.openclaw/config-backups")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(config, reason="manual"):
    """安全写入配置：备份 → 验证 → 写入"""
    # 1. 备份
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"openclaw_{ts}.json")
    shutil.copy2(CONFIG_PATH, backup_path)
    print(f"📦 备份: {backup_path}")

    # 2. 验证
    errors = validate_config(config)
    if errors:
        print("❌ 验证失败，未写入:")
        for e in errors:
            print(f"  - {e}")
        return False

    # 3. 对比 agent 数量
    old_config = load_config()
    old_count = len(old_config.get("agents", {}).get("list", []))
    new_count = len(config.get("agents", {}).get("list", []))
    if new_count < old_count:
        old_ids = {a["id"] for a in old_config["agents"]["list"]}
        new_ids = {a["id"] for a in config["agents"]["list"]}
        missing = old_ids - new_ids
        print(f"🚨 Agent 数量减少! {old_count} → {new_count}")
        print(f"   丢失的 agent: {missing}")
        confirm = input("确定要继续吗? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ 已取消")
            return False

    # 4. 写入
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ 配置已写入 ({reason})")
    return True

def validate_config(config):
    """验证配置完整性"""
    errors = []

    # 基本结构
    if "agents" not in config or config.get("agents") is None:
        errors.append("agents 缺失或为空")
    elif "list" not in config.get("agents", {}) or config["agents"].get("list") is None:
        errors.append("agents.list 缺失或为空")
    if "bindings" not in config or config.get("bindings") is None:
        errors.append("bindings 缺失或为空")
    if "channels" not in config or config.get("channels") is None:
        errors.append("channels 缺失或为空")

    if errors:
        return errors

    # Agent 定义检查
    agent_ids = {a["id"] for a in config["agents"]["list"]}
    if not agent_ids:
        errors.append("agents.list 为空!")

    # 每个 agent 必须有 model
    defaults_model = config["agents"].get("defaults", {}).get("model", {}).get("primary") if config["agents"].get("defaults") else None
    for agent in config["agents"]["list"]:
        aid = agent.get("id", "unknown")
        model = agent.get("model", {}).get("primary") if agent.get("model") else None
        if not model and not defaults_model:
            errors.append(f"agent '{aid}' 无 model.primary 且无默认模型")

    # Binding 引用检查
    for binding in config.get("bindings", []):
        bid = binding.get("agentId")
        if bid not in agent_ids:
            errors.append(f"binding 引用了不存在的 agent: '{bid}'")

    # 模型引用检查（可选）
    known_providers = set(config.get("models", {}).get("providers", {}).keys())
    for agent in config["agents"]["list"]:
        model = agent.get("model", {}).get("primary", "")
        if "/" in model:
            provider = model.split("/")[0]
            if provider not in known_providers:
                errors.append(f"agent '{agent['id']}' 引用了未知 provider: '{provider}'")

    return errors

def list_agents(config):
    """显示 agent 列表"""
    print(f"\n{'ID':<15} {'Model':<30} {'Heartbeat':<10} {'Tools'}")
    print("-" * 80)
    for agent in config["agents"]["list"]:
        aid = agent["id"]
        model = agent.get("model", {}).get("primary", "(default)")
        hb = agent.get("heartbeat", {}).get("every", "-")
        tools_count = len(agent.get("tools", {}).get("allow", []))
        tools_str = f"{tools_count} tools" if tools_count else "(default)"
        print(f"{aid:<15} {model:<30} {hb:<10} {tools_str}")

    print(f"\n总计: {len(config['agents']['list'])} agents, {len(config.get('bindings', []))} bindings")

def set_model(config, agent_ids_str, model):
    """修改 agent 模型（安全方式）"""
    # 验证模型格式
    if "/" not in model:
        print(f"❌ 模型格式错误: '{model}'")
        print(f"   正确格式: provider/model (如 <provider>/<model>)")
        return config
    
    # 验证 provider 存在
    providers = config.get("models", {}).get("providers", {}).keys()
    provider = model.split("/")[0]
    if provider not in providers:
        print(f"⚠️ 警告: provider '{provider}' 未在配置中定义")
        print(f"   已配置的 providers: {list(providers)}")
    
    # 验证 agent 存在
    agent_ids = [x.strip() for x in agent_ids_str.split(",")]
    agent_map = {a["id"]: a for a in config["agents"]["list"]}

    for aid in agent_ids:
        if aid not in agent_map:
            print(f"❌ agent '{aid}' 不存在")
            return config

    for aid in agent_ids:
        old_model = agent_map[aid].get("model", {}).get("primary", "(default)")
        agent_map[aid].setdefault("model", {})["primary"] = model
        print(f"  {aid}: {old_model} → {model}")

    return config

def set_heartbeat(config, agent_id, interval):
    """修改 agent 心跳"""
    agent_map = {a["id"]: a for a in config["agents"]["list"]}
    if agent_id not in agent_map:
        print(f"❌ agent '{agent_id}' 不存在")
        return config

    agent_map[agent_id].setdefault("heartbeat", {})["every"] = interval
    print(f"  {agent_id} heartbeat → {interval}")
    return config

def diff_config(config):
    """对比当前配置与上次备份"""
    backups = sorted(Path(BACKUP_DIR).glob("openclaw_*.json")) if Path(BACKUP_DIR).exists() else []
    if not backups:
        print("无备份文件可对比")
        return

    latest_backup = backups[-1]
    with open(latest_backup) as f:
        old = json.load(f)

    old_ids = {a["id"] for a in old.get("agents", {}).get("list", [])}
    new_ids = {a["id"] for a in config.get("agents", {}).get("list", [])}

    added = new_ids - old_ids
    removed = old_ids - new_ids

    print(f"\n对比: 当前 vs {latest_backup.name}")
    print(f"  Agents: {len(old_ids)} → {len(new_ids)}")
    if added:
        print(f"  ➕ 新增: {added}")
    if removed:
        print(f"  ❌ 删除: {removed}")

    # 模型变化
    old_models = {a["id"]: a.get("model", {}).get("primary", "") for a in old.get("agents", {}).get("list", [])}
    new_models = {a["id"]: a.get("model", {}).get("primary", "") for a in config.get("agents", {}).get("list", [])}
    for aid in old_ids & new_ids:
        if old_models.get(aid) != new_models.get(aid):
            print(f"  🔄 {aid}: {old_models.get(aid)} → {new_models.get(aid)}")

    if not added and not removed:
        changes = sum(1 for aid in old_ids & new_ids if old_models.get(aid) != new_models.get(aid))
        if not changes:
            print("  无 agent 变化")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="OpenClaw 配置安全编辑工具")
    parser.add_argument("--list", action="store_true", help="列出所有 agent")
    parser.add_argument("--validate", action="store_true", help="验证配置")
    parser.add_argument("--diff", action="store_true", help="对比配置变化")
    parser.add_argument("--set-model", nargs=2, metavar=("AGENTS", "MODEL"), help="修改模型 (逗号分隔多个 agent)")
    parser.add_argument("--set-heartbeat", nargs=2, metavar=("AGENT", "INTERVAL"), help="修改心跳")
    parser.add_argument("--apply", action="store_true", help="应用修改")
    parser.add_argument("--restart", action="store_true", help="应用后重启 gateway")
    args = parser.parse_args()

    config = load_config()

    if args.list:
        list_agents(config)
        return

    if args.validate:
        errors = validate_config(config)
        if errors:
            print("❌ 验证失败:")
            for e in errors:
                print(f"  - {e}")
        else:
            agent_count = len(config["agents"]["list"])
            binding_count = len(config.get("bindings", []))
            print(f"✅ 配置验证通过 (agents: {agent_count}, bindings: {binding_count})")
        return

    if args.diff:
        diff_config(config)
        return

    modified = False

    if args.set_model:
        config = set_model(config, args.set_model[0], args.set_model[1])
        modified = True

    if args.set_heartbeat:
        config = set_heartbeat(config, args.set_heartbeat[0], args.set_heartbeat[1])
        modified = True

    if modified and args.apply:
        reason = " ".join(sys.argv[1:])
        if save_config(config, reason):
            if args.restart:
                print("🔄 重启 gateway...")
                os.system("openclaw gateway restart")
        return

    if modified and not args.apply:
        print("\n⚠️ 预览模式，加 --apply 写入，加 --apply --restart 写入并重启")

    if not any([args.list, args.validate, args.diff, args.set_model, args.set_heartbeat]):
        parser.print_help()

if __name__ == "__main__":
    main()
