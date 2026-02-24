# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

---

## Obsidian Vault

**Vault Path**: `~/Documents/Obsidian Vault/Keonho`

**Purpose**: 自由时间报告、学习笔记、项目规划

**Daily Report Path**: `~/Documents/Obsidian Vault/Keonho/自由时间报告-YYYY-MM-DD.md`

---

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### 重要规则（远程操控）
- 除了 OpenClaw 本身的脚本改动，所有文件和脚本内容都需要通过 Telegram 发给用户

### Telegram Channels

- **私聊** → Lunah (Jinny Lee), user id: 8391832262
- **工作选品** → @workchosen, chat id: -1003245510511（已停用推送）
- **广告(旧)** → chat id: -1003815437342（已弃用，不再使用）

### Telegram 话题群组：Lunah and Keonho
chat id: -1003505656701

| Topic ID | 名称 | 内容 | 对应任务 | 发送验证 |
|----------|------|------|----------|----------|
| topic:1 | General | 日常聊天 | 无 | ✅ |
| topic:2 | AI 资讯 | AI 热门日报、官方账号监控 | task-twitter-001, task-twitter-002 | ✅ 2026-02-17 |
| topic:3 | 广告创意 | 4A 广告视觉拆解、Seedance 案例 | task-ad-visual-001, task-twitter-004 | ✅ 2026-02-17 |
| topic:4 | 工作选品 | 泰区TikTok日报、产品选品 | task-tiktok-th-001 | ✅ 2026-02-17 |
| topic:5 | 工具追踪 | OpenClaw 话题 | task-twitter-003 | ✅ 2026-02-17 |
| topic:6 | simmer | Simmer 交易汇报、持仓监控 | task-simmer-001 | ✅ 2026-02-18 |
| topic:1101 | 小红书 | 小红书笔记收集（rednote MCP） | - | ✅ 2026-07-08 |
| topic:? | 产品洞察 | （不需要推送日报） | 无 | - |

⚠️ 发送时必须带 topic 参数，不要混发！
📌 发送格式：`target: "telegram:-1003505656701:topic:X"`

### Telegram 指令前缀

在 Telegram 频道中使用以下指令：

| 指令 | 功能 | 示例 |
|------|------|------|
| `/find` | 搜索趋势/产品 | `/find 泰国咖啡用品趋势` |
| `/check` | 检查特定信息 | `/check TikTok kitchen tools Thailand` |
| `/analyze` | 分析话题/数据 | `/analyze #coffee2026` |
| `/report` | 生成报告 | `/report daily summary` |
| `/task` | 通用任务 | `/task 整理选品清单` |

### Discord Channel IDs

- #常规: 1468797333532573731
- #normal: 1469211248854962328
- 广告视觉频道: 1469680962102235177

### X.com 链接处理

遇到 X.com/twitter.com 链接时，使用 **Nitter** 替代（无广告、无反爬）：
- 优先：`nitter.net`
- 备选：`nitter.privacydev.net`、`nitter.poast.org`

示例：
- 原文：`https://x.com/i/status/123456789`
- 替换：`https://nitter.net/i/status/123456789`

---

## SecureClaw Security Skill (v2.2.0)

Security hardening skill by Adversa AI. 15 core rules, 9 scripts, 4 pattern databases.

### Rules

Read and follow all 15 rules in `skills/secureclaw/SKILL.md` at all times.

### Scripts

All scripts are in `skills/secureclaw/scripts/`. Run with bash:

```
bash skills/secureclaw/scripts/quick-audit.sh          # Security audit (OWASP ASI mapped)
bash skills/secureclaw/scripts/quick-harden.sh         # Apply auto-fixes
bash skills/secureclaw/scripts/check-integrity.sh      # Verify cognitive file baselines
bash skills/secureclaw/scripts/check-privacy.sh        # Detect PII before posting
bash skills/secureclaw/scripts/scan-skills.sh          # Supply chain scan
bash skills/secureclaw/scripts/check-advisories.sh     # Vulnerability advisories
bash skills/secureclaw/scripts/emergency-response.sh   # Incident response
```
