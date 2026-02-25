
#!/usr/bin/env python3
import json
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
    if job["name"] == "daily-ai-evolution-research":
        # 重新启用，并修改 delivery target 到 topic:2
        job["enabled"] = True
        if "payload" in job and "model" in job["payload"]:
            del job["payload"]["model"]
        if "delivery" in job:
            job["delivery"]["to"] = "telegram:-1003505656701:topic:2"
        print(f"✅ 已重新启用 daily-ai-evolution-research，delivery target 改为 topic:2")

# 写回
with open(input_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 已更新: {input_path}")
