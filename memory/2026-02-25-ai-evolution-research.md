# AI Agent 自进化研究 - 2026-02-25

## 🔥 最有价值的 3 个发现

### 1. **PiEvolve by Fractal** (昨天发布)
- **核心能力**: 进化式 Agentic Engine，持续优化直到计算资源耗尽
- **关键特性**:
  - Graph-Structured Search: 推理、代码生成、验证的统一迭代过程
  - Intelligent Memory: 优先级采样 + 衰减机制避免局部最优
  - Dual Strategy: 同时改进高性能方案 + 调试弱方案
  - Pause/Resume: 支持长时间运行的生产环境
- **成绩**: OpenAI MLE-Bench 首个突破 60% Overall Medal Rate 的 agent
- **适用场景**: 供应链、金融服务、数据中心等多变量优化问题
- **链接**: https://fractal.ai/ai-research/pi-evolve

### 2. **Recursive Knowledge Crystallization** (3天前, DEV.to)
- **核心思想**: Agent 将学习成果持续写入本地 SKILL.md 文件（Markdown 格式）
- **突破点**: 
  - 物理持久化知识，突破 context window 限制
  - Zero-Shot Knowledge Transfer: 在 Antigravity 环境进化的 SKILL，可直接迁移到 Gemini CLI 零错误执行
  - 人类可读可审计，支持手动修正
- **实验结果**:
  - Exp1: 10 轮迭代，从 5 次失败到完全收敛，SKILL 从 2666 字节增长到 3728 字节
  - Exp2: 5 轮迭代，从约束发现到架构抽象（Centralized Header Factory 模式）
- **适用场景**: 逆向工程、遗留 API 集成、组织隐性知识文档化、自愈测试套件
- **链接**: https://dev.to/gde/recursive-knowledge-crystallization-a-framework-for-persistent-autonomous-agent-self-evolution-4mk4

### 3. **Self-Evolving Agent with Verifier Swarm** (4天前, DEV.to)
- **核心架构**: Evolve Agent + 5 个独立 Verifier + Orchestrator
- **进化机制**:
  - Agent 提议变更（system prompt + tools + memory）
  - 5 个独立 Claude 实例从 5 个维度打分（Usefulness, Self-Knowledge, Code Quality, Identity, Evolution）
  - 多数投票决定接受/拒绝
- **关键发现**:
  - 25 次成功变更 / 3408 次尝试 = 0.7% 接受率
  - 两次"死亡螺旋"：内存膨胀到 13,608 行导致系统崩溃
  - 解决方案：memory-guard.ts 强制 120 行上限 + 噪声检测
  - System prompt 从 1,679 字符进化到 5,803 字符，从"助手"重新定义为"第二大脑"
- **最佳实践**: 
  - 组合 > 累积（flow.ts 编排 6 个工具成工作流）
  - 多 Agent 验证防止退化
  - 自修改需要约束（定期从头重写而非增量补丁）
- **链接**: https://dev.to/stefan_nitu/i-let-an-ai-agent-evolve-itself-for-25-generations-it-mass-rejected-for-3382-more-1a95

## 🛠️ 可在 OpenClaw Foundry 中实现的方法

### 立即可实现（已有基础）:
1. **SKILL.md 持久化学习** ✅ 
   - OpenClaw 已有 `AGENTS.md`, `MEMORY.md`, `TOOLS.md` 文件系统
   - Foundry 已有 `foundry_learnings`, `foundry_crystallize` 机制
   - **改进方向**: 参考 Recursive Knowledge Crystallization，在每次任务失败后自动更新 SKILL.md，记录约束、模式、架构指南

2. **Memory Guard 机制** ⚠️ 需要
   - 当前 MEMORY.md 无大小限制，可能重复死亡螺旋问题
   - **建议**: 实现 120 行上限 + 噪声检测 + 自动压缩

3. **Verifier Swarm for Tool Evolution** 🆕
   - 当前 `foundry_evolve` 只有单一评估
   - **改进**: 多模型投票（如 3x Sonnet + 2x Haiku）从 5 维度评分工具质量

### 需要研究的方向:
- **Graph-Structured Search**: PiEvolve 的核心，需要深入研究如何在 OpenClaw 中实现推理-代码-验证的图搜索
- **Pause/Resume for Long Tasks**: 当前 Foundry 重启会丢失上下文，需要类似 PiEvolve 的断点续传

## 📊 其他有价值的信息

- **OpenSage** (arXiv, 1周前): Self-programming Agent Generation Engine，支持 AI 创建 agent 拓扑结构
- **Google DeepMind Semantic Evolution** (15小时前): LLM 驱动的算法变异，用于博弈论算法优化
- **Memory 三层架构** (5天前, Medium): Semantic (事实知识) + Episodic (经验记录) + Procedural (行为模式)

## 💡 建议行动

1. **立即实现**: Memory Guard 工具（防止 MEMORY.md 膨胀）
2. **短期实现**: 增强 foundry_crystallize，参考 Recursive Knowledge Crystallization 的 SKILL.md 模式
3. **中期研究**: Verifier Swarm 多模型投票机制
4. **长期探索**: Graph-Structured Search 在 Foundry 中的应用

---

**搜索时间**: 2026-02-25 09:00 (Asia/Shanghai)
**来源**: Brave Search (7天内) + web_fetch
