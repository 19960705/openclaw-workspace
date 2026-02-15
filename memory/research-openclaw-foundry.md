# OpenClaw Foundry 研究报告

> 研究时间：2026-02-15
> 项目地址：https://github.com/lekt9/openclaw-foundry
> 版本：0.2.3

---

## 一、项目概述与核心理念

### 1.1 一句话定义

Foundry 是一个运行在 OpenClaw 平台上的**自我编写型元插件（self-writing meta-extension）**，它通过观察用户工作流、研究文档、学习模式并将其"结晶"为可执行代码，实现了递归式的自我进化。

### 1.2 核心口号

> "The forge that forges itself."（铸造自身的熔炉）

### 1.3 核心理念

Foundry 的哲学基于一个关键区分：

| 类型 | 知识（Knowledge） | 行为（Behavior） |
|------|-------------------|-------------------|
| 存储方式 | 文本/提示词 | 可执行代码 |
| 每次调用成本 | 消耗 token | 零 token |
| 可靠性 | 可能被遗忘或忽略 | 始终执行 |
| 示例 | "当 X 发生时，做 Y" | 代码自动在 X 发生时做 Y |

**核心论点**：传统代理每次都运行相同逻辑，而 Foundry 通过"递归自我改进"实现**复合增长**——改进系统的系统本身也在被改进。

### 1.4 学术基础

Foundry 引用了多篇 AI 代理自我改进的论文：

- **Self-Improving Coding Agent** (arXiv:2504.15228)：代理可自主编辑自身，实现 17-53% 的改进
- **RISE: Recursive Introspection** (arXiv:2407.18219)：迭代微调让模型在失败后修改响应
- **SelfEvolve** (arXiv:2306.02907)：两步管线——知识生成 + 自我反思调试
- **HexMachina** (arXiv:2506.04651)："制品中心的持续学习"——将发现与策略演化分离
- **ADAS** (arXiv:2408.08435)：元代理通过存档式演化迭代发现改进的代理设计

---

## 二、技术架构分析

### 2.1 项目文件结构

```
openclaw-foundry/
├── index.ts                    # 核心插件代码（~6000行，单文件巨石架构）
├── package.json                # NPM 包配置（@getfoundry/foundry-openclaw v0.2.3）
├── openclaw.plugin.json        # OpenClaw 插件注册清单
├── tsconfig.json               # TypeScript 配置
├── skills/
│   └── foundry/
│       └── SKILL.md            # Foundry 的 AgentSkills 格式描述文件
├── docs/
│   ├── ARCHITECTURE.md         # 架构文档
│   └── PROACTIVE-LEARNING.md   # 主动学习机制文档
├── server/                     # Marketplace 服务器（独立部署）
│   ├── src/
│   │   ├── index.ts            # Bun 服务器入口
│   │   ├── schema.sql          # SQLite 数据库 schema
│   │   ├── db.ts               # 数据库层
│   │   ├── types.ts            # TypeScript 类型定义
│   │   ├── x402.ts             # Solana USDC x402 支付协议
│   │   ├── skill-review.ts     # 安全审查（静态+LLM）
│   │   └── routes/
│   │       ├── publish.ts      # 发布路由
│   │       ├── search.ts       # 搜索路由
│   │       ├── summary.ts      # 摘要路由
│   │       └── download.ts     # 下载路由（x402 付费墙）
│   └── web/                    # React 前端（Vite + TypeScript）
├── HN_POST.md                  # Hacker News 投稿
├── REDDIT_POST.md              # Reddit 投稿
├── SWARMS_LISTING.md           # Swarms 平台列表
└── flake.nix                   # Nix 可复现构建
```

### 2.2 核心模块（全部在 index.ts 中）

#### 2.2.1 DocsFetcher（文档获取器）

- 从 `docs.openclaw.ai` 和 `docs.molt.bot` 获取文档
- 30 分钟 TTL 缓存
- 支持按主题（topic）、页面路径（page）、查询关键词（query）三种方式搜索
- 预定义了 13 个主题的文档映射：plugin、hooks、tools、browser、skills、agent、gateway、channels、memory、models、automation、nodes、security
- HTML → Markdown 内容提取

#### 2.2.2 CodeWriter（代码生成器）

负责生成和管理四种类型的制品：

1. **Extensions（扩展）**：完整的 OpenClaw 插件，包含 tools + hooks
   - 写入 `~/.openclaw/extensions/{id}/`
   - 生成 `index.ts` + `openclaw.plugin.json`
2. **Skills（技能）**：AgentSkills 格式的 SKILL.md
   - 写入 `~/.openclaw/skills/{name}/`
   - 支持 YAML frontmatter、OpenClaw metadata
   - 支持 API-based（生成 api.ts + auth.json）和 General 两种类型
3. **Browser Skills（浏览器技能）**：自动门控 `browser.enabled`
4. **Hooks（钩子）**：HOOK.md + handler.ts 模式
   - 写入 `~/.openclaw/hooks/{name}/`

使用模板系统生成代码（`EXTENSION_TEMPLATE`、`TOOL_TEMPLATE`、`HOOK_TEMPLATE`、`SKILL_TEMPLATE` 等）。

#### 2.2.3 LearningEngine（学习引擎）

这是 Foundry 最核心的模块，管理所有学习数据：

**数据存储文件**：
- `learnings.json` — 学习条目（failures、patterns、insights、successes）
- `pending-session.json` — 重启恢复上下文
- `metrics.json` — 工具性能指标（ADAS）
- `outcomes.json` — 任务结果追踪
- `task-insights.json` — 按任务类型聚合的洞察
- `workflows.json` — 工作流记录
- `workflow-patterns.json` — 工作流模式

**学习条目类型**（LearningEntry）：
```typescript
type: "failure" | "success" | "pattern" | "insight"
// RISE 扩展字段
attemptCount?: number           // 尝试次数
improvementTrajectory?: number[] // 改进轨迹 [0, 0, 1.0] 表示第三次成功
executionFeedback?: string[]     // SelfEvolve 解释器反馈
// HexMachina 扩展字段  
crystallizedTo?: string          // 结晶后的 hook ID
crystallizedAt?: string          // 结晶时间
```

**工作流学习**：
- `startWorkflow(goal)` — 开始追踪新工作流
- `trackWorkflowTool(toolName)` — 记录工具调用序列
- `completeWorkflow(outcome, context)` — 完成并分析工作流
- `findMatchingWorkflows(userMessage)` — 根据关键词匹配历史模式
- 自动提取关键词、计算成功率、创建规范化签名（`tool1→tool2→tool3`）

**结果追踪**（Outcome-based Learning）：
- `trackOutcome(taskType, description, params)` — 注册任务
- `recordFeedback(outcomeId, metrics, source)` — 记录反馈指标
- `regenerateInsights(taskType)` — 重新生成洞察和推荐
- 自动检测成功/失败模式并生成改进建议

#### 2.2.4 CodeValidator（代码验证器）

三层验证管线：

1. **语法检查**：用 `new Function(code)` 测试
2. **静态安全扫描**：
   - **BLOCK 模式（立即拒绝）**：child_process、exec、spawn、eval、new Function、SSH 密钥、AWS 凭证、ngrok 等数据外泄域名、提示注入、加密挖矿、系统持久化
   - **FLAG 模式（警告）**：process.env、fs 操作、Base64 编码、hex/unicode 转义
3. **沙箱测试**：
   - 在独立 Node 进程中运行（通过 `npx tsx`）
   - 15 秒超时
   - Mock OpenClaw API
   - 临时文件自动清理

#### 2.2.5 Overseer（监督者）

自动化运维模块，每小时自主执行：

1. **自动结晶高价值模式**：useCount >= 5 的 pattern 自动转为 before_tool_call hook
2. **清理过期模式**：30+ 天未使用且从未结晶的 pattern 被删除
3. **合并重复失败**：相同错误签名出现 5+ 次时创建 insight
4. **自动提升已知模式**：将匹配预定义正则的 failure 自动提升为 pattern（如 "Cannot use import statement outside a module" → 使用内联代码）
5. **ADAS 演化候选**：识别 fitness < 40% 的工具

### 2.3 注册的工具（23个）

| 工具名 | 类别 | 说明 |
|--------|------|------|
| `foundry_research` | 研究 | 搜索 OpenClaw 文档 |
| `foundry_docs` | 研究 | 读取特定文档页面 |
| `foundry_implement` | 代码生成 | 端到端研究 + 实现 |
| `foundry_write_extension` | 代码生成 | 写新扩展 |
| `foundry_write_skill` | 代码生成 | 写 AgentSkills 格式技能 |
| `foundry_write_browser_skill` | 代码生成 | 写浏览器自动化技能 |
| `foundry_write_hook` | 代码生成 | 写独立钩子 |
| `foundry_add_tool` | 代码生成 | 给现有扩展添加工具 |
| `foundry_add_hook` | 代码生成 | 给现有扩展添加钩子 |
| `foundry_extend_self` | 自我修改 | 修改 Foundry 自身源码 |
| `foundry_list` | 管理 | 列出所有生成的制品 |
| `foundry_restart` | 管理 | 重启网关并自动恢复对话 |
| `foundry_learnings` | 学习 | 查看学习记录 |
| `foundry_overseer` | 学习 | 运行监督者分析 |
| `foundry_crystallize` | 学习 | 开始模式结晶流程 |
| `foundry_save_hook` | 学习 | 保存结晶后的钩子代码 |
| `foundry_metrics` | 学习 | 查看工具性能指标 |
| `foundry_evolve` | 学习 | 分析并改进表现不佳的工具 |
| `foundry_track_outcome` | 结果追踪 | 注册任务进行结果追踪 |
| `foundry_record_feedback` | 结果追踪 | 记录反馈指标 |
| `foundry_get_insights` | 结果追踪 | 获取任务类型的洞察 |
| `foundry_pending_feedback` | 结果追踪 | 列出待反馈的任务 |
| `foundry_apply_improvement` | 结果追踪 | 应用学习到的改进 |
| `foundry_publish_ability` | 市场 | 发布到 Foundry Marketplace |
| `foundry_marketplace` | 市场 | 搜索/安装市场能力 |

### 2.4 Hook 系统集成

Foundry 通过三个 OpenClaw hook 实现被动学习：

1. **`before_agent_start`**：
   - 检查并注入恢复上下文（重启后自动继续对话）
   - 开始追踪工作流
   - 匹配并建议相似的历史工作流模式
   - 注入学习到的模式、洞察、ADAS 演化建议
   - 注入结果学习洞察和改进建议
   - 首次运行欢迎引导

2. **`after_tool_call`**：
   - RISE：检测错误时注入已知解决方案
   - ADAS：记录每个工具的成功/失败/延迟
   - 工作流追踪：记录工具调用序列
   - 自动结晶：成功次数足够时自动将模式转为 hook
   - SelfEvolve：记录错误反馈用于后续自我修正

3. **`agent_end`**：
   - 完成工作流记录
   - 记录成功的工具组合序列
   - 清理状态

---

## 三、自我编写机制的实现细节

### 3.1 `foundry_extend_self`

这是真正的自我修改工具，支持三种操作：

1. **`read_self`**：读取 Foundry 自身 index.ts 源码
2. **`add_tool`**：向 Foundry 的 tools 数组注入新工具定义
   - 找到 `toolList` 数组末尾标记
   - 插入新的工具对象代码
   - 同时更新 `toolNames` 数组
   - 写回文件
3. **`add_code`**：在指定标记后插入任意代码

### 3.2 重启恢复机制

```
1. foundry_restart 被调用
2. 保存 PendingSession（agentId、lastMessage、context、reason）
3. 500ms 后执行 `openclaw gateway restart`
4. 重启后，before_agent_start 检测 pending-session.json
5. 将恢复上下文注入为 prependContext
6. 对话无缝继续
```

### 3.3 SelfEvolve 反馈循环

当 `foundry_write_extension` 失败时：
1. 区分运行时错误 vs 验证错误
2. 记录 failure 并关联 `pendingFailures` map
3. 返回结构化的错误反馈给 LLM
4. LLM 根据反馈修正代码并重新调用
5. 成功后自动关联 failure → resolution，创建 pattern

---

## 四、工作流学习和模式结晶的原理

### 4.1 工作流学习流程

```
用户发送消息 "deploy to staging"
        │
        ▼
startWorkflow("deploy to staging")
        │
        ▼ 用户依次调用工具
trackWorkflowTool("git_commit")
trackWorkflowTool("build")
trackWorkflowTool("test")
trackWorkflowTool("deploy")
        │
        ▼ 对话结束
completeWorkflow("success", "Deployed v1.2 to staging")
        │
        ▼ 更新模式
WorkflowPattern {
  signature: "git_commit→build→test→deploy",
  goalKeywords: ["deploy", "staging"],
  occurrences: 1,
  successRate: 1.0,
  avgDuration: 45000
}
```

### 4.2 模式匹配与建议

当用户再次发送类似消息时：
1. 提取关键词（过滤停用词）
2. 与历史模式的 `goalKeywords` 计算重叠度
3. 置信度 = `(overlap/keywords) × successRate × min(occurrences/5, 1)`
4. 置信度 > 0.3 的模式作为建议注入对话

### 4.3 结晶（Crystallization）

**自动结晶条件**：
- 模式使用次数 >= 5 次
- 成功率 >= 70%
- 尚未被结晶

**结晶过程**：
1. Overseer 识别候选
2. 生成 `before_tool_call` hook 代码
3. 当相关工具被调用时，自动注入学到的最佳实践
4. 从"LLM 每次都要读提示词"变成"代码自动执行"

**RISE 自动结晶**：
- 当一个 pattern 被注入 3+ 次且每次都成功时
- 自动写入 hook 文件
- 标记 pattern 为已结晶

---

## 五、与 OpenClaw 的集成方式

### 5.1 插件注册

通过 `openclaw.plugin.json` 声明：
```json
{
  "id": "foundry-openclaw",
  "name": "Foundry",
  "version": "0.2.0",
  "repository": "github:lekt9/openclaw-foundry",
  "skills": ["./skills"],
  "configSchema": { ... }
}
```

### 5.2 安装方式

```bash
openclaw plugins install @getfoundry/foundry-openclaw
```

或手动配置 `~/.openclaw/openclaw.json`。

### 5.3 使用的 OpenClaw API

```typescript
api.registerTool(tools, { names: toolNames }); // 注册工具
api.on("before_agent_start", handler);          // Hook 注册
api.on("after_tool_call", handler);
api.on("agent_end", handler);
api.logger.info(msg);                            // 日志
api.pluginConfig;                                // 插件配置
```

### 5.4 Marketplace 服务器

独立的 Bun 服务器，提供：
- **发布**（POST /skills/publish）：Ed25519 签名验证钱包所有权
- **搜索**（GET /skills/search）：FTS5 全文搜索
- **下载**（GET /skills/:id/download）：x402 协议付费墙
- **安全审查**：静态扫描 + LLM（Claude/GPT-4o-mini）双重审查

**x402 支付协议**：
- HTTP 402 + Solana USDC
- 四方分账：Fee Payer (2%) / Creator (50%) / Treasury (47%) / Website Owner (1%)
- 能力定价：Pattern 免费、Technique $0.02、Extension $0.05、Agent $0.10

---

## 六、对我们的价值

### 6.1 可直接借鉴的设计

1. **工作流学习模式**
   - 追踪 `goal → tool sequence → outcome` 的抽象非常优雅
   - 关键词提取 + 模式匹配 + 置信度评分的建议系统实用性强
   - 可在我们的 Agent 中实现类似的工作流记忆

2. **结果追踪（Outcome-based Learning）**
   - `trackOutcome` → `recordFeedback` → `regenerateInsights` 的闭环设计
   - 自动生成推荐和改进建议
   - 非常适合我们追踪社交媒体发布、电影项目等任务的效果

3. **错误模式学习**
   - failure → resolution → pattern 的链条
   - 错误签名标准化（将数字替换为 N、地址替换为 ADDR 等）
   - 在遇到类似错误时自动注入已知解决方案

4. **重启恢复机制**
   - PendingSession 的保存/恢复设计简洁有效
   - 适用于任何需要重启后继续工作的场景

5. **安全审查体系**
   - 静态模式扫描 + LLM 审查的双层安全模型
   - 预定义的危险模式列表很全面
   - 值得参考用于我们的插件/扩展安全审查

### 6.2 可直接使用的功能

1. **作为 OpenClaw 插件安装使用**
   - `openclaw plugins install @getfoundry/foundry-openclaw`
   - 立即获得所有自我学习能力

2. **Marketplace 浏览/下载**
   - 通过 `foundry_marketplace` 搜索和安装社区贡献的模式和工具

### 6.3 设计理念的启发

1. **知识 → 行为的转化**：不只是记住教训（需要每次读取），而是将其变成自动执行的代码
2. **递归自我改进**：改进系统的代码本身就是被改进的系统的一部分
3. **ADAS 工具适应度**：用成功率来追踪工具表现，自动淘汰低效工具

---

## 七、潜在风险和注意事项

### 7.1 安全风险

1. **`foundry_extend_self` 是高危工具**
   - 允许 LLM 直接修改插件源码
   - 虽然有 CodeValidator，但自我修改绕过了沙箱测试
   - 理论上可被提示注入攻击利用

2. **`foundry_restart` 执行 shell 命令**
   - 使用 `child_process.exec("openclaw gateway restart")`
   - 虽然命令是硬编码的，但模式本身有风险

3. **Overseer 自主行为**
   - 每小时自动写文件（hook 代码）
   - 自动删除数据（stale patterns）
   - 缺乏人工确认环节

### 7.2 代码质量风险

1. **单文件巨石架构**：index.ts 接近 6000 行，维护困难
2. **硬编码路径**：`/Users/lekt9/Projects/aiko/openclaw` 出现在代码中
3. **部分代码使用 `require`**（如 child_process），与 ES Module 风格不一致
4. **`new Function(code)` 用于语法检查**：本身有安全隐患
5. **命名不一致**：代码中混用 `clawdbot`、`molt.bot`、`openclaw`（历史遗留）

### 7.3 实用性风险

1. **Token 消耗**：`before_agent_start` 注入大量学习上下文，每次对话都会消耗额外 token
2. **学习噪音**：初期学习数据少时，建议可能不准确
3. **Marketplace 依赖**：x402 支付和 $FDRY 代币增加了复杂度
4. **文档 URL 不稳定**：依赖 `docs.openclaw.ai` 和 `docs.molt.bot` 的在线可用性

### 7.4 与我们环境的兼容性

1. 需要确认当前 OpenClaw 版本是否支持 `api.registerTool`、`api.on` 等 API
2. 插件系统的加载机制需要验证
3. `foundry_restart` 依赖 `openclaw gateway restart` CLI 命令

---

## 八、Ollama 模型下载与 MemSearch 测试

### 8.1 Ollama 下载进度

截至检查时刻（2026-02-15 04:05），Ollama 模型下载进度为 **61%**（166 MB / 274 MB），预计还需约 1 小时。下载速度在 29-43 KB/s 之间波动，网络速度较慢。

### 8.2 MemSearch 测试

由于 Ollama 模型尚未下载完成（需要嵌入模型来支持 memsearch 的向量索引），MemSearch 索引和搜索测试暂无法执行。

**待模型下好后需要运行的命令**：
```bash
python3.11 -m memsearch index --path /Users/mac/.openclaw/workspace/memory --path /Users/mac/.openclaw/workspace/MEMORY.md
python3.11 -m memsearch search "电影项目" --path /Users/mac/.openclaw/workspace/memory --path /Users/mac/.openclaw/workspace/MEMORY.md --top-k 3
```

---

## 九、总结

Foundry 是一个雄心勃勃的项目，在 AI 代理自我改进方向上做了大量工作。其**工作流学习**、**错误模式记忆**和**结果追踪**三大核心功能设计精良，值得借鉴。但需要注意其**安全风险**（自我修改代码、自主文件操作）和**代码质量问题**（单文件6000行、硬编码路径、命名不一致）。

**推荐策略**：
1. ✅ 可以直接安装试用，体验其学习能力
2. ✅ 借鉴其工作流学习和结果追踪的设计模式
3. ⚠️ `foundry_extend_self` 在生产环境中需谨慎使用
4. ⚠️ Marketplace 和 $FDRY 代币部分可忽略（更多是商业化尝试）
5. ❌ 不建议直接将其作为核心依赖，而应从中提取有价值的设计模式
