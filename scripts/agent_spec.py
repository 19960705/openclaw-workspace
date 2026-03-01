#!/usr/bin/env python3
"""
Agent Spec - YAML 规格定义系统
来自 SpecMarket 的最佳实践：规格即合约
"""
import os
import yaml
import json
from pathlib import Path
from datetime import datetime

# 配置目录
SPEC_DIR = Path("/Users/mac/.openclaw/specs")
SPEC_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SPEC = """
# OpenClaw Agent Spec - 默认规格
# 来自 SpecMarket 最佳实践

spec:
  name: "OpenClaw-Agent"
  version: "1.0"
  created: "{timestamp}"

# 约束定义
constraints:
  # 时间约束
  time:
    max_task_duration: 300  # 5分钟
    cooldown_between_tasks: 10  # 10秒
    max_daily_runtime: 7200  # 2小时
  
  # 资源约束
  resources:
    max_api_calls_per_hour: 100
    max_tokens_per_day: 1000000
    max_concurrent_tasks: 3
  
  # 安全约束
  security:
    require_approval_for:
      - financial_transaction
      - social_media_post
      - create_account
      - delete_file
    blocked_commands:
      - rm -rf /
      - curl | sh
      - sudo
  
  # 允许的操作
  allowed_channels:
    - telegram
    - discord
    - slack
  
  # 输出限制
  output:
    max_length: 10000
    require_confirmation_for_delete: true

# 成功标准
success_criteria:
  - type: "task_completion"
    rate: 0.95
  - type: "error_rate"
    max: 0.05
  - type: "response_time"
    max_seconds: 30

# 验证规则
verification:
  log_all_tasks: true
  log_rejections: true
  require_receipt_chain: false
""".format(timestamp=datetime.now().isoformat())

def load_spec(name="default"):
    """加载规格"""
    spec_file = SPEC_DIR / f"{name}.yaml"
    
    if spec_file.exists():
        with open(spec_file) as f:
            return yaml.safe_load(f)
    
    # 返回默认规格
    return yaml.safe_load(DEFAULT_SPEC)

def save_spec(name, spec):
    """保存规格"""
    spec_file = SPEC_DIR / f"{name}.yaml"
    with open(spec_file, 'w') as f:
        yaml.dump(spec, f, default_flow_style=False)
    print(f"✅ Spec saved: {spec_file}")

def validate_task(task, spec=None):
    """
    验证任务是否符合规格
    
    Returns:
        (allowed: bool, reason: str, details: dict)
    """
    if spec is None:
        spec = load_spec()
    
    constraints = spec.get('constraints', {})
    
    # 检查安全约束
    security = constraints.get('security', {})
    
    # 检查需要审批的操作
    require_approval = security.get('require_approval_for', [])
    if task.get('action') in require_approval:
        return False, "requires_approval", {"action": task.get('action')}
    
    # 检查被阻止的命令
    blocked = security.get('blocked_commands', [])
    cmd = task.get('command', '')
    for b in blocked:
        if b in cmd:
            return False, "blocked_command", {"command": b}
    
    # 检查频道
    allowed_channels = security.get('allowed_channels', [])
    channel = task.get('channel')
    if channel and channel not in allowed_channels:
        return False, "channel_not_allowed", {"channel": channel}
    
    return True, "allowed", {}

def get_spec_status(spec=None):
    """获取规格状态"""
    if spec is None:
        spec = load_spec()
    
    constraints = spec.get('constraints', {})
    
    return {
        "name": spec.get('spec', {}).get('name'),
        "version": spec.get('spec', {}).get('version'),
        "constraints": {
            "max_task_duration": constraints.get('time', {}).get('max_task_duration'),
            "require_approval_for": constraints.get('security', {}).get('require_approval_for', []),
            "allowed_channels": constraints.get('security', {}).get('allowed_channels', []),
        }
    }

def list_specs():
    """列出所有规格"""
    return [f.stem for f in SPEC_DIR.glob("*.yaml")]

# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            print("📋 Available specs:")
            for s in list_specs():
                print(f"  - {s}")
        
        elif sys.argv[1] == "status":
            status = get_spec_status()
            print(f"📊 Spec: {status['name']} v{status['version']}")
            print(f"\nConstraints:")
            print(f"  Max task duration: {status['constraints']['max_task_duration']}s")
            print(f"  Require approval: {status['constraints']['require_approval_for']}")
            print(f"  Allowed channels: {status['constraints']['allowed_channels']}")
        
        elif sys.argv[1] == "validate":
            task = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
            allowed, reason, details = validate_task(task)
            print(f"{'✅' if allowed else '❌'} {reason}")
            if details:
                print(f"   {details}")
        
        else:
            # 保存自定义规格
            name = sys.argv[1]
            save_spec(name, yaml.safe_load(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SPEC))
    else:
        status = get_spec_status()
        print(f"📊 Current spec: {status['name']} v{status['version']}")
        print("\nUsage:")
        print("  spec.py list          - List specs")
        print("  spec.py status       - Show current spec")
        print("  spec.py validate {}  - Validate task")
