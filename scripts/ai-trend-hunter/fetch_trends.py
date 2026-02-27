#!/usr/bin/env python3
"""
AI Trend Hunter - 多数据源版 v8
接入 newsnow + 手动调研
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path

TRENDS_FILE = Path(__file__).parent / "data" / "trends.json"
TRENDS_FILE.parent.mkdir(exist_ok=True)

NEWSNOW_SOURCES = [
    "hackernews",
    "github-trending-today", 
    "producthunt",
    "36kr",
    "sspai",
    "juejin",
]

def get_newsnow_trends():
    """从 newsnow 获取趋势"""
    trends = []
    for source in NEWSNOW_SOURCES:
        try:
            result = subprocess.run(
                ["/Users/mac/bin/newsnow", source, "--json"],
                capture_output=True,
                text=True,
                timeout=15
            )
            if result.returncode == 0 and result.stdout:
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, list):
                        for item in data[:3]:  # 取前3条
                            title = item.get('title', '')
                            if title and len(title) > 5:
                                trends.append(f"[{source}] {title[:80]}")
                except:
                    pass
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    return trends

def get_manual_insights():
    """手动调研 insights - 基于近期观察"""
    insights = [
        "🤖 多 Agent 系统爆发 - 2026 是多 Agent 元年",
        "⚡ 事件驱动 Agent - 从被动响应到主动触发", 
        "🎨 AI 视频生成 - Seedance/Kling/Veo3 三国大战",
        "💻 AI Coding - Claude Code vs GPT-5.3 Codex 对决",
    ]
    return insights

def main():
    print(f"\n{'='*50}")
    print(f"🤖 AI Trend Hunter - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # 1. 从 newsnow 获取
    print("📡 Fetching from newsnow...")
    newsnow_trends = get_newsnow_trends()
    print(f"   Got {len(newsnow_trends)} items")
    
    # 2. 手动 insights
    manual_insights = get_manual_insights()
    
    # 3. 合并
    all_trends = manual_insights + newsnow_trends
    
    # 4. 打印
    print(f"\n📊 Manual Insights:")
    for i, t in enumerate(manual_insights, 1):
        print(f"   {i}. {t}")
    
    print(f"\n📰 NewsNow Trends ({len(newsnow_trends)} items):")
    for i, t in enumerate(newsnow_trends[:5], 1):
        print(f"   {i}. {t[:60]}...")
    
    # 5. 保存
    data = {
        "timestamp": datetime.now().isoformat(),
        "sources": ["manual", "newsnow"],
        "insights": manual_insights,
        "newsnow": newsnow_trends[:20],
        "all_trends": all_trends[:25]
    }
    with open(TRENDS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved to {TRENDS_FILE}")
    return data

if __name__ == "__main__":
    main()
