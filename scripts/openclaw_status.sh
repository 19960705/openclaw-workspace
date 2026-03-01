#!/bin/bash
# OpenClaw Agent 状态检查 Cron
# 每小时运行一次

cd /Users/mac/.openclaw/workspace/scripts

# 运行工作流状态检查
python3 workflow_auto.py > /tmp/openclaw_status.txt 2>&1

# 输出日志
echo "$(date): OpenClaw status check completed" >> /tmp/openclaw_cron.log
