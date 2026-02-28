#!/usr/bin/env python3
"""
AI Trend Hunter - 健壮版
增加错误处理和重试机制
"""
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

TRENDS_FILE = Path(__file__).parent / "data" / "trends.json"
LOG_FILE = Path(__file__).parent / "logs" / "workflow.log"
TRENDS_FILE.parent.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

NEWSNOW_SOURCES = [
    "hackernews",
    "github-trending-today", 
    "producthunt",
    "36kr",
    "sspai",
    "juejin",
]

MANUAL_INSIGHTS = [
    "🤖 AI 员工概念 - 从写推文的人变成审推文的人",
    "⚡ 审批流程 - AI 生成 → Telegram 推送 → 回复 ok → 自动发",
    "📊 多源情报 - AI/独立开发者/竞品/社区/行业 5 方向",
    "⏰ 定时发布 - 3 个时间节点 (10:30/15:30/20:30)",
    "🎯 核心原则 - 没审批的绝不发，AI 干活人把关",
]

CONTENT_TEMPLATES = [
    # 模板1: 实验风格
    """试了一下 AI 自动发推，聊聊结果。

🤖 用了什么：
   - AI 写手自动搜热点
   - 每天生成 3 条草稿
   - 我审批后自动发

📊 效果：
   - 每天投入：2 分钟
   - 之前：1 小时手动
   - 效率提升：30x

💡 心得：
   - AI 解决的是'写什么'，不是'什么时候发'
   - 审批流程必须有，AI 也会翻车
   - 关键是让人做决策，AI 干活

你们有用 AI 运营社交媒体吗？效果怎么样？

#AI #Automation #Twitter""",

    # 模板2: 数据驱动
    """OpenAI 估值 $730B。

但我有点担心。

钱太多 = 压力太大 = 必须找到 killer app。
投资人不是做慈善的。

上次这么大压力，还是移动互联网刚起来的时候。
真正爆发是微信、Uber、抖音出现之后。

对普通人来说：
在 killer app 出现之前，先学会用 AI。

你怎么看？

#AI #OpenAI #Tech""",

    # 模板3: 提问风格
    """AI 时代，学什么技能最有用？

我的答案：会用 AI。

不是学 AI 原理（那是科学家的事），
是学会指挥 AI 干活。

就像 2012 年，
不是每个人都去学编程，
但会用电脑的人赢了。

2026，
不是每个人都要调模型，
但会用 AI 的人会赢。

你同意吗？

#AI #技能 #2026""",

    # 模板4: 短暴风格
    """OpenAI 估值 $730B。

一面是资本狂欢，
一面是监管大棒。

2026 了，AI 正式进入「被监管」时代。

#AI #Tech""",
]

def log(msg):
    """日志记录"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def get_newsnow_trends(max_retries=3):
    """获取趋势 - 带重试"""
    for attempt in range(max_retries):
        try:
            trends = []
            for source in NEWSNOW_SOURCES:
                result = subprocess.run(
                    ["/Users/mac/bin/newsnow", source, "--json"],
                    capture_output=True,
                    text=True,
                    timeout=20
                )
                if result.returncode == 0 and result.stdout:
                    try:
                        data = json.loads(result.stdout)
                        if isinstance(data, list):
                            for item in data[:3]:
                                title = item.get('title', '')
                                if title and len(title) > 5:
                                    trends.append(f"[{source}] {title[:80]}")
                    except json.JSONDecodeError:
                        pass
            log(f"获取趋势成功: {len(trends)} 条")
            return trends
        except Exception as e:
            log(f"获取趋势失败 (尝试 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5)  # 等待后重试
    return []

def generate_content():
    """生成内容"""
    import random
    content = random.choice(CONTENT_TEMPLATES)
    log(f"生成内容: {content[:50]}...")
    return content

def save_to_file(content):
    """保存到文件"""
    content_file = Path(__file__).parent / "output" / "draft_content.txt"
    content_file.parent.mkdir(exist_ok=True)
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(content)
    log(f"内容已保存: {content_file}")

def main():
    log("=" * 50)
    log("🤖 AI Trend Hunter 开始")
    log("=" * 50)
    
    # 1. 获取趋势
    trends = get_newsnow_trends()
    if not trends:
        log("警告: 未能获取趋势，使用默认 insights")
        trends = MANUAL_INSIGHTS
    
    # 保存趋势数据
    data = {
        "timestamp": datetime.now().isoformat(),
        "insights": MANUAL_INSIGHTS,
        "newsnow": trends[:20],
    }
    with open(TRENDS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # 2. 生成内容
    content = generate_content()
    
    # 3. 保存
    save_to_file(content)
    
    log("✅ 工作流完成")
    return 0

if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except Exception as e:
        log(f"❌ 错误: {e}")
        sys.exit(1)
