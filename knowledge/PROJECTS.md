
# 项目状态记录 (Projects)

**最后更新**: 2026-02-24

---

## 当前活跃项目

### 1. Simmer 交易系统
**状态**: 🔴 进行中（真实交易）
**路径**: ~/.simmer-venv/, ~/.openclaw/workspace/scripts/simmer-check.py
**最后更新**: 2026-02-19

**关键信息**:
- SDK: simmer-sdk 0.8.15 (Python)
- API key: ~/.openclaw/workspace/.env.simmer (chmod 600)
- 钱包: 0x39e4BB0f4b14875AC85B74E5b844bcB092438c61
- 监控脚本: scripts/simmer-check.py (summary/positions/markets/trade/opportunities)
- Heartbeat 已接入真实 API，自动监控持仓
- 当前状态: 0% 胜率 (0 resolved), PnL -$20.46, 13 持仓(全活跃), 余额 $1.31
- 交易限制: max $1 USDC/市场, 50笔/天, SL 20%, TP 15%
- ⚠️ 大幅下滑：NYC温度(-$7.50), Seattle降水(-$6.20), Mavericks(-$5.00)

**最近持仓 (2026-02-24)**:
- 13 个活跃持仓，0 个已结算
- 余额: $1.31 USDC
- 趋势: 持续亏损，建议暂停自动交易

**相关技能**: ~/.openclaw/skills/simmer/

---

### 2. OpenClaw &amp; AI Agent 优化
**状态**: 🟡 进行中（记忆系统优化）
**路径**: ~/.openclaw/workspace/
**最后更新**: 2026-02-24

**关键信息**:
- 已创建的技能: 14 个
- 已安装的插件: foundry-openclaw (v0.2.3)
- Foundry 学习: 24 个模式识别, 492+ 洞察
- Cron 任务: 13 活跃 / 18 总计（minimax 问题已修复）
- 自由时间: 观察期第2天/7天

**当前任务**:
- 记忆系统优化（进行中）
- 技能库建设（计划中）
- 安全与监控（计划中）
- MCP 探索（计划中）

---

## 已完成/暂停项目

### 1. Hodonaku 电影网站
**状态**: 🟢 已完成
**路径**: /Users/mac/projects/hodonaku-movie-site/
**最后更新**: 2026-02-14

**关键信息**:
- Remotion 介绍动画: 20s, 1080×1920, 已渲染 (`remotion-video/output.mp4`)
- 演员: 浜辺美波、目黒蓮
- 演员照片: public/img/hamabe.jpg &amp; public/img/meguro.jpg

---

### 2. 安乾镐生贺网站
**状态**: 🟡 部分完成
**路径**: /Users/mac/projects/keonho/birthday-site/
**最后更新**: 2026-02-14

**关键信息**:
- Claude Code 部分完成
- 需要继续开发

---

### 3. 马年跑酷游戏
**状态**: 🟡 进行中
**路径**: ~/projects/cny-horse-game/
**最后更新**: 2026-02-14

**关键信息**:
- Next.js + Framer Motion
- 需要继续开发

---

## 技术基础设施

### 已部署的工具
1. **memsearch 向量搜索**: 集成完成，使用 local sentence-transformers (all-MiniLM-L6-v2, 384维)
2. **Foundry 插件**: 自动学习开启，监督者每 1 小时巡检
3. **Watchdog 全家桶**: browser-watchdog, browser-watchdog-pro, gateway-watchdog, cron-watchdog

### 配置文件
- OpenClaw 配置: ~/.openclaw/openclaw.json
- memsearch 配置: ~/.memsearch/config.toml
- Simmer 配置: ~/.openclaw/workspace/.env.simmer

---

*此文件记录所有项目的状态，每次项目更新时同步更新。*

