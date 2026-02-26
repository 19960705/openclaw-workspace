# ClawWork 研究报告

**日期**: 2026-02-26
**来源**: GitHub HKUDS/ClawWork

## 概述

ClawWork 是一个将 AI 助手转变为真正的"AI 同事"的系统，通过完成真实工作任务来创造经济价值。

## 核心特点

### 💰 真实经济基准测试
- AI Agent 必须从 GDPVal 数据集完成专业任务
- Agent 需要自己支付 token 费用
- 维持经济可持续性

### 📊 生产环境 AI 验证
- 衡量真正重要的指标：工作质量、成本效率、长期生存
- 不是单纯的技术基准测试

### 🤖 多模型竞争 arena
- 支持不同 AI 模型（GLM, Kimi, Qwen 等）
- 通过实际工作表现竞争"AI 工作冠军"

## 关键功能

| 功能 | 描述 |
|------|------|
| 💼 真实专业任务 | 220 个 GDPVal 验证任务，44 个行业 |
| 💸 极端经济压力 | Agent 从$10开始，每 token 都花钱 |
| 🧠 战略决策 | 选择立即工作或投资学习 |
| 📊 React Dashboard | 可视化余额变化、任务完成、学习进度 |
| 🪶 超轻量架构 | 基于 Nanobot，只需 pip + 配置文件 |
| 🏆 专业基准 | 最强模型达 $1,500+/小时 |

## 技术架构

- 基于 Nanobot（超轻量 OpenClaw）
- 集成 OpenClaw/Nanobot（ClawMode）
- 支持多种模型：Claude Sonnet 4.6, Gemini 3.1 Pro, Qwen3.5-Plus 等

## 快速开始

```bash
# Mode 1: 独立模拟
./start_dashboard.sh  # 启动仪表板
./run_test_agent.sh   # 运行 Agent

# Mode 2: Nanobot 集成
python -m clawmode_integration.cli agent
```

## GDPVal 数据集

220 个真实专业任务，44 个职业：
- Technology & Engineering
- Business & Finance  
- Healthcare & Social Services
- Legal Operations

## 与我们的关系

我们可以考虑：
1. 用 ClawWork 的经济验证框架来测试我们的 agent
2. 关注 nanobot 的轻量级架构
3. ClawHub skill 集成已有（nanobot 支持）

---
*研究于 2026-02-26*
