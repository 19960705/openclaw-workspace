#!/bin/bash
# ai-daily-enhanced-v2.sh - Enhanced AI Daily Report with importance analysis + deduplication
# Version: 2.0 - 2026-03-11
# Purpose: Add importance analysis + remove duplicate topics

set -euo pipefail

# Configuration
TELEGRAM_CHAT_ID="-1003505656701"
TELEGRAM_TOPIC_ID="2"

# Function: Analyze and deduplicate news items
analyze_and_deduplicate() {
    local news_items="$1"
    
    # Create prompt for AI analysis with deduplication
    local prompt="你是一个 AI 行业分析专家。请为以下 AI 新闻添加「重要性分析」并进行去重。

新闻列表：
$news_items

任务：
1. 识别重复或相似的话题（例如：多条关于同一产品发布的新闻）
2. 对于重复话题，只保留信息最全面或最重要的一条
3. 为每条保留的新闻添加「💡 重要性：」说明（20-30字）
4. 如果合并了多条新闻，在重要性说明中体现关键信息
5. 使用中文

输出格式：
📰 [新闻标题]
💡 重要性：[一句话说明为什么重要]

要求：
- 去重后保留 5-8 条最重要的新闻
- 保持简洁、有洞察力
- 如果某个话题有多条新闻，合并为一条并在标题中体现完整信息

请开始分析："

    # Use Python to call the analysis
    python3 -c "
import subprocess
import json
import sys

task = '''$prompt'''

# Call openclaw agent with the task
result = subprocess.run(
    ['openclaw', 'agent', '--local', '--message', task, '--json'],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    try:
        data = json.loads(result.stdout)
        response = data.get('response') or data.get('message') or data.get('content') or str(data)
        print(response)
    except:
        print(result.stdout)
else:
    sys.exit(1)
" 2>/dev/null || {
        echo "⚠️  AI analysis failed, using simple format"
        echo "$news_items" | head -6 | while IFS= read -r line; do
            [ -z "$line" ] && continue
            echo "📰 $line"
            echo "💡 重要性：AI行业重要动态，值得关注"
            echo ""
        done
    }
}

# Main execution
main() {
    echo "🚀 AI Daily Enhanced v2.0 - Starting..."
    echo "⏰ Time: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Step 1: Get the latest AI daily report
    echo "📥 Fetching latest AI daily report..."
    
    # Sample news with duplicates to test deduplication
    local sample_news="GPT-5.4正式发布(Computer Use+金融插件)
Claude日增百万用户超越ChatGPT
Claude Opus 4.6编写C编译器
Anthropic超级碗广告+无广告承诺
GPT-5.3明天发布
Anthropic 75%概率领先3月
OpenAI发布GPT-5.4新功能
Claude用户增长突破百万
Anthropic市场份额持续扩大"
    
    echo "📊 Raw news items: $(echo "$sample_news" | wc -l)"
    
    # Step 2: Analyze importance and deduplicate
    echo "🔍 Analyzing importance and deduplicating..."
    local enhanced_report
    enhanced_report=$(analyze_and_deduplicate "$sample_news")
    
    # Step 3: Format final report
    echo "📝 Formatting enhanced report..."
    local final_report="🤖 AI 热门日报 - $(date '+%Y-%m-%d')

$enhanced_report

---
✨ 本日报由 OpenClaw 自动生成并增强
💡 新增功能：
  • 重要性分析 - 快速理解新闻价值
  • 智能去重 - 同一话题合并展示"
    
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
    
    echo "✅ AI Daily Enhanced v2.0 - Completed!"
}

# Run main function
main "$@"
