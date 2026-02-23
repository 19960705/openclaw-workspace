#!/bin/bash
# GitHub AI 趋势推送脚本

cd ~/.openclaw/workspace/skills/github-ai-trends
python3 scripts/fetch_trends.py --period daily --limit 10
