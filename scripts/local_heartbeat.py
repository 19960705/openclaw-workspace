#!/usr/bin/env python3
"""
OpenClaw HeartBeat with Local AI
使用 Ollama 本地模型判断是否需要人工介入
"""
import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

# 配置
OLLAMA_MODEL = "qwen2.5:3b"
OLLAMA_PATH = "/opt/homebrew/bin/ollama"
TASKS_FILE = Path("/Users/mac/.openclaw/workspace/tasks/tasks.json")
LOG_FILE = Path("/Users/mac/.openclaw/logs/heartbeat.log")

# LaunchAgent / log mapping (source of truth)
# If a task is in this mapping, we prioritize:
# 1) launchctl print label -> runs/last exit
# 2) stdout/stderr log mtime
TASK_RUNTIME = {
    "task-github-ai-trends": {
        "label": "com.keonho.github-trending",
        "stdout": "/Users/mac/.openclaw/logs/github-trending.log",
        "stderr": "/Users/mac/.openclaw/logs/github-trending_err.log",
    },
    "task-qveris-ai-trending": {
        "label": "com.keonho.qveris-trending",
        "stdout": "/Users/mac/.openclaw/logs/qveris-trending.log",
        "stderr": "/Users/mac/.openclaw/logs/qveris-trending_err.log",
    },
    "task-tiktok-th-001": {
        "label": "com.keonho.thailand-trend",
        "stdout": "/Users/mac/.openclaw/logs/thailand-trend.log",
        "stderr": "/Users/mac/.openclaw/logs/thailand-trend_err.log",
    },

    # Newly added for full heartbeat coverage
    "task-twitter-001": {
        "label": "com.keonho.ai-twitter-digest",
        "stdout": "/Users/mac/.openclaw/logs/ai-twitter-digest.log",
        "stderr": "/Users/mac/.openclaw/logs/ai-twitter-digest_err.log",
    },
    "task-ad-visual-001": {
        "label": "com.keonho.ad-visual-daily",
        "stdout": "/Users/mac/.openclaw/logs/ad-visual-daily.log",
        "stderr": "/Users/mac/.openclaw/logs/ad-visual-daily_err.log",
    },
    "task-simmer-001": {
        "label": "com.keonho.simmer-opportunities",
        "stdout": "/Users/mac/.openclaw/logs/simmer-opportunities-launchd.log",
        "stderr": "/Users/mac/.openclaw/logs/simmer-opportunities-launchd_err.log",
    },
}

def call_local_model(prompt: str, timeout: int = 30) -> str:
    """调用本地模型"""
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", OLLAMA_MODEL, prompt],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def get_task_summary() -> str:
    """获取任务摘要（优先用 launchctl + log mtime 判断是否真的跑过）"""
    if not TASKS_FILE.exists():
        return "无任务文件"

    with open(TASKS_FILE) as f:
        data = json.load(f)

    tasks = data.get("tasks", [])
    now = datetime.now()

    def parse_last_run(s: str):
        if not s:
            return None
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                pass
        return None

    def parse_schedule_time(s: str):
        if not s:
            return None
        try:
            hh, mm = s.split(":")
            return int(hh), int(mm)
        except Exception:
            return None

    def launchctl_print(label: str) -> str:
        try:
            # Use gui domain so it matches LaunchAgents
            uid = subprocess.check_output(["id", "-u"], text=True).strip()
            return subprocess.check_output(["launchctl", "print", f"gui/{uid}/{label}"], text=True, stderr=subprocess.STDOUT)
        except Exception as e:
            return f"ERROR: {e}"

    def extract_int(text: str, key: str):
        # naive parse: look for 'key = N'
        for line in text.splitlines():
            if line.strip().startswith(key):
                try:
                    return int(line.split("=")[1].strip())
                except Exception:
                    return None
        return None

    def file_mtime(path: str):
        try:
            p = Path(path)
            if not p.exists():
                return None
            return datetime.fromtimestamp(p.stat().st_mtime)
        except Exception:
            return None

    def file_tail_contains(path: str, needles, lines: int = 40) -> bool:
        try:
            p = Path(path)
            if not p.exists():
                return False
            tail = "".join(p.read_text(errors='ignore').splitlines(True)[-lines:])
            return any(n in tail for n in needles)
        except Exception:
            return False

    summary_lines = []
    enabled_count = 0
    ok_count = 0
    warn_count = 0

    for task in tasks:
        if not task.get("enabled"):
            continue

        enabled_count += 1
        task_id = task.get("id")
        name = task.get("name", "Unknown")
        schedule = task.get("schedule")
        schedule_time = task.get("scheduleTime")

        # Determine due time for daily schedules
        due = None
        if schedule == "daily":
            t = parse_schedule_time(schedule_time)
            if t:
                hh, mm = t
                due = now.replace(hour=hh, minute=mm, second=0, microsecond=0)

        # Source of truth: LaunchAgent/logs if mapped
        rt = TASK_RUNTIME.get(task_id)
        if rt and rt.get("label"):
            label = rt["label"]
            out = launchctl_print(label)
            runs = extract_int(out, "runs")
            last_exit = extract_int(out, "last exit code")

            m_stdout = file_mtime(rt.get("stdout")) if rt.get("stdout") else None
            m_stderr = file_mtime(rt.get("stderr")) if rt.get("stderr") else None
            last_log = max([d for d in [m_stdout, m_stderr] if d], default=None)

            # A run is considered "today" if logs updated today.
            # (launchctl 'runs' is often 0 for calendar triggers; log mtime is more reliable here.)
            ran_today = bool(last_log and last_log.date() == now.date())

            if due and now < due:
                ok_count += 1
                summary_lines.append(f"🕒 {name}: 未到点 (计划 {schedule_time})")
            else:
                if ran_today:
                    # If the stderr log indicates NOT_IMPLEMENTED/ERROR, treat as failure even if it "ran"
                    bad = False
                    if rt.get("stderr"):
                        # Only treat stderr as "bad" if the stderr log was updated today.
                        m_err = file_mtime(rt["stderr"])
                        if m_err and m_err.date() == now.date():
                            bad = file_tail_contains(rt["stderr"], ["[NOT_IMPLEMENTED]", "Traceback", "ERROR"], lines=60)
                    if bad:
                        warn_count += 1
                        summary_lines.append(
                            f"❌ {name}: 运行失败/未实现 (label={label}, runs={runs}, lastExit={last_exit}, log={last_log.strftime('%Y-%m-%d %H:%M') if last_log else 'n/a'})"
                        )
                    else:
                        ok_count += 1
                        summary_lines.append(
                            f"✅ {name}: 已运行 (label={label}, runs={runs}, lastExit={last_exit}, log={last_log.strftime('%Y-%m-%d %H:%M') if last_log else 'n/a'})"
                        )
                else:
                    warn_count += 1
                    if due:
                        minutes_late = int((now - due).total_seconds() // 60)
                        summary_lines.append(
                            f"❌ {name}: 逾期未运行 (晚 {minutes_late} 分钟, label={label}, runs={runs}, lastExit={last_exit}, log={last_log.strftime('%Y-%m-%d %H:%M') if last_log else 'missing'})"
                        )
                    else:
                        summary_lines.append(
                            f"❌ {name}: 未检测到今日运行 (label={label}, runs={runs}, lastExit={last_exit}, log={last_log.strftime('%Y-%m-%d %H:%M') if last_log else 'missing'})"
                        )
            continue

        # Fallback: tasks.json heuristic (least reliable). We should NOT mark these as ✅ just because status says completed.
        last_run_raw = task.get("lastRun")
        last_run = parse_last_run(last_run_raw) if last_run_raw else None

        note = "（无 LaunchAgent/log 运行证据；tasks.json 可能陈旧）"

        if schedule == "daily" and due:
            ran_today = bool(last_run and last_run.date() == now.date())
            if now < due:
                ok_count += 1
                summary_lines.append(f"🕒 {name}: 未到点 {note} (计划 {schedule_time}, lastRun={last_run_raw or '从未运行'})")
            elif ran_today:
                # still treat as warning because not verified
                warn_count += 1
                summary_lines.append(f"⚠️ {name}: 可能已运行 {note} (lastRun={last_run_raw})")
            else:
                warn_count += 1
                minutes_late = int((now - due).total_seconds() // 60)
                summary_lines.append(f"❌ {name}: 逾期未运行 {note} (晚 {minutes_late} 分钟, lastRun={last_run_raw or '从未运行'})")
        elif schedule == "hourly":
            if not last_run:
                warn_count += 1
                summary_lines.append(f"❌ {name}: 从未运行 {note} (hourly)")
            else:
                mins = int((now - last_run).total_seconds() // 60)
                if mins <= 70:
                    warn_count += 1
                    summary_lines.append(f"⚠️ {name}: 可能最近运行 {note} ({mins} 分钟内, lastRun={last_run_raw})")
                else:
                    warn_count += 1
                    summary_lines.append(f"❌ {name}: 超过 {mins} 分钟未运行 {note} (hourly, lastRun={last_run_raw})")
        else:
            status = task.get("status", "unknown")
            warn_count += 1
            summary_lines.append(f"⚠️ {name}: {status} {note} (lastRun={last_run_raw or '从未运行'})")

    header = f"任务(启用): {ok_count}/{enabled_count} 正常"
    if warn_count:
        header += f"，{warn_count} 个异常/待关注"

    return header + "\n" + "\n".join(summary_lines)

def analyze_with_local_ai(task_summary: str) -> str:
    """用本地 AI 分析任务状态"""
    
    prompt = f"""你是AI助手，负责判断以下任务状态是否正常。

任务状态：
{task_summary}

请判断：
1. 如果所有任务正常 → 只回复 "OK"
2. 如果有问题需要人工处理 → 简要说明需要做什么

只回复简短结果，不要多余解释。"""

    print(f"🤖 调用本地模型: {OLLAMA_MODEL}...")
    # Heartbeat should be fast; longer timeouts cause repeated TIMEOUT/"same" outputs.
    response = call_local_model(prompt, timeout=20)
    return response

def log(message: str):
    """记录日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

def send_telegram(message: str, chat_id: str = "8391832262"):
    """发送 Telegram 消息"""
    import urllib.request
    import urllib.parse
    
    bot_token = "8244872479:AAHuzDb0xQdixsDCEEzjjWQ9vHr5bRv0Gwk"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode()
    
    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        log(f"Telegram发送失败: {e}")
        return False

def main():
    print("=" * 40)
    print("🔔 OpenClaw HeartBeat (Local AI Mode)")
    print("=" * 40)
    
    # 1. 获取任务摘要
    print("\n📋 获取任务状态...")
    task_summary = get_task_summary()
    print(task_summary)
    
    # 2. 调用本地 AI 分析
    print("\n🤖 AI 分析中...")
    result = analyze_with_local_ai(task_summary)
    
    print(f"\n📝 AI 判断:")
    print(result)
    
    # 3. 记录日志
    log(f"AI判断: {result}")
    
    # 4. 返回结果
    if "OK" in result.upper():
        print("\n✅ 一切正常")
        sys.exit(0)
    else:
        print("\n⚠️ 需要人工介入")
        print(result)

        # If local AI timed out, fall back to deterministic rules:
        # - If task_summary has no ❌ lines, treat as OK.
        if (not result) or (result.strip().upper() == "TIMEOUT"):
            has_fail = any(line.strip().startswith("❌") for line in task_summary.splitlines())
            if not has_fail:
                print("\n✅ (Fallback) 无失败项，判定正常")
                sys.exit(0)

        # 发送 Telegram 通知
        alert_msg = f"🔔 OpenClaw HeartBeat 警报\n\n{task_summary}\n\n🤖 AI 判断:\n{result}"
        # Avoid spamming: only send if result has meaningful content
        if result and result.strip() not in {"❌", "TIMEOUT", "ERROR"}:
            if send_telegram(alert_msg):
                print("\n📱 已推送 Telegram 通知")
        else:
            print("\n📵 跳过 Telegram 推送（AI 输出无效/过短）")

        sys.exit(1)

if __name__ == "__main__":
    main()
