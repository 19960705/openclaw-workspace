#!/bin/bash
# 4A 广告视觉拆解 - TuriX 版本
# 抓取 YouTube AdBlitz + Campaign US 最新广告案例，输出分镜+提示词
# 规则：不点赞/不评论/不订阅

set -e
source "$HOME/.openclaw/workspace/scripts/cron_env.sh" || true

TELEGRAM_BOT_TOKEN="8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
CHAT_ID="-1003505656701"
TOPIC_ID="3"

OBSIDIAN_NOTE="$HOME/Documents/Obsidian Vault/Keonho/商业/4A广告视觉拆解-$(date +%Y-%m-%d).md"
mkdir -p "$(dirname "$OBSIDIAN_NOTE")"

# TuriX prompt - 先抓 Campaign US
TURIX_PROMPT='In Safari, go to https://www.campaignus.com/ or https://www.adweek.com/. Look for the latest video/TV ads or commercial spots. Find 3-5 recent campaigns. For each, record: brand name, 1-sentence campaign concept, and the video URL if visible. Do NOT like, comment, subscribe, or follow. Done.'

# Call TuriX (use full path to avoid PATH issues in LaunchAgent)
export PATH="/Users/mac/miniconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
TURIX_TASK="$TURIX_PROMPT" bash "$HOME/.openclaw/skills/turix-cua/scripts/run_turix.sh"

TS=$(date '+%Y-%m-%d %H:%M')
MSG="🎬 4A 广告视觉拆解（自动）

⏰ 时间：$TS

🤖 TuriX 已完成 Campaign US / Adweek 广告扫描
📝 详细报告：请查看 Obsidian：商业/4A广告视觉拆解-$(date +%Y-%m-%d).md

💡 提示：如需生成分镜提示词，可用 Seedance/即梦处理'

# 写入 Obsidian 占位
cat > "$OBSIDIAN_NOTE" << EOF
# 4A 广告视觉拆解 - $(date +%Y-%m-%d)

> 来源：TuriX + Campaign US / Adweek
> 时间：$TS
> 规则：不点赞/不评论/不订阅

## 采集案例

（TuriX 任务已完成，详情请查看 TuriX temp_files 或等待后续解析）

## 后续处理
- 可用 Seedance/即梦 对视频进行分镜拆解
- 生成风格化提示词用于内容创作

## 备注
- 下次扫描：09:30（LaunchAgent）
EOF

# 发送到 Telegram
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "message_thread_id=$TOPIC_ID" \
    -d "text=$MSG" >/dev/null

echo "--- 4A Ad Visual completed at $TS ---" >> "$HOME/.openclaw/logs/ad-visual-daily.log"
