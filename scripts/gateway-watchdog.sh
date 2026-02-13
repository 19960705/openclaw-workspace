#!/bin/bash
#
# OpenClaw Gateway Watchdog
# 自动检测并重启 Gateway 服务，保证频道机器人稳定性
#
# 用法：
#   ./gateway-watchdog.sh              # 单次检查
#   ./gateway-watchdog.sh --daemon     # 守护进程模式
#   ./gateway-watchdog.sh --status     # 查看状态
#
# 建议配合 cron 或 launchd 使用

set -e

# ============== 配置 ==============
OPENCLAW_BIN="/Users/mac/hodonaku-video/.npm/bin/openclaw"
LOG_DIR="/Users/mac/.openclaw/logs"
LOG_FILE="${LOG_DIR}/watchdog.log"
PID_FILE="${LOG_DIR}/watchdog.pid"
CHECK_INTERVAL=60          # 守护模式检查间隔（秒）
MAX_RESTART_ATTEMPTS=3     # 最大连续重启次数
RESTART_COOLDOWN=300       # 连续重启后冷却时间（秒）
HEALTH_CHECK_TIMEOUT=10    # 健康检查超时（秒）

# ============== 初始化 ==============
mkdir -p "$LOG_DIR"

# ============== 日志函数 ==============
log() {
    local level="$1"
    shift
    local msg="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $msg" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }

# ============== 核心函数 ==============

# 检查 Gateway 进程是否存在
check_process() {
    ps aux | grep -E "openclaw-gateway|openclaw gateway" | grep -v grep > /dev/null 2>&1
}

# 获取 Gateway PID
get_gateway_pid() {
    ps aux | grep -E "openclaw-gateway|openclaw gateway" | grep -v grep | awk '{print $2}' | head -1
}

# 检查 Gateway 是否响应（通过进程状态）
check_health() {
    local pid=$(get_gateway_pid)
    if [ -z "$pid" ]; then
        return 1
    fi
    
    # 检查进程是否僵死（CPU 时间是否在增长）
    # 简单检查：进程存在且状态正常
    if ps -p "$pid" -o state= 2>/dev/null | grep -qE '^[RS]'; then
        return 0
    fi
    return 1
}

# 启动 Gateway
start_gateway() {
    log_info "Starting OpenClaw Gateway..."
    
    cd /Users/mac
    nohup "$OPENCLAW_BIN" gateway start > "${LOG_DIR}/gateway-stdout.log" 2>&1 &
    
    # 等待启动
    sleep 3
    
    if check_process; then
        local pid=$(get_gateway_pid)
        log_info "Gateway started successfully (PID: $pid)"
        return 0
    else
        log_error "Failed to start Gateway"
        return 1
    fi
}

# 停止 Gateway
stop_gateway() {
    log_info "Stopping OpenClaw Gateway..."
    
    local pid=$(get_gateway_pid)
    if [ -n "$pid" ]; then
        kill "$pid" 2>/dev/null || true
        sleep 2
        
        # 强制杀死
        if check_process; then
            kill -9 "$pid" 2>/dev/null || true
            sleep 1
        fi
    fi
    
    if ! check_process; then
        log_info "Gateway stopped"
        return 0
    else
        log_error "Failed to stop Gateway"
        return 1
    fi
}

# 重启 Gateway
restart_gateway() {
    log_warn "Restarting OpenClaw Gateway..."
    stop_gateway
    sleep 2
    start_gateway
}

# 单次健康检查
do_health_check() {
    if ! check_process; then
        log_warn "Gateway process not found!"
        return 1
    fi
    
    if ! check_health; then
        log_warn "Gateway health check failed!"
        return 1
    fi
    
    return 0
}

# 显示状态
show_status() {
    echo "====== OpenClaw Gateway Watchdog Status ======"
    echo ""
    
    # Gateway 状态
    if check_process; then
        local pid=$(get_gateway_pid)
        echo "Gateway: ✅ Running (PID: $pid)"
        
        # 进程详情
        ps -p "$pid" -o pid,ppid,%cpu,%mem,etime,command 2>/dev/null | tail -1
    else
        echo "Gateway: ❌ Not Running"
    fi
    
    echo ""
    
    # Watchdog 守护进程状态
    if [ -f "$PID_FILE" ]; then
        local wpid=$(cat "$PID_FILE")
        if ps -p "$wpid" > /dev/null 2>&1; then
            echo "Watchdog Daemon: ✅ Running (PID: $wpid)"
        else
            echo "Watchdog Daemon: ❌ Stale PID file"
        fi
    else
        echo "Watchdog Daemon: ⚪ Not Running"
    fi
    
    echo ""
    
    # 最近日志
    if [ -f "$LOG_FILE" ]; then
        echo "Recent logs:"
        tail -5 "$LOG_FILE"
    fi
}

# 守护进程主循环
daemon_loop() {
    local restart_count=0
    local last_restart_time=0
    
    log_info "Watchdog daemon started (PID: $$)"
    echo $$ > "$PID_FILE"
    
    trap 'log_info "Watchdog daemon stopping..."; rm -f "$PID_FILE"; exit 0' SIGTERM SIGINT
    
    while true; do
        local current_time=$(date +%s)
        
        # 重置重启计数（如果冷却时间已过）
        if [ $((current_time - last_restart_time)) -gt $RESTART_COOLDOWN ]; then
            restart_count=0
        fi
        
        # 健康检查
        if ! do_health_check; then
            if [ $restart_count -lt $MAX_RESTART_ATTEMPTS ]; then
                restart_count=$((restart_count + 1))
                last_restart_time=$current_time
                log_warn "Attempting restart ($restart_count/$MAX_RESTART_ATTEMPTS)..."
                
                if restart_gateway; then
                    log_info "Restart successful"
                else
                    log_error "Restart failed"
                fi
            else
                log_error "Max restart attempts reached. Cooling down for ${RESTART_COOLDOWN}s..."
                sleep $RESTART_COOLDOWN
                restart_count=0
            fi
        fi
        
        sleep $CHECK_INTERVAL
    done
}

# ============== 主程序 ==============

case "${1:-check}" in
    --daemon|-d)
        # 检查是否已有守护进程运行
        if [ -f "$PID_FILE" ]; then
            wpid=$(cat "$PID_FILE")
            if ps -p "$wpid" > /dev/null 2>&1; then
                log_error "Watchdog daemon already running (PID: $wpid)"
                exit 1
            fi
        fi
        daemon_loop
        ;;
    
    --status|-s|status)
        show_status
        ;;
    
    --start|start)
        if check_process; then
            log_info "Gateway already running"
        else
            start_gateway
        fi
        ;;
    
    --stop|stop)
        stop_gateway
        ;;
    
    --restart|restart)
        restart_gateway
        ;;
    
    --check|check|"")
        if do_health_check; then
            log_info "Gateway is healthy"
            exit 0
        else
            log_warn "Gateway is unhealthy, restarting..."
            restart_gateway
            exit $?
        fi
        ;;
    
    --help|-h|help)
        echo "OpenClaw Gateway Watchdog"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  check     Single health check and restart if needed (default)"
        echo "  status    Show current status"
        echo "  start     Start Gateway if not running"
        echo "  stop      Stop Gateway"
        echo "  restart   Restart Gateway"
        echo "  --daemon  Run as daemon (continuous monitoring)"
        echo "  help      Show this help"
        ;;
    
    *)
        echo "Unknown command: $1"
        echo "Use '$0 help' for usage"
        exit 1
        ;;
esac
