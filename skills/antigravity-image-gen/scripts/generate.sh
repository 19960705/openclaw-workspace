#!/bin/bash
#
# Antigravity Nano Banana Pro Image Generator
# 使用本地 Antigravity Manager 调用 Imagen 3 4K (Pro)
#

set -e

PROMPT="$1"
SIZE="${2:-1024x1024}" # 默认尺寸
API_KEY="sk-bee934b0b6ec47f69391ee65d80d031b"
BASE_URL="http://127.0.0.1:8045/v1"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 <prompt> [size]"
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="/Users/mac/.openclaw/media/generated_images"
mkdir -p "$OUTPUT_DIR"
FILENAME="nanobanana_pro_${TIMESTAMP}.png"
FILEPATH="${OUTPUT_DIR}/${FILENAME}"

# 调用 Antigravity Manager API
# 强制使用 quality: "hd" 和 imageSize: "4K" 以启用 Pro 模型
RESPONSE=$(curl -s -X POST "${BASE_URL}/images/generations" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gemini-3-pro-image\",
    \"prompt\": \"${PROMPT}\",
    \"size\": \"${SIZE}\",
    \"quality\": \"hd\",
    \"imageSize\": \"4K\",
    \"response_format\": \"b64_json\"
  }")

# 检查是否报错
ERROR=$(echo "$RESPONSE" | grep -o "\"error\":{[^}]*}")
if [ -n "$ERROR" ]; then
    echo "ERROR: ${ERROR}"
    exit 1
fi

# 提取 Base64 并保存
echo "$RESPONSE" | grep -o "\"b64_json\":\"[^\"]*\"" | cut -d'"' -f4 | base64 -d > "$FILEPATH"

if [ -f "$FILEPATH" ]; then
    echo "SUCCESS: ${FILEPATH}"
else
    echo "ERROR: Failed to save image"
    exit 1
fi
