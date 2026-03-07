#!/usr/bin/env python3
"""
Self-Healing Agent - 自动检测和修复工具失败
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

HOME = Path.home()
STATE_PATH = HOME / ".openclaw/foundry/cron-self-improve-loop.json"
FIXES_PATH = HOME / ".openclaw/foundry/self-heal-fixes.json"
BACKUP_DIR = HOME / ".openclaw/foundry/backups"

def load_failure_stats():
    """加载失败统计"""
    if not STATE_PATH.exists():
        return None
    with open(STATE_PATH) as f:
        return json.load(f)

def analyze_failures(state, threshold=3):
    """分析高频失败"""
    candidates = []
    counts = state.get("counts", {})
    
    for sig, count in counts.items():
        if count >= threshold:
            candidates.append({"sig": sig, "count": count})
    
    return candidates

def generate_fix(sig):
    """为失败签名生成修复建议"""
    fixes = {
        "gateway:device_token_mismatch": {
            "title": "Gateway Token 自动检查",
            "description": "在连接前检查 token 有效性，失败时触发轮换",
            "code": """
# 添加到 gateway 连接逻辑前
async def check_gateway_token(gateway_url):
    try:
        response = await fetch(f"{gateway_url}/health")
        if response.status == 401:
            print("[auto-heal] Token 失效，需要轮换")
            # 触发 token 重新生成
            return False
        return True
    except Exception as e:
        print(f"[auto-heal] Gateway 健康检查失败: {e}")
        return False
""",
            "apply_to": "gateway connection hooks"
        },
        
        "browser:control_unreachable": {
            "title": "浏览器服务健康检查",
            "description": "操作前检查服务状态，失败时自动重启",
            "code": """
# 添加到浏览器操作前
async def ensure_browser_ready():
    import subprocess
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:3000/health"],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            print("[auto-heal] 浏览器服务不可达，尝试重启")
            # 可以添加重启逻辑
            return False
        return True
    except Exception as e:
        print(f"[auto-heal] 浏览器检查失败: {e}")
        return False
""",
            "apply_to": "browser tool wrappers"
        },
        
        "exec:openclaw_not_found": {
            "title": "OpenClaw 路径检测",
            "description": "使用绝对路径或动态检测",
            "code": """
# 替换裸 exec openclaw 调用
import subprocess
import shutil

def get_openclaw_path():
    # 优先使用环境变量
    if path := os.environ.get("OPENCLAW_PATH"):
        return path
    
    # 尝试 which
    if path := shutil.which("openclaw"):
        return path
    
    # Fallback 到常见位置
    common_paths = [
        "/opt/homebrew/bin/openclaw",
        "/usr/local/bin/openclaw",
        str(Path.home() / ".local/bin/openclaw")
    ]
    
    for p in common_paths:
        if Path(p).exists():
            return p
    
    raise FileNotFoundError("openclaw not found")

# 使用
openclaw = get_openclaw_path()
subprocess.run([openclaw, "status"])
""",
            "apply_to": "exec tool calls"
        }
    }
    
    return fixes.get(sig, {
        "title": f"未知失败: {sig}",
        "description": "需要手动分析",
        "code": "# 暂无自动修复方案",
        "apply_to": "manual"
    })

def save_fixes(fixes):
    """保存修复建议"""
    FIXES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(FIXES_PATH, "w") as f:
        json.dump(fixes, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Self-Healing Agent")
    parser.add_argument("--dry-run", action="store_true", help="仅分析不修改")
    parser.add_argument("--threshold", type=int, default=3, help="失败阈值")
    parser.add_argument("--apply", action="store_true", help="应用修复")
    
    args = parser.parse_args()
    
    # 1. 加载失败统计
    state = load_failure_stats()
    if not state:
        print("❌ 无法读取失败统计")
        print("提示：请先运行 cron-self-improve-loop hook")
        sys.exit(1)
    
    # 2. 分析失败
    candidates = analyze_failures(state, args.threshold)
    if not candidates:
        print("✅ 当前无需自愈的问题")
        print(f"失败统计: {state.get('counts', {})}")
        sys.exit(0)
    
    print(f"🔍 发现 {len(candidates)} 个可自愈的问题:\n")
    
    # 3. 生成修复
    fixes = []
    for item in candidates:
        sig = item["sig"]
        count = item["count"]
        fix = generate_fix(sig)
        
        print(f"📌 {fix['title']}")
        print(f"   失败次数: {count}")
        print(f"   描述: {fix['description']}")
        print(f"   应用到: {fix['apply_to']}")
        print()
        
        fixes.append({
            "sig": sig,
            "count": count,
            "fix": fix,
            "generated_at": datetime.now().isoformat()
        })
    
    # 4. 保存修复建议
    save_fixes(fixes)
    print(f"💾 修复建议已保存到: {FIXES_PATH}")
    
    if args.dry_run:
        print("\n🔬 Dry run 模式 - 未应用任何修改")
        print("提示：使用 --apply 应用修复")
    elif args.apply:
        print("\n⚠️  自动应用功能开发中")
        print("当前请手动应用修复代码")
    else:
        print("\n提示：使用 --apply 应用修复，或 --dry-run 仅查看")

if __name__ == "__main__":
    main()
