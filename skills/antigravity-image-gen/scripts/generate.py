import sys
import json
import requests
import base64
import time
import os

prompt = sys.argv[1]
size = sys.argv[2] if len(sys.argv) > 2 else "1024x1024"
api_key = "sk-bee934b0b6ec47f69391ee65d80d031b"
base_url = "http://127.0.0.1:8045/v1"

output_dir = "/Users/mac/.openclaw/media/generated_images"
os.makedirs(output_dir, exist_ok=True)

filename = f"nanobanana_pro_{int(time.time())}.png"
filepath = os.path.join(output_dir, filename)

payload = {
    "model": "gemini-3-pro-image",
    "prompt": prompt,
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
    response = requests.post(f"{base_url}/images/generations", json=payload, headers=headers, timeout=120)
    data = response.json()
    
    if "error" in data:
        print(f"ERROR: {data['error']}")
        sys.exit(1)
        
    b64_data = data["data"][0]["b64_json"]
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(b64_data))
        
    print(f"SUCCESS: {filepath}")
except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
