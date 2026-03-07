#!/bin/bash
# recurring-failure-guard.sh — local guard for known recurring OpenClaw failures
# Handles:
# 1) cron/gateway false alarms caused by device token mismatch when no nodes are paired
# 2) browser control service/CDP unreachability

set -euo pipefail

source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

check_openclaw_bin() {
  [ -n "${OPENCLAW_BIN:-}" ] && [ -x "$OPENCLAW_BIN" ]
}

check_gateway_ok() {
  check_openclaw_bin && "$OPENCLAW_BIN" gateway status 2>&1 | grep -q "RPC probe: ok"
}

nodes_zero() {
  check_openclaw_bin && "$OPENCLAW_BIN" nodes status 2>/dev/null | grep -Eq "Known: 0|Known 0" && \
  "$OPENCLAW_BIN" nodes status 2>/dev/null | grep -Eq "Paired: 0|Paired 0" && \
  "$OPENCLAW_BIN" nodes status 2>/dev/null | grep -Eq "Connected: 0|Connected 0"
}

check_cdp_ok() {
  curl -s --max-time 3 http://127.0.0.1:18800/json/version >/dev/null 2>&1
}

case "${1:-status}" in
  gateway)
    if ! check_openclaw_bin; then
      echo "OPENCLAW_BIN_MISSING"
      exit 1
    fi

    if check_gateway_ok; then
      if nodes_zero; then
        echo "GATEWAY_OK_IGNORE_LEGACY_TOKEN_MISMATCH"
      else
        echo "GATEWAY_OK"
      fi
      exit 0
    fi

    echo "GATEWAY_NEEDS_ATTENTION"
    exit 1
    ;;
  browser)
    if check_cdp_ok; then
      echo "BROWSER_OK"
      exit 0
    fi

    bash "$HOME/.openclaw/workspace/scripts/fix-browser-service.sh"

    if check_cdp_ok; then
      echo "BROWSER_RECOVERED"
      exit 0
    fi

    echo "BROWSER_NEEDS_ATTENTION"
    exit 1
    ;;
  status)
    "$0" gateway
    "$0" browser
    ;;
  *)
    echo "Usage: $0 [gateway|browser|status]" >&2
    exit 2
    ;;
esac
