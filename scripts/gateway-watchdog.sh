#!/bin/bash
# Gateway Watchdog - 自动监控并重启 Gateway
# 用法：每 5 分钟通过系统 cron 运行

export PATH="$HOME/.nvm/versions/node/v22.12.0/bin:$PATH"
LOG_FILE="$HOME/logs/gateway-watchdog.log"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查 Gateway 进程是否存在
check_gateway() {
    if pgrep -f "openclaw.*gateway" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# 重启 Gateway
restart_gateway() {
    log "Gateway not running, attempting restart..."
    
    # 杀死旧进程
    pkill -f "openclaw.*gateway" 2>/dev/null
    sleep 2
    
    # 启动新进程
    nohup openclaw gateway > /dev/null 2>&1 &
    sleep 5
    
    # 验证
    if check_gateway; then
        log "✅ Gateway restarted successfully"
        return 0
    else
        log "❌ Gateway restart failed"
        return 1
    fi
}

# 主逻辑
log "--- Watchdog check ---"

if check_gateway; then
    log "✅ Gateway healthy (process running)"
else
    log "⚠️ Gateway not running"
    restart_gateway
fi
