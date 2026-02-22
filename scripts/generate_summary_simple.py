
#!/usr/bin/env python3
"""
简单的对话摘要生成脚本
"""

import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/mac/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"

def main():
    # 今天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 检查参数
    if len(sys.argv) &gt; 1:
        target_date = sys.argv[1]
    else:
        target_date = today
    
    print("处理日期:", target_date)
    
    # 读取文件
    input_file = MEMORY_DIR / (target_date + ".md")
    if not input_file.exists():
        print("文件不存在:", input_file)
        return 1
    
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 简单摘要
    summary = "# " + target_date + " 对话摘要\n\n"
    summary += "## 要点\n\n"
    summary += "- 详见完整对话文件\n\n"
    summary += "## 详情\n\n"
    summary += "文件大小: " + str(len(content)) + " 字符\n"
    
    # 保存摘要
    output_file = MEMORY_DIR / (target_date + "-summary.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("摘要已保存:", output_file)
    return 0

if __name__ == "__main__":
    sys.exit(main())

