#!/usr/bin/env python3
"""
OpenClaw 自愈系统 - 统一入口
整合所有自动修复功能
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

def run_fix(script_name, description):
    """运行修复脚本"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    script_path = SCRIPTS_DIR / script_name
    try:
        result = subprocess.run(
            ["python3", str(script_path)],
            timeout=60
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⚠️  {description} 超时")
        return False
    except Exception as e:
        print(f"❌ {description} 失败: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║          OpenClaw Self-Healing System v1.0              ║
║                                                          ║
║  自动检测和修复常见问题：                                  ║
║  1. OpenClaw 命令路径问题                                 ║
║  2. 浏览器服务不可达                                       ║
║  3. Gateway device token 不匹配                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    results = {}
    
    # 1. 修复 openclaw 路径问题
    results['openclaw_path'] = run_fix(
        "fix-openclaw-path.py",
        "修复 OpenClaw 命令路径问题"
    )
    
    # 2. 修复浏览器服务
    results['browser_service'] = run_fix(
        "fix-browser-service.py",
        "修复浏览器服务连接问题"
    )
    
    # 3. 修复 gateway token
    results['gateway_token'] = run_fix(
        "fix-gateway-token.py",
        "修复 Gateway Device Token"
    )
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("📊 修复结果汇总")
    print(f"{'='*60}")
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}: {'成功' if success else '失败'}")
    
    print(f"\n总计: {success_count}/{total_count} 修复成功")
    
    if success_count == total_count:
        print("\n🎉 所有问题已修复！")
        return 0
    else:
        print("\n⚠️  部分问题未能自动修复，请查看上方详细信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
