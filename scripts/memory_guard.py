#!/usr/bin/env python3
"""
Memory Guardian - 记忆守护
自动压缩和限制 MEMORY.md 行数
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# 配置
MEMORY_FILE = Path("/Users/mac/.openclaw/workspace/MEMORY.md")
CEILING = 120  # 行数上限

def count_lines(file_path):
    """统计行数"""
    if file_path.exists():
        with open(file_path) as f:
            return len(f.readlines())
    return 0

def check():
    """检查内存文件状态"""
    lines = count_lines(MEMORY_FILE)
    
    print(f"📊 MEMORY.md 状态")
    print(f"当前行数: {lines}/{CEILING}")
    
    if lines > CEILING:
        print(f"⚠️ 超过上限 {CEILING} 行！需要压缩")
        return False
    elif lines > CEILING * 0.8:
        print(f"⚡ 超过 80% 上限，建议压缩")
        return True
    else:
        print(f"✅ 状态正常")
        return True

def compress():
    """压缩内存文件 - 保留关键信息"""
    if not MEMORY_FILE.exists():
        print("❌ 文件不存在")
        return
    
    with open(MEMORY_FILE) as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # 保留区域（不会被压缩）
    protected_sections = ["## User", "## Me", "## Projects", "## Key Facts"]
    
    protected_lines = []
    content_lines = []
    is_protected = False
    
    for line in lines:
        # 检查是否在保护区域
        for section in protected_sections:
            if section in line:
                is_protected = True
                break
        
        if is_protected:
            protected_lines.append(line)
        else:
            # 检查是否是空行或分隔线
            if line.strip() in ['', '---', '***']:
                continue
            content_lines.append(line)
    
    # 重新构建
    new_lines = protected_lines + ['', '---', ''] + content_lines[-50:]  # 保留最后50条
    
    # 备份
    backup = MEMORY_FILE.with_suffix('.md.bak')
    MEMORY_FILE.rename(backup)
    
    with open(MEMORY_FILE, 'w') as f:
        f.write('\n'.join(new_lines))
    
    new_count = count_lines(MEMORY_FILE)
    print(f"✅ 压缩完成")
    print(f"  备份: {backup.name}")
    print(f"  新行数: {new_count}")
    return True

def enforce():
    """强制执行上限"""
    if count_lines(MEMORY_FILE) > CEILING:
        print(f"❌ 拒绝: 超过 {CEILING} 行限制")
        return False
    return True

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    
    if action == "check":
        check()
    elif action == "compress":
        compress()
    elif action == "enforce":
        enforce()
    else:
        print("用法: memory_guard.py [check|compress|enforce]")

if __name__ == "__main__":
    main()
