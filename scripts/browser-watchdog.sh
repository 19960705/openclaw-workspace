#!/bin/bash
# browser-watchdog.sh — 自动检测并重启浏览器

echo "🔍 检查浏览器状态..."

# cron-safe env
source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

# 检查 browser 是否正常运行
BROKEN=false

# 尝试用 OpenClaw 检查 browser 状态
if ! "$OPENCLAW_BIN" browser status 2>/dev/null | grep -q "running"; then
    BROKEN=true
fi

# 如果检测到问题，重启
if [ "$BROKEN" = true ]; then
    echo "⚠️ 浏览器似乎挂了，尝试重启..."
    "$OPENCLAW_BIN" gateway restart 2>/dev/null
    sleep 3
    echo "✅ Gateway 重启完成"
else
    echo "✅ 浏览器正常运行"
fi
