# 自我进化记录

## 每周自检清单

### 1. 能力盘点
- [ ] 这周学到了什么新技能？
- [ ] 有没有重复解决以前解决过的问题？
- [ ] 有哪些经验可以写成 skill？

### 2. 效率检查
- [ ] 工具调用有没有可以优化的？
- [ ] 有没有更高效的方式完成常见任务？

### 3. 记忆检查
- [ ] 学到的重要东西是否都存到 MEMORY.md 了？
- [ ] 有没有忘记之前记录的重要信息？

### 4. 主动性检查
- [ ] 有没有主动发现问题/机会？
- [ ] 有没有主动推进项目？

---

## 进化触发条件

满足任一即触发深度自检：
- 连续 3 次用同一种方式解决类似问题
- 用户反馈"这个之前做过"
- 发现可以复用的工具/流程

## 产出要求

每次自检必须产出：
1. 至少 1 条可复用的经验 → 写入 MEMORY.md
2. 至少 1 个可优化的流程 → 考虑写成 skill/hook

---

## 自检记录

### 2026-02-23（自由活动 Day 1）

**能力盘点：**
- 学到：STELLA/AgentEvolver 自进化框架、Seedance 2.0 最新教程
- 重复操作：每次启动都要读一堆文件 → 已加入 health-check 脚本自动化
- 写成 skill：workspace-health-check.sh（自动检查 cron/磁盘/memory/git/安全）

**效率检查：**
- cron 用不可用模型静默失败 → 已修复，health-check 会自动检测
- CLI 环境不可用时反复尝试 → 教训：直接读配置文件

**记忆检查：**
- ✅ MEMORY.md 已更新（补充 02-21/02-22 事实）
- ✅ 默认模型信息已修正

**主动性检查：**
- ✅ 主动发现 5 个 cron 问题 + .gitignore 缺失
- ✅ 主动研究自进化方法论并落地 Self-Questioning 机制

**产出：**
1. knowledge/ai-agent-self-evolution.md — 自进化研究笔记
2. knowledge/seedance-2.0-latest.md — Seedance 最新技巧
3. scripts/workspace-health-check.sh — 自动健康检查
4. FREE_TIME_RULES.md 更新 — 加入自进化环节 + health-check

### 2026-02-24（自由活动 Day 2）

**能力盘点：**
- 学到：Seedance 2.0 vs Sora 2/Veo 3.1 竞品对比、突破15秒限制工作流
- 重复操作：edit 工具频繁因文本不匹配失败 → 应先 read 确认再 edit
- 可复用：cron 错误诊断流程（检查 jobs.json → 分析模型/delivery → 准备修复方案）

**效率检查：**
- edit 工具失败率高 → 教训：先 read 文件确认精确文本，再 edit
- 长时间 sleep 等待不高效 → 应该持续做有价值的工作直到结束

**记忆检查：**
- ✅ MEMORY.md 已更新（Simmer 状态、Cron 错误、自由时间记录）
- ✅ Seedance 知识已合并到 knowledge/seedance-2.0-latest.md

**主动性检查：**
- ✅ 主动发现 cron 错误根因（minimax 模型 + announce delivery）
- ✅ 准备了修复方案（memory/2026-02-24-cron-fix-plan.md）
- ✅ 深入研究 Seedance 2.0 并更新知识库

**产出：**
1. knowledge/seedance-2.0-latest.md 更新 — 竞品对比 + 突破15秒
2. memory/2026-02-24-cron-fix-plan.md — Cron 修复方案
3. MEMORY.md 更新 — 新增 2 条 FACT
4. Git commit + push — 48 files committed
