# RapidAPI 电商数据 API 调研

**调研日期**：2026-03-08  
**目标**：找到 Lazada/TikTok Shop 的数据 API 替代方案

---

## RapidAPI 平台概述

**优势**：
- 统一的 API 接口
- 按需付费
- 免费试用额度
- 多种电商平台支持

**劣势**：
- 需要 API Key
- 有请求限制
- 价格可能较高

---

## 已知的电商 API（RapidAPI）

### 1. Real-Time Product Search API
**功能**：
- 搜索多个电商平台产品
- 支持 Amazon, eBay, Walmart 等
- 实时价格和库存

**是否支持 Lazada/TikTok Shop**：待确认

---

### 2. E-Commerce Product Data API
**功能**：
- 产品详情
- 价格历史
- 评论数据

**是否支持 Lazada/TikTok Shop**：待确认

---

### 3. Shopee API (如果有)
**功能**：
- Shopee 产品搜索
- 价格监控
- 销量数据

**替代方案**：可以用 Shopee 数据替代 Lazada

---

## 调研方法

### 方法 1：直接访问 RapidAPI
1. 访问 https://rapidapi.com/hub
2. 搜索 "lazada"
3. 搜索 "tiktok shop"
4. 搜索 "shopee"
5. 搜索 "thailand ecommerce"

### 方法 2：GitHub 搜索
搜索已有的 RapidAPI 集成项目：
```bash
site:github.com rapidapi lazada
site:github.com rapidapi tiktok shop
site:github.com rapidapi shopee thailand
```

### 方法 3：查看 Apify 替代品
- ScraperAPI
- Oxylabs
- Bright Data
- Zyte (formerly Scrapinghub)

---

## 替代方案对比

| 方案 | 优势 | 劣势 | 月成本 |
|------|------|------|--------|
| **Apify** | 专业、稳定 | 需付费 | $15-60 |
| **RapidAPI** | 统一接口 | 可能无 Lazada API | $10-50 |
| **ScraperAPI** | 简单易用 | 需自己解析 | $29+ |
| **自建爬虫** | 免费 | 维护成本高 | $0 |

---

## 下一步行动

### 立即行动
1. ✅ 停掉备份数据的定时任务
2. ⏳ 访问 RapidAPI 搜索可用 API
3. ⏳ 测试 API 可用性
4. ⏳ 对比价格和功能

### 如果 RapidAPI 有合适的 API
1. 注册账号
2. 获取 API Key
3. 测试数据质量
4. 编写 skill 集成

### 如果 RapidAPI 没有
**Plan B**：
- 继续优化 agent-browser 方案
- 或者注册 Apify
- 或者用 Shopee 替代 Lazada

---

## 需要确认的问题

1. RapidAPI 上是否有 Lazada API？
2. RapidAPI 上是否有 TikTok Shop API？
3. 如果没有，是否有泰国电商的通用 API？
4. 价格是否在预算内（<$30/月）？
5. 数据质量是否满足需求？

---

**更新日志**：
- 2026-03-08：初始调研文档创建
- 待更新：RapidAPI 实际搜索结果
