# AI Agent 自进化研究笔记
**更新日期**: 2026-02-23 | **来源**: STELLA, AgentEvolver, KAD8, ICLR 2026

## 核心趋势：2026 是自进化之年

2024 = 能力，2025 = Agent，2026 = 自进化
- 静态 LLM 不够了，关键瓶颈不是推理深度，而是「不可变性」
- 从「人类数据时代」→「经验时代」（Richard Sutton 预言成真）
- ICLR 2026 把 RSI（递归自我改进）从哲学问题变成工程问题

## 五维自进化框架（ICLR 2026 共识）

1. **Change Targets** — 什么在进化？参数/记忆/工具/策略/架构
2. **Adaptation Timing** — 何时进化？任务中/任务间/部署间
3. **Mechanisms** — 如何进化？自我批评/模仿/进化搜索/梯度更新
4. **Operating Contexts** — 在哪运行？沙盒/生产环境
5. **Safeguards** — 如何验证改进、防止退化？

## STELLA 架构（最接近 Foundry）

四个 Agent 角色：
- Manager → 任务分解，选择工作流模板
- Dev → 执行代码和工具调用
- Critic → 评估中间结果，发现缺失步骤
- Tool Creation → 检测能力缺口，自动创建新工具

两个进化存储：
- Template Library → 成功的多步推理计划（≈ Foundry patterns）
- Tool Ocean → 动态增长的工具注册表（≈ Foundry extensions/skills）

## AgentEvolver 三大机制

1. **Self-Questioning**（好奇心驱动）
   - 用高温策略探索多样化动作
   - LLM 从轨迹中合成新任务
   - 去重+可行性检查过滤幻觉任务

2. **Self-Navigating**（经验引导）
   - 过去的成功/失败总结为自然语言"经验"
   - 新任务时检索 top-k 相关经验指导
   - 经验引导的样本在优化中获得加权提升

3. **Self-Attributing**（细粒度归因）
   - LLM 对完整轨迹做 token 级 GOOD/BAD 标注
   - 不只是"成功/失败"，而是分析每一步的贡献
   - 样本效率翻倍

## 2026 三大硬问题

1. **Zero-Data Evolution** — 无标注数据环境下自我生成反馈
2. **Algorithmic Self-Modification** — 受控地改写自身代码（Sakana AI DGM）
3. **Meta-Cognitive Shaping** — 选择性学习：这个经验值得记住吗？该泛化还是丢弃？

## 可在 Foundry 实现的改进

### 已有（对标 STELLA）
- ✅ foundry_overseer → Manager/Critic
- ✅ foundry_crystallize → Template Library
- ✅ foundry_evolve → Tool Creation Agent
- ✅ foundry_learnings → 经验存储

### 可新增
1. **Self-Questioning 机制** — 在自由活动时间主动发现能力缺口
   - 实现：分析最近的失败 patterns，生成"如果有 X 工具就能解决"的假设
   - 然后尝试用 foundry 创建该工具

2. **细粒度归因** — 升级 outcome tracking
   - 现在只有 success/failure
   - 改进：对每个工具调用链做步骤级评分

3. **Meta-Cognitive Filter** — 选择性记忆
   - 不是所有经验都值得记住
   - 实现：在 crystallize 前加一个"值得结晶吗？"的评估步骤

4. **经验引导探索** — 新任务前检索相关经验
   - 已有 foundry_get_insights，但可以更深入
   - 改进：用 memory_search 检索相关历史轨迹，注入到任务 prompt 中
