#!/bin/bash
# Simmer 快速查询脚本
# 用法: 
#   ./simmer-status.sh         -> 默认查真实交易 (polymarket)
#   ./simmer-status.sh sim    -> 查询模拟盘 (simmer/LMSR)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../.env.simmer"

if [ "$1" = "sim" ]; then
    echo "=== 🟢 模拟盘 (Simmer LMSR) ==="
    export SIMMER_API_KEY="$SIMMER_TESTNET_API_KEY"
    export SIMMER_VENUE="$SIMMER_TESTNET_VENUE"
else
    echo "=== 🔴 真实交易 (Polymarket) ==="
    # 默认已设置为 polymarket
    export SIMMER_VENUE="$SIMMER_VENUE"
fi

/Users/mac/.simmer-venv/bin/python3 "$SCRIPT_DIR/simmer-check.py" summary
