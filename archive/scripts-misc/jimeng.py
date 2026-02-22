
#!/usr/bin/env python3
"""
即梦 AI 图像生成工具
使用 jimeng-free-api 反代服务
"""

import sys
import json
import argparse
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("⚠️  requests 模块未安装，使用 urllib")
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False
else:
    HAS_REQUESTS = True


class JimengAPI:
    def __init__(self, base_url="http://localhost:8000", session_id=None):
        self.base_url = base_url
        self.session_id = session_id

    def _request(self, endpoint, data=None, method="POST"):
        headers = {
            "Content-Type": "application/json"
        }
        if self.session_id:
            headers["Authorization"] = f"Bearer {self.session_id}"

        url = f"{self.base_url}{endpoint}"

        if HAS_REQUESTS:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=data,
                timeout=120
            )
            return response.json()
        else:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8') if data else None,
                headers=headers,
                method=method
            )
            with urllib.request.urlopen(req, timeout=120) as f:
                return json.loads(f.read().decode('utf-8'))

    def ping(self):
        """测试连接"""
        return self._request("/ping", method="GET")

    def generate_image(self, prompt, negative_prompt="", width=1024, height=1024,
                       sample_strength=0.5, model="jimeng-3.0"):
        """生成图像"""
        data = {
            "model": model,
            "prompt": prompt,
            "negativePrompt": negative_prompt,
            "width": width,
            "height": height,
            "sample_strength": sample_strength
        }
        return self._request("/v1/images/generations", data)

    def chat(self, messages, model="jimeng-3.0", stream=False):
        """对话补全"""
        data = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        return self._request("/v1/chat/completions", data)


def main():
    parser = argparse.ArgumentParser(description="即梦 AI 图像生成工具")
    parser.add_argument("--session-id", required=True, help="即梦 sessionId")
    parser.add_argument("--prompt", required=True, help="图像生成提示词")
    parser.add_argument("--negative-prompt", default="", help="反向提示词")
    parser.add_argument("--width", type=int, default=1024, help="图像宽度")
    parser.add_argument("--height", type=int, default=1024, help="图像高度")
    parser.add_argument("--model", default="jimeng-3.0", help="模型版本")
    parser.add_argument("--base-url", default="http://localhost:8000", help="API 地址")

    args = parser.parse_args()

    api = JimengAPI(base_url=args.base_url, session_id=args.session_id)

    print("📡 测试连接...")
    try:
        ping_result = api.ping()
        print(f"✅ 连接成功: {ping_result}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return 1

    print("\n🎨 生成图像...")
    try:
        result = api.generate_image(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            width=args.width,
            height=args.height,
            model=args.model
        )
        print(f"\n✅ 生成结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("data"):
            print(f"\n🖼️  图像 URL:")
            for i, img in enumerate(result["data"]):
                print(f"{i+1}. {img.get('url', 'N/A')}")

    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

