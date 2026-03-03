#!/usr/bin/env python3
"""
OpenClaw HeartBeat with Local AI
使用 Ollama 本地模型判断是否需要人工介入
"""
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

# 配置
OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_PATH = "/opt/homebrew/bin/ollama"
TASKS_FILE = Path("/Users/mac/.openclaw/workspace/tasks/tasks.json")
LOG_FILE = Path("/Users/mac/.openclaw/logs/heartbeat.log")

def call_local_model(prompt: str, timeout: int = 30) -> str:
    """调用本地模型"""
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_task_summary() -> str:
    """获取任务摘要"""
    if not TASKS_FILE.exists():
        return "无任务文件"
    
    with open(TASKS_FILE) as f:
        data = json.load(f)
    
    tasks = data.get("tasks", [])
    
    summary_lines = []
    enabled_count = 0
    completed_count = 0
    
    for task in tasks:
        if task.get("enabled"):
            enabled_count += 1
            status = task.get("status", "unknown")
            name = task.get("name", "Unknown")
            last_run = task.get("lastRun", "从未运行")
            
            if status == "completed":
                completed_count += 1
                summary_lines.append(f"✅ {name}: 完成 ({last_run})")
            else:
                summary_lines.append(f"⚠️ {name}: {status} ({last_run})")
    
    summary = f"任务: {completed_count}/{enabled_count} 完成\n"
    summary += "\n".join(summary_lines)
    
    return summary

def analyze_with_local_ai(task_summary: str) -> str:
    """用本地 AI 分析任务状态"""
    
    prompt = f"""你是AI助手，负责判断以下任务状态是否正常。

任务状态：
{task_summary}

请判断：
1. 如果所有任务正常 → 只回复 "OK"
2. 如果有问题需要人工处理 → 简要说明需要做什么

只回复简短结果，不要多余解释。"""

    print(f"🤖 调用本地模型: {OLLAMA_MODEL}...")
    response = call_local_model(prompt, timeout=45)
    return response

def log(message: str):
    """记录日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

def send_telegram(message: str, chat_id: str = "8391832262"):
    """发送 Telegram 消息"""
    import urllib.request
    import urllib.parse
    
    bot_token = "8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        log(f"Telegram发送失败: {e}")
        return False

def main():
    print("=" * 40)
    print("🔔 OpenClaw HeartBeat (Local AI Mode)")
    print("=" * 40)
    
    # 1. 获取任务摘要
    print("\n📋 获取任务状态...")
    task_summary = get_task_summary()
    print(task_summary)
    
    # 2. 调用本地 AI 分析
    print("\n🤖 AI 分析中...")
    result = analyze_with_local_ai(task_summary)
    
    print(f"\n📝 AI 判断:")
    print(result)
    
    # 3. 记录日志
    log(f"AI判断: {result}")
    
    # 4. 返回结果
    if "OK" in result.upper():
        print("\n✅ 一切正常")
        sys.exit(0)
    else:
        print("\n⚠️ 需要人工介入")
        print(result)
        
        # 发送 Telegram 通知
        alert_msg = f"🔔 OpenClaw HeartBeat 警报\n\n{task_summary}\n\n🤖 AI 判断:\n{result}"
        if send_telegram(alert_msg):
            print("\n📱 已推送 Telegram 通知")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
