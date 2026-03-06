#!/bin/bash
# Common env for cron jobs (macOS): ensure stable PATH and expected runtime.
# Source this at top of cron scripts: `source "$HOME/.openclaw/workspace/scripts/cron_env.sh"`

# Minimal sane PATH (cron often has a very small PATH)
export PATH="/Users/mac/miniconda3/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# Prefer the Homebrew-managed openclaw shim (stable across shells)
export OPENCLAW_BIN="/opt/homebrew/bin/openclaw"

# If openclaw still not found, fall back to the nvm-installed binary
if [ ! -x "$OPENCLAW_BIN" ]; then
  if [ -x "$HOME/.nvm/versions/node/v22.12.0/bin/openclaw" ]; then
    export OPENCLAW_BIN="$HOME/.nvm/versions/node/v22.12.0/bin/openclaw"
  fi
fi
