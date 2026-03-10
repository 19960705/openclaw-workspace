# AI日报增强版使用指南

## 快速开始

### 立即测试
```bash
# 运行增强版 AI 日报（推荐 v2.0）
bash scripts/ai-daily-enhanced-v2.sh
```

这会：
1. 分析示例 AI 新闻
2. 添加重要性说明
3. 智能去重
4. 发送到 Telegram topic:2

### 查看效果
打开 Telegram，查看 topic:2，你会看到类似这样的日报：

```
🤖 AI 热门日报 - 2026-03-11

📰 GPT-5.4正式发布(Computer Use+金融插件)
💡 重要性：OpenAI首次集成计算机控制能力，直接对标Claude，AI应用场景从对话扩展到自动化操作。

📰 Claude日增百万用户超越ChatGPT
💡 重要性：市场格局重大转变，Anthropic凭借产品力打破OpenAI垄断，标志AI竞争进入新阶段。

...

---
✨ 本日报由 OpenClaw 自动生成并增强
💡 新增功能：
  • 重要性分析 - 快速理解新闻价值
  • 智能去重 - 同一话题合并展示
```

## 版本对比

| 功能 | 原版 | v1.0 | v2.0 (推荐) |
|------|------|------|-------------|
| 列出新闻 | ✅ | ✅ | ✅ |
| 重要性分析 | ❌ | ✅ | ✅ |
| 智能去重 | ❌ | ❌ | ✅ |
| 新闻数量 | 10条 | 10条 | 5-8条（精选） |
| 信息密度 | 低 | 中 | 高 |

## 集成到每日 cron

### 选项1：手动运行（推荐先测试）
每天 09:00 手动运行几天，验证效果：
```bash
bash scripts/ai-daily-enhanced-v2.sh
```

### 选项2：替换现有任务
如果效果满意，可以替换现有的 AI日报 任务：

1. 找到现有任务配置（通过 Gateway UI 或配置文件）
2. 修改任务的执行命令为：`bash scripts/ai-daily-enhanced-v2.sh`
3. 保存并测试

### 选项3：创建新任务
创建一个新的 cron 任务：
- Name: AI日报增强版
- Schedule: `cron 0 9 * * * @ Asia/Shanghai`
- Command: `bash scripts/ai-daily-enhanced-v2.sh`

然后禁用旧的 AI日报 任务。

## 自定义配置

### 修改发送目标
编辑 `scripts/ai-daily-enhanced-v2.sh`：
```bash
TELEGRAM_CHAT_ID="-1003505656701"  # 你的 chat ID
TELEGRAM_TOPIC_ID="2"               # 你的 topic ID
```

### 修改新闻源
目前使用示例数据。要使用真实数据，需要：
1. 从现有 AI日报 cron 获取输出
2. 或者集成 Twitter/RSS 数据源
3. 修改脚本中的 `sample_news` 变量

## 技术细节

### v2.0 工作原理
1. 获取 AI 新闻列表（当前使用示例）
2. 调用 AI 模型分析：
   - 识别重复或相似话题
   - 合并同一话题的多条新闻
   - 为每条新闻生成重要性说明
3. 格式化为增强版日报
4. 发送到 Telegram

### 依赖
- OpenClaw CLI
- Python 3
- jq (JSON 处理)
- 可访问的 AI 模型（通过 openclaw agent）

## 故障排除

### 问题：Telegram 发送失败
**解决**：检查 Telegram 配置，确保 chat ID 和 topic ID 正确

### 问题：AI 分析失败
**解决**：脚本会自动降级到简单格式，不会中断执行

### 问题：脚本权限错误
**解决**：
```bash
chmod +x scripts/ai-daily-enhanced-v2.sh
```

## 下一步优化

可以继续实现的功能：
- [ ] 方案B：趋势预测（这些新闻可能带来什么影响）
- [ ] 方案C：相关性评分（与你的工作有多相关）
- [ ] 从真实数据源获取新闻（而不是示例）
- [ ] 添加配置文件支持
- [ ] 支持多语言

## 反馈

如果你觉得增强版有用，或者有改进建议，可以：
1. 在 improvement-proposals.md 中添加新提案
2. 直接修改脚本
3. 告诉我你的想法

---

**创建时间**：2026-03-11  
**版本**：v2.0  
**状态**：已测试，可用
