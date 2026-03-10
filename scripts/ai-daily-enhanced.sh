#!/bin/bash
# ai-daily-enhanced.sh - Enhanced AI Daily Report with importance analysis
# Version: 1.1 - 2026-03-11
# Purpose: Add "why this matters" analysis to AI daily reports

set -euo pipefail

# Configuration
TELEGRAM_CHAT_ID="-1003505656701"
TELEGRAM_TOPIC_ID="2"

# Function: Analyze importance of news items using subagent
analyze_importance() {
    local news_items="$1"
    
    # Create a temporary file for the subagent task
    local task_file=$(mktemp)
    cat > "$task_file" <<EOF
你是一个 AI 行业分析专家。请为以下 AI 新闻添加「重要性分析」。

新闻列表：
$news_items

要求：
1. 为每条新闻添加一行「💡 重要性：」说明（20-30字）
2. 解释为什么这条新闻值得关注
3. 保持简洁、有洞察力
4. 使用中文

输出格式：
📰 [新闻标题]
💡 重要性：[一句话说明为什么重要]

请开始分析：
EOF
    
    local task=$(cat "$task_file")
    rm "$task_file"
    
    # Use Python to call the analysis (simpler than bash JSON handling)
    python3 -c "
import subprocess
import json
import sys

task = '''$task'''

# Call openclaw agent with the task
result = subprocess.run(
    ['openclaw', 'agent', '--local', '--message', task, '--json'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    try:
        data = json.loads(result.stdout)
        # Try different possible response fields
        response = data.get('response') or data.get('message') or data.get('content') or str(data)
        print(response)
    except:
        print(result.stdout)
else:
    sys.exit(1)
" 2>/dev/null || {
        echo "⚠️  AI analysis failed, using simple format"
        echo "$news_items" | while IFS= read -r line; do
            [ -z "$line" ] && continue
            echo "📰 $line"
            echo "💡 重要性：AI行业重要动态，值得关注"
            echo ""
        done
    }
}

# Main execution
main() {
    echo "🚀 AI Daily Enhanced - Starting..."
    echo "⏰ Time: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Step 1: Get the latest AI daily report
    echo "📥 Fetching latest AI daily report..."
    
    # For now, we'll use a sample. In production, this would fetch from the actual cron output
    local sample_news="GPT-5.4正式发布(Computer Use+金融插件)
Claude日增百万用户超越ChatGPT
Claude Opus 4.6编写C编译器
Anthropic超级碗广告+无广告承诺
GPT-5.3明天发布
Anthropic 75%概率领先3月"
    
    echo "📊 News items found: $(echo "$sample_news" | wc -l)"
    
    # Step 2: Analyze importance
    echo "🔍 Analyzing importance with AI..."
    local enhanced_report
    enhanced_report=$(analyze_importance "$sample_news")
    
    # Step 3: Format final report
    echo "📝 Formatting enhanced report..."
    local final_report="🤖 AI 热门日报 - $(date '+%Y-%m-%d')

$enhanced_report

---
✨ 本日报由 OpenClaw 自动生成并增强
💡 新增：重要性分析，帮助快速理解新闻价值"
    
    # Step 4: Send to Telegram
    echo "📤 Sending to Telegram..."
    openclaw message send \
        --channel telegram \
        --target "$TELEGRAM_CHAT_ID" \
        --thread-id "$TELEGRAM_TOPIC_ID" \
        --message "$final_report" 2>&1 | grep -v "^\[plugins\]" || {
        echo "⚠️  Telegram send failed, printing to stdout instead:"
        echo "$final_report"
    }
    
    echo "✅ AI Daily Enhanced - Completed!"
}

# Run main function
main "$@"
