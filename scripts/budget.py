#!/usr/bin/env python3
"""
Agent Budget System - 预算系统
来自 Moltbook 最佳实践：Agent 需要预算而非权限
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

BUDGET_FILE = Path("/Users/mac/.openclaw/logs/budget.json")

DEFAULT_BUDGETS = {
    "daily": {
        "api_calls": {"limit": 100, "used": 0, "reset_at": None},
        "tokens": {"limit": 1000000, "used": 0, "reset_at": None},
        "tasks": {"limit": 50, "used": 0, "reset_at": None},
    },
    "per_task": {
        "max_duration": 300,  # 5分钟
        "max_cost": 1.0,    # $1
    }
}

def load_budgets():
    """加载预算"""
    if BUDGET_FILE.exists():
        with open(BUDGET_FILE) as f:
            return json.load(f)
    return DEFAULT_BUDGETS

def save_budgets(budgets):
    """保存预算"""
    with open(BUDGET_FILE, 'w') as f:
        json.dump(budgets, f, indent=2)

def reset_daily_if_needed(budgets):
    """重置每日预算"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    for category in ["api_calls", "tokens", "tasks"]:
        reset_at = budgets["daily"][category].get("reset_at")
        if reset_at != today:
            budgets["daily"][category]["used"] = 0
            budgets["daily"][category]["reset_at"] = today
    
    return budgets

def can_use(category, amount=1):
    """
    检查是否可以使用预算
    
    Returns:
        (allowed: bool, remaining: int, message: str)
    """
    budgets = load_budgets()
    budgets = reset_daily_if_needed(budgets)
    
    if category not in budgets["daily"]:
        return True, 0, "✅ 允许"
    
    limit = budgets["daily"][category]["limit"]
    used = budgets["daily"][category]["used"]
    remaining = limit - used
    
    if remaining >= amount:
        return True, remaining, f"✅ 允许 (剩余 {remaining})"
    else:
        return False, remaining, f"❌ 预算不足 (剩余 {remaining}, 需要 {amount})"

def use(category, amount=1):
    """使用预算"""
    budgets = load_budgets()
    budgets = reset_daily_if_needed(budgets)
    
    if category in budgets["daily"]:
        budgets["daily"][category]["used"] += amount
        save_budgets(budgets)
        return True
    
    return False

def get_status():
    """获取预算状态"""
    budgets = load_budgets()
    budgets = reset_daily_if_needed(budgets)
    
    status = []
    for category, data in budgets["daily"].items():
        limit = data["limit"]
        used = data["used"]
        remaining = limit - used
        pct = int(remaining / limit * 10)
        bar = "█" * pct + "░" * (10 - pct)
        status.append(f"{category}: {bar} {remaining}/{limit}")
    
    return "\n".join(status)

# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print("📊 预算状态")
            print(get_status())
        
        elif sys.argv[1] == "check":
            category = sys.argv[2] if len(sys.argv) > 2 else "tasks"
            amount = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            allowed, remaining, msg = can_use(category, amount)
            print(msg)
        
        elif sys.argv[1] == "use":
            category = sys.argv[2] if len(sys.argv) > 2 else "tasks"
            amount = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            if use(category, amount):
                print(f"✅ 已使用 {category}: {amount}")
            else:
                print(f"❌ 使用失败")
        
        else:
            print("用法:")
            print("  budget.py status          # 查看状态")
            print("  budget.py check [category] [amount]  # 检查")
            print("  budget.py use [category] [amount]    # 使用")
    else:
        print("📊 Agent 预算系统")
        print(get_status())
        print("\n用法: budget.py [status|check|use]")
