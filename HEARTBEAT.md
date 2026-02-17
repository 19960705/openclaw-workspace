# HEARTBEAT.md

## 任务检查

每次 heartbeat 时：

1. 读取 `tasks/tasks.json`
2. 检查是否有待执行的任务（enabled + pending + 到达执行时间）
3. 如果有，执行并汇报
4. 如果没有，继续下面的检查

## Simmer 交易监控（每次 heartbeat）

运行真实 API 检查：
```bash
export SIMMER_API_KEY="..." SIMMER_VENUE="polymarket" && /Users/mac/.simmer-venv/bin/python3 /Users/mac/.openclaw/workspace/scripts/simmer-check.py summary
```

**注意：**
- `SIMMER_API_KEY`: 从 ~/.openclaw/workspace/.env.simmer 读取
- `SIMMER_VENUE`: `simmer`=testnet（模拟盘），`polymarket`=mainnet（真金 USDC）

每次 heartbeat 时：
1. 检查持仓状态（summary）
2. 如果有新已结算交易，推送给用户
3. 如果任何持仓 PnL < -5，立即推送警报
4. 如果胜率掉到 70% 以下，推送提醒
5. 检查高确信度机会（scan），有则推送建议

**不需要打扰用户：**
- 一切正常时，不推送，直接 HEARTBEAT_OK
- 凌晨 23:00-08:00 除非紧急亏损，否则不推送

**记录状态到** `memory/simmer-state.json`：
```json
{
  "lastSimmerCheck": "<ISO timestamp>",
  "lastPositionCount": 34,
  "lastResolvedCount": 17,
  "lastWinRate": 76,
  "lastTotalPnl": 24.23
}
```

## 如果没有任何需要处理的事项

回复 HEARTBEAT_OK
