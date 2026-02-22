
# 用户偏好记录 (Preferences)

**最后更新**: 2026-02-22

---

## 沟通风格
- **Style preference**: 正经 + 可爱 🐶
- **Wants me to be**: Bold and proactive
- **说话风格**: 简洁、直接、有价值，不啰嗦
- **Emoji**: 🐶 (Keonho 的标志)

---

## 话题关注点

### AI 资讯 (topic:2)
- **关注内容**: AI 热门日报、官方账号监控
- **任务**: task-twitter-001, task-twitter-002
- **关键词**: #OpenClaw, #AIagent, #AutonomousAgent, 最新 AI 趋势

### 广告创意 (topic:3)
- **关注内容**: 4A 广告视觉拆解、Seedance 案例
- **任务**: task-ad-visual-001, task-twitter-004
- **偏好**: 高质量创意、视觉分析

### 工作选品 (topic:4)
- **关注内容**: 泰区 TikTok 日报、产品选品
- **任务**: task-tiktok-th-001
- **类目**: 咖啡、厨房、家居、工具
- **市场**: 泰国 TikTok

### 工具追踪 (topic:5)
- **关注内容**: OpenClaw 话题、AI Agent 最新工具
- **任务**: task-twitter-003

### Simmer 交易 (topic:6)
- **关注内容**: Simmer 交易汇报、持仓监控
- **任务**: task-simmer-001
- **交易限制**: max $1 USDC/市场, 50笔/天, SL 20%, TP 15%
- **钱包地址**: 0x39e4BB0f4b14875AC85B74E5b844bcB092438c61
- **静默期**: 23:00-08:00 不推送（紧急亏损除外）

### 产品洞察 (topic:?)
- **状态**: 不需要推送日报

---

## 工作流程偏好

### 定时任务时间
| 时间 | 任务 | 发送至 |
|------|------|--------|
| 09:00 | AI 日报 | topic:2 |
| 09:30 | 4A 广告 | topic:3 |
| 10:00 | TikTok 泰区 | topic:4 |
| 18:00 | OpenClaw 话题 | topic:5 |
| 20:00 | Seedance 案例 | topic:3 |

### 群聊规则
- **被@或被问才回复**
- **能增加价值再说话**
- **人类规则**: 不回每条消息

---

## 工具和技术偏好

### 已创建的技能
- model-switcher (2026-02-15)
- simmer (2026-02-16)
- localhost-troubleshoot (2026-02-19)
- browser-watchdog (2026-02-19)
- x-mission-fetcher (2026-02-20)
- evomap (2026-02-20)
- browser-watchdog-pro (2026-02-21)
- gateway-watchdog (2026-02-21)
- cron-watchdog (2026-02-22)

### 已安装的插件
- foundry-openclaw (v0.2.3)
- google-antigravity-auth
- minimax-portal-auth
- qwen-portal-auth
- telegram

### 已启用的 hooks
- boot-md
- bootstrap-extra-files
- command-logger
- session-memory
- pdca-self-evolution-loop
- evaluation-optimizer
- browser-auto-retry

---

## 决策记录

### 重要决策
| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-02-15 | 安装 openclaw-mem skill | 解决 Discord context overflow 记忆丢失 |
| 2026-02-15 | 安装 openclaw-foundry 插件 (v0.2.3) | 自我编写元插件，观察工作流→学习→结晶 |
| 2026-02-15 | 放弃 Ollama，改用 local sentence-transformers | Ollama API 502 错误 |
| 2026-02-19 | httpx/requests 设置 trust_env=False | 防止 localhost 请求被 proxy 劫持 |

---

## 学习成果和最佳实践

### 技术教训
1. **OpenViking 调试**: httpx 默认走系统 proxy，需要禁用
2. **memsearch 向量搜索**: 使用 local provider 更稳定
3. **browser 自动化**: 已有 watchdog 技能，不需要结晶化

### Foundry 学习
- 9 个模式识别（1 个已结晶）
- 310+ 洞察
- 工具性能监控和优化

---

## 记住的规则（来自 Luna）
1. 任何长时间任务，完成后必须主动通知我
2. 做不到的事不要承诺，直接说做不到
3. 犯错了要说，不要假装没发生
4. 记忆要当下写入，不要等之后再记

---

*此文件记录用户的所有偏好，每次对话前读取，确保理解用户需求。*

