# Twitter API Alternatives 对比 - 2026

> 研究日期: 2026-03-06
> 背景: TuriX Screen Recording 权限问题，寻找无需浏览器的 Twitter 抓取方案

## 方案对比

| 方案 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| **Agent Reach** | ✅ 专用 CLI，稳定<br>✅ 无需浏览器权限<br>✅ 支持多平台（13个渠道）<br>✅ 已安装 | ⚠️ 需要 xreach-cli 配置 | **推荐** - 定时任务、自动化 |
| **Nitter** | ✅ 无广告<br>✅ 无反爬<br>✅ 免费 | ❌ 实例不稳定<br>❌ 部分功能受限 | 临时查看、备选方案 |
| **vxtwitter/fxtwitter** | ✅ 简单<br>✅ 返回 JSON | ❌ 单条推文<br>❌ 无搜索功能 | 单条推文抓取 |
| **Xpoz MCP** | ✅ MCP 集成<br>✅ 功能完整 | ⚠️ 需要配置<br>⚠️ 可能有费用 | 深度集成场景 |
| **Brave Search** | ✅ 已配置<br>✅ 免费 | ❌ 搜索结果有限<br>❌ 非实时 | 话题搜索、趋势发现 |
| **TuriX (浏览器)** | ✅ 功能最全<br>✅ 可视化 | ❌ 需要 Screen Recording<br>❌ 权限复杂<br>❌ 不稳定 | 交互式操作、调试 |

## 最终选择: Agent Reach

### 实现方案
```bash
# 搜索 AI 相关推文
agent-reach search twitter "AI OR Claude OR OpenAI" --limit 20

# 输出为 JSON
agent-reach search twitter "AI" --format json > tweets.json
```

### 优势
1. **无需浏览器权限** - 纯 CLI 工具
2. **稳定可靠** - 专用工具，不依赖浏览器状态
3. **易于集成** - 直接在 shell 脚本中调用
4. **多平台支持** - 可扩展到其他社交媒体

### 部署
- 脚本: `~/.openclaw/workspace/scripts/ai-twitter-digest-v2.sh`
- LaunchAgent: 已更新配置
- 测试: 2026-03-06 成功推送到 Telegram topic:2

## 经验教训

1. **浏览器自动化不是唯一选择** - 专用 CLI 工具往往更稳定
2. **权限问题优先考虑绕过** - 而不是深入解决（除非必要）
3. **工具选择看场景** - 定时任务用 CLI，交互式用浏览器

## 相关文档

- `/tmp/twitter_alternatives.md` - 详细对比
- `~/OpenClaw_Adventure_Log/2026-03-06.md` - 探险日志
- `~/.openclaw/skills/agent-reach/SKILL.md` - Agent Reach 使用指南

---

*探险 C 产出 - 2026-03-06*
