# TuriX Screen Recording 权限研究 - 2026

> 研究日期: 2026-03-06
> 背景: AI Twitter Digest 和 4A 广告视觉拆解脚本在 LaunchAgent 中因权限失败

## 问题描述

### 症状
```
2026-03-06 17:25:00 [ERROR] Screen recording permission denied
Quartz.CGPreflightScreenCaptureAccess() returns False
```

### 环境
- **系统**: macOS (Darwin 25.3.0)
- **Python**: miniconda3/envs/turix_env
- **执行方式**: LaunchAgent (com.keonho.ai-twitter-digest.plist)
- **权限状态**: Terminal 已授权 Screen Recording

## 权限机制研究

### macOS TCC (Transparency, Consent, and Control)

1. **权限授予对象**: 可执行文件（不是脚本）
   - Terminal.app ✅
   - Python 可执行文件 ⚠️
   - Shell 脚本 ❌

2. **LaunchAgent 权限继承**:
   - ❌ 不继承 Terminal 的 TCC 权限
   - ✅ 需要为 Python 可执行文件单独授权
   - ⚠️ 或使用 AppleScript/Automator 作为中间层

3. **权限生效时机**:
   - 授权后需要重启应用
   - Terminal 需要完全退出并重新打开
   - LaunchAgent 需要 unload/load

## 解决方案对比

| 方案 | 优势 | 劣势 | 推荐度 |
|------|------|------|--------|
| **为 Python 授权** | ✅ 彻底解决<br>✅ LaunchAgent 可用 | ❌ 需要手动添加<br>❌ Python 更新后失效 | ⭐⭐⭐ |
| **AppleScript 中间层** | ✅ 继承 Terminal 权限<br>✅ 稳定 | ❌ 增加复杂度<br>❌ 调试困难 | ⭐⭐ |
| **Automator 包装** | ✅ GUI 友好<br>✅ 权限管理简单 | ❌ 性能开销<br>❌ 不适合 CLI | ⭐ |
| **绕过浏览器方案** | ✅ 无需权限<br>✅ 更稳定<br>✅ 易维护 | ⚠️ 需要替代工具 | ⭐⭐⭐⭐⭐ |

## 最终选择: 绕过浏览器（Agent Reach）

### 原因
1. **权限问题根本解决** - 不依赖 Screen Recording
2. **更稳定** - 专用 CLI 工具，无浏览器状态依赖
3. **易维护** - 纯 shell 脚本，无复杂权限配置
4. **可扩展** - 支持多平台（Twitter, Reddit, YouTube 等）

### 实现
- 工具: Agent Reach CLI (v1.3.0)
- 脚本: `ai-twitter-digest-v2.sh`
- 部署: LaunchAgent 已更新

## 权限授予步骤（备用）

如果未来需要为 Python 授权 Screen Recording:

```bash
# 1. 找到 Python 可执行文件路径
which python
# /Users/mac/miniconda3/envs/turix_env/bin/python

# 2. 在 System Settings 中添加
# Privacy & Security → Screen Recording → + → 选择 Python 可执行文件

# 3. 重启 LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.keonho.ai-twitter-digest.plist
launchctl load ~/Library/LaunchAgents/com.keonho.ai-twitter-digest.plist
```

## 经验教训

1. **权限问题优先考虑绕过** - 而不是深入解决（除非必要）
2. **LaunchAgent 权限复杂** - 不继承 Terminal 权限
3. **专用工具优于通用工具** - Agent Reach > TuriX（对于定时任务）
4. **Python 权限需要可执行文件级别** - 不是脚本级别

## 相关文档

- `/tmp/tcc_research.sh` - TCC 权限研究脚本
- `~/OpenClaw_Adventure_Log/2026-03-06.md` - 探险日志
- `~/.openclaw/workspace/knowledge/twitter-api-alternatives-2026.md` - 替代方案对比

---

*探险 A 产出 - 2026-03-06*
