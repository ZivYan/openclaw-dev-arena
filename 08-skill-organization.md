# 08 - Skill 安装与目录组织

## 安装方式

推荐将整个仓库作为一个根 Skill 安装：

```bash
mkdir -p ~/.openclaw/skills
cp -r feishu-multi-agent ~/.openclaw/skills/single-agent-multi-role-rd
```

或：

```bash
git clone git@github.com:ZivYan/feishu-multi-agent.git ~/.openclaw/skills/single-agent-multi-role-rd
```

## 目录约定

```text
single-agent-multi-role-rd/
├── SKILL.md
├── INDEX.md
├── 01-11 *.md
├── AGENTS.md
├── scripts/
├── examples/
└── skills/
```

## 推荐角色目录

如果要在 OpenClaw 中按三角色落地，建议准备三个 workspace：

```text
~/.openclaw/
├── workspace-rd-lead/
├── workspace-rd-coder/
└── workspace-rd-ship/
```

其中：

- `rd-lead` 负责对外入口与裁决
- `rd-coder` 负责编码与自测
- `rd-ship` 负责复核与交付

## 建议读取策略

- 首次进入：只读 `SKILL.md`、`INDEX.md`、`01-03`、`10`
- 进入实现阶段：再读 `05-07`、`09`
- 遇到阻塞：再读 `11`

## 兼容说明

- `examples/`：保留为历史参考素材
- `skills/`：保留为兼容资料，不作为主入口
- 根目录 `SKILL.md` 是当前唯一主入口
