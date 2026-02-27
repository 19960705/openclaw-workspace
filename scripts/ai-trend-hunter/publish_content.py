#!/usr/bin/env python3
"""
AI Trend Hunter - 优化版文案生成
学习 X 爆火帖特点
"""
import json
from datetime import datetime
from pathlib import Path

TRENDS_FILE = Path(__file__).parent / "data" / "trends.json"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_trends():
    with open(TRENDS_FILE, 'r') as f:
        return json.load(f)

def format_for_x(trends_data):
    """X 文案 - 短小精悍+个人观察+互动"""
    # 随机选一个角度切入
    lines = [
        "最近观察到一个趋势:",
        "",
        "AI 不只是聊天了。",
        "",
        "多个 Agent 配合干活已成现实。",
        "客服场景: 一个分类问题，一个查数据库，一个写回复。",
        "",
        "事件驱动的也在起来。",
        "服务器异常? AI 自动报警+修复。",
        "",
        "我的感觉: AI 是超级助手，不是取代人类。",
        "",
        "你怎么看?",
        "",
        "#AI #Agent"
    ]
    return '\n'.join(lines)

def format_for_xiaohongshu(trends_data):
    """小红书 - 更接地气+个人经历"""
    lines = [
        "最近 AI 圈的变化:",
        "",
        "1️⃣ 多 Agent 协作",
        "不只是聊天! 多个 AI 配合干活",
        "例子: 客服，一个分类，一个查资料，一个回复",
        "",
        "2️⃣ 事件驱动",
        "从你问我答 → 自动触发",
        "例子: 服务器异常时 AI 自动处理",
        "",
        "3️⃣ AI 视频爆发",
        "即梦 Seedance vs 可灵 vs Veo 3",
        "",
        "4️⃣ AI Coding",
        "GPT 写代码强，Claude 解释更好",
        "",
        "💡 感觉: AI 更像超级助手",
        "你怎么看? 评论区聊聊",
        "",
        "#AI #人工智能 #2026 #科技"
    ]
    return '\n'.join(lines)

def save_outputs(x_content, xhs_content):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    x_file = OUTPUT_DIR / f"x_{timestamp}.txt"
    xhs_file = OUTPUT_DIR / f"xiaohongshu_{timestamp}.txt"
    with open(x_file, 'w', encoding='utf-8') as f:
        f.write(x_content)
    with open(xhs_file, 'w', encoding='utf-8') as f:
        f.write(xhs_content)
    return str(x_file), str(xhs_file)

def main():
    print("AI Trend Hunter - Optimized Content")
    print("=" * 40)
    data = load_trends()
    x_content = format_for_x(data)
    xhs_content = format_for_xiaohongshu(data)
    x_file, xhs_file = save_outputs(x_content, xhs_content)
    print(f"\n📝 X (English):")
    print(x_content)
    print(f"\n📝 小红书 (中文):")
    print(xhs_content)
    print(f"\n✅ Saved: {x_file}, {xhs_file}")

if __name__ == "__main__":
    main()
