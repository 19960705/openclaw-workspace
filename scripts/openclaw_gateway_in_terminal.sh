#!/bin/bash
set -euo pipefail

PORT="18789"
NODE_BIN="/opt/homebrew/bin/node"
OPENCLAW_ENTRY="/Users/mac/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/dist/index.js"

# Ensure stable PATH for Terminal sessions
export PATH="/Users/mac/miniconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# If something is already listening, do nothing.
if /usr/bin/nc -z 127.0.0.1 "$PORT" 2>/dev/null; then
  echo "[gateway-terminal] Port $PORT already listening. Not starting another gateway."
  exit 0
fi

echo "[gateway-terminal] Starting OpenClaw gateway on 127.0.0.1:$PORT"
exec "$NODE_BIN" "$OPENCLAW_ENTRY" gateway --port "$PORT"
