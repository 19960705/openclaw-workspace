# HEARTBEAT.md

## 任务检查
每次 heartbeat：
1. 读取 tasks/tasks.json，检查待执行任务
2. 有任务→执行并汇报；无任务→继续

## 定时任务表
| 时间 | 任务 | 发送至 |
|------|------|--------|
| 08:00 | GitHub AI 趋势 | topic:2 |
| 08:30 | QVeris AI 趋势 (X/Twitter) | topic:2 |
| 09:00 | AI 日报（NewsNow 聚合：hackernews + producthunt + github-trending-today + 36kr + juejin + ithome + sspai，筛选 AI/创意相关） | topic:2 |
| 09:30 | 4A 广告 | topic:3 |
| 10:00 | TikTok 泰区 | topic:4 |
| 18:00 | OpenClaw 话题 | topic:5 |
| 20:00 | Seedance 案例 | topic:3 |

## Simmer 交易监控
每次 heartbeat 运行 → 推送至 topic:6

检查：
- 持仓状态 → PnL < -5 或胜率 <70% → 推送警报
- 高确信度机会 → 有则推送
- BTC/ETH 5分钟市场 → 40-60%概率机会 → 推送

## 会话健康检查
检查 token 使用率 >80% → 提醒用户

## 无任务时
回复 HEARTBEAT_OK
