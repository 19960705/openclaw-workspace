#!/usr/bin/env python3
"""
探索冒险模式 - 提前提案系统
在前一天 23:00 生成明日提案
"""
import os
from datetime import datetime, timedelta

LOG_DIR = "/Users/mac/Openclaw_Adventure_Log"
OBSIDIAN_DIR = "/Users/mac/Documents/Obsidian Vault/Keonho"
MAP_FILE = "/Users/mac/OpenClaw_Exploration_Map.md"

def get_proposals():
    """生成明日提案"""
    proposals = [
        {
            "id": "A",
            "type": "知识探险",
            "title": "深入研究 AI 视频生成工具",
            "detail": "对比 Seedance 2.0 vs Kling 2.6 vs Veo 3，产出对比表",
            "value": "为 TikTok 选品提供技术参考"
        },
        {
            "id": "B", 
            "type": "实用探险",
            "title": "优化 Lazada 爬虫方案",
            "detail": "解决 Selenium 被杀问题，找替代方案（API/代理）",
            "value": "稳定获取泰国电商数据"
        },
        {
            "id": "C",
            "type": "创意探险",
            "title": "生成 TikTok 短视频脚本",
            "detail": "用现有咖啡产品数据，生成 3 个泰语广告脚本",
            "value": "快速产出内容素材"
        }
    ]
    return proposals

def read_map():
    """读取探索地图"""
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE) as f:
            return f.read()
    return None

def main():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 50)
    print("🌙 探索冒险模式 - 明日提案")
    print(f"今日: {today}")
    print(f"明日: {tomorrow}")
    print("=" * 50)
    
    # 读取本周主线
    map_content = read_map()
    if map_content:
        print("\n📍 本周主线:")
        print(map_content[:300])
    
    # 生成提案
    proposals = get_proposals()
    
    print(f"\n🎯 明日探险提案 ({tomorrow}):\n")
    
    for p in proposals:
        print(f"{p['id']}. [{p['type']}] {p['title']}")
        print(f"   详情: {p['detail']}")
        print(f"   价值: {p['value']}")
        print()
    
    print("-" * 50)
    print("请回复: Yes + A/B/C (或 Yes 让我选)")
    print("-" * 50)
    
    # 保存提案到文件
    proposal_file = f"{LOG_DIR}/proposals_{tomorrow}.md"
    with open(proposal_file, 'w') as f:
        f.write(f"# 明日探险提案 - {tomorrow}\n\n")
        for p in proposals:
            f.write(f"## {p['id']}. [{p['type']}] {p['title']}\n")
            f.write(f"- 详情: {p['detail']}\n")
            f.write(f"- 价值: {p['value']}\n\n")
    
    print(f"\n✅ 提案已保存: {proposal_file}")

if __name__ == "__main__":
    main()
