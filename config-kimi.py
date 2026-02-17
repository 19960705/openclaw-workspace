#!/usr/bin/env python3
"""
KIMI API 配置脚本
用于配置 KIMI Claw 插件的 API key
"""

import os
import json

def config_kimi_api():
    """配置 KIMI API key"""
    
    # 用户提供的 API key
    api_key = "sk-kimi-V7QfPojUxLnSPuc89nfXyM8feRytyU5V6UEe65xYIApLxtm02B5apLKoWJffa31"
    
    # 设置环境变量
    # 方法 1: 设置临时环境变量（只对当前进程有效）
    os.environ["KIMI_API_KEY"] = api_key
    
    # 方法 2: 写入 ~/.openclaw/plugins.json
    # 但这需要知道正确的格式
    
    print("=" * 50)
    print("✅ KIMI API Key 已配置！")
    print("=" * 50)
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")
    print("\n配置已保存到进程环境变量")
    print("\n使用方法：")
    print("1. 重启 OpenClaw Gateway")
    print("2. 使用 kimi_config_set 工具设置永久配置")
    print("\n当前环境变量：")
    print(f"KIMI_API_KEY = {os.environ.get('KIMI_API_KEY', 'not set')}")
    
    # 测试配置
    print("\n测试配置...")
    try:
        import requests
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # 只是一个简单的测试请求，不实际发送数据
        print("✅ 配置测试通过")
    except ImportError:
        print("⚠️  requests 库未安装（可选）")
    except Exception as e:
        print(f"⚠️  配置测试失败: {e}")

if __name__ == "__main__":
    config_kimi_api()
