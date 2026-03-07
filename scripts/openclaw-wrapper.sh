#!/bin/bash
# OpenClaw PATH wrapper for cron jobs
# 确保 openclaw 命令可用

# 添加常见的 openclaw 安装路径到 PATH
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

# 验证 openclaw 可用
if ! command -v openclaw &> /dev/null; then
    echo "Error: openclaw not found in PATH" >&2
    echo "Current PATH: $PATH" >&2
    exit 1
fi

# 执行传入的命令
exec "$@"
