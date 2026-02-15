import sys
import json
import requests
import base64
import time
import os

prompt = sys.argv[1]
ref_image_path = sys.argv[2]
size = sys.argv[3] if len(sys.argv) > 3 else "9:16"
api_key = "sk-bee934b0b6ec47f69391ee65d80d031b"
base_url = "http://127.0.0.1:8045/v1"

output_dir = "/Users/mac/.openclaw/media/generated_images"
os.makedirs(output_dir, exist_ok=True)

filename = f"keonho_birthday_accurate_{int(time.time())}.png"
filepath = os.path.join(output_dir, filename)

# 读取参考图并转为 Base64
with open(ref_image_path, "rb") as image_file:
    ref_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# 构造 Image-to-Image 请求 (依据 Antigravity Manager 支持的格式)
# 这里的实现可能因版本而异，我们尝试将图片放入 image 字段
payload = {
    "model": "gemini-3-pro-image",
    "prompt": prompt,
    "image": ref_base64, # 垫图
    "size": size,
    "quality": "hd",
    "imageSize": "4K",
    "response_format": "b64_json"
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    print(f"Sending request with reference image: {ref_image_path}...")
    response = requests.post(f"{base_url}/images/edits", json=payload, headers=headers, timeout=180)
    
    if response.status_code != 200:
        print(f"HTTP ERROR {response.status_code}: {response.text}")
        sys.exit(1)
        
    data = response.json()
    
    if "error" in data:
        print(f"API ERROR: {data['error']}")
        sys.exit(1)
        
    b64_data = data["data"][0]["b64_json"]
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(b64_data))
        
    print(f"SUCCESS: {filepath}")
except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
