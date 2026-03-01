#!/usr/bin/env python3
"""
Rejection Log - 记录被拒绝的决策
来自 Moltbook 的最佳实践：rejection log 比 action log 更重要
"""
import json
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/Users/mac/.openclaw/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

REJECTION_LOG_FILE = LOG_DIR / "rejection_log.json"

def load_log():
    """加载现有日志"""
    if REJECTION_LOG_FILE.exists():
        with open(REJECTION_LOG_FILE) as f:
            return json.load(f)
    return []

def save_log(log):
    """保存日志"""
    with open(REJECTION_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def log_rejection(task, reason, details=None, severity="low"):
    """
    记录一个被拒绝的决策
    
    Args:
        task: 任务名称
        reason: 拒绝原因
        details: 详细信息
        severity: 严重程度 (low/medium/high/critical)
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "reason": reason,
        "details": details or {},
        "severity": severity
    }
    
    log = load_log()
    log.append(entry)
    
    # 只保留最近 1000 条
    if len(log) > 1000:
        log = log[-1000:]
    
    save_log(log)
    
    print(f"📝 Rejection logged: {task} - {reason}")
    return entry

def get_rejections(limit=50, severity=None):
    """获取最近的拒绝记录"""
    log = load_log()
    
    if severity:
        log = [e for e in log if e.get('severity') == severity]
    
    return log[-limit:][::-1]

def get_stats():
    """获取统计信息"""
    log = load_log()
    
    if not log:
        return {"total": 0, "by_severity": {}, "by_reason": {}}
    
    by_severity = {}
    by_reason = {}
    
    for entry in log:
        # by severity
        sev = entry.get('severity', 'unknown')
        by_severity[sev] = by_severity.get(sev, 0) + 1
        
        # by reason
        reason = entry.get('reason', 'unknown')
        by_reason[reason] = by_reason.get(reason, 0) + 1
    
    return {
        "total": len(log),
        "by_severity": by_severity,
        "by_reason": by_reason
    }

def print_summary():
    """打印摘要"""
    stats = get_stats()
    
    print("=" * 40)
    print("📊 Rejection Log 统计")
    print("=" * 40)
    print(f"总记录数: {stats['total']}")
    
    if stats['by_severity']:
        print("\n按严重程度:")
        for sev, count in sorted(stats['by_severity'].items(), key=lambda x: -x[1]):
            emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(sev, "⚪")
            print(f"  {emoji} {sev}: {count}")
    
    if stats['by_reason']:
        print("\n按原因:")
        for reason, count in sorted(stats['by_reason'].items(), key=lambda x: -x[1])[:10]:
            print(f"  • {reason}: {count}")
    
    print("=" * 40)

# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "stats":
            print_summary()
        elif sys.argv[1] == "list":
            for r in get_rejections(20):
                print(f"{r['timestamp'][:19]} | {r['task']} | {r['reason']} | {r.get('severity', '')}")
        else:
            task = sys.argv[1]
            reason = sys.argv[2] if len(sys.argv) > 2 else "unknown"
            log_rejection(task, reason)
    else:
        print_summary()
