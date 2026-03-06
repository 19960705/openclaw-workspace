#!/bin/bash
# Simmer opportunities（LaunchAgent 入口：每日 01:00）
# 发送到 Telegram simmer topic

set -e

source "$HOME/.openclaw/workspace/scripts/cron_env.sh" || true

TELEGRAM_BOT_TOKEN="8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
CHAT_ID="-1003505656701"
TOPIC_ID="6"

OUT=$(python3 "$HOME/.openclaw/workspace/scripts/simmer-check.py" opportunities 2>&1 || true)

# Build short message
TS=$(date '+%Y-%m-%d %H:%M')
if echo "$OUT" | grep -q '"error"'; then
  MSG="🔍 Simmer 机会扫描（每日）\n\n⏰ 时间：$TS\n\n⚠️ 扫描失败：$OUT"
else
  # keep it short; raw json is ok for now
  MSG="🔍 Simmer 机会扫描（每日）\n\n⏰ 时间：$TS\n\n$OUT"
fi

curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=$CHAT_ID" \
  -d "message_thread_id=$TOPIC_ID" \
  -d "text=$MSG" >/dev/null

echo "--- $TS ---" >> "$HOME/.openclaw/logs/simmer-opportunities.log"
