# OpenClaw Gateway Watchdog

自动监控并重启 Gateway 服务，保证频道机器人的稳定性。

## 文件说明

- `gateway-watchdog.sh` - 主脚本
- `ai.openclaw.gateway-watchdog.plist` - macOS launchd 配置

## 快速使用

### 手动检查（单次）
```bash
./gateway-watchdog.sh check
```

### 查看状态
```bash
./gateway-watchdog.sh status
```

### 手动重启 Gateway
```bash
./gateway-watchdog.sh restart
```

### 守护进程模式（前台运行）
```bash
./gateway-watchdog.sh --daemon
```

## 安装为系统服务（推荐）

### macOS (launchd)

```bash
# 复制 plist 到 LaunchAgents
cp ai.openclaw.gateway-watchdog.plist ~/Library/LaunchAgents/

# 加载服务（立即生效 + 开机自启）
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist

# 查看状态
launchctl list | grep openclaw

# 停止服务
launchctl unload ~/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist
```

### Linux (cron)

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每分钟检查一次）
* * * * * /path/to/gateway-watchdog.sh check >> /var/log/openclaw-watchdog.log 2>&1
```

### Linux (systemd)

创建 `/etc/systemd/system/openclaw-watchdog.service`:
```ini
[Unit]
Description=OpenClaw Gateway Watchdog
After=network.target

[Service]
Type=simple
ExecStart=/path/to/gateway-watchdog.sh --daemon
Restart=always
User=your-user

[Install]
WantedBy=multi-user.target
```

然后：
```bash
sudo systemctl enable openclaw-watchdog
sudo systemctl start openclaw-watchdog
```

## 配置参数

在 `gateway-watchdog.sh` 顶部可以调整：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CHECK_INTERVAL` | 60 | 守护模式检查间隔（秒） |
| `MAX_RESTART_ATTEMPTS` | 3 | 最大连续重启次数 |
| `RESTART_COOLDOWN` | 300 | 连续重启后冷却时间（秒） |
| `HEALTH_CHECK_TIMEOUT` | 10 | 健康检查超时（秒） |

## 日志位置

- 主日志：`~/.openclaw/logs/watchdog.log`
- Gateway 输出：`~/.openclaw/logs/gateway-stdout.log`
- launchd 日志：`~/.openclaw/logs/watchdog-launchd.log`

## 工作原理

1. 每 60 秒检查 Gateway 进程是否存在
2. 检查进程状态是否正常（非僵死）
3. 如果异常，自动重启 Gateway
4. 连续重启 3 次失败后，冷却 5 分钟再试
5. 所有操作记录到日志
