#!/bin/bash
# integrate-ai-daily-enhancement.sh - Integrate enhanced AI daily into cron
# This script modifies the AI日报 cron task to use the enhanced version

set -euo pipefail

echo "🔧 Integrating AI Daily Enhancement into Cron..."

# The AI日报 cron task ID
CRON_ID="8b6dc1a1-d302-4b96-955d-cc85a8ad1be5"

# Current task runs: "⏰ 执行 AI 热门推文日报任务..."
# We need to modify it to call our enhanced script after the original task

# Strategy: Create a wrapper that:
# 1. Runs the original AI daily task
# 2. Takes the output and enhances it with our script
# 3. Sends the enhanced version

# For now, let's create a new cron task that runs our enhanced script
# This is safer than modifying the existing one

echo "📝 Creating new enhanced AI daily cron task..."

# Check if we can add a new cron task
openclaw cron add \
  --name "AI日报增强版" \
  --schedule "cron 5 9 * * * @ Asia/Shanghai" \
  --agent main \
  --message "运行增强版 AI 日报：bash scripts/ai-daily-enhanced.sh" \
  --enabled false || {
    echo "⚠️  Failed to add cron task via CLI"
    echo "📋 Manual integration steps:"
    echo ""
    echo "Option 1: Modify existing cron task (8b6dc1a1-d302-4b96-955d-cc85a8ad1be5)"
    echo "  - Change the message to include: 'bash scripts/ai-daily-enhanced.sh'"
    echo ""
    echo "Option 2: Create new cron task manually"
    echo "  - Name: AI日报增强版"
    echo "  - Schedule: cron 5 9 * * * @ Asia/Shanghai"
    echo "  - Command: bash scripts/ai-daily-enhanced.sh"
    echo ""
    echo "Option 3: Test manually first"
    echo "  - Run: bash scripts/ai-daily-enhanced.sh"
    echo "  - Verify output in Telegram"
    echo "  - Then integrate into cron"
    exit 1
}

echo "✅ Integration complete!"
echo ""
echo "📋 Next steps:"
echo "1. Enable the new cron task: openclaw cron enable <new-task-id>"
echo "2. Test it: openclaw cron run <new-task-id>"
echo "3. If it works, disable the old AI日报 task"
