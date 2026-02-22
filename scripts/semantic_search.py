#!/usr/bin/env python3
"""
Semantic Memory Search - 基于向量的语义搜索
用于快速从历史记录中找到相关内容，减少 token 消耗

使用方式：
  python3 scripts/semantic_search.py "我想找之前关于EvoMap的讨论"
"""

import os
import sys
import json
from pathlib import Path

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")

def get_recent_memories(days=7):
    """获取最近N天的记忆文件"""
    from datetime import datetime, timedelta
    
    memories = []
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        
        # Check for daily memory
        daily_file = os.path.join(MEMORY_DIR, f"{date_str}.md")
        if os.path.exists(daily_file):
            with open(daily_file, 'r', encoding='utf-8') as f:
                memories.append({
                    'file': f"{date_str}.md",
                    'content': f.read()
                })
        
        # Check for summary files
        summary_file = os.path.join(MEMORY_DIR, f"{date_str}-summary.md")
        if os.path.exists(summary_file):
            with open(summary_file, 'r', encoding='utf-8') as f:
                memories.append({
                    'file': f"{date_str}-summary.md",
                    'content': f.read()
                })
    
    return memories


def simple_search(query, memories, top_k=3):
    """
    简单的关键词搜索
    找到包含查询关键词的记忆
    """
    query_lower = query.lower()
    results = []
    
    for memory in memories:
        content = memory['content']
        # Simple keyword matching
        query_words = query_lower.split()
        matches = sum(1 for word in query_words if word in content.lower())
        
        if matches > 0:
            # Find context around matches
            lines = content.split('\n')
            matched_lines = []
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in query_words):
                    matched_lines.append(line.strip())
            
            if matched_lines:
                results.append({
                    'file': memory['file'],
                    'score': matches,
                    'context': '\n'.join(matched_lines[:5])
                })
    
    # Sort by score and return top k
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]


def format_results(results):
    """格式化搜索结果"""
    if not results:
        return "没有找到相关记忆"
    
    output = ["## 找到的相关记忆\n"]
    for r in results:
        output.append(f"### 📄 {r['file']} (匹配度: {r['score']})")
        output.append(f"```\n{r['context'][:500]}...\n```")
        output.append("")
    
    return '\n'.join(output)


if __name__ == "__main__":
    # Get query from command line or use default
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = "EvoMap"
    
    print(f"🔍 搜索: {query}\n")
    
    # Get recent memories
    memories = get_recent_memories(days=7)
    print(f"📚 已加载 {len(memories)} 个记忆文件\n")
    
    # Search
    results = simple_search(query, memories)
    
    # Output
    print(format_results(results))
