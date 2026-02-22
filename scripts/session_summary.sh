#!/bin/bash
# Auto Session Summary - Run this to generate session summary
# Usage: ./session_summary.sh

WORKSPACE="$HOME/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
MEMORY_DIR="$WORKSPACE/memory"
SUMMARY_FILE="$MEMORY_DIR/${DATE}-summary.md"

echo "# Session Summary - $(date)" > "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Count messages in today's memory
if [ -f "$MEMORY_DIR/${DATE}.md" ]; then
    MSG_COUNT=$(wc -l < "$MEMORY_DIR/${DATE}.md")
    echo "## Today's Activity" >> "$SUMMARY_FILE"
    echo "- Lines in memory: $MSG_COUNT" >> "$SUMMARY_FILE"
fi

# Get recent files
echo "" >> "$SUMMARY_FILE"
echo "## Recent Memory Files" >> "$SUMMARY_FILE"
ls -t "$MEMORY_DIR"/*.md 2>/dev/null | head -5 | while read f; do
    echo "- $(basename $f)" >> "$SUMMARY_FILE"
done

# Recent events
if [ -f "$WORKSPACE/RECENT_EVENTS.md" ]; then
    echo "" >> "$SUMMARY_FILE"
    echo "## Recent Events" >> "$SUMMARY_FILE"
    tail -10 "$WORKSPACE/RECENT_EVENTS.md" >> "$SUMMARY_FILE"
fi

echo "" >> "$SUMMARY_FILE"
echo "---" >> "$SUMMARY_FILE"
echo "*Generated: $(date)*" >> "$SUMMARY_FILE"

echo "Summary saved to: $SUMMARY_FILE"
cat "$SUMMARY_FILE"
