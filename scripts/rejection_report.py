#!/usr/bin/env python3
"""
Rejection Log 自动报告
每天自动生成并推送到 Telegram
"""
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("/Users/mac/.openclaw/logs/rejection_log.json")

def generate_report():
    """生成每日报告"""
    if not LOG_FILE.exists():
        return "暂无记录"
    
    with open(LOG_FILE) as f:
        log = json.load(f)
    
    if not log:
        return "📊 Rejection Log: 暂无记录"
    
    # 统计
    by_reason = {}
    by_severity = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    
    for entry in log:
        reason = entry.get("reason", "unknown")
        by_reason[reason] = by_reason.get(reason, 0) + 1
        
        sev = entry.get("severity", "low")
        by_severity[sev] = by_severity.get(sev, 0) + 1
    
    # 生成消息
    lines = [
        "📊 Rejection Log 日报",
        f"📅 {datetime.now().strftime('%Y-%m-%d')}",
        f"总记录: {len(log)}",
        ""
    ]
    
    if by_severity:
        lines.append("按严重程度:")
        for sev, count in by_severity.items():
            if count > 0:
                emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(sev, "⚪")
                lines.append(f"  {emoji} {sev}: {count}")
    
    if by_reason:
        lines.append("")
        lines.append("Top 原因:")
        for reason, count in sorted(by_reason.items(), key=lambda x: -x[1])[:5]:
            lines.append(f"  • {reason}: {count}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(generate_report())
