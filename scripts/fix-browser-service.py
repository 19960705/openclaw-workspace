#!/usr/bin/env python3
"""
浏览器服务健康检查和自动恢复
"""

import subprocess
import time
import sys
import json
from pathlib import Path

BROWSER_SERVICE_URL = "http://localhost:3000"
MAX_RETRIES = 3
RETRY_DELAY = 5

def check_browser_service():
    """检查浏览器服务是否可达"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
             f"{BROWSER_SERVICE_URL}/health"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() == "200"
    except Exception as e:
        print(f"❌ 浏览器服务检查失败: {e}")
        return False

def restart_browser_service():
    """尝试重启浏览器服务"""
    print("🔄 尝试重启浏览器服务...")
    
    # 方法 1: 通过 OpenClaw gateway 重启
    try:
        subprocess.run(
            ["/opt/homebrew/bin/openclaw", "gateway", "restart"],
            timeout=30,
            check=True
        )
        print("✅ Gateway 重启成功")
        time.sleep(10)  # 等待服务启动
        return True
    except Exception as e:
        print(f"⚠️  Gateway 重启失败: {e}")
    
    return False

def ensure_browser_ready():
    """确保浏览器服务就绪"""
    print("🔍 检查浏览器服务状态...")
    
    if check_browser_service():
        print("✅ 浏览器服务正常")
        return True
    
    print("❌ 浏览器服务不可达")
    
    for attempt in range(MAX_RETRIES):
        print(f"\n🔄 尝试修复 ({attempt + 1}/{MAX_RETRIES})...")
        
        if restart_browser_service():
            time.sleep(RETRY_DELAY)
            if check_browser_service():
                print("✅ 浏览器服务已恢复")
                return True
        
        if attempt < MAX_RETRIES - 1:
            print(f"⏳ 等待 {RETRY_DELAY} 秒后重试...")
            time.sleep(RETRY_DELAY)
    
    print("\n❌ 无法恢复浏览器服务")
    print("建议手动操作：")
    print("1. 检查 OpenClaw.app 是否运行")
    print("2. 重启 OpenClaw gateway: openclaw gateway restart")
    print("3. 检查端口占用: lsof -i :3000")
    
    return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="浏览器服务健康检查")
    parser.add_argument("--check-only", action="store_true", help="仅检查不修复")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    if args.check_only:
        is_healthy = check_browser_service()
        if args.json:
            print(json.dumps({"healthy": is_healthy}))
        else:
            print("✅ 浏览器服务正常" if is_healthy else "❌ 浏览器服务不可达")
        sys.exit(0 if is_healthy else 1)
    
    success = ensure_browser_ready()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
