# Cron 修复方案（待 Lunah 批准）

**日期**: 2026-02-24
**问题**: 3 个 cron 任务使用 minimax 模型，其中 2 个持续报错

## 问题 1: simmer-opportunity-scan
- **错误**: cron announce delivery failed (8x consecutive)
- **原因**: 使用 minimax-portal/MiniMax-M2.5 模型，delivery announce 失败
- **修复方案**: 
  - 建议直接禁用（heartbeat 已经在做 Simmer 监控了，这个任务重复）

## 问题 2: daily-ai-evolution-research
- **错误**: cron announce delivery failed (1x)
- **原因**: 同样使用 minimax 模型
- **修复方案**:
  - 改模型为 `claude-sonnet-4-5`（研究类任务需要中等能力）

## 问题 3: foundry-weekly-report
- **状态**: 目前未报错，但使用 minimax 模型（潜在风险）
- **修复方案**:
  - 改模型为 `claude-sonnet-4-5`

## 推荐操作
```bash
# 1. 禁用重复的 simmer 扫描
npx openclaw cron disable 880de2d8

# 2. 修复 AI 进化研究模型
npx openclaw cron update 94d11b08 --model claude-sonnet-4-5

# 3. 修复 foundry 周报模型
npx openclaw cron update dae52af1 --model claude-sonnet-4-5
```
