#!/usr/bin/env python3
"""Simple Simmer Test"""

import os
import json

# Load config
env_file = os.path.expanduser("~/.openclaw/workspace/.env.simmer")
api_key = None
wavelet_key = None
venue = "polymarket"

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith("SIMMER_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
            elif line.startswith("WAVELET_PRIVATE_KEY="):
                wavelet_key = line.strip().split("=", 1)[1]
            elif line.startswith("SIMMER_VENUE="):
                venue = line.strip().split("=", 1)[1]

if not api_key:
    print(json.dumps({"error": "No SIMMER_API_KEY found"}))
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.simmer-venv/lib/python3.14/site-packages"))
from simmer_sdk.client import SimmerClient

try:
    client = SimmerClient(api_key=api_key, venue=venue)
    
    print("=== Simmer SDK 初始化 ===")
    print(f"API Key: {api_key[:20]}...")
    print(f"Venue: {venue}")
    
    # Check wallet
    wallet = client.wallet_address if hasattr(client, "wallet_address") else "未检测到"
    print(f"Wallet: {wallet}")
    
    # Check portfolio
    portfolio = client.get_portfolio()
    balance = portfolio.get("balance_usdc", 0)
    print(f"Portfolio: {portfolio is not None}")
    print(f"USDC 余额: {balance}")
    
    print("✅ SDK 初始化成功！")
    
except Exception as e:
    print(f"❌ 初始化失败: {e}")
