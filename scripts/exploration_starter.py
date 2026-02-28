#!/usr/bin/env python3
"""
探索冒险模式 - 详细日志版
"""
import os
from datetime import datetime

LOG_DIR = "/Users/mac/OpenClaw_Adventure_Log"
OBSIDIAN_DIR = "/Users/mac/Documents/Obsidian Vault/Keonho"

def get_template():
    return f"""# 探索冒险日志 - {datetime.now().strftime('%Y-%m-%d')}

## 🎯 探险主题

**提案编号**: [待确认]
**探险类型**: [知识/实用/创意/实验]
**启动时间**: {datetime.now().strftime('%H:%M')}

---

### 1. 探索目标

**为什么要做：**
> [填写原因]

**预期结果：**
> [填写预期]

**对老板的价值：**
> [填写价值]

---

### 2. 执行过程

| 时间 | 操作 | 结果 | 学到 |
|------|------|------|------|
| | | | |

---

### 3. 产出物

**文件/链接**:
- 

**内容摘要**:


---

### 4. 反思 (15分钟)

**做得好的：**
- 

**可以改进的：**
- 

**下次更好的方法：**
- 

---

### 5. 明日计划

**待完成任务：**
- 

**新探险方向：**
- 

---

### 6. 给老板的惊喜建议

1. 
2. 
3. 

---

### 7. 探险家内心独白

> [用第一人称写 200 字探险感受]

---

**探险点数**: +0  
**当前等级**: Lv.1  
**称号**: 见习探险家
"""

def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = f"{LOG_DIR}/{today}.md"
    obsidian_file = f"{OBSIDIAN_DIR}/探索冒险_{today}.md"
    
    # 如果文件不存在，创建
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write(get_template())
        print(f"✅ Created: {log_file}")
    
    if not os.path.exists(obsidian_file):
        with open(obsidian_file, 'w') as f:
            f.write(get_template())
        print(f"✅ Created: {obsidian_file}")
    
    print(f"\n📝 探险日志已准备好")
    print(f"📁 {log_file}")
    print(f"📁 {obsidian_file}")

if __name__ == "__main__":
    main()
