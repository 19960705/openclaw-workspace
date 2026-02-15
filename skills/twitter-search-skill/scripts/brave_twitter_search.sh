#!/bin/bash
#
# Twitter/X Search using Brave Search API
# This script provides simple Twitter/X search without requiring Twitter API key
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

warn() {
    echo -e "${YELLOW}Warning: $1${NC}" >&2
}

# Check Python
if ! command -v python3 &> /dev/null; then
    error_exit "python3 is not installed"
fi

# Check requests module
if ! python3 -c "import requests" 2>/dev/null; then
    warn "Installing requests module..."
    pip3 install requests --user 2>/dev/null || pip install requests --user 2>/dev/null
fi

# Parse arguments
QUERY=""
LIMIT=20
JSON_OUTPUT=false
LINK_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --json)
            JSON_OUTPUT=true
            shift
            ;;
        --link-only)
            LINK_ONLY=true
            shift
            ;;
        -*)
            error_exit "Unknown option: $1"
            ;;
        *)
            QUERY="$1"
            shift
            ;;
    esac
done

# Validate query
if [[ -z "$QUERY" ]]; then
    error_exit "No query specified. Usage: $0 \"search query\" [options]

Examples:
  $0 \"AI news\"
  $0 \"GPT-4\" --limit 10
  $0 \"Anthropic\" --json"
fi

# Run the search
if [[ "$LINK_ONLY" == "true" ]]; then
    echo "https://x.com/search?q=$(python3 -c "from urllib.parse import quote; print(quote('$QUERY'))")&f=live"
else
    python3 "$SCRIPT_DIR/simple_twitter_search.py" "$QUERY" --limit "$LIMIT" $([[ "$JSON_OUTPUT" == "true" ]] && echo "--json")
fi
