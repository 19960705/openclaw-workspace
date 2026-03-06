# INDEX.md - 知识导航

> Last updated: 2026-03-06
> Agent: Keonho

## 📊 健康度总览

| 类别 | 数量 | 状态 |
|------|------|------|
| 项目 (projects/) | 2 | ✅ 活跃 |
| 技能 (skills/) | 20+ | ✅ 活跃（Agent Reach v1.3.0） |
| 日志 (memory/) | 6天（3月） | ✅ 正常 |
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
- `knowledge/lessons/turix-screen-recording-permission-2026.md` - TuriX Screen Recording 权限研究（探险 A）
- `knowledge/lessons/agent-reach-migration-2026.md` - Agent Reach 迁移实践（探险 C）
- `knowledge/twitter-api-alternatives-2026.md` - Twitter API alternatives 对比
- `knowledge/seedance-2.0-latest.md` - Seedance 2.0 最新技巧
- `knowledge/thai-tiktok-ad-templates.md` - 泰区 TikTok 广告模板
- `knowledge/github-copilot-memory-system.md` - GitHub Copilot 记忆系统
- `knowledge/openclaw-v2026.2.25.md` - OpenClaw v2.25 更新
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

- 2026-03-06: Agent Reach 更新（v1.0.0 → v1.3.0）
- 2026-03-06: Feishu 插件更新（2026.2.25 → 2026.3.2）
- 2026-03-06: 部署 ai-twitter-digest-v2.sh（Agent Reach 方案）
- 2026-03-06: 全局模型切换（yunyi-claude/claude-sonnet-4-5）
- 2026-03-06: 探险活动 +100 点（Lv.1 → Lv.2）
- 2026-03-02: 新增 `knowledge/lessons/openclaw-recurring-failures.md`（为 crystallize 准备）
- 2026-02-27: 添加 gateway-watchdog cron (每2小时)

---

*自动生成，每日晚间反思更新*
