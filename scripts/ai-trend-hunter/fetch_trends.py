#!/usr/bin/env python3
"""
AI Trend Hunter - 超级增强版 v10
整合 sitinme 的 AI 运营 Twitter 经验
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

# 手动 insights - 来自 sitinme 文章的深度总结
MANUAL_INSIGHTS = [
    "🤖 AI 员工概念 - 从写推文的人变成审推文的人",
    "⚡ 审批流程 - AI 生成 → Telegram 推送 → 回复 ok → 自动发",
    "📊 多源情报 - AI/独立开发者/竞品/社区/行业 5 方向",
    "⏰ 定时发布 - 3 个时间节点 (10:30/15:30/20:30)",
    "🎯 核心原则 - 没审批的绝不发，AI 干活人把关",
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
                        for item in data[:3]:
                            title = item.get('title', '')
                            if title and len(title) > 5:
                                trends.append(f"[{source}] {title[:80]}")
                except:
                    pass
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    return trends

def get_sitinme_case():
    """sitinme 的 AI 运营 Twitter 案例"""
    return {
        "author": "@sitinme",
        "title": "我让 AI 员工接管了 Twitter 运营，每天只花 2 分钟",
        "metrics": {
            "daily_time": "2 分钟",
            "posts_per_day": "3 条",
            "views": "1.2 万",
            "likes": "56",
            "bookmarks": "147",
            "cost": "$0"
        },
        "architecture": {
            "roles": ["AI 写手 (8:00)", "我 (审批)", "发布机器人 (定时)"],
            "workflow": "搜情报 → 写草稿 → 推 Telegram → 审批 ok → 自动发"
        },
        "lessons": [
            "OAuth + 代理 = 签名失败 → 用 Python",
            "Cookie + GraphQL 静默失败 → 只适合读数据",
            "JavaScript 精度丢失 → 用 _string 版本",
            "图片上传三步走 → INIT → APPEND → FINALIZE",
            "Node.js multipart + 代理 hang → 换 Python"
        ],
        "insight": "AI 解决上游问题（写什么），不是下游（定时发）"
    }

def main():
    print(f"\n{'='*50}")
    print(f"🤖 AI Trend Hunter v10 - 超级增强版")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # 1. 从 newsnow 获取
    print("📡 Fetching from newsnow...")
    newsnow_trends = get_newsnow_trends()
    print(f"   Got {len(newsnow_trends)} items")
    
    # 2. sitinme 案例
    sitinme_case = get_sitinme_case()
    
    # 3. 手动 insights
    manual_insights = MANUAL_INSIGHTS
    
    # 4. 合并
    all_trends = manual_insights + newsnow_trends
    
    # 5. 打印
    print(f"\n📊 深度 Insights (来自 @sitinme):")
    for i, insight in enumerate(manual_insights, 1):
        print(f"   {i}. {insight}")
    
    print(f"\n📰 NewsNow Trends ({len(newsnow_trends)} items):")
    for i, t in enumerate(newsnow_trends[:5], 1):
        print(f"   {i}. {t[:60]}...")
    
    print(f"\n📈 Case Study:")
    print(f"   作者: {sitinme_case['author']}")
    print(f"   投入: {sitinme_case['metrics']['daily_time']} → {sitinme_case['metrics']['posts_per_day']}")
    print(f"   效果: {sitinme_case['metrics']['views']} 观看")
    
    # 6. 保存
    data = {
        "timestamp": datetime.now().isoformat(),
        "version": "v10",
        "sources": ["manual", "newsnow", "sitinme_case"],
        "insights": manual_insights,
        "newsnow": newsnow_trends[:20],
        "sitinme_case": sitinme_case,
        "all_trends": all_trends[:25]
    }
    with open(TRENDS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved to {TRENDS_FILE}")
    return data

if __name__ == "__main__":
    main()
