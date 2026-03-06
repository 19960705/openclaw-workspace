#!/bin/bash
# AI 热门推文日报 - Agent Reach 版本
# 使用 Agent Reach 搜索 Twitter，无需浏览器自动化

set -e
source "$HOME/.openclaw/workspace/scripts/cron_env.sh" || true

TELEGRAM_BOT_TOKEN="8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
CHAT_ID="-1003505656701"
TOPIC_ID="2"

OBSIDIAN_NOTE="$HOME/Documents/Obsidian Vault/Keonho/AI/AI推文日报-$(date +%Y-%m-%d).md"
mkdir -p "$(dirname "$OBSIDIAN_NOTE")"

TS=$(date '+%Y-%m-%d %H:%M')

echo "=== AI Twitter Digest v2 (Agent Reach) ==="
echo "Time: $TS"

# 使用 Agent Reach 搜索 AI 相关推文
RESULTS=$(/Users/mac/.local/bin/agent-reach search-twitter "AI Claude OpenAI GPT LLM Agent OpenClaw" -n 10 2>&1)

# 生成报告
MSG="📊 AI 热门推文日报（Agent Reach）

⏰ 时间：$TS

🔥 热门话题：
$(echo "$RESULTS" | head -20)

📝 详细报告：Obsidian/AI/AI推文日报-$(date +%Y-%m-%d).md"

# 写入 Obsidian
cat > "$OBSIDIAN_NOTE" << EOF
# AI 推文日报 - $(date +%Y-%m-%d)

> 来源：Agent Reach (Twitter Search)
> 时间：$TS
> 关键词：AI, Claude, OpenAI, GPT, LLM, Agent, OpenClaw

## 搜索结果

$RESULTS

## 备注
- 使用 Agent Reach CLI 搜索 Twitter
- 无需浏览器权限，更稳定
- 下次扫描：09:00（LaunchAgent）
EOF

# 发送到 Telegram
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "message_thread_id=$TOPIC_ID" \
    -d "text=$MSG" >/dev/null

echo "--- AI Twitter Digest v2 completed at $TS ---"
