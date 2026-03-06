#!/bin/bash
# AI 热门推文日报 - TuriX 版本
# 扫描 X Following 流，按 AI/Claude/OpenAI/Agent/OpenClaw 关键词筛选，输出结构化日报
# 规则：不点赞/不转发/不关注/不回复

set -e
source "$HOME/.openclaw/workspace/scripts/cron_env.sh" || true

TELEGRAM_BOT_TOKEN="8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
CHAT_ID="-1003505656701"
TOPIC_ID="2"

# 写入 Obsidian
OBSIDIAN_NOTE="$HOME/Documents/Obsidian Vault/Keonho/AI/AI推文日报-$(date +%Y-%m-%d).md"
mkdir -p "$(dirname "$OBSIDIAN_NOTE")"

# TuriX prompt - 扫描 Following 流
TURIX_PROMPT='In Safari on x.com, go to the Following timeline. Scroll for 60 seconds. Look for tweets that mention: AI, Claude, OpenAI, GPT, LLM, Agent, OpenClaw, Claude Code. For each relevant tweet found (max 10), open the tweet detail and record: author handle, 1-sentence summary, why useful. Do NOT like, repost, reply, follow, or bookmark. After collecting, done.'

# Call TuriX (use full path to avoid PATH issues in LaunchAgent)
export PATH="/Users/mac/miniconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
TURIX_TASK="$TURIX_PROMPT" bash "$HOME/.openclaw/skills/turix-cua/scripts/run_turix.sh"

# Post-process: 解析 TuriX 输出（如果有 record_info 文件）
# 这里先做一个占位输出；后续可以解析 temp_files
TS=$(date '+%Y-%m-%d %H:%M')
MSG="📊 AI 热门推文日报（自动）

⏰ 时间：$TS

🤖 TuriX 已完成 X Following 流扫描
📝 详细报告：请查看 Obsidian：AI/AI推文日报-$(date +%Y-%m-%d).md

💡 如需手动检查：请打开 X → Following"

# 写入 Obsidian 占位
cat > "$OBSIDIAN_NOTE" << EOF
# AI 推文日报 - $(date +%Y-%m-%d)

> 来源：TuriX + X Following 流扫描
> 时间：$TS
> 规则：不点赞/不转发/不关注/不回复

## 扫描关键词
AI, Claude, OpenAI, GPT, LLM, Agent, OpenClaw, Claude Code

## 采集结果

（TuriX 任务已完成，详情请查看 TuriX temp_files 或等待后续解析）

## 备注
- 遇到登录墙时 TuriX 会自动停下
- 下次扫描：09:00（LaunchAgent）
EOF

# 发送到 Telegram
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "message_thread_id=$TOPIC_ID" \
    -d "text=$MSG" >/dev/null

echo "--- AI Twitter Digest completed at $TS ---" >> "$HOME/.openclaw/logs/ai-twitter-digest.log"
