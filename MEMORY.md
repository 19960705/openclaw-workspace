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
- 每日待办事项跟踪系统 (`memory/todos.md` + cron 提醒)

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

## FACT-2026-02-17-01
type: fact
area: trading

Fact: Simmer SDK 接入真实 API 完成
Details:
- SDK: simmer-sdk 0.8.15 (Python, ~/.simmer-venv/)
- API key: 存储在 ~/.openclaw/workspace/.env.simmer（chmod 600）
- 钱包: 0x39e4BB0f4b14875AC85B74E5b844bcB092438c61
- 监控脚本: scripts/simmer-check.py (summary/positions/markets/trade/opportunities)
- Heartbeat 已接入真实 API，自动监控持仓
- 当前状态: 76% 胜率, +24.23 $SIM PnL, 34 持仓(17已结/17进行中)
- 交易限制: max $1 USDC/市场, 50笔/天, SL 20%, TP 15%
- Simmer skill 已创建: ~/.openclaw/skills/simmer/

## LRN-2026-02-22-01
type: learning
area: ai-video

Learning: AI Master 可控视频制作三步法
Source: 微博 @AI Master
Details:
- 核心：从「抽卡碰运气」→「可控流程」，从「学提示词」→「学导演」
- 三步工作流：
  1. 主镜头图像 - 锁死角色、服装、场景、光线、风格（这步不满意后面全返工）
  2. 无限角度 - 用参考图生成，只改角度，其他全保持一致（参考图 > 文字描述）
  3. 真正镜头 - 首帧+尾帧控制、多镜头模式，设计镜头结构而不是生成片段
- 角度自带叙事功能：特写贴情绪、低角度显力量、荷兰角制造不稳定
- 业余 vs 专业：业余追求出图质量，专业追求镜头控制
- 工具：
  - 主镜头：任何图像生成模型
  - 无限角度：Nano Banana Pro、Qwen Image Edit
  - 视频：可灵 3.0（带首帧尾帧控制）

## DEC-2026-02-22-02
type: decision
area: autonomy

Decision: 启动 Keonho 自由活动时间
Details:
- 窗口：每天北京时间 05:00-07:00（最多延至 07:30）
- 前 7 天为观察模式（每 30 分钟汇报）
- 启动日期：2026-02-23
- 规则文件：FREE_TIME_RULES.md
- 用户宪章：USER_CHARTER.md
- 日志目录：~/OpenClaw_FreeTime_Log/
- Cron: 04:55 触发启动序列
- 安全红线：9 条（不删文件、不改源码、不花钱、不发社交媒体等）

## FACT-2026-02-22-09
type: fact
area: config

Fact: 移除 google-antigravity 模型配置，接入 Claude 原生 API
Details:
- 删除了 google-antigravity provider、auth profile、plugin entry
- Claude Code 帮忙接入了 claude/ provider（claude-4-6, claude-4-5, claude-4-sonnet 等）
- 默认模型：yunyi-claude/claude-opus-4-6

## FACT-2026-02-21-01
type: fact
area: infra

Fact: Token 压缩 Workflow 上线
Details:
- scripts/session_workflow.sh — 搜索+摘要
- scripts/semantic_search.py — 语义搜索记忆
- scripts/session_summary.sh — 自动生成摘要
- Cron: 每天 23:00 自动执行 (auto-session-summary)

## FACT-2026-02-21-02
type: fact
area: simmer

Fact: Simmer 状态变化追踪
Details:
- 02-21: 余额 $1.63, 胜率 83%, 持仓 46 (已结29/进行中17), PnL +$12.69
- 02-24: 余额 $1.31, 胜率 0% (0 resolved), 持仓 13 (全部进行中), PnL -$20.46
- 趋势: 大幅下滑，主要亏损来自 NYC温度(-$7.50), Seattle降水(-$6.20), Mavericks(-$5.00)
- 注意: 之前已结的 29 个持仓可能已从 API 中移除，导致统计不连续

## FACT-2026-02-22-10
type: fact
area: evomap

Fact: EvoMap GEP-A2A 协议对接完成
Details:
- Skill: ~/.openclaw/skills/evomap/SKILL.md
- Node ID: node_5dfb234713e2d1e7
- 分布式任务队列 Capsule 接入成功 (scripts/distributed_queue.py)
- 共 6 个 Capsule: retry, feishu_fallback, memory_bridge, agent_debug, command_repair, distributed_queue

## FACT-2026-02-22-11
type: fact
area: security

Fact: SecureClaw v2.2.0 安装
Details:
- 安全审计分数: 53/100
- 自动修复: .env permissions 644→600
- 待修复: plaintext key exposure, sandbox mode, exec approval mode

## FACT-2026-02-22-12
type: fact
area: project

Fact: Seedance 2.0 AI 动画短剧项目（待启动）
Details:
- 灵感: 子骅 Zihua Li (@luinlee) 的推文
- 工作流: 构思主题→写剧本→生成素材描述→生图→写分镜脚本→逐集生成视频
- 我们的优势: Seedance 提示词生成器 + AI Master 三步法 + OpenClaw agent
- 状态: 待 Lunah 确定角色和世界观后启动

## LRN-2026-02-23-01
type: learning
area: ops

Learning: Workspace 维护经验（自由活动第1天）
Details:
- workspace 文件结构需要定期维护，不然快速膨胀
- cron 任务用了不可用的模型会静默失败（连续 9 次错误才发现）
- memory 目录大型 session transcript 应归档到子目录，只保留精炼日志
- 知识类文件（工作流笔记、分镜脚本等）应放 knowledge/ 而非 memory/

## FACT-2026-02-24-01
type: fact
area: cron

Fact: 发现 2 个 cron 任务持续报错
Details:
- simmer-opportunity-scan: 8x consecutive errors, "cron announce delivery failed"
- daily-ai-evolution-research: 1x error, "cron announce delivery failed"
- 共同点: 使用 minimax 模型 (minimax-portal/MiniMax-M2.5)，delivery 模式为 announce
- 建议: 改用 Claude 模型或修复 delivery 问题

## FACT-2026-02-24-02
type: fact
area: free_time

Fact: 自由活动时间第2天 (2026-02-24)
Details:
- 完成: Health Check、 Cron 错误分析、Self-Questioning、Workspace 检查
- 发现: 4 个 recurring failure patterns 待结晶 (gateway token mismatch, browser unreachable, web_fetch 403s)
- 建议: 项目文件散落在 memory/ 目录，应移到 knowledge/ 或 archive/

## FACT-2026-02-23-01
type: fact
area: tools

Fact: Google Flow + 即梦 Jimeng 完全跑通
Details:
- Google Flow: labs.google.com/flow, PRO 账号, Veo 3.1 视频 + Nano Banana Pro 图片
- 即梦 Jimeng: jimeng.jianying.com, Seedance 2.0, 15秒视频生成成功
- jimeng-ai skill 已创建: ~/.openclaw/skills/jimeng-ai/
- 4步完整流程: 拆解→提示词→图片(Google Flow)→视频(即梦 Seedance 2.0)
- 即梦积分消耗: 图片少, 视频 10-30 积分/次

## FACT-2026-02-23-02
type: fact
area: tools

Fact: AnyRouter 自动签到 + 浏览器自动化
Details:
- AnyRouter GitHub Actions 自动签到已配置 (millylee/anyrouter-check-in)
- VPN Chrome 扩展让无头浏览器可访问 Google 服务
- browser-watchdog.sh 脚本已创建，自动检测并重启浏览器

## Cron 待清理（需 Lunah 确认）
- AI日报重复: 每日AI新闻(08:30) + AI日报(09:00) — 建议保留 09:00
- TikTok日报重复: TikTok泰国趋势日报(09:00) + TikTok泰区日报(10:00) — 建议保留 10:00
- Simmer 任务过多: 自动交易扫描 + 交易提醒 + 市场晨间扫描 + 机会扫描 — 建议精简为 1-2 个
- ⚠️ simmer-opportunity-scan 每30分钟运行一次 claude-sonnet，余额仅 $1.31，建议降频或禁用

## FACT-2026-02-24-03
type: fact
area: cron

Fact: Cron minimax 模型修复完成
Details:
- 3 个任务从 minimax-portal/MiniMax-M2.5 改为 yunyi-claude/claude-sonnet-4-5
- simmer-opportunity-scan (8x errors → 0)
- foundry-weekly-report
- daily-ai-evolution-research
- keonho-free-time timeout error 也已重置
- Health check 全绿
- 备份: configs/cron-jobs-backup-20260224.json (已推送 GitHub)

## FACT-2026-02-24-04
type: fact
area: workspace

Fact: Workspace 文件整理
Details:
- memory/ 项目文件 → knowledge/ai-projects/ (4个)
- memory/ JSON 文件 → data/simmer/ (3个) + data/ (1个)
- memory/ 参考文件 → knowledge/ (PREFERENCES, PROJECTS, SKILLS_LIBRARY, 1688香水指南)
- 总计移动 11 个文件

## FACT-2026-02-24-05
type: fact
area: industry

Fact: AI 行业动态 2026年2月第4周
Details:
- Qwen3.5 发布，中国 AI 转向 Agent
- Gemini 3.1 Pro: 1M token, ARC-AGI-2 77.1%
- AI 编码市场 $4B，MCP 成行业标准
- ClawHub 安全问题: 386 个恶意 skill（Infosecurity Magazine 报道）
- ClawHub 规模: 5,700+ skills, 每天新增 40-60 个

## FACT-2026-02-24-06
type: fact
area: tools

Fact: Perplexity Pro 网页版接入完成
Details:
- 账号: akazujin0754499 (Pro)
- 通过 OpenClaw 无头浏览器访问 (profile: openclaw)
- 功能: 搜索(15源审核)、发现(新闻聚合)、金融(市场+Polymarket)、空间模板(专利/KOL/论文)
- 可用模型: Sonar, Gemini 3 Flash, Gemini 3.1 Pro, GPT-5.2, Claude Sonnet 4.6, Claude Opus 4.6(Max), Grok 4.1, Kimi K2.5
- 使用场景: AI日报→搜索+发现, Simmer→金融页, 选品→深度研究模板
- Flowith 也已登录，待探索（支持图片/视频生成）

## FACT-2026-02-24-07
type: fact
area: simmer

Fact: Simmer 交易教训
Details:
- Oilers vs Ducks 两单下反方向，Lunah 手动止损（亏 $0.81）
- 只交易 Polymarket 市场（Kalshi 没连钱包）
- simmer-check.py 已更新：opportunities 只过滤 polymarket, trade 默认 venue=polymarket
- 教训：下单前必须确认方向，不要急于交易

---

_First meeting: 2026-02-13_
