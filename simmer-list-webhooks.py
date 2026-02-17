#!/usr/bin/env python3
"""
列出 Simmer Webhooks
"""

import os
from simmer_sdk import SimmerClient

SIMMER_API_KEY = os.environ.get("SIMMER_API_KEY")

def main():
    print("📋 列出 Simmer Webhooks...")

    client = SimmerClient(api_key=SIMMER_API_KEY, venue="simmer")

    try:
        webhooks = client.list_webhooks()
        print(f"找到 {len(webhooks)} 个 webhook:\n")

        for wh in webhooks:
            print(f"ID: {wh.get('id')}")
            print(f"URL: {wh.get('url')}")
            print(f"Events: {wh.get('events', 'all')}")
            print(f"Secret: {wh.get('secret', 'None')}")
            print(f"Created: {wh.get('created_at', 'Unknown')}")
            print()
    except Exception as e:
        print(f"❌ 失败: {e}")

if __name__ == "__main__":
    if not SIMMER_API_KEY:
        print("❌ SIMMER_API_KEY 未设置")
    else:
        main()
