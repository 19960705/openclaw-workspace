#!/bin/bash
# Common env for cron jobs (macOS): ensure stable PATH and expected runtime.
# Source this at top of cron scripts: `source "$HOME/.openclaw/workspace/scripts/cron_env.sh"`

# Minimal sane PATH (cron often has a very small PATH)
export PATH="/Users/mac/miniconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$HOME/.local/bin:$HOME/.nvm/versions/node/v22.12.0/bin:$PATH"

# Resolve a stable openclaw binary path for non-interactive shells.
OPENCLAW_CANDIDATES=(
  "/opt/homebrew/bin/openclaw"
  "/usr/local/bin/openclaw"
  "$HOME/.nvm/versions/node/v22.12.0/bin/openclaw"
)

for candidate in "${OPENCLAW_CANDIDATES[@]}"; do
  if [ -x "$candidate" ]; then
    export OPENCLAW_BIN="$candidate"
    break
  fi
done

if [ -z "$OPENCLAW_BIN" ] && command -v openclaw >/dev/null 2>&1; then
  export OPENCLAW_BIN="$(command -v openclaw)"
fi

# Back-compat for older scripts.
export OPENCLAW_PATH="${OPENCLAW_BIN:-}"
