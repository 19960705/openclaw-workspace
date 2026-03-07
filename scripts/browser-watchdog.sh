#!/bin/bash
# browser-watchdog.sh — 自动检测并恢复浏览器控制服务

set -euo pipefail

echo "🔍 检查浏览器状态..."

source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

if [ -z "${OPENCLAW_BIN:-}" ] || [ ! -x "$OPENCLAW_BIN" ]; then
    echo "❌ openclaw binary not found in cron env" >&2
    exit 1
fi

# 优先检查本地 CDP，避免被 chrome relay / 旧 ref 误导
if curl -s --max-time 3 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ 浏览器控制服务正常 (CDP ready)"
    exit 0
fi

# 再用 openclaw 状态作为辅助判断
BROKEN=false
if ! "$OPENCLAW_BIN" browser status 2>/dev/null | grep -qi "running"; then
    BROKEN=true
fi

if [ "$BROKEN" = true ]; then
    echo "⚠️ 浏览器控制服务不可达，执行恢复链..."
else
    echo "⚠️ browser status 显示运行中，但 CDP 不可达，按挂起状态处理并执行恢复链..."
fi

bash "$HOME/.openclaw/workspace/scripts/fix-browser-service.sh"
sleep 2
if curl -s --max-time 5 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ 浏览器控制服务已恢复"
    exit 0
fi

echo "❌ 浏览器控制服务恢复失败" >&2
exit 1
