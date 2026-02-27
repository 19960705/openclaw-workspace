# 🤖 Keonho 多 Agent 团队架构

> 基于 OpenClaw 多 Agent 架构实战 (香蕉Banana)
> 创建日期: 2026-02-27

---

## 1. 团队成员

| Agent | 角色 | 模型 | 描述 |
|-------|------|------|------|
| **Keonho** | Main (卡卡西) | Claude Sonnet | 总指挥、任务调度、验收 |
| **Code** | 鸣人 | GPT-5.3 Codex | 代码开发、Bug修复 |
| **Researcher** | 佐助 | Claude Opus 4.6 | 深度调研、分析 |
| **Archivist** | 小樱 | Claude Sonnet | 知识管理、文档整理 |

---

## 2. 协作协议

### 2.1 沟通规则

| 规则 | 说明 |
|------|------|
| **唯一沟通枢纽** | 所有对外沟通必须经过 Main |
| **不直接@用户** | 执行 Agent 永远不直接 @ 用户 |
| **任务完成后@Main** | 执行 Agent 完成任务后 @Main 请求验收 |
| **Main 决定通知用户** | 只有 Main 可以决定是否通知用户 |

### 2.2 任务分配流程

```
用户需求 → Main 评估
    ↓
[简单任务] → Main 直接处理
[单人任务] → 分配给对应 Agent，给方向
[复杂任务] → 拉团队讨论，逐个召集
```

### 2.3 紧急情况

可以直接 @Main + 用户的情况：
- 🚨 系统故障/安全问题
- 🚨 需要用户立即决策
- 🚨 Main 超过 2小时未响应且任务紧急

---

## 3. Skills 分配

### Main Agent (Keonho)
```
skills:
  - kanban-team      # 看板管理
  - telegram         # Telegram 基础操作
  - github           # GitHub 查看状态
  - heartbeat        # 心跳监控
  - self-improvement # 自我改进
```

### Code Agent
```
skills:
  - brainstorming      # 需求分析
  - writing-plans     # 编写计划
  - executing-plans   # 执行计划
  - github            # GitHub 操作
  - browser-use       # 浏览器自动化
  - context7          # 技术文档查询
  - code-mentor       # 代码指导
```

### Researcher Agent
```
skills:
  - tavily-search       # AI 搜索
  - context7            # 技术文档
  - github              # GitHub 调研
  - browser-use         # 网页抓取
  - twitter-search      # Twitter 搜索
  - exa-web-search-free # 搜索
  - newsnow             # 新闻聚合
```

### Archivist Agent
```
skills:
  - obsidian           # Obsidian 操作
  - memory             # 记忆管理
  - knowledge          # 知识库
  - wechat-gzh         # 微信公众号
  - youtube-transcript # YouTube 转录
  - notebooklm         # 内容生成
```

---

## 4. Heartbeat 监控

### Main Agent Heartbeat (每30分钟)

```
优先级检查清单：
1. No tags → 读取 + 分配 + 添加 TODO 标签
2. Review → 验证并关闭
3. Blocked → 帮助解决
4. In Progress >48h → 检查进度
5. TODO >24h → 催促或重新分配
```

### 返回规则
- 有任务需要处理 → 返回任务列表
- 无任务 → 返回 HEARTBEAT_OK（静默模式）

---

## 5. 实施计划

### Phase 1: 创建子 Agents
- [ ] 创建 Code Agent
- [ ] 创建 Researcher Agent  
- [ ] 创建 Archivist Agent

### Phase 2: 配置 Skills
- [ ] 为每个 Agent 分配对应 Skills
- [ ] 测试 Skills 可用性

### Phase 3: 配置 Heartbeat
- [ ] 配置 Main Agent Heartbeat
- [ ] 配置任务看板（Discord/Telegram）

### Phase 4: 测试协作
- [ ] 简单任务测试
- [ ] 复杂任务测试
- [ ] 紧急情况测试

---

## 6. 参考资料

- 来源: https://x.com/treydtw/status/2026956167864586424
- 作者: 香蕉Banana (@treydtw)
- 标题: 从零设计一个 AI 团队：OpenClaw 多 Agent 架构实战
