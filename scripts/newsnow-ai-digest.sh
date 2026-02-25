#!/bin/bash
# NewsNow AI & 创意新闻聚合脚本
# 用途：每日定时抓取 AI 和创意相关新闻源
# 输出：JSON 格式，供 AI 整理成日报

export PATH="$HOME/bin:$PATH"

SOURCES=(
  "hackernews"
  "producthunt"
  "github-trending-today"
  "36kr"
  "juejin"
  "ithome"
  "sspai"
)

echo "{"
echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
echo "  \"sources\": {"

for i in "${!SOURCES[@]}"; do
  src="${SOURCES[$i]}"
  echo "    \"$src\": " 
  newsnow "$src" --json 2>/dev/null || echo "[]"
  if [ $i -lt $((${#SOURCES[@]} - 1)) ]; then
    echo ","
  fi
done

echo "  }"
echo "}"
