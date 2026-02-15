---
name: tiktok-thailand-trends
description: 泰国 TikTok 趋势日报。监控泰区热门话题、爆款视频和产品趋势，专注咖啡、厨房、家居、工具类目。用于每日定时汇报或用户询问泰国 TikTok 趋势时触发。
---

# TikTok 泰国趋势日报

为 TikTok 泰区运营提供每日趋势洞察，聚焦咖啡、厨房、家居、工具类目。

## 核心类目

- ☕ **咖啡** - 咖啡机、咖啡豆、手冲器具、咖啡周边
- 🍳 **厨房** - 厨具、小家电、收纳、清洁用品
- 🏠 **家居** - 装饰、收纳、生活用品、智能家居
- 🔧 **工具** - 五金工具、DIY 器材、维修设备

## 日报结构

### 1. 热门话题 (Trending Hashtags)
- 搜索泰国 TikTok 热门标签
- 筛选与核心类目相关的话题
- 标注话题热度和增长趋势

### 2. 爆款视频分析
- 找出近24小时内高互动视频
- 分析视频风格、拍摄手法、文案套路
- 提炼可复用的内容策略

### 3. 产品趋势
- 识别当前热卖产品
- 分析价格带和卖点
- 对比竞品表现

### 4. 运营建议
- 基于趋势给出选品建议
- 推荐内容创作方向
- 提示潜在爆款机会

## 数据来源

使用以下方式获取泰国 TikTok 数据：

```bash
# 使用 web_search 搜索泰国 TikTok 趋势
web_search "TikTok Thailand trending 2026" country="TH"
web_search "TikTok ประเทศไทย trending coffee kitchen"
web_search "泰国 TikTok 热门 咖啡 厨房 家居"
```

## 泰语关键词参考

| 中文 | 泰语 | 英文 |
|------|------|------|
| 咖啡 | กาแฟ | coffee |
| 厨房 | ห้องครัว | kitchen |
| 家居 | บ้าน | home |
| 工具 | เครื่องมือ | tools |
| 热门 | ยอดนิยม | trending |
| 推荐 | แนะนำ | recommend |

## 输出格式

```markdown
# 🇹🇭 TikTok 泰国趋势日报 - YYYY-MM-DD

## 📊 今日概览
- 核心类目热度变化
- 重点关注事项

## 🔥 热门话题 Top 5
1. #话题1 - 热度/增长率
2. ...

## 🎬 爆款视频精选
- 视频1: 内容摘要 | 互动数据 | 可借鉴点
- ...

## 🛒 产品趋势
- 类目A: 热卖产品 + 价格带
- ...

## 💡 运营建议
- 选品方向
- 内容策略
- 注意事项

---
数据来源: TikTok Thailand / 泰区电商平台
```

## 定时汇报

配合 OpenClaw cron 实现每日定时推送：

```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Bangkok" },
  "payload": { "kind": "agentTurn", "message": "生成今日 TikTok 泰国趋势日报" },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```
