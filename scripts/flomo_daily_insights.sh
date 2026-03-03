#!/bin/bash
set -euo pipefail

# Generate a compact daily insight note and push to flomo
# Source: memory/YYYY-MM-DD.md (today)

source "$HOME/.openclaw/workspace/scripts/cron_env.sh"

TODAY=$(date '+%Y-%m-%d')
MEM_FILE="$HOME/.openclaw/workspace/memory/$TODAY.md"

if [ ! -f "$MEM_FILE" ]; then
  echo "No memory file for today: $MEM_FILE" >&2
  exit 0
fi

# Keep it short: send last ~80 lines (usually contains today's entries)
SNIPPET=$(tail -80 "$MEM_FILE")

CONTENT=$(cat <<EOF
#DailyInsight #OpenClaw

${SNIPPET}
EOF
)

bash "$HOME/.openclaw/workspace/scripts/flomo_push.sh" "$CONTENT"
