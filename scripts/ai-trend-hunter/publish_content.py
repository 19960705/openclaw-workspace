#!/usr/bin/env python3
"""
AI Trend Hunter - X 风格优化版 v11
基于 X 热门 AI 推文风格
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

def format_x_data_driven(trends_data):
    """数据驱动风格 - 参考热门推文"""
    lines = [
        "OpenAI 估值 $730B。",
        "",
        "我的第一反应：钱越多，压力越大。",
        "",
        "投资人要回报。",
        "$730B 意味着必须找到 killer app。",
        "",
        "上次这么大压力，",
        "还是移动互联网刚起来的时候。",
        "",
        "2012-2014，移动互联网融资也疯狂。",
        "真正爆发是微信、Uber、抖音出现之后。",
        "",
        "---",
        "",
        "💡 所以普通人机会在哪？",
        "",
        "在 killer app 出现之前，先学会用 AI。",
        "",
        "就像 2012 年学编程，",
        "不一定当程序员，",
        "但第一批吃到了红利。",
        "",
        "会用 AI 的人，比不会的更有优势。",
        "",
        "你怎么看？融资变多会让 AI 发展更快还是更慢？",
        "",
        "#AI #OpenAI #Tech",
    ]
    return '\n'.join(lines)

def format_x_experiment_style(trends_data):
    """实验风格 - 参考 @aixuexi_ai"""
    lines = [
        "试了一下 AI 自动发推，聊聊结果。",
        "",
        "🤖 用了什么：",
        "   - AI 写手自动搜热点",
        "   - 每天生成 3 条草稿",
        "   - 我审批后自动发",
        "",
        "📊 效果：",
        "   - 每天投入：2 分钟",
        "   - 之前：1 小时手动",
        "   - 效率提升：30x",
        "",
        "💡 心得：",
        "   - AI 解决的是'写什么'，不是'什么时候发'",
        "   - 审批流程必须有，AI 也会翻车",
        "   - 关键是让人做决策，AI 干活",
        "",
        "你们有用 AI 运营社交媒体吗？效果怎么样？",
        "",
        "#AI #Automation #Twitter",
    ]
    return '\n'.join(lines)

def format_x_question_style(trends_data):
    """提问风格 - 引导互动"""
    lines = [
        "AI 时代，学什么技能最有用？",
        "",
        "我的答案：会用 AI。",
        "",
        "不是学 AI 原理（那是科学家的事），",
        "是学会指挥 AI 干活。",
        "",
        "---",
        "",
        "就像 2012 年，",
        "不是每个人都去学编程，",
        "但会用电脑的人赢了。",
        "",
        "2026，",
        "不是每个人都要调模型，",
        "但会用 AI 的人会赢。",
        "",
        "你同意吗？还是觉得我在制造焦虑？",
        "",
        "#AI #技能 #2026",
    ]
    return '\n'.join(lines)

def format_x_short_stylish(trends_data):
    """简短酷炫风格"""
    lines = [
        "OpenAI 估值 $730B。",
        "",
        "钱太多 = 压力太大。",
        "",
        "上次这样，还是移动互联网起来的时候。",
        "",
        "2012 年学编程的人，",
        "2016 年做 App 的人，",
        "",
        "2026，该学什么了？",
        "",
        "#AI",
    ]
    return '\n'.join(lines)

def save_outputs(*contents):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    files = []
    names = ['data_driven', 'experiment', 'question', 'short']
    for i, content in enumerate(contents):
        f = OUTPUT_DIR / f"x_{names[i]}_{timestamp}.txt"
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        files.append(str(f))
    return files

def main():
    print("AI Trend Hunter v11 - X 风格优化版")
    print("=" * 40)
    data = load_trends()
    
    c1 = format_x_data_driven(data)
    c2 = format_x_experiment_style(data)
    c3 = format_x_question_style(data)
    c4 = format_x_short_stylish(data)
    
    files = save_outputs(c1, c2, c3, c4)
    
    print(f"\n📝 数据驱动风格 ({len(c1)} 字):\n{c1}\n")
    print(f"📝 实验风格 ({len(c2)} 字):\n{c2}\n")
    print(f"📝 提问风格 ({len(c3)} 字):\n{c3}\n")
    print(f"📝 简短酷炫 ({len(c4)} 字):\n{c4}\n")
    print(f"✅ Saved to:\n" + "\n".join(files))

if __name__ == "__main__":
    main()
