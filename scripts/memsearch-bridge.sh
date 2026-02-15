#!/bin/bash
# memsearch-bridge.sh — Bridge between OpenClaw memory and memsearch vector search
# Usage:
#   ./memsearch-bridge.sh index    — Index all memory files
#   ./memsearch-bridge.sh search "query" [top_k]  — Semantic search
#   ./memsearch-bridge.sh watch    — Watch for file changes and auto-index

MEMORY_DIR="/Users/mac/.openclaw/workspace/memory"
MEMORY_MD="/Users/mac/.openclaw/workspace/MEMORY.md"
PYTHON="python3.11"
MEMSEARCH="$PYTHON -m memsearch"

case "$1" in
  index)
    echo "🔄 Indexing memory files..."
    $MEMSEARCH index --path "$MEMORY_DIR" --path "$MEMORY_MD" 2>&1
    echo "✅ Index complete"
    ;;
  search)
    QUERY="${2:?Usage: memsearch-bridge.sh search \"query\" [top_k]}"
    TOP_K="${3:-5}"
    $MEMSEARCH search "$QUERY" --path "$MEMORY_DIR" --path "$MEMORY_MD" --top-k "$TOP_K" 2>&1
    ;;
  watch)
    echo "👁 Watching memory files for changes..."
    $MEMSEARCH watch --path "$MEMORY_DIR" --path "$MEMORY_MD" 2>&1
    ;;
  *)
    echo "Usage: $0 {index|search|watch} [args...]"
    exit 1
    ;;
esac
