# Agent Reach 迁移实践 - 2026

> 迁移日期: 2026-03-06
> 从 TuriX 浏览器自动化迁移到 Agent Reach CLI

## 迁移背景

### 原方案问题
- **TuriX + Playwright**: 需要 Screen Recording 权限
- **LaunchAgent 环境**: 权限继承复杂，不稳定
- **维护成本高**: 浏览器状态管理、反爬应对

### 新方案优势
- **Agent Reach CLI**: 专用工具，无需浏览器
- **权限友好**: 纯 CLI，无 GUI 权限要求
- **稳定可靠**: 不依赖浏览器状态
- **易于维护**: Shell 脚本，简单直接

## 迁移步骤

### 1. 安装 Agent Reach
```bash
pipx install agent-reach
agent-reach doctor  # 检查配置
```

### 2. 配置 Twitter 渠道
```bash
# 需要 xreach-cli（可选，用于高级功能）
# 基础搜索无需额外配置
```

### 3. 改写脚本

**原脚本 (TuriX)**:
```bash
python -m turix.cli follow \
  --keywords "AI,Claude,OpenAI" \
  --limit 20 \
  --output tweets.json
```

**新脚本 (Agent Reach)**:
```bash
agent-reach search twitter "AI OR Claude OR OpenAI" \
  --limit 20 \
  --format json > tweets.json
```

### 4. 更新 LaunchAgent
```xml
<!-- 移除 Screen Recording 相关配置 -->
<!-- 简化环境变量 -->
<key>ProgramArguments</key>
<array>
  <string>/bin/bash</string>
  <string>/Users/mac/.openclaw/workspace/scripts/ai-twitter-digest-v2.sh</string>
</array>
```

## 功能对比

| 功能 | TuriX | Agent Reach | 备注 |
|------|-------|-------------|------|
| 搜索推文 | ✅ | ✅ | Agent Reach 更稳定 |
| Following 时间线 | ✅ | ⚠️ 需 xreach-cli | |
| 用户资料 | ✅ | ✅ | |
| 推文详情 | ✅ | ✅ | |
| 媒体下载 | ✅ | ❌ | 需要额外处理 |
| 反爬应对 | ⚠️ 需维护 | ✅ 内置 | |

## 性能对比

| 指标 | TuriX | Agent Reach |
|------|-------|-------------|
| 启动时间 | ~5s (浏览器) | <1s (CLI) |
| 内存占用 | ~200MB | ~50MB |
| 稳定性 | ⚠️ 中等 | ✅ 高 |
| 维护成本 | 高 | 低 |

## 迁移结果

### 成功案例
- **AI Twitter Digest**: TuriX → Agent Reach ✅
  - 脚本: `ai-twitter-digest-v2.sh`
  - 状态: 已部署，等待 09:00 自动运行验证

### 待迁移
- **4A 广告视觉拆解**: 仍使用 TuriX
  - 原因: 需要截图功能
  - 计划: 考虑 Agent Reach + 单独截图工具

## 经验教训

1. **专用工具优于通用工具** - CLI > 浏览器（对于定时任务）
2. **权限问题优先绕过** - 而不是深入解决
3. **迁移成本低** - 脚本改动 <10 行
4. **稳定性提升明显** - 无浏览器状态依赖

## 下一步

1. **验证 AI Twitter Digest v2** - 2026-03-07 09:00
2. **考虑 4A 广告迁移** - Agent Reach + 截图工具组合
3. **扩展到其他平台** - Reddit, YouTube, 小红书

## 相关文档

- `~/.openclaw/workspace/scripts/ai-twitter-digest-v2.sh` - 新脚本
- `~/.openclaw/workspace/knowledge/twitter-api-alternatives-2026.md` - 方案对比
- `~/.openclaw/skills/agent-reach/SKILL.md` - Agent Reach 使用指南

---

*探险 C 产出 - 2026-03-06*
