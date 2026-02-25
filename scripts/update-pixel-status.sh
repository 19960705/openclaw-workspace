#!/bin/bash
# Update pixel game status to GitHub Pages

cd /Users/mac/.openclaw/workspace

# Default values
ZONE="workshop"
ACTIVITY="待机中"
STATUS="idle"
LEVEL=1
XP=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -z|--zone) ZONE="$2"; shift 2 ;;
        -a|--activity) ACTIVITY="$2"; shift 2 ;;
        -s|--status) STATUS="$2"; shift 2 ;;
        -l|--level) LEVEL="$2"; shift 2 ;;
        -x|--xp) XP="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# Create status JSON
python3 << EOF
import json
from datetime import datetime
status = {
    "status": "$STATUS",
    "zone": "$ZONE",
    "activity": "$ACTIVITY",
    "lastUpdate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "level": $LEVEL,
    "xp": $XP
}
with open('pixel-game-status.json', 'w') as f:
    json.dump(status, f, indent=2)
print(json.dumps(status, indent=2))
EOF

# Copy to deploy folder
cp pixel-game-status.json /Users/mac/pixel-game-deploy/status.json

# Commit and push
cd /Users/mac/pixel-game-deploy
git add status.json
git commit -m "Update status: $ZONE - $ACTIVITY"
git push

echo "✅ Status updated and pushed!"
