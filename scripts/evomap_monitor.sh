#!/bin/bash
# EvoMap Keyword Monitor
# 监控特定领域的 Capsule，自动推送通知

# 配置
SENDER_ID="hub_0f978bbe1fb5"
KEYWORDS=("openclaw" "telegram" "agent" "automation" "memory" "retry")
OUTPUT_FILE="$HOME/.openclaw/workspace/data/evomap_monitoring.json"
LOG_FILE="$HOME/.openclaw/workspace/logs/evomap_monitor.log"

# 创建目录
mkdir -p "$(dirname "$OUTPUT_FILE")"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 发送请求到 EvoMap
fetch_capsules() {
    local keyword="$1"
    
    curl -s -X POST "https://evomap.ai/a2a/fetch" \
        -H "Content-Type: application/json" \
        -d "{
            \"protocol\": \"gep-a2a\",
            \"protocol_version\": \"1.0.0\",
            \"message_type\": \"fetch\",
            \"message_id\": \"msg_$(date +%s)_${keyword}\",
            \"sender_id\": \"$SENDER_ID\",
            \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
            \"payload\": {
                \"asset_type\": \"Capsule\",
                \"query\": \"$keyword\",
                \"limit\": 5
            }
        }"
}

# 检查关键词，返回新 Capsule
check_keyword() {
    local keyword="$1"
    local last_checked="$2"
    
    local result=$(fetch_capsules "$keyword")
    
    # 解析结果
    echo "$result" | python3 -c "
import json, sys, os
from datetime import datetime

data = json.load(sys.stdin)
results = data.get('payload', {}).get('results', [])

# 读取上次检查记录
last_file = os.environ.get('LAST_FILE', '/tmp/last_checked_' + sys.argv[1])
last_known = {}
if os.path.exists(last_file):
    with open(last_file, 'r') as f:
        last_known = json.load(f)

new_count = 0
for r in results:
    asset_id = r.get('asset_id', '')
    if asset_id not in last_known:
        new_count += 1
        p = r.get('payload', {})
        print(f\"[{sys.argv[1]}] NEW: {p.get('summary', '')[:80]}... (GDI: {r.get('gdi_score', 'N/A')})\")
        
        # 保存 asset_id
        last_known[asset_id] = datetime.now().isoformat()

# 保存状态
with open(last_file, 'w') as f:
    json.dump(last_known, f)

if new_count == 0:
    print(f\"[{sys.argv[1]}] No new capsules\")
" "$keyword" 2>/dev/null
}

# 主循环
main() {
    log "EvoMap Keyword Monitor Started"
    log "Monitoring keywords: ${KEYWORDS[*]}"
    
    while true; do
        for keyword in "${KEYWORDS[@]}"; do
            log "Checking keyword: $keyword"
            check_keyword "$keyword"
        done
        
        log "Cycle complete, waiting 1 hour..."
        sleep 3600  # 每小时检查一次
    done
}

# 单次运行（不带参数）
if [ "$1" == "once" ]; then
    for keyword in "${KEYWORDS[@]}"; do
        echo "=== Checking: $keyword ==="
        fetch_capsules "$keyword" | python3 -c "
import json, sys
data = json.load(sys.stdin)
results = data.get('payload', {}).get('results', [])
for r in results:
    p = r.get('payload', {})
    print(f\"GDI: {r.get('gdi_score', 'N/A')} | {p.get('summary', '')[:100]}...\")
" 2>/dev/null
        echo ""
    done
else
    main
fi
