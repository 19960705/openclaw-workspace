# Screenshot Service - 截图服务

在 Mac mini 本地截图并发送到 Discord。

## 使用场景

当用户需要我截图并发送到 Discord 时使用（例如预览网页、项目状态等）。

## 前置要求

### 1. 安装依赖工具

```bash
# 确保有截图工具（macOS 内置）
which screencapture

# 如果需要上传到 Discord，需要 curl
which curl
```

### 2. 配置 Discord Webhook

在 Discord 服务器创建 Webhook：

1. 服务器设置 → 整合 → Webhooks
2. 创建 Webhook，复制 URL
3. 配置：

```bash
./scripts/screenshot-service.sh --configure "https://discord.com/api/webhooks/..."
```

Webhook URL 保存在：`~/.openclaw/screenshots/.discord_webhook_url`

## 使用方式

### 方式 1：通过脚本命令

```bash
# 截取整个屏幕
./scripts/screenshot-service.sh --full

# 截取当前窗口
./scripts/screenshot-service.sh --window

# 用户选择区域
./scripts/screenshot-service.sh --selection

# 截屏并发送到 Discord
./scripts/screenshot-service.sh --discord
```

### 方式 2：通过 OpenClaw 调用（需要 host 权限）

```bash
# 截图并发送
./scripts/screenshot-service.sh --discord
```

## Discord 发送格式

发送截图时，支持附加消息：

```bash
./scripts/screenshot-service.sh --discord "📸 首页预览"
```

## 截图存储位置

```
~/.openclaw/screenshots/
├── screenshot_20260214_120000.png
├── screenshot_20260214_120101.png
└── .discord_webhook_url
```

## 常见问题

### Q: 截图命令失败

A: 确保在 Mac mini 本地运行，需要 GUI 环境。

### Q: Discord 发送失败

A: 检查 Webhook URL 是否正确配置：
```bash
cat ~/.openclaw/screenshots/.discord_webhook_url
```

### Q: 想发送现有文件

A: 直接修改脚本或使用 curl：

```bash
curl -X POST \
    -H "Content-Type: multipart/form-data" \
    -F "file=@/path/to/image.png" \
    -F "content=📸 截图描述" \
    "YOUR_DISCORD_WEBHOOK_URL"
```

## 与 Discord 集成

在 OpenClaw 中发送截图到 Discord：

```bash
# 1. 截图
./scripts/screenshot-service.sh --discord "📸 项目状态"

# 2. 文件已通过 webhook 发送
```

## 定时截图（可选）

设置定时截图监控：

```bash
# crontab -e 添加
# 每小时截取一次屏幕
0 * * * * /path/to/screenshot-service.sh --discord "📸 $(date '+%Y-%m-%d %H:%M') 系统状态"
```
