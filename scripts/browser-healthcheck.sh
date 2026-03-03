#!/bin/bash
# Browser service healthcheck - ensures browser control service is reachable before use
# Usage: bash browser-healthcheck.sh (returns 0 if healthy, 1 if recovery failed)

# cron-safe env
source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

# Check if browser CDP port is responding
if curl -s --max-time 3 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    exit 0  # healthy
fi

# Not responding - attempt recovery
echo "⚠️ Browser service not responding, attempting recovery..." >&2
bash "$HOME/.openclaw/workspace/scripts/fix-browser-service.sh"

# Verify recovery
sleep 2
if curl -s --max-time 5 http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
    echo "✅ Browser service recovered" >&2
    exit 0
else
    echo "❌ Browser service recovery failed" >&2
    exit 1
fi
