#!/bin/bash
# Gateway connection healthcheck for cron jobs
# Verifies gateway is reachable and device token is valid before cron tasks
# Usage: bash gateway-healthcheck.sh (returns 0 if healthy, 1 if failed)

# cron-safe env
source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

LOG_FILE="$HOME/.openclaw/logs/gateway-healthcheck.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if gateway is reachable via RPC probe
check_gateway_rpc() {
    if [ -z "$OPENCLAW_BIN" ] || [ ! -x "$OPENCLAW_BIN" ]; then
        log "❌ openclaw binary not found in cron env"
        return 1
    fi

    if "$OPENCLAW_BIN" gateway status 2>&1 | grep -q "RPC probe: ok"; then
        return 0
    else
        return 1
    fi
}

# Attempt recovery
recover_gateway() {
    log "⚠️ Gateway not reachable, attempting restart..."
    "$OPENCLAW_BIN" gateway restart >> "$LOG_FILE" 2>&1
    sleep 5
    
    if check_gateway_rpc; then
        log "✅ Gateway recovered"
        return 0
    else
        log "❌ Gateway recovery failed"
        return 1
    fi
}

# Main check
if check_gateway_rpc; then
    exit 0  # healthy
else
    log "❌ Gateway RPC probe failed"
    recover_gateway
    exit $?
fi
