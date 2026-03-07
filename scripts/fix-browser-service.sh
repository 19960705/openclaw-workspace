#!/bin/bash
# Browser service auto-recovery script
# Usage: bash fix-browser-service.sh

set -euo pipefail

echo "🔍 Checking browser service..."

if curl -s --max-time 3 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ Browser service is healthy (CDP port 18800 responding)"
    exit 0
fi

echo "❌ Browser service not responding. Attempting recovery..."

source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

# Kill any stale Chrome/Chromium processes tied to OpenClaw profile
pkill -f "[Cc]hrome.*openclaw" 2>/dev/null || true
pkill -f "[Cc]hromium.*openclaw" 2>/dev/null || true
sleep 2

if [ -n "${OPENCLAW_BIN:-}" ] && [ -x "$OPENCLAW_BIN" ]; then
    "$OPENCLAW_BIN" gateway restart >/dev/null 2>&1 || true
    echo "🔄 Gateway restarted"
else
    GATEWAY_PID=$(pgrep -f "openclaw.*gateway" 2>/dev/null | head -1 || true)
    if [ -n "$GATEWAY_PID" ]; then
        kill -HUP "$GATEWAY_PID" 2>/dev/null || true
        echo "🔄 Sent HUP to gateway (PID: $GATEWAY_PID)"
    fi
fi

sleep 6

if curl -s --max-time 5 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ Browser service recovered!"
    exit 0
fi

echo "⚠️ Browser service still down. Manual intervention needed."
exit 1
