
#!/usr/bin/env python3
import json
import sys
from datetime import datetime

# 读取原始文件
input_path = "/Users/mac/.openclaw/cron/jobs.json"
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 备份
backup_path = f"/Users/mac/.openclaw/workspace/configs/cron-jobs-backup-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
with open(backup_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已备份到: {backup_path}")

# 修复任务
for job in data["jobs"]:
    if job["name"] == "simmer-opportunity-scan":
        # 移除无效的 model 指定
        if "payload" in job and "model" in job["payload"]:
            del job["payload"]["model"]
            print(f"✅ 已移除 simmer-opportunity-scan 的无效模型指定")
    
    if job["name"] == "daily-ai-evolution-research":
        # 暂时禁用这个任务，等确认 delivery target 后再启用
        job["enabled"] = False
        print(f"⚠️  已暂时禁用 daily-ai-evolution-research（待确认 delivery target）")

# 写回
with open(input_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已更新: {input_path}")
