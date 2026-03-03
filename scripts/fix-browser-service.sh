#!/bin/bash
# Browser service auto-recovery script
# Usage: bash fix-browser-service.sh

echo "🔍 Checking browser service..."

# Check if browser CDP port is responding
if curl -s --max-time 3 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ Browser service is healthy (CDP port 18800 responding)"
    exit 0
fi

echo "❌ Browser service not responding. Attempting recovery..."

# Kill any stale chrome processes
pkill -f "chrome.*user-data-dir.*openclaw" 2>/dev/null
sleep 2

# Restart via openclaw gateway (use cron-safe env)
source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

if [ -x "$OPENCLAW_BIN" ]; then
    "$OPENCLAW_BIN" gateway restart 2>/dev/null
    echo "🔄 Gateway restarted"
else
    # Fallback: find and restart the gateway process
    GATEWAY_PID=$(pgrep -f "openclaw.*gateway" 2>/dev/null | head -1)
    if [ -n "$GATEWAY_PID" ]; then
        kill -HUP "$GATEWAY_PID" 2>/dev/null
        echo "🔄 Sent HUP to gateway (PID: $GATEWAY_PID)"
    fi
fi

sleep 5

# Verify recovery
if curl -s --max-time 5 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ Browser service recovered!"
    exit 0
else
    echo "⚠️ Browser service still down. Manual intervention needed."
    exit 1
fi
