# GitHub Copilot 跨 Agent 记忆系统

> 来源: GitHub Blog
> 日期: 2026-01-15
> 作者: Tiferet Gazit

## 核心概念

### 1. Just-in-time Verification (即时验证)

> "Information retrieval is an asymmetrical problem: It's hard to solve, but easy to verify."

**核心思路**：不做离线的记忆管理，而是在使用时实时验证。

- 存储记忆时带上 **citations**（代码位置引用）
- Agent 使用记忆前先验证引用的代码位置
- 验证失败则自我修正

### 2. Memory 结构

```json
{
  "subject": "API version synchronization",
  "fact": "API version must match between client SDK, server routes, and documentation.",
  "citations": [
    "src/client/sdk/constants.ts:12",
    "server/routes/api.go:8", 
    "docs/api-reference.md:37"
  ],
  "reason": "If the API version is not kept properly synchronized..."
}
```

### 3. Cross-agent Memory Sharing

- **Code Review** 发现代码规范 → 存储记忆
- **Coding Agent** 使用记忆 → 自动应用相同规范
- **CLI** Debug 时检索记忆 → 快速定位问题

### 4. 自我修复机制

测试发现：
- 即使植入错误的记忆，Agent 也能验证并修正
- 记忆池会自动"自愈"

## 效果数据

| 指标 | 提升 |
|------|------|
| PR 合并率 (Coding Agent) | +7% |
| Code Review 正面反馈 | +2% |

## 与我们系统的对比

| GitHub Copilot | 我们 (Keonho) |
|----------------|---------------|
| citations 引用 | 目前无 |
| 即时验证 | 夜间反思 |
| 跨 Agent 共享 | 目前仅主 Agent |
| 自动过期 | 每周 GC |

## 可借鉴点

1. **添加 citations** - 写入知识时记录来源位置
2. **使用前验证** - Agent 读取时验证信息有效性
3. **跨 Agent 聚合** - 子 Agent 产出聚合到主 Agent

---
*来源: https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/*
