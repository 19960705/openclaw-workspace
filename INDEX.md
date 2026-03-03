# INDEX.md - 知识导航

> Last updated: 2026-03-02
> Agent: Keonho

## 📊 健康度总览

| 类别 | 数量 | 状态 |
|------|------|------|
| 项目 (projects/) | 2 | ✅ 活跃 |
| 技能 (skills/) | 20+ | ✅ 活跃 |
| 日志 (memory/) | 14天 | ✅ 正常 |
| 知识 (knowledge/) | 40+ | ✅ 正常（新增 lessons/） |

---

## 🗂️ 目录结构

```
workspace/
├── memory/              # 日志层 (事件流水)
│   ├── YYYY-MM-DD.md   # 每日对话
│   └── todos.md        # 待办 (NOW)
├── knowledge/           # 知识层 (提炼后)
│   ├── lessons/         # 经验教训（已启用）
│   ├── decisions/       # 决策记录
│   ├── projects/        # 项目文档
│   └── ai-projects/     # AI 项目研究
├── skills/             # 技能库
├── scripts/            # 自动化脚本
└── docs/               # 文档
```

---

## 🔥 优先级知识

### 高优先级 (高频使用)
- `knowledge/lessons/openclaw-recurring-failures.md` - OpenClaw 高频故障解决套路（待 crystallize）
- `knowledge/seedance-2.0-latest.md` - Seedance 2.0 最新技巧
- `knowledge/thai-tiktok-ad-templates.md` - 泰区 TikTok 广告模板
- `knowledge/github-copilot-memory-system.md` - GitHub Copilot 记忆系统 (新增)
- `knowledge/openclaw-v2026.2.25.md` - OpenClaw v2.25 更新 (新增)
- `knowledge/mcp-2026.md` - Model Context Protocol (新增)
- `knowledge/ai-video-tools-comparison-2026.md` - AI 视频工具对比 (新增)
- `skills/simmer/` - Simmer 交易策略

### 中优先级 (定期更新)
- `knowledge/ai-trends-feb-2026-week4.md` - AI 趋势周报
- `knowledge/ai-video-tools-comparison-2026.md` - AI 视频工具对比

### 待验证 (超过30天)
- `knowledge/naval-blog.md` - Naval 博客笔记

---

## ⚙️ 系统配置

| 组件 | 状态 | 备注 |
|------|------|------|
| Gateway | ✅ 正常 | 需监控 token |
| Browser | ✅ 正常 | |
| Cron 任务 | ⚠️ 3个失败 | 需修复 |
| Simmer | 🔴 暂停 | PnL 负 |

---

## 📝 最近操作

- 2026-03-02: 新增 `knowledge/lessons/openclaw-recurring-failures.md`（为 crystallize 准备）
- 2026-03-02: 写入 `memory/2026-03-02-summary.md`
- 2026-02-28: 夜间反思 cron 执行
- 2026-02-27: 添加 gateway-watchdog cron (每2小时)
- 2026-02-27: 添加 daily-workflow cron (每日23:00)
- 2026-02-27: 安装 capability-evolver, self-evolve

---

*自动生成，每日晚间反思更新*
