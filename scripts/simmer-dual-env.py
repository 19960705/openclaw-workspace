#!/usr/bin/env python3
"""Simmer 双环境同步学习脚本 - 同时在模拟盘和真金盘运行"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta

# Load API keys
env_file = os.path.expanduser("~/.openclaw/workspace/.env.simmer")
simmer_key = None
poly_key = None

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith("SIMMER_API_KEY="):
                simmer_key = line.strip().split("=", 1)[1]
            elif line.startswith("REAL_SIMMER_API_KEY="):
                poly_key = line.strip().split("=", 1)[1]

if not simmer_key or not poly_key:
    print(json.dumps({"error": "Missing API keys"}))
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.simmer-venv/lib/python3.14/site-packages"))
from simmer_sdk.client import SimmerClient

# Create two clients
simmer_client = SimmerClient(api_key=simmer_key, venue="simmer")  # 模拟盘
poly_client = SimmerClient(api_key=poly_key, venue="polymarket")  # 真金盘

mode = sys.argv[1] if len(sys.argv) > 1 else "summary"

def get_env_summary(client, env_name):
    """获取单个环境的摘要"""
    positions = client.get_positions()
    portfolio = client.get_portfolio()

    resolved = [p for p in positions if p.status == "resolved"]
    active = [p for p in positions if p.status == "active"]
    wins = [p for p in resolved if p.pnl > 0]
    losses = [p for p in resolved if p.pnl < 0]

    total_pnl = sum(p.pnl for p in positions)
    win_rate = round(len(wins) / len(resolved) * 100) if resolved else 0

    return {
        "env": env_name,
        "balance": round(portfolio.get("balance_usdc", 0), 2),
        "total_positions": len(positions),
        "resolved": len(resolved),
        "active": len(active),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": win_rate,
        "total_pnl": round(total_pnl, 2)
    }

if mode == "summary":
    """双环境对比摘要"""
    simmer_summary = get_env_summary(simmer_client, "simmer")
    poly_summary = get_env_summary(poly_client, "polymarket")

    result = {
        "simmer": simmer_summary,
        "polymarket": poly_summary,
        "comparison": {
            "win_rate_diff": poly_summary["win_rate"] - simmer_summary["win_rate"],
            "pnl_diff": poly_summary["total_pnl"] - simmer_summary["total_pnl"],
            "simmer_advantage": "数据量大，可快速试错",
            "poly_advantage": "真实盈利，小额定力测试"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

elif mode == "test":
    """在模拟盘执行测试交易"""
    # 查找高确信度机会
    markets = simmer_client.get_markets(status="active", limit=20)
    opps = [m for m in markets if m.divergence and abs(m.divergence) > 0.1]
    opps.sort(key=lambda x: abs(x.divergence), reverse=True)

    if opps:
        market = opps[0]
        result = simmer_client.trade(
            market_id=market.id,
            side="YES" if market.current_probability < 0.5 else "NO",
            amount=5,  # 模拟盘可以大额测试
            source="sdk:dual-env-test",
            reasoning=f"High divergence: {market.divergence}"
        )

        print(json.dumps({
            "action": "simmer_test_trade",
            "market": market.question[:60],
            "side": "YES" if market.current_probability < 0.5 else "NO",
            "amount": 5,
            "success": result.success
        }, ensure_ascii=False))
    else:
        print(json.dumps({"action": "no_opportunity", "reason": "No high-divergence markets found"}))

elif mode == "real":
    """在真金盘执行小额真实交易"""
    # 查找满足条件的真实市场
    markets = poly_client.get_markets(status="active", limit=50)

    from datetime import datetime, timezone, timedelta
    eligible = []
    for m in markets:
        if not m.resolves_at:
            continue
        try:
            resolves_at = datetime.fromisoformat(m.resolves_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            time_left = (resolves_at - now).total_seconds() / 3600
        except:
            continue

        shares = round(1 / m.current_probability, 1)

        if time_left > 12 and shares >= 5 and m.current_probability <= 0.25:
            eligible.append({
                "question": m.question,
                "prob": m.current_probability,
                "shares": shares,
                "time_left": time_left,
                "id": m.id
            })

    if eligible:
        market = eligible[0]
        result = poly_client.trade(
            market_id=market["id"],
            side="YES",
            amount=1,  # 真金盘小额测试
            source="sdk:dual-env-real",
            reasoning=f"Probability {market['prob']}, shares {market['shares']}"
        )

        print(json.dumps({
            "action": "polymarket_real_trade",
            "market": market["question"][:60],
            "amount": 1,
            "success": result.success,
            "trade_id": result.trade_id if result.success else None
        }, ensure_ascii=False))
    else:
        print(json.dumps({"action": "no_eligible_market", "reason": "No markets matching criteria"}))

elif mode == "compare":
    """对比两个环境的持仓"""
    simmer_positions = simmer_client.get_positions()
    poly_positions = poly_client.get_positions()

    result = {
        "simmer_active": len([p for p in simmer_positions if p.status == "active"]),
        "poly_active": len([p for p in poly_positions if p.status == "active"]),
        "simmer_resolved": len([p for p in simmer_positions if p.status == "resolved"]),
        "poly_resolved": len([p for p in poly_positions if p.status == "resolved"]),
        "simmer_avg_pnl": round(sum(p.pnl for p in simmer_positions) / len(simmer_positions), 2) if simmer_positions else 0,
        "poly_avg_pnl": round(sum(p.pnl for p in poly_positions) / len(poly_positions), 2) if poly_positions else 0
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

else:
    print("Usage: simmer-dual-env.py [summary|test|real|compare]")
    print("  summary  - 双环境对比摘要")
    print("  test     - 模拟盘测试交易（$5）")
    print("  real     - 真金盘小额交易（$1）")
    print("  compare  - 对比两个环境持仓")
