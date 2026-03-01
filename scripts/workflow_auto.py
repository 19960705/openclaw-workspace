#!/usr/bin/env python3
"""
OpenClaw Agent 自动化工作流
集成: Rejection Log + Spec 验证 + Budget 管理
"""
import json
import sys
from pathlib import Path
from datetime import datetime

# 路径配置
SCRIPT_DIR = Path("/Users/mac/.openclaw/workspace/scripts")
LOG_FILE = Path("/Users/mac/.openclaw/logs/rejection_log.json")
BUDGET_FILE = Path("/Users/mac/.openclaw/logs/budget.json")
SPEC_FILE = Path("/Users/mac/.openclaw/specs/openclaw_agent.yaml")

def load_json(path, default):
    """加载 JSON"""
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path, data):
    """保存 JSON"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def check_budget(category="tasks", amount=1):
    """检查预算"""
    budget = load_json(BUDGET_FILE, {"daily": {}})
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    if category not in budget.get("daily", {}):
        budget["daily"][category] = {"limit": 100, "used": 0, "reset_at": today}
    
    cat = budget["daily"][category]
    
    # 重置
    if cat.get("reset_at") != today:
        cat["used"] = 0
        cat["reset_at"] = today
    
    remaining = cat["limit"] - cat["used"]
    
    if remaining >= amount:
        # 使用预算
        cat["used"] += amount
        save_json(BUDGET_FILE, budget)
        return True, remaining - amount
    
    return False, remaining

def log_decision(task, decision, details=None):
    """记录决策"""
    log = load_json(LOG_FILE, [])
    
    log.append({
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "decision": decision,
        "details": details or {}
    })
    
    # 只保留 1000 条
    if len(log) > 1000:
        log = log[-1000:]
    
    save_json(LOG_FILE, log)

def validate_spec(action, command=None):
    """验证规格"""
    import yaml
    
    if not SPEC_FILE.exists():
        return True, "no_spec"
    
    with open(SPEC_FILE) as f:
        spec = yaml.safe_load(f)
    
    security = spec.get('constraints', {}).get('security', {})
    
    # 需要审批的操作
    if action in security.get('require_approval_for', []):
        return False, "requires_approval"
    
    # 被阻止的命令
    for blocked in security.get('blocked_commands', []):
        if command and blocked in command:
            return False, "blocked_command"
    
    return True, "allowed"

def run_task(task_name, action, command=None, budget_category="tasks"):
    """
    运行任务的完整工作流
    
    Returns: (success, message)
    """
    print(f"\n🔄 {task_name}")
    print(f"   Action: {action}")
    
    # 1. Spec 验证
    allowed, reason = validate_spec(action, command)
    if not allowed:
        log_decision(task_name, "rejected", {"reason": reason, "action": action})
        return False, f"❌ Spec 拒绝: {reason}"
    
    # 2. Budget 检查
    has_budget, remaining = check_budget(budget_category)
    if not has_budget:
        log_decision(task_name, "rejected", {"reason": "budget_exceeded"})
        return False, f"❌ 预算不足: {remaining} 剩余"
    
    # 3. 记录执行
    log_decision(task_name, "executed", {"action": action, "remaining": remaining})
    
    return True, f"✅ 执行中 (剩余预算: {remaining})"

# CLI
if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = sys.argv[1]
        action = sys.argv[2] if len(sys.argv) > 2 else "default"
        command = sys.argv[3] if len(sys.argv) > 3 else None
        
        success, msg = run_task(task, action, command)
        print(msg)
        sys.exit(0 if success else 1)
    else:
        print("📊 OpenClaw Agent Workflow")
        print("\n用法:")
        print("  workflow.py <task_name> <action> [command]")
        print("\n示例:")
        print("  workflow.py twitter_post social_media_post")
        print("  workflow.py run_script exec 'rm -rf /'")
        
        # 显示状态
        print("\n📈 状态:")
        budget = load_json(BUDGET_FILE, {})
        for cat, data in budget.get("daily", {}).items():
            print(f"  {cat}: {data.get('used', 0)}/{data.get('limit', 100)}")
