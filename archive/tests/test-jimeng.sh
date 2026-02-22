
#!/bin/bash

# 即梦反代 API 配置
BASE_URL="http://localhost:8000"
SESSION_ID="0274fd2ca64e4cc606099baf2428f618"

echo "🚀 测试即梦图像生成..."

# 先测试 ping
echo ""
echo "📡 测试连接..."
curl -s "$BASE_URL/ping"

echo ""
echo "🎨 测试图像生成..."

PROMPT="Photorealistic cinematic shot, 25-year-old Asian woman in loose cream sweater, sleepy but with smile, walking towards a spring-limited coffee machine in bright modern kitchen, morning sunlight streaming from right 45 degrees, soft backlight, cherry blossom branches visible outside window, warm healing tones, movie still, 35mm lens, f/1.8, shallow depth of field, 8K, ultra detailed"

curl -s -X POST "$BASE_URL/v1/images/generations" \
  -H "Authorization: Bearer $SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jimeng-3.0",
    "prompt": "'"$PROMPT"'",
    "width": 1024,
    "height": 1024,
    "sample_strength": 0.5
  }' \
  | python3 -m json.tool

