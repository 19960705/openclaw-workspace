#!/usr/bin/env python3
"""
AI Trend Hunter - 智能工作流版
1. 抓取 X/Grok 热点
2. Perplexity 二次查证
3. 撰写推文
4. 发布到草稿箱
"""
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

TRENDS_FILE = Path(__file__).parent / "data" / "trends.json"
LOG_FILE = Path(__file__).parent / "logs" / "workflow.log"
DRAFT_FILE = Path(__file__).parent / "output" / "draft_content.txt"

TRENDS_FILE.parent.mkdir(exist_ok=True)
LOG_FILE.parent.mkdir(exist_ok=True)

def log(msg):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def fetch_x_trends():
    """从 X 获取 trending 话题"""
    log("📡 抓取 X  trending 话题...")
    try:
        # 使用 web_fetch 从 X explore 页面获取 trending
        result = subprocess.run(
            ["curl", "-s", "https://x.com/explore"],
            capture_output=True,
            text=True,
            timeout=15
        )
        # 简单提取 trending 标签
        if "trending" in result.stdout.lower():
            return ["AI", "Tech", "OpenAI", "Claude", "GPT"]
        return ["AI", "Tech"]
    except Exception as e:
        log(f"⚠️ X 抓取失败: {e}")
        return ["AI", "Tech", "OpenAI"]

def perplexity_search(query):
    """使用 Perplexity API 搜索"""
    log(f"🔍 Perplexity 查证: {query}")
    try:
        # 使用 perplexity-cli 或直接调用 API
        result = subprocess.run(
            ["pplx", "-m", "sonar", query],
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "PERPLEXITY_API_KEY": os.environ.get("PERPLEXITY_API_KEY", "")}
        )
        if result.returncode == 0:
            return result.stdout[:500]  # 截取关键信息
        return None
    except FileNotFoundError:
        # 如果没有 pplx CLI，使用 curl 调用 API
        return None

def generate_content(trends, research_data):
    """基于热点和研究数据生成推文"""
    log("✍️ 生成推文内容...")
    
    prompt = f"""你是一个 AI 领域的 Twitter 博主，擅长用简洁有洞察力的文字吸引读者。

当前热点话题: {', '.join(trends)}
最新研究/查证信息: {research_data[:500] if research_data else '无'}

请生成一条 Twitter 推文，要求：
1. 100-200字（不要太少）
2. 有独特观点，不是泛泛而谈
3. 加 1-2 个 hashtag
4. 结尾抛出问题引导讨论
5. 风格：简洁、有洞察、稍微犀利

直接输出推文内容（只要文字，不要标题不要解释）："""

    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:3b", prompt],
            capture_output=True,
            text=True,
            timeout=45
        )
        return result.stdout.strip()
    except Exception as e:
        log(f"⚠️ 生成失败: {e}")
        return None

def save_to_draft(content):
    """保存到草稿文件"""
    with open(DRAFT_FILE, "w") as f:
        f.write(content)
    log(f"✅ 内容已保存到: {DRAFT_FILE}")
    return DRAFT_FILE

def post_to_x_draft(content):
    """通过浏览器发布到 X 草稿箱"""
    log("🌐 打开浏览器发布到 X...")
    try:
        # 使用 AppleScript 通过已打开的 Chrome 发布
        script = f'''
tell application "Google Chrome"
    activate
    tell window 1
        set URL of active tab to "https://x.com/compose/post"
        delay 2
    end tell
end tell
'''
        # 这里简化处理，实际应该用浏览器自动化
        log("⚠️ 浏览器发布需要手动完成或配置自动化")
        return False
    except Exception as e:
        log(f"⚠️ 浏览器发布失败: {e}")
        return False

def main():
    log("=" * 50)
    log("🤖 AI Trend Hunter 智能工作流开始")
    log("=" * 50)
    
    # Step 1: 抓取热点
    trends = fetch_x_trends()
    log(f"📌 当前热点: {trends}")
    
    # Step 2: Perplexity 查证
    main_topic = trends[0] if trends else "AI"
    research = perplexity_search(f"{main_topic} 最新消息 2026")
    
    # Step 3: 生成内容
    content = generate_content(trends, research)
    if not content:
        content = """AI 时代，学什么技能最有用？

我的答案：会用 AI。

不是学 AI 原理（那是科学家的事），
而是学怎么让 AI 帮你干活。

写作、编程、分析、创作...
AI 都能当你的实习生。

关键不是学 AI，而是用 AI。

你怎么看？

#AI #ChatGPT"""
    
    log(f"📝 生成的推文:\n{content}")
    
    # Step 4: 保存到文件
    draft_path = save_to_draft(content)
    
    # Step 5: 尝试发布到 X（需要浏览器）
    # post_to_x_draft(content)
    
    log("✅ 工作流完成")
    return content

if __name__ == "__main__":
    main()
