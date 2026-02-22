
#!/usr/bin/env python3
import requests
import json

# 即梦反代 API 配置
BASE_URL = "http://localhost:8000"
SESSION_ID = "0274fd2ca64e4cc606099baf2428f618"

# 测试图像生成
def test_image_generation():
    print("🚀 测试即梦图像生成...")

    prompt = "Photorealistic cinematic shot, 25-year-old Asian woman in loose cream sweater, sleepy but with期待的 smile, walking towards a spring-limited coffee machine in bright modern kitchen, morning sunlight streaming from right 45 degrees, soft backlight, cherry blossom branches visible outside window, warm healing tones, movie still, 35mm lens, f/1.8, shallow depth of field, 8K, ultra detailed"

    headers = {
        "Authorization": f"Bearer {SESSION_ID}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "jimeng-3.0",
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "sample_strength": 0.5
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/images/generations",
            headers=headers,
            json=data,
            timeout=60
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_image_generation()

