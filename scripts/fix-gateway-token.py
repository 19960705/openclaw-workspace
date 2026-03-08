#!/usr/bin/env python3
"""
Gateway Device Token 检查和修复
"""

import subprocess
import json
import sys
from pathlib import Path

def check_gateway_status():
    """检查 gateway 状态"""
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/openclaw", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)

def rotate_device_token():
    """轮换 device token"""
    print("🔄 轮换 device token...")
    
    try:
        # 方法 1: 重启 gateway (会自动重新生成 token)
        result = subprocess.run(
            ["/opt/homebrew/bin/openclaw", "gateway", "restart"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Gateway 重启成功，token 已轮换")
            return True
        else:
            print(f"⚠️  Gateway 重启失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 轮换失败: {e}")
        return False

def fix_device_token_mismatch():
    """修复 device token mismatch"""
    print("🔍 检查 gateway 状态...")
    
    is_ok, output = check_gateway_status()
    
    if is_ok:
        print("✅ Gateway 状态正常")
        print(output)
        return True
    
    print("❌ Gateway 状态异常")
    print(output)
    
    # 尝试修复
    print("\n🔧 尝试修复...")
    
    if rotate_device_token():
        # 验证修复
        import time
        print("⏳ 等待 10 秒后验证...")
        time.sleep(10)
        
        is_ok, output = check_gateway_status()
        if is_ok:
            print("✅ 修复成功！")
            return True
        else:
            print("❌ 修复后仍有问题")
            print(output)
    
    print("\n📝 手动修复步骤：")
    print("1. 完全停止 gateway: openclaw gateway stop")
    print("2. 清理旧的 device token: rm ~/.openclaw/devices/*.json")
    print("3. 重新启动: openclaw gateway start")
    print("4. 重新配对设备（如果需要）")
    
    return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Gateway Device Token 修复")
    parser.add_argument("--check-only", action="store_true", help="仅检查不修复")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    if args.check_only:
        is_ok, output = check_gateway_status()
        if args.json:
            print(json.dumps({"healthy": is_ok, "output": output}))
        else:
            print("✅ Gateway 正常" if is_ok else "❌ Gateway 异常")
            if not is_ok:
                print(output)
        sys.exit(0 if is_ok else 1)
    
    success = fix_device_token_mismatch()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
