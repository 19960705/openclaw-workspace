#!/bin/bash
# Keep the launchd-managed gateway loaded and listening.

set -u

LABEL="ai.openclaw.gateway"
PORT="18789"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOG_FILE="$HOME/.openclaw/logs/gateway-watchdog.log"
UID_VALUE="$(id -u)"
DOMAIN="gui/${UID_VALUE}"
TARGET="${DOMAIN}/${LABEL}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

service_loaded() {
    launchctl print "$TARGET" >/dev/null 2>&1
}

service_running() {
    launchctl print "$TARGET" 2>/dev/null | grep -q "state = running"
}

port_listening() {
    lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1
}

ensure_service_loaded() {
    if service_loaded; then
        return 0
    fi
    log "service missing from launchd; bootstrapping ${PLIST}"
    launchctl bootstrap "$DOMAIN" "$PLIST" >/dev/null 2>&1 || return 1
}

kickstart_service() {
    log "kickstarting ${TARGET}"
    launchctl kickstart "$TARGET" >/dev/null 2>&1 || return 1
}

if ! ensure_service_loaded; then
    log "bootstrap failed for ${PLIST}"
    exit 1
fi

if port_listening; then
    exit 0
fi

if service_running; then
    log "gateway service is running but port ${PORT} is not ready yet; skipping forced restart"
    exit 0
fi

log "gateway port ${PORT} is down"
if ! kickstart_service; then
    log "kickstart failed for ${TARGET}"
    exit 1
fi

sleep 2
if port_listening; then
    log "gateway recovered and is listening on ${PORT}"
    exit 0
fi

log "gateway still not listening after kickstart"
exit 1
