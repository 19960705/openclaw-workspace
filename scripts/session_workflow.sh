#!/bin/bash
# Auto Session Summary with Semantic Search
# Usage: ./session_workflow.sh [search_query]
# If search_query provided, runs semantic search + summary
# If no args, just generates summary

WORKSPACE="$HOME/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"
DATE=$(date +%Y-%m-%d)
SUMMARY_FILE="$WORKSPACE/memory/${DATE}-summary.md"

echo "=== Session Workflow Started: $(date) ==="

# If query provided, do semantic search first
if [ $# -gt 0 ]; then
    QUERY="$*"
    echo "🔍 Running semantic search for: $QUERY"
    python3 "$SCRIPT_DIR/semantic_search.py" "$QUERY" > /tmp/search_result.txt 2>&1
    cat /tmp/search_result.txt
    echo ""
fi

# Generate summary
echo "📝 Generating session summary..."
bash "$SCRIPT_DIR/session_summary.sh"

echo ""
echo "=== Workflow Complete ==="
