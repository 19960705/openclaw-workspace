#!/bin/bash
set -euo pipefail

# Push a note to flomo via webhook
# Usage:
#   bash flomo_push.sh "text to send"
# Env:
#   FLOMO_WEBHOOK_URL in scripts/.env.flomo

source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

ENV_FILE="$HOME/.openclaw/workspace/scripts/.env.flomo"
if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

if [ -z "${FLOMO_WEBHOOK_URL:-}" ]; then
  echo "FLOMO_WEBHOOK_URL not set (expected in $ENV_FILE)" >&2
  exit 1
fi

TEXT="${1:-}"
if [ -z "$TEXT" ]; then
  echo "No text provided" >&2
  exit 1
fi

JSON=$(python3 - <<PY
import json
text = '''$TEXT'''
print(json.dumps({"content": text}, ensure_ascii=False))
PY
)

curl -sS -X POST "$FLOMO_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d "$JSON" \
  >/dev/null

echo "OK"
