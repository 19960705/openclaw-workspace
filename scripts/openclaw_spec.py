#!/usr/bin/env python3
"""
OpenClaw Agent Spec - 实践 SpecMarket 理念
定义 Agent 的行为约束和规格
"""
import json
import yaml
from pathlib import Path
from datetime import datetime

SPEC_FILE = Path("/Users/mac/.openclaw/specs/openclaw_agent.yaml")

# OpenClaw Agent 规格定义
OPENCLAW_SPEC = {
    "spec": {
        "name": "OpenClaw-Agent",
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "description": "Personal AI assistant for Lunah"
    },
    
    # 约束定义
    "constraints": {
        "time": {
            "max_task_duration": 300,  # 5分钟
            "cooldown_between_tasks": 10,
            "max_daily_runtime": 7200  # 2小时
        },
        "resources": {
            "max_api_calls_per_hour": 100,
            "max_tokens_per_day": 1000000,
            "max_concurrent_tasks": 3
        },
        "security": {
            "require_approval_for": [
                "financial_transaction",
                "social_media_post", 
                "create_account",
                "delete_file",
                "system_change"
            ],
            "blocked_commands": [
                "rm -rf /",
                "curl | sh",
                "sudo",
                "chmod 777"
            ],
            "allowed_channels": ["telegram", "discord", "slack"]
        },
        "output": {
            "max_length": 10000,
            "require_confirmation_for_delete": True
        }
    },
    
    # 验证规则
    "verification": {
        "log_all_tasks": True,
        "log_rejections": True,
        "log_decisions": True,
        "receipt_chain": False
    },
    
    # 预算系统
    "budget": {
        "daily": {
            "api_calls": 100,
            "tokens": 1000000,
            "tasks": 50
        },
        "per_task": {
            "max_duration": 300,
            "max_cost": 1.0
        }
    },
    
    # 能力定义
    "capabilities": {
        "can_do": [
            "search_web",
            "read_write_files", 
            "run_scripts",
            "send_messages",
            "schedule_tasks",
            "browser_automation"
        ],
        "cannot_do": [
            "financial_transactions",
            "social_media_without_approval",
            "system_admin"
        ]
    }
}

def save_spec():
    """保存规格"""
    with open(SPEC_FILE, 'w') as f:
        yaml.dump(OPENCLAW_SPEC, f, default_flow_style=False)
    print(f"✅ Saved: {SPEC_FILE}")

def load_spec():
    """加载规格"""
    if SPEC_FILE.exists():
        with open(SPEC_FILE) as f:
            return yaml.safe_load(f)
    return OPENCLAW_SPEC

def validate_task(task_dict):
    """验证任务"""
    spec = load_spec()
    constraints = spec.get('constraints', {})
    security = constraints.get('security', {})
    
    action = task_dict.get('action', '')
    command = task_dict.get('command', '')
    channel = task_dict.get('channel', '')
    
    # 检查需要审批
    if action in security.get('require_approval_for', []):
        return False, f"⚠️ 需要审批: {action}"
    
    # 检查被阻止的命令
    for blocked in security.get('blocked_commands', []):
        if blocked in command:
            return False, f"❌ 禁止命令: {blocked}"
    
    # 检查频道
    allowed = security.get('allowed_channels', [])
    if allowed and channel not in allowed:
        return False, f"❌ 不允许频道: {channel}"
    
    return True, "✅ 允许执行"

# 测试
if __name__ == "__main__":
    save_spec()
    
    print("\n📋 OpenClaw Agent Spec")
    print("=" * 40)
    
    spec = load_spec()
    print(f"Name: {spec['spec']['name']}")
    print(f"Version: {spec['spec']['version']}")
    print(f"\nConstraints:")
    print(f"  Max task: {spec['constraints']['time']['max_task_duration']}s")
    print(f"  Require approval: {spec['constraints']['security']['require_approval_for']}")
    print(f"  Allowed channels: {spec['constraints']['security']['allowed_channels']}")
    
    print(f"\n✅ Can do: {spec['capabilities']['can_do']}")
    print(f"❌ Cannot do: {spec['capabilities']['cannot_do']}")
