# 🤖 Keonho Agent Team

> Multi-Agent Team Configuration

## Agents

| Agent | ID | Model | Role |
|-------|-----|-------|------|
| **Keonho** | main | MiniMax M2.5 | Main - 总指挥 |
| **Code** | code-agent | Claude Sonnet 4.5 | 代码开发 |
| **Researcher** | researcher-agent | Claude Opus 4.6 | 深度调研 |
| **Archivist** | archivist-agent | Claude Sonnet 4.5 | 知识管理 |

## Usage

### 分配任务给子 Agent

```
/task @code-agent 帮我写一个 Python 脚本
/task @researcher 研究 Seedance API
/task @archivist 整理今天的知识笔记
```

### 直接 spawn

```
/spawn code-agent --task "修复 GitHub issue #123"
/spawn researcher-agent --task "调研 MCP 协议最新动态"
```

## 配置

- Main: ~/.openclaw/workspace/
- Code: ~/.openclaw/agents/code-agent/
- Researcher: ~/.openclaw/agents/researcher-agent/
- Archivist: ~/.openclaw/agents/archivist-agent/

## 共享能力

### 自质疑模式 (Self-Questioning)
所有 agent 执行重要操作前需自问：
- 🤔 确定要执行吗？可逆吗？
- 🤔 有更安全的方式吗？
- 🤔 符合核心价值观吗？

完成后反思：
- ✅ 结果符合预期吗？
- ✅ 学到了什么？

---

## ContentFactory 共享知识库

所有 Agent 通过软链接共享 ContentFactory 知识库：

- **物理路径**：`~/Documents/Obsidian Vault/Keonho/ContentFactory`
- **软链接**：`~/.openclaw/workspace/ContentFactory`
- **操作工具**：obsidian-cli（严禁使用 mv/rm）
- **元数据规范**：所有文件必须包含 YAML 头部
- **配置文件**：SOUL.md / USER.md / SOP_CONTENT.md

### Agent 分工

- **Keonho (主)**：总指挥、内容审核、选题确认、终稿把关、发布决策
- **Researcher**：素材收集、趋势研究、抓取爆款、分析趋势、竞品调研
- **Code**：工具开发、技术教程、AI 工具评测、代码示例、技术文档
- **Archivist**：知识整理、归档管理、标签管理、知识图谱、数据清理
