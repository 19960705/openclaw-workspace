#!/usr/bin/env python3
"""Simmer portfolio check script - called by OpenClaw heartbeat/commands."""

import json
import sys
import os

# Load API key and venue
env_file = os.path.expanduser("~/.openclaw/workspace/.env.simmer")
api_key = None
venue = os.environ.get("SIMMER_VENUE", "simmer")  # 默认使用模拟环境
wallet_address = os.environ.get("SIMMER_WALLET_ADDRESS", None)

# 优先读取环境变量（支持 real 模式）
if os.environ.get("REAL_SIMMER_API_KEY"):
    api_key = os.environ.get("REAL_SIMMER_API_KEY")
    venue = os.environ.get("REAL_SIMMER_VENUE", "polymarket")
elif os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith("SIMMER_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
            elif line.startswith("SIMMER_VENUE="):
                venue = line.strip().split("=", 1)[1]
            elif line.startswith("SIMMER_WALLET_ADDRESS="):
                wallet_address = line.strip().split("=", 1)[1]

if not api_key:
    print(json.dumps({"error": "No SIMMER_API_KEY found"}))
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.simmer-venv/lib/python3.14/site-packages"))
from simmer_sdk.client import SimmerClient

client = SimmerClient(api_key=api_key, venue=venue)

mode = sys.argv[1] if len(sys.argv) > 1 else "summary"

if mode == "summary":
    positions = client.get_positions()
    portfolio = client.get_portfolio()
    
    resolved = [p for p in positions if p.status == "resolved"]
    active = [p for p in positions if p.status == "active"]
    wins = [p for p in resolved if p.pnl > 0]
    losses = [p for p in resolved if p.pnl < 0]
    
    total_pnl = sum(p.pnl for p in positions)
    resolved_pnl = sum(p.pnl for p in resolved)
    active_pnl = sum(p.pnl for p in active)
    
    result = {
        "balance_usdc": portfolio.get("balance_usdc", 0) if portfolio else 0,
        "total_positions": len(positions),
        "resolved": len(resolved),
        "active": len(active),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(len(wins) / len(resolved) * 100) if resolved else 0,
        "resolved_pnl": round(resolved_pnl, 2),
        "active_pnl": round(active_pnl, 2),
        "total_pnl": round(total_pnl, 2),
        "top_active": [
            {
                "question": p.question[:60],
                "pnl": round(p.pnl, 2),
                "side": "YES" if p.shares_yes > 0 else "NO"
            }
            for p in sorted(active, key=lambda x: abs(x.pnl), reverse=True)[:5]
        ],
        "alerts": []
    }
    
    # Check for positions needing attention (big losses or near expiry)
    for p in active:
        if p.pnl < -5:
            result["alerts"].append(f"⚠️ 大额亏损: {p.question[:40]}... PnL: {p.pnl:+.2f}")
    
    print(json.dumps(result, ensure_ascii=False))

elif mode == "markets":
    query = sys.argv[2] if len(sys.argv) > 2 else ""
    if query:
        markets = client.find_markets(query)
    else:
        markets = client.get_markets(status="active", limit=20)
    
    result = []
    for m in markets:
        result.append({
            "id": m.id,
            "question": m.question,
            "probability": round(m.current_probability, 3),
            "source": m.import_source,
            "divergence": round(m.divergence, 3) if m.divergence else None,
            "resolves_at": m.resolves_at
        })
    print(json.dumps(result, ensure_ascii=False))

elif mode == "trade":
    # trade <market_id> <side> <amount> [reasoning]
    market_id = sys.argv[2]
    side = sys.argv[3]
    amount = float(sys.argv[4])
    reasoning = sys.argv[5] if len(sys.argv) > 5 else None
    
    result = client.trade(
        market_id=market_id,
        side=side,
        amount=amount,
        source="sdk:keonho",
        reasoning=reasoning
    )
    print(json.dumps({
        "success": result.success,
        "trade_id": result.trade_id,
        "market_id": result.market_id,
        "side": result.side,
        "venue": result.venue
    }))

elif mode == "positions":
    positions = client.get_positions()
    active = [p for p in positions if p.status == "active"]
    for p in sorted(active, key=lambda x: x.pnl, reverse=True):
        icon = "🟢" if p.pnl >= 0 else "🔴"
        side = "YES" if p.shares_yes > 0 else "NO"
        print(f"{icon} {p.question[:55]} | {side} | PnL: {p.pnl:+.2f}")

elif mode == "opportunities":
    # Find high-divergence markets (Simmer vs Polymarket price gap)
    markets = client.get_markets(status="active", limit=50)
    opps = [m for m in markets if m.divergence and abs(m.divergence) > 0.1]
    opps.sort(key=lambda x: abs(x.divergence), reverse=True)
    
    result = []
    for m in opps[:10]:
        result.append({
            "question": m.question,
            "id": m.id,
            "probability": round(m.current_probability, 3),
            "divergence": round(m.divergence, 3),
            "source": m.import_source,
            "resolves_at": m.resolves_at
        })
    print(json.dumps(result, ensure_ascii=False))
