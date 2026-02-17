#!/usr/bin/env python3
"""
Simmer Auto-Trader — Polymarket USDC Trading
支持 WAVELET_PRIVATE_KEY（Polymarket 真金私钥）
"""

import json
import sys
import os
from datetime import datetime, timezone, timedelta

# Setup
env_file = os.path.expanduser("~/.openclaw/workspace/.env.simmer")
api_key = None
wavelet_key = None
venue = "polymarket"  # 默认使用 Polymarket mainnet

if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            if line.startswith("SIMMER_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
            elif line.startswith("WAVELET_PRIVATE_KEY="):
                wavelet_key = line.strip().split("=", 1)[1]

if not api_key:
    print(json.dumps({"error": "No API key"}))
    sys.exit(1)

sys.path.insert(0, os.path.expanduser("~/.simmer-venv/lib/python3.14/site-packages"))
from simmer_sdk.client import SimmerClient

client = SimmerClient(api_key=api_key, venue=venue)

TRADE_LOG = os.path.expanduser("~/.openclaw/workspace/memory/auto-trades.json")

def load_trade_log():
    if os.path.exists(TRADE_LOG):
        with open(TRADE_LOG) as f:
            return json.load(f)
    return {"trades": [], "daily_count": 0, "daily_date": "", "total_invested": 0}

def save_trade_log(log):
    with open(TRADE_LOG, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def get_crypto_price(symbol):
    """获取实时加密货币价格"""
    try:
        r = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot", timeout=5)
        return float(r.json()["data"]["amount"])
    except:
        return None

def evaluate_crypto_threshold(question, current_price):
    """评估加密货币阈值市场是否安全"""
    import re
    
    match = re.search(r'above \$([0-9,]+)', question)
    if not match:
        return None, None
    
    threshold = float(match.group(1).replace(",", ""))
    
    if "Bitcoin" in question or "BTC" in question:
        price = current_price.get("BTC")
    elif "Ethereum" in question or "ETH" in question:
        price = current_price.get("ETH")
    else:
        return None, None
    
    if not price:
        return None, None
    
    margin_pct = (price - threshold) / threshold * 100
    return margin_pct, {
        "threshold": threshold,
        "current_price": price,
        "margin_pct": round(margin_pct, 2)
    }

def find_safe_trades():
    """查找符合保守策略的交易机会"""
    client = SimmerClient(api_key=api_key, venue=venue)
    markets = client.get_markets(status="active", limit=50)
    current_prices = {
        "BTC": get_crypto_price("BTC"),
        "ETH": get_crypto_price("ETH")
    }
    
    now = datetime.now(timezone.utc)
    candidates = []
    
    positions = client.get_positions()
    existing_market_ids = set()
    for p in positions:
        existing_market_ids.add(p.market_id)
    
    for m in markets:
        if m.id in existing_market_ids:
            continue
        
        if m.resolves_at:
            try:
                resolve_time = datetime.fromisoformat(m.resolves_at.replace("Z", "+00:00"))
                if resolve_time < now + timedelta(minutes=30):
                    continue
            except:
                pass
        
        if "Up or Down" in m.question:
            continue
        
        prob = m.current_probability
        
        # 检查是否提供了 WAVELET_PRIVATE_KEY
        if wavelet_key:
            # Polymarket 真金：使用 wavelet 参数
            if ("above $" in m.question or "below $" in m.question) and ("Bitcoin" in m.question or "Ethereum" in m.question):
                margin_pct, details = evaluate_crypto_threshold(m.question, current_prices)
                
                if margin_pct is not None:
                    # 高确信度策略
                    if margin_pct > 3 and prob > 0.95:
                        candidates.append({
                            "market": m,
                            "side": "yes",
                            "amount": 1.0,
                            "confidence": prob,
                            "strategy": "crypto-threshold-real",
                            "reasoning": f"价格 {details['current_price']:.0f} 高于阈值 {details['threshold']:.0f} ({margin_pct:.1f}%)。YES 概率高，使用真金。",
                            "details": details
                        })
                    elif margin_pct < -5 and prob < 0.05:
                        candidates.append({
                            "market": m,
                            "side": "no",
                            "amount": 1.0,
                            "confidence": 1 - prob,
                            "strategy": "crypto-threshold-real",
                            "reasoning": f"价格 {details['current_price']:.0f} 低于阈值 {details['threshold']:.0f} ({abs(margin_pct):.1f}%)。NO 概率高，使用真金。",
                            "details": details
                        })
        
        # 模拟盘：低门槛策略
        else:
            # Simmer 模拟盘：宽松阈值策略
            if prob > 0.85:
                candidates.append({
                    "market": m,
                    "side": "yes",
                    "amount": 0.50,
                    "confidence": prob,
                    "strategy": "near-certain-yes",
                    "reasoning": f"市场概率 {prob*100:.1f}%，接近确定的 YES 结果。",
                    "details": {}
                })
            elif prob < 0.15 and prob > 0:
                candidates.append({
                    "market": m,
                    "side": "no",
                    "amount": 0.50,
                    "confidence": 1 - prob,
                    "strategy": "near-certain-no",
                    "reasoning": f"市场概率 {prob*100:.1f}%，接近确定的 NO 结果。",
                    "details": {}
                })
    
    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    return candidates

def execute_trades(dry_run=False, max_trades=3):
    """执行安全交易"""
    client = SimmerClient(api_key=api_key, venue=venue)
    log = load_trade_log()
    
    today = datetime.now().strftime("%Y-%m-%d")
    if log["daily_date"] != today:
        log["daily_count"] = 0
        log["daily_date"] = today
    
    if log["daily_count"] >= 10:
        print(json.dumps({"status": "daily_limit", "message": "已达每日自动交易上限(10笔)"}))
        return
    
    candidates = find_safe_trades()
    
    if not candidates:
        print(json.dumps({"status": "no_opportunities", "message": "没有符合条件的安全交易机会"}))
        return
    
    results = []
    trades_made = 0
    
    for c in candidates[:max_trades]:
        if log["daily_count"] >= 10:
            break
        
        trade_info = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": c["market"].question,
            "market_id": c["market"].id,
            "side": c["side"],
            "amount": c["amount"],
            "strategy": c["strategy"],
            "reasoning": c["reasoning"],
            "confidence": c["confidence"],
            "probability": c["market"].current_probability,
        }
        
        if dry_run:
            trade_info["status"] = "dry_run"
            results.append(trade_info)
        else:
            try:
                result = client.trade(
                    market_id=c["market"].id,
                    side=c["side"],
                    amount=c["amount"],
                    venue=venue,
                    source=f"sdk:auto-{c['strategy']}",
                    reasoning=c["reasoning"]
                )
                trade_info["status"] = "executed" if result.success else "failed"
                trade_info["trade_id"] = result.trade_id
                trades_made += 1
                log["daily_count"] += 1
                log["total_invested"] += c["amount"]
            except Exception as e:
                trade_info["status"] = "error"
                trade_info["error"] = str(e)
            
            results.append(trade_info)
            log["trades"].append(trade_info)
    
    save_trade_log(log)
    print(json.dumps({
        "status": "ok",
        "venue": venue,
        "has_wavelet_key": bool(wavelet_key),
        "trades_found": len(candidates),
        "trades_executed": trades_made,
        "results": results,
        "daily_count": log["daily_count"]
    }, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    
    if mode == "scan":
        execute_trades(dry_run=True)
    elif mode == "trade":
        max_trades = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        execute_trades(dry_run=False, max_trades=max_trades)
    elif mode == "log":
        log = load_trade_log()
        print(json.dumps(log, indent=2, ensure_ascii=False))
