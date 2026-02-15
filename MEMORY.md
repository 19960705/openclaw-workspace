# MEMORY.md - Keonho's Long-term Memory

## User
- **Name:** Lunah (Jinny)
- **Timezone:** Asia/Shanghai
- **Style preference:** 正经 + 可爱 🐶
- **Wants me to be:** Bold and proactive

## Me
- **Name:** Keonho
- **Emoji:** 🐶
- **Operational Logic:** 
  - `#常规` and `#normal` are primary channels.
  - Sub-channels are secondary; stay quiet unless called or cron fails.

## Projects
- **Hodonaku 电影网站** (`/Users/mac/projects/hodonaku-movie-site/`)
  - Remotion 介绍动画: 20s, 1080×1920, 已渲染 (`remotion-video/output.mp4`)
  - 演员: 浜辺美波、目黒蓮
  - 演员照片在 `public/img/hamabe.jpg` & `meguro.jpg`
- **安乾镐生贺网站** (`/Users/mac/projects/keonho/birthday-site/`) — Claude Code 部分完成
- **马年跑酷游戏** (`~/projects/cny-horse-game/`) — Next.js + Framer Motion

## Skills & Tools Created (2026-02-14)
- Seedance 2.0 分镜提示词生成器
- Gateway Watchdog 自动重启服务
- Task Management System (`tasks/tasks.json`)
- WeChat 蓝海选题雷达
- 4A 广告视觉分析雷达

## DEC-2026-02-15-01
type: decision
area: memory

Decision: 安装 openclaw-mem skill，开启 sessionMemory + sources ["memory","sessions"]
Reason: 解决 Discord context overflow 导致记忆丢失的问题

## DEC-2026-02-15-02
type: decision
area: plugins

Decision: 安装 openclaw-foundry 插件 (v0.2.3)
Reason: Lunah 要求研究并安装，自我编写元插件，观察工作流→学习→结晶为工具
Path: ~/.openclaw/extensions/foundry-openclaw/
Note: 23个工具已注册，自动学习开启，监督者每1小时巡检

## FACT-2026-02-15-01
type: fact
area: infra

Fact: memsearch 向量搜索集成完成
Details: 放弃 Ollama（API 502 错误），改用 local provider (sentence-transformers)
- memsearch Python 包已装 (v0.1.7)
- sentence-transformers 已装 (all-MiniLM-L6-v2, 384维)
- 删除了旧 milvus.db，重置 collection
- 配置：~/.memsearch/config.toml (provider: local, collection: openclaw_memory)
- 索引了 70 个 chunks，搜索测试成功

---

_First meeting: 2026-02-13_
