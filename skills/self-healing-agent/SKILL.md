---
name: self-healing-agent
description: 自动检测工具失败模式，生成修复代码，测试并应用（失败则回滚）
---

## 工作原理

1. **检测阶段** - 读取 `cron-self-improve-loop` 统计的失败签名
2. **分析阶段** - 识别连续失败 3+ 次的工具/模式
3. **生成阶段** - 为每个失败模式生成修复代码
4. **测试阶段** - 在沙盒中测试修复代码
5. **应用阶段** - 替换原工具（保留备份）
6. **回滚阶段** - 如果新版本也失败，自动回滚

## 使用方法

```bash
# Dry run - 仅分析不修改
python3 ~/.openclaw/skills/self-healing-agent/heal.py --dry-run

# 实际修复
python3 ~/.openclaw/skills/self-healing-agent/heal.py --apply

# 指定失败阈值
python3 ~/.openclaw/skills/self-healing-agent/heal.py --threshold 5
```

## 修复策略

### gateway:device_token_mismatch
- 添加 token 有效性检查
- 自动触发 token 轮换
- 记录轮换历史

### browser:control_unreachable
- 添加服务健康检查
- 失败时自动重启浏览器服务
- 使用 profile=openclaw 作为 fallback

### exec:openclaw_not_found
- 使用绝对路径 `/opt/homebrew/bin/openclaw`
- 添加 PATH 检查
- 提供降级方案

## 安全机制

- 所有修改前自动备份
- 测试失败自动回滚
- 保留最近 5 个版本
- 审计日志记录所有变更

