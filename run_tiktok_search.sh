#!/bin/bash
export $(grep APIFY_TOKEN .env | xargs)

# 搜索泰国洗车喷雾剂相关话题
~/.nvm/versions/node/v22.12.0/bin/node ~/.openclaw/skills/agent-skills/scripts/run_actor.js \
  --actor "clockworks/tiktok-hashtag-scraper" \
  --input '{
    "hashtags": ["สเปรย์ล้างรถ", "ล้างรถ", "ดูแลรถ"],
    "resultsPerPage": 50
  }' \
  --output "tiktok-car-wash-spray-$(date +%Y-%m-%d).json" \
  --format json
