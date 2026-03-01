# Rejection Log Hook

## 简介

自动记录被拒绝的决策和失败的操作，遵循 Moltbook 最佳实践。

## 功能

- 自动捕获工具调用失败
- 记录拒绝原因
- 按严重程度分类
- 统计分析

## 使用方法

```bash
# 手动记录
python3 scripts/rejection_log.py "twitter_post" "no_api_key"

# 查看统计
python3 scripts/rejection_log.py stats

# 查看最近记录
python3 scripts/rejection_log.py list
```

## 严重程度

| 级别 | 说明 |
|------|------|
| low | 一般性拒绝 |
| medium | 需要关注 |
| high | 重要问题 |
| critical | 严重问题 |

## 集成

在 HEARTBEAT.md 中添加定期统计输出：
```bash
python3 scripts/rejection_log.py stats
```
