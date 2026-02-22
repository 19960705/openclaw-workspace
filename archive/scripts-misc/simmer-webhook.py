#!/usr/bin/env python3
"""
注册 Simmer Webhook
"""

import os
from simmer_sdk import SimmerClient

SIMMER_API_KEY = os.environ.get("SIMMER_API_KEY")

def main():
    print("🔗 注册 Simmer Webhook...")

    client = SimmerClient(api_key=SIMMER_API_KEY, venue="simmer")

    # 注册 webhook（需要 HTTPS URL）
    # 这里先用一个示例 URL，实际需要替换为你的服务器
    webhook_url = "https://your-server.example.com/webhook"

    try:
        webhook = client.register_webhook(
            url=webhook_url,
            events=["trade.executed", "market.resolved"],
            secret="36cb3a77aa9bda191cd1c0b2f23678d6"  # 用户提供的 token
        )

        print(f"✅ Webhook 注册成功！")
        print(f"   Webhook ID: {webhook.get('id')}")
        print(f"   URL: {webhook_url}")
        print(f"   Events: trade.executed, market.resolved")
    except Exception as e:
        print(f"❌ 注册失败: {e}")

if __name__ == "__main__":
    if not SIMMER_API_KEY:
        print("❌ SIMMER_API_KEY 未设置")
    else:
        main()
