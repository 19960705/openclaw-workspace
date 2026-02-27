#!/usr/bin/env python3
"""
每日对话自动分析器
1. 读取当天对话记录
2. 提取关键主题和待办
3. 归类到 Obsidian 项目
4. 生成任务完成报告
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/Users/mac/.openclaw/workspace")
OBSIDIAN = Path("/Users/mac/Documents/Obsidian Vault/Keonho")
MEMORY_DIR = WORKSPACE / "memory"
SESSION_DIR = MEMORY_DIR / "session-transcripts"
TODOS_FILE = MEMORY_DIR / "todos.md"

def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

def find_today_transcripts():
    """找到今天的对话记录"""
    today = get_today_date()
    transcripts = []
    
    if SESSION_DIR.exists():
        for f in SESSION_DIR.glob(f"{today}*.md"):
            transcripts.append(f)
    
    # 也检查 memory 文件
    today_memory = MEMORY_DIR / f"{today}.md"
    if today_memory.exists():
        transcripts.append(today_memory)
    
    return transcripts

def read_conversations():
    """读取今天所有对话"""
    transcripts = find_today_transcripts()
    content = []
    
    for f in transcripts:
        try:
            with open(f, 'r') as fp:
                content.append(fp.read())
        except:
            pass
    
    return "\n\n".join(content)

def extract_topics(content):
    """提取关键主题"""
    topics = []
    
    # 提取任务关键词
    task_patterns = [
        r'创建.*skill',
        r'安装.*skill',
        r'研究.*',
        r'写.*脚本',
        r'修复.*问题',
        r'检查.*状态',
    ]
    
    for pattern in task_patterns:
        matches = re.findall(pattern, content)
        topics.extend(matches)
    
    return list(set(topics))[:10]

def extract_todos():
    """提取待办事项"""
    todos = []
    
    if TODOS_FILE.exists():
        with open(TODOS_FILE, 'r') as f:
            content = f.read()
            
            # 提取未完成的待办
            in_pending = False
            for line in content.split('\n'):
                if '待办 (Pending)' in line:
                    in_pending = True
                elif '进行中' in line or '已完成' in line:
                    in_pending = False
                elif in_pending and line.strip().startswith('-'):
                    todos.append(line.strip())
    
    return todos[:5]

def create_project_note(topic, content):
    """在 Obsidian 创建项目笔记"""
    # 清理主题名
    safe_name = re.sub(r'[^\w\s-]', '', topic)[:50]
    safe_name = safe_name.strip().replace(' ', '-')
    
    if not safe_name:
        return None
    
    project_file = OBSIDIAN / f"项目-{safe_name}.md"
    
    if not project_file.exists():
        with open(project_file, 'w') as f:
            f.write(f"""# {topic}

## 创建时间
{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 来源
日常对话自动提取

## 内容
{content[:500]}

## 状态
- [ ] 进行中

## 相关任务

## 笔记

---
*自动生成*
""")
        return project_file.name
    
    return None

def generate_daily_report():
    """生成每日报告"""
    content = read_conversations()
    topics = extract_topics(content)
    todos = extract_todos()
    
    report = f"""# 每日工作汇报 - {get_today_date()}

## 今日主题
{chr(10).join(f"- {t}" for t in topics) if topics else "- 无提取到主题"}

## 待办事项
{chr(10).join(f"- {t}" for t in todos) if todos else "- 无待办"}

## 对话记录
字数: {len(content)} 字符

---
*由自动工作流生成 - {datetime.now().strftime('%H:%M:%S')}*
"""
    
    return report

if __name__ == "__main__":
    print("📋 每日对话自动分析器")
    print("=" * 40)
    
    # 1. 读取对话
    print("\n1. 读取今日对话...")
    content = read_conversations()
    print(f"   读取 {len(content)} 字符")
    
    # 2. 提取主题
    print("\n2. 提取关键主题...")
    topics = extract_topics(content)
    for t in topics[:5]:
        print(f"   - {t}")
    
    # 3. 提取待办
    print("\n3. 提取待办事项...")
    todos = extract_todos()
    for t in todos[:3]:
        print(f"   - {t}")
    
    # 4. 生成报告
    print("\n4. 生成每日报告...")
    report = generate_daily_report()
    report_file = OBSIDIAN / "自由时间报告" / f"自动汇报-{get_today_date()}.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"   已保存到: {report_file.name}")
    print("\n✅ 完成!")
