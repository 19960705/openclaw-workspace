#!/usr/bin/env python3
"""
自由时间探险任务 (05:00-07:00)
自动执行有价值的探索任务
"""
import subprocess
import json
from datetime import datetime

def run_command(cmd):
    """运行命令"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout[:500] if result.returncode == 0 else f"Error: {result.stderr[:200]}"
    except Exception as e:
        return f"Exception: {str(e)}"

def main():
    print(f"🌅 自由时间探险 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 40)
    
    tasks = [
        ("📰 AI 新闻搜索", "curl -s 'https://newsnow.ai/' | head -20"),
        ("🔍 搜索新技术趋势", "curl -s 'https://news.ycombinator.com/' | grep -o '<a href=\"[^\"]*\" rel' | head -10"),
    ]
    
    results = []
    for name, cmd in tasks:
        print(f"\n{name}...")
        output = run_command(cmd)
        results.append({"task": name, "output": output[:200]})
        print(f"  ✓ 完成")
    
    # 保存结果
    output_file = f"/Users/mac/.openclaw/workspace/data/exploration_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ 探险完成，保存在: {output_file}")

if __name__ == "__main__":
    main()
