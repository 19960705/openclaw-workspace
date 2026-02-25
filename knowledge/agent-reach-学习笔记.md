# Agent Reach — 学习笔记

> 来源：@Neo_Reidlab (X/Twitter)
> 仓库：github.com/Panniantong/Agent-Reach
> 学习时间：2026-02-25

---

## 核心理念

**一句话给 AI Agent 装上全网搜索能力。**

痛点：每个平台都有门槛（付费API、反爬、登录、数据清洗），一个个配太麻烦。
Agent Reach 把选型和配置全做完了，是一个"脚手架"而非框架。

---

## 支持平台

| 平台 | 装好即用 | 配置后解锁 | 底层工具 |
|------|---------|-----------|---------|
| 🌐 网页 | 阅读任意网页 | — | Jina Reader |
| 📺 YouTube | 字幕提取+搜索 | — | yt-dlp |
| 📡 RSS | 阅读任意源 | — | feedparser |
| 🔍 全网搜索 | — | 语义搜索 | Exa (MCP, 免费) |
| 📦 GitHub | 公开仓库+搜索 | 私有仓库/Issue/PR | gh CLI |
| 🐦 Twitter/X | 读单条推文 | 搜索/时间线/发推 | bird (Cookie) |
| 📺 B站 | 字幕提取+搜索 | 服务器也能用 | yt-dlp |
| 📖 Reddit | 搜索(Exa) | 读帖子和评论 | JSON API + Exa |
| 📕 小红书 | — | 阅读/搜索/发帖 | xiaohongshu-mcp (Docker) |

## 技术选型亮点

- **Jina Reader** — 读网页（我们刚装了！）
- **bird** — 读推特，Cookie 登录免费（官方 API 读一条 $0.005）
- **yt-dlp** — 148K Star，YouTube+B站+1800站通吃
- **Exa** — AI 语义搜索，MCP 接入免 Key
- **mcporter** — MCP 工具桥接

## 设计理念

- 每个渠道可插拔（独立 Python 文件，统一接口）
- 底层工具随时可换
- `agent-reach doctor` 一条命令检测所有渠道状态
- 兼容所有 Agent（Claude Code、OpenClaw、Cursor 等）

---

## 💡 我们的对比

### 已有的
- ✅ Jina Reader（刚装）
- ✅ Brave Search
- ✅ web_fetch
- ✅ GitHub (gh CLI)
- ✅ 浏览器自动化

### Agent Reach 能补充的
- ⭐ bird (Twitter/X) — 比 Nitter 更强，能搜索和发推
- ⭐ yt-dlp (YouTube/B站) — 字幕提取，视频内容理解
- ⭐ Exa 语义搜索 — AI 原生搜索，比关键词搜索更精准
- ⭐ 小红书 MCP — 阅读/搜索/发帖
- ⭐ RSS 订阅 — feedparser

## ⭐ 行动建议

1. [ ] 安装 Agent Reach（一句话安装）
2. [ ] 配置 bird (Twitter Cookie) — 替代 Nitter
3. [ ] 配置 yt-dlp — YouTube/B站字幕提取
4. [ ] 考虑 Exa 语义搜索 — 补充 Brave Search

---

_学习笔记 by Keonho 🐶_
