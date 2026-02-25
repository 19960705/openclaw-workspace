
#!/usr/bin/env python3
import json
from datetime import datetime

# 读取原始文件
input_path = "/Users/mac/.openclaw/openclaw.json"
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 备份
backup_path = f"/Users/mac/.openclaw/workspace/configs/openclaw-backup-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
with open(backup_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已备份到: {backup_path}")

# 修改默认模型
if "agents" in data and "defaults" in data["agents"] and "model" in data["agents"]["defaults"]:
    # 把 minimax-portal/MiniMax-M2.5 放在 fallback 列表第一位
    fallbacks = data["agents"]["defaults"]["model"].get("fallbacks", [])
    target_model = "minimax-portal/MiniMax-M2.5"
    
    if target_model in fallbacks:
        fallbacks.remove(target_model)
    fallbacks.insert(0, target_model)
    
    data["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
    print(f"✅ 已将默认模型改为: {target_model}")
    print(f"   Fallback 列表: {fallbacks[:3]}...")

# 写回
with open(input_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已更新: {input_path}")
