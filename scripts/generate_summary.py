
#!/usr/bin/env python3
"""
自动对话摘要生成脚本
读取当天的对话记录，生成摘要并保存
节省 token：不用保留完整对话历史
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加 workspace 到路径
WORKSPACE = Path("/Users/mac/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"

def get_today_date():
    """获取今天的日期字符串"""
    return datetime.now().strftime("%Y-%m-%d")

def get_yesterday_date():
    """获取昨天的日期字符串"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def read_daily_file(date_str):
    """读取某天的对话文件"""
    file_path = MEMORY_DIR / (date_str + ".md")
    if not file_path.exists():
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_summary(content, date_str):
    """
    生成对话摘要
    实际使用时可以调用 LLM 来生成更智能的摘要
    """
    # 这里是简化版，实际可以集成 LLM
    summary_lines = []
    summary_lines.append("# " + date_str + " 对话摘要")
    summary_lines.append("")
    summary_lines.append("## 要点")
    summary_lines.append("")
    
    # 简单提取关键词
    lines = content.split("\n")
    keywords = set()
    
    for line in lines:
        if "技能" in line or "skill" in line.lower():
            keywords.add("技能创建/优化")
        if "记忆" in line or "memory" in line.lower():
            keywords.add("记忆系统优化")
        if "token" in line.lower():
            keywords.add("Token 节省")
        if "cron" in line.lower():
            keywords.add("Cron 任务")
        if "browser" in line.lower():
            keywords.add("浏览器自动化")
        if "simmer" in line.lower():
            keywords.add("Simmer 交易")
        if "foundry" in line.lower():
            keywords.add("Foundry 学习")
    
    if keywords:
        for keyword in sorted(keywords):
            summary_lines.append("- " + keyword)
    else:
        summary_lines.append("- 常规对话")
    
    summary_lines.append("")
    summary_lines.append("## 详情")
    summary_lines.append("")
    summary_lines.append("详细内容请查看完整对话文件。")
    
    return "\n".join(summary_lines)

def save_summary(summary, date_str):
    """保存摘要文件"""
    summary_path = MEMORY_DIR / (date_str + "-summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print("✅ 摘要已保存: " + str(summary_path))
    return summary_path

def main():
    """主函数"""
    # 默认处理今天
    target_date = get_today_date()
    
    # 如果有参数，处理指定日期
    if len(sys.argv) &gt; 1:
        target_date = sys.argv[1]
    
    print("📅 处理日期: " + target_date)
    
    # 读取对话文件
    content = read_daily_file(target_date)
    if not content:
        print("⚠️ 未找到对话文件: " + target_date + ".md")
        return 1
    
    print("✅ 读取到对话内容: " + str(len(content)) + " 字符")
    
    # 生成摘要
    summary = generate_summary(content, target_date)
    
    # 保存摘要
    save_summary(summary, target_date)
    
    print("")
    print("🎉 摘要生成完成！")
    print("💡 提示：实际使用时可以集成 LLM 生成更智能的摘要")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

