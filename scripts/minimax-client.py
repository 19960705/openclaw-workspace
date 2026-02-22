#!/usr/bin/env python3
"""
Minimax API 调用脚本
支持 chat completion 功能
"""

import os
import json
import sys
from pathlib import Path

# 加载环境变量
ENV_FILE = Path.home() / ".openclaw/workspace/.env.minimax"

def load_env():
    """从 .env 文件加载环境变量"""
    if not ENV_FILE.exists():
        print(f"❌ 配置文件不存在: {ENV_FILE}")
        sys.exit(1)

    env_vars = {}
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars

def call_minimax(prompt, model=None):
    """
    调用 Minimax Chat Completions API

    Args:
        prompt (str): 用户输入的提示词
        model (str): 模型名称，默认从环境变量读取

    Returns:
        dict: API 响应
    """
    env = load_env()

    api_key = env.get('MINIMAX_API_KEY')
    base_url = env.get('MINIMAX_BASE_URL', 'https://api.minimax.chat/v1')
    model_name = model or env.get('MINIMAX_MODEL', 'abab5.5s-chat')

    if not api_key:
        print("❌ 错误: MINIMAX_API_KEY 未配置")
        sys.exit(1)

    url = f"{base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False
    }

    try:
        import urllib.request
        import urllib.error

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method='POST'
        )

        print(f"📡 正在调用 Minimax {model_name}...")
        print(f"📝 提示词: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

        with urllib.request.urlopen(req, timeout=60) as response:
            response_data = response.read().decode('utf-8')
            result = json.loads(response_data)

            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0]['message']['content']
                usage = result.get('usage', {})

                print("\n✅ 响应成功!")
                print(f"\n📤 回答:\n{message}")

                if usage:
                    print(f"\n📊 Token 使用:")
                    print(f"  - Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"  - Completion tokens: {usage.get('completion_tokens', 'N/A')}")
                    print(f"  - Total tokens: {usage.get('total_tokens', 'N/A')}")

                return {"success": True, "message": message, "usage": usage}
            else:
                print(f"\n❌ 响应格式异常: {result}")
                return {"success": False, "error": "Invalid response format"}

    except urllib.error.URLError as e:
        print(f"\n❌ 网络错误: {e}")
        return {"success": False, "error": str(e)}
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 解析错误: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"\n❌ 未知错误: {e}")
        return {"success": False, "error": str(e)}

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("📖 Minimax API 调用工具")
        print("\n使用方法:")
        print("  python minimax_client.py '你的问题'")
        print("  python minimax_client.py '你的问题' --model abab5.5-chat")
        print("\n可用模型:")
        print("  - abab5.5-chat (默认)")
        print("  - abab5.5s-chat")
        print("\n配置文件位置:")
        print(f"  {ENV_FILE}")
        sys.exit(0)

    prompt = ' '.join(sys.argv[1:])
    model = None

    # 解析 --model 参数
    if '--model' in sys.argv:
        model_idx = sys.argv.index('--model')
        if model_idx + 1 < len(sys.argv):
            model = sys.argv[model_idx + 1]

    result = call_minimax(prompt, model)

    if not result['success']:
        print(f"\n💡 提示: {result['error']}")
        print("   检查配置文件和网络连接")

if __name__ == "__main__":
    main()
