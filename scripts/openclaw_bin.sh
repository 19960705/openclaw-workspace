#!/bin/bash
# Resolve the openclaw binary in a cron-safe way.
# Usage: OPENCLAW=$(bash openclaw_bin.sh)

set -euo pipefail

CANDIDATES=(
  "/opt/homebrew/bin/openclaw"
  "/usr/local/bin/openclaw"
  "$HOME/.nvm/versions/node/v22.12.0/bin/openclaw"
)

for c in "${CANDIDATES[@]}"; do
  if [ -x "$c" ]; then
    echo "$c"
    exit 0
  fi
done

if command -v openclaw >/dev/null 2>&1; then
  command -v openclaw
  exit 0
fi

echo "openclaw_not_found" >&2
exit 1
