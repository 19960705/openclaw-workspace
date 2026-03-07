#!/usr/bin/env python3
"""
应用 openclaw_not_found 修复
"""

import os
import json
from pathlib import Path

HOME = Path.home()
WRAPPER_PATH = HOME / ".openclaw/workspace/scripts/openclaw-wrapper.sh"

def apply_openclaw_path_fix():
    """应用 openclaw 路径修复"""
    
    print("🔧 应用 openclaw_not_found 修复...\n")
    
    # 1. 创建环境变量配置
    env_fix = """
# OpenClaw PATH fix
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
export OPENCLAW_PATH="/opt/homebrew/bin/openclaw"
"""
    
    # 2. 检查 shell 配置文件
    shell_configs = [
        HOME / ".zshrc",
        HOME / ".bashrc",
        HOME / ".profile"
    ]
    
    for config in shell_configs:
        if config.exists():
            with open(config, 'r') as f:
                content = f.read()
            
            if "OPENCLAW_PATH" not in content:
                print(f"✅ 添加 PATH 到 {config}")
                with open(config, 'a') as f:
                    f.write(f"\n{env_fix}\n")
            else:
                print(f"⏭️  {config} 已包含 OPENCLAW_PATH")
    
    # 3. 创建 cron 环境文件
    cron_env = HOME / ".openclaw/cron/env.sh"
    cron_env.parent.mkdir(parents=True, exist_ok=True)
    
    with open(cron_env, 'w') as f:
        f.write(env_fix)
    
    print(f"✅ 创建 cron 环境文件: {cron_env}")
    
    # 4. 验证修复
    import subprocess
    try:
        result = subprocess.run(
            ["bash", "-c", f"source {cron_env} && which openclaw"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ 验证成功: openclaw 位于 {result.stdout.strip()}")
        else:
            print(f"⚠️  验证失败: {result.stderr}")
    except Exception as e:
        print(f"⚠️  验证出错: {e}")
    
    print("\n📝 下一步:")
    print("1. 重启终端或运行: source ~/.zshrc")
    print("2. 在 cron 任务中添加: source ~/.openclaw/cron/env.sh")
    print("3. 或使用 wrapper: bash ~/.openclaw/workspace/scripts/openclaw-wrapper.sh <command>")

if __name__ == "__main__":
    apply_openclaw_path_fix()
