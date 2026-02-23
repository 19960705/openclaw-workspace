#!/bin/bash
# QVeris AI 趋势搜索脚本 (Twitter/X)
# 搜索 AI/科技领域的热门话题和最新帖子

export QVERIS_API_KEY=sk-95NXCyLGBm5vWiO1jT23AoEwHWPyRl75mmQSU6fuL9I
cd ~/.openclaw/workspace/skills/qveris

# 搜索 AI 技术相关工具
echo "=== QVeris AI 趋势搜索 ==="
uv run scripts/qveris_tool.py search "X Twitter AI tech news" --limit 5
