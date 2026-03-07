# AI Agent 自进化研究 (2026-03-07)

## 核心发现

### 1. OpenClaw Evolution Framework (TerryFYL)
**GitHub**: https://github.com/TerryFYL/openclaw-evolution-framework

**核心机制**:
- **自触发循环**: Agent 完成探索后调用 `exec` 触发下一轮，不依赖固定 cron
- **主题轮换**: 5个主题加权随机选择，避免重复
- **安全机制**: 
  - 时间限制 (max_duration_hours)
  - HITL 检查点 (round 20, 40 暂停)
  - 夜间静默模式 (silent_delivery)

**实测数据**:
- 运行时长: 10小时 (22:50 → 07:53)
- 完成轮次: 59轮
- 生成内容: ~200,000字
- 自触发成功率: 98%
- 间隔: 8分钟 (实际9分钟/轮)

**架构**:
```
┌─────────────────────────────────────────┐
│ Cron Trigger (every 8 min)              │
└──────────────────┬──────────────────────┘
                   ├→ Check time (stop if past deadline)
                   ├→ Select theme (rotate from 5 options)
                   ├→ Deep exploration (8-15 min thinking)
                   ├→ Save insights (markdown file)
                   └→ Self-trigger next round (exec background)
```

**主题分布**:
- Domain Expertise: 15轮 (25%)
- System Thinking: 12轮 (20%)
- User Understanding: 12轮 (20%)
- Free Exploration: 10轮 (17%)
- Practical Application: 10轮 (17%)

**示例输出**:
- Round 14: "AI's Intuition - System 1 vs System 2"
- Round 42: "Designing Emotion for AI Agents" (3层架构)
- Round 58: "Medical LLMs - 10 Cognitive Blind Spots"

---

### 2. GitHub Agentic Workflows (GitHub 官方, 2026-02-13)
**文档**: https://github.github.com/gh-aw/

**核心创新**:
- **Markdown 定义**: YAML frontmatter + Markdown body
- **编译模型**: `.md` → `.lock.yml` (50-60KB 生成的 YAML)
- **安全模型**: 16层防御

**架构**:
```
┌─────────────────────────────────────────┐
│ issue-triage-agent.md                   │
│ (你编写的 Markdown)                      │
└──────────────────┬──────────────────────┘
                   │ gh aw compile
                   ▼
┌─────────────────────────────────────────┐
│ issue-triage-agent.lock.yml             │
│ (GitHub Actions 运行的 YAML)             │
└─────────────────────────────────────────┘
```

**Safe Inputs** (内联工具定义):
```yaml
safe-inputs:
  check-npm-package-info:
    description: "Look up an npm package's latest version"
    inputs:
      package_name:
        type: string
        required: true
    script: |
      const resp = await fetch(`https://registry.npmjs.org/${package_name}/latest`);
      const data = await resp.json();
      return { name: data.name, latest_version: data.version };
```

**MCP Server 集成**:
```yaml
mcp-servers:
  deepwiki:
    url: "https://mcp.deepwiki.com/sse"
    allowed:
      - read_wiki_structure
      - read_wiki_contents
      - ask_question
```

**安全层**:
1. WASM Dual-Metered Sandbox
2. Merkle Hash-Chain Audit Trail
3. Information Flow Taint Tracking
4. Ed25519 Signed Agent Manifests
5. SSRF Protection
6. Secret Zeroization
7. OFP Mutual Authentication
8. Capability Gates
9. Security Headers
10. Health Endpoint Redaction
11. Subprocess Sandbox
12. Prompt Injection Scanner
13. Loop Guard
14. Session Repair
15. Path Traversal Prevention
16. GCRA Rate Limiter

**实际应用**:
- Issue Triage Agent
- CI Doctor (故障诊断)
- Daily Repo Status
- Doc Sync
- Code Simplifier
- Test Improver
- Security Monitor (+ DeepWiki MCP)
- Dependency Health Check

---

### 3. OpenFang Agent OS (RightNow-AI, 11.5K⭐)
**GitHub**: https://github.com/RightNow-AI/openfang

**核心特性**:
- **语言**: Rust (137K LOC, 14 crates, 1,767+ tests)
- **大小**: 单二进制 32MB
- **冷启动**: <200ms
- **架构**: Agent 操作系统（不是框架）

**Hands 系统** (7个自主能力包):
| Hand | 功能 |
|------|------|
| Clip | YouTube → 竖屏短视频 (8阶段流水线) |
| Lead | 每日潜在客户发现 + ICP 评分 |
| Collector | OSINT 情报收集 + 知识图谱 |
| Predictor | 超级预测引擎 (Brier 评分) |
| Researcher | 深度研究 + CRAAP 可信度评估 |
| Twitter | 自主 Twitter 账号管理 (7种内容格式) |
| Browser | Web 自动化 (Playwright + 购买审批门) |

**Hand 结构**:
```
HAND.toml         # 清单：工具、设置、要求、指标
System Prompt     # 500+ 字操作手册
SKILL.md          # 领域专业知识
Guardrails        # 敏感操作审批门
```

**性能对比** (vs OpenClaw):
- 冷启动: 180ms vs 5.98s
- 内存: 40MB vs 394MB
- 二进制: 32MB vs 500MB
- 自主 Hands: 16 vs 0
- 安全层: 16 vs 3

**14个 Rust Crates**:
- openfang-kernel: 编排、工作流、计量、RBAC
- openfang-runtime: Agent 循环、WASM 沙箱、MCP、A2A
- openfang-api: 140+ REST/WS/SSE 端点
- openfang-channels: 40个消息适配器
- openfang-memory: SQLite + 向量嵌入
- openfang-hands: 7个自主 Hands
- openfang-migrate: OpenClaw 迁移引擎

---

## OpenClaw Foundry 可实现的改进

### ✅ 已实现

**evolution-loop hook**:
- 自触发探索循环
- 5个主题轮换（AI架构、工具生态、安全机制、实战案例、自由探索）
- HITL 检查点（第10、20轮）
- 夜间静默模式
- 配置文件: `evolution-config.json`
- 状态文件: `.evolution-state.json`
- 输出: `memory/evolution-round-XXX.md`

启用: `openclaw hooks enable evolution-loop`
触发: `/evolve`

### 🔜 待实现

**1. Markdown → Hook 编译器** (借鉴 GitHub Agentic Workflows)
```typescript
foundry_compile_workflow({
  input: "workflow.md",  // YAML frontmatter + Markdown body
  output: "hook/"        // 生成 HOOK.md + handler.ts
})
```

**2. Hands 系统** (借鉴 OpenFang)
- 扩展 SKILL.md 格式支持 `schedule` 字段
- 创建 `foundry_write_hand` 工具
- 预构建能力包：Lead Gen、OSINT、Forecasting

**3. Safe Inputs** (内联工具定义)
- 在 hook frontmatter 中定义自定义工具
- 支持 JS/Python/Shell/Go
- 运行时沙箱隔离

---

## 关键洞察

### 自进化的三个层次

**Level 1: 自触发循环** (已实现)
- Agent 完成任务后自己启动下一轮
- 主题轮换避免重复
- 时间限制 + HITL 检查点

**Level 2: 编译时元编程** (待实现)
- Markdown → 可执行代码
- 声明式配置 → 命令式逻辑
- 安全约束编译时验证

**Level 3: 运行时自适应** (未来)
- 根据结果调整策略
- 动态工具组合
- 自我评估 + 改进

### 架构模式

**1. 自触发 vs Cron**
- 自触发: 完成即启动，无等待
- Cron: 固定间隔，可能错过
- 最佳: 自触发 + Cron 备份

**2. 主题轮换 vs 自由探索**
- 轮换: 平衡覆盖，避免偏好
- 自由: 深度挖掘，可能重复
- 最佳: 加权随机 + 避免上一轮

**3. HITL vs 全自动**
- HITL: 质量控制，及时纠偏
- 全自动: 高效，但可能跑偏
- 最佳: 关键检查点暂停

---

## 参考资源

- [OpenClaw Evolution Framework](https://github.com/TerryFYL/openclaw-evolution-framework)
- [GitHub Agentic Workflows](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)
- [OpenFang Agent OS](https://github.com/RightNow-AI/openfang)
- [Josh's Demo: 11 Agentic Workflows](https://github.com/joshjohanning-org/agents-and-agentic-workflows)
- [Continuous AI - GitHub Next](https://githubnext.com/projects/continuous-ai/)

---

**研究时间**: 2026-03-07 09:01-09:02 (1分钟)
**来源**: Web Search (Brave) + Web Fetch
**状态**: ✅ 完成 + evolution-loop hook 已创建
