#!/usr/bin/env python3
"""
Agent Spec 自动化验证
在执行关键操作前自动验证
"""
import json
import sys
from pathlib import Path

SPEC_FILE = Path("/Users/mac/.openclaw/specs/default.yaml")
REJECTION_LOG = Path("/Users/mac/.openclaw/logs/rejection_log.json")

def load_spec():
    """加载规格"""
    import yaml
    if SPEC_FILE.exists():
        with open(SPEC_FILE) as f:
            return yaml.safe_load(f)
    return {}

def load_rejection_log():
    """加载拒绝日志"""
    if REJECTION_LOG.exists():
        with open(REJECTION_LOG) as f:
            return json.load(f)
    return []

def validate_and_log(task_name, action, channel=None, command=None):
    """
    验证任务并在不符合规格时记录
    
    Returns:
        (allowed: bool, message: str)
    """
    spec = load_spec()
    constraints = spec.get('constraints', {})
    security = constraints.get('security', {})
    
    # 检查需要审批的操作
    require_approval = security.get('require_approval_for', [])
    if action in require_approval:
        log_rejection(task_name, "requires_approval", {"action": action, "spec": "default"})
        return False, f"⚠️ 需要审批: {action}"
    
    # 检查被阻止的命令
    blocked = security.get('blocked_commands', [])
    if command:
        for b in blocked:
            if b in command:
                log_rejection(task_name, "blocked_command", {"command": b, "spec": "default"})
                return False, f"❌ 禁止命令: {b}"
    
    # 检查频道
    allowed_channels = security.get('allowed_channels', [])
    if channel and allowed_channels:
        if channel not in allowed_channels:
            log_rejection(task_name, "channel_not_allowed", {"channel": channel, "spec": "default"})
            return False, f"❌ 不允许的频道: {channel}"
    
    return True, "✅ 允许执行"

def log_rejection(task, reason, details):
    """记录拒绝"""
    log = load_rejection_log()
    log.append({
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "reason": reason,
        "details": details,
        "severity": "medium"
    })
    with open(REJECTION_LOG, 'w') as f:
        json.dump(log, f, indent=2)

from datetime import datetime

# CLI
if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = sys.argv[1]
        action = sys.argv[2] if len(sys.argv) > 2 else None
        channel = sys.argv[3] if len(sys.argv) > 3 else None
        command = sys.argv[4] if len(sys.argv) > 4 else None
        
        allowed, msg = validate_and_log(task, action, channel, command)
        print(msg)
        sys.exit(0 if allowed else 1)
    else:
        print("用法: validate_spec.py <task> <action> [channel] [command]")
        print("示例: validate_spec.py twitter_post social_media_post telegram")
