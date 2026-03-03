#!/bin/bash
# Simmer 市场定时扫描脚本
# 每 30 分钟运行一次，发送到 Telegram simmer topic

# cron-safe env
source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

# keep existing python env
export PYTHONPATH="$HOME/.simmer-venv/lib/python3.14/site-packages:$PYTHONPATH"

TELEGRAM_BOT_TOKEN="8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
CHAT_ID="-1003505656701"
TOPIC_ID="6"

# 使用和 simmer-check.py 一样的方式运行扫描
RESULT=$(~/.simmer-venv/bin/python3 << 'PYEOF'
import sys
import os

# Load API key the same way as simmer-check.py
env_file = os.path.expanduser("~/.openclaw/workspace/.env.simmer")
api_key = None
venue = "polymarket"

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith("SIMMER_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
            elif line.startswith("SIMMER_VENUE="):
                venue = line.strip().split("=", 1)[1]

if not api_key:
    print("ERROR: No SIMMER_API_KEY found")
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.simmer-venv/lib/python3.14/site-packages"))
from simmer_sdk.client import SimmerClient

client = SimmerClient(api_key=api_key, venue=venue)

markets = client.get_markets(limit=50)

btc_markets = []
eth_markets = []

for m in markets:
    q = getattr(m, 'question', '').lower()
    accepting = getattr(m, 'accepting_orders', False)
    closed = getattr(m, 'closed', False)
    prob = getattr(m, 'probability', 0)
    
    if not accepting or closed:
        continue
    
    if 'bitcoin' in q or 'btc' in q:
        if 'minute' in q or 'up or down' in q:
            btc_markets.append({'q': getattr(m, 'question', ''), 'p': prob})
    elif 'ethereum' in q or 'eth' in q:
        if 'minute' in q or 'up or down' in q:
            eth_markets.append({'q': getattr(m, 'question', ''), 'p': prob})

print(f"BTC:{len(btc_markets)}|ETH:{len(eth_markets)}")
for m in btc_markets[:3]:
    print(f"BTC|{m['q'][:50]}|{m['p']*100:.1f}")
for m in eth_markets[:3]:
    print(f"ETH|{m['q'][:50]}|{m['p']*100:.1f}")
PYEOF
)

# 检查是否有错误
if echo "$RESULT" | grep -q "ERROR:"; then
    MESSAGE="🔍 Simmer 市场扫描 (自动)
    
⏰ 时间: $(date '+%H:%M')

⚠️ 扫描失败: $RESULT"
else
    # 解析结果
    BTC_COUNT=$(echo "$RESULT" | grep "^BTC:" | cut -d: -f2 | cut -d'|' -f1)
    ETH_COUNT=$(echo "$RESULT" | grep "^BTC:" | cut -d: -f2 | cut -d'|' -f2)

    # 构建消息
    if [ "$BTC_COUNT" = "0" ] && [ "$ETH_COUNT" = "0" ]; then
        MESSAGE="🔍 Simmer 市场扫描 (自动)

⏰ 时间: $(date '+%H:%M')

⚠️ 暂无可交易 BTC/ETH 5分钟市场
💡 下次扫描: 30 分钟后"
    else
        MARKETS_INFO=$(echo "$RESULT" | grep -v "^BTC:" | head -6)
        MESSAGE="🔍 Simmer 市场扫描 (自动)

⏰ 时间: $(date '+%H:%M')

🎯 找到可交易市场！
$MARKETS_INFO

💡 有机会可考虑下单（max \$1）"
    fi
fi

# 发送 Telegram 消息
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    -d "chat_id=$CHAT_ID" \
    -d "message_thread_id=$TOPIC_ID" \
    -d "text=$MESSAGE" \
    -d "parse_mode=Markdown"

echo "--- Scan complete at $(date) ---" >> ~/.openclaw/workspace/logs/simmer-scan.log
