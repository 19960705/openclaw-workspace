# TikTok Shop 数据获取方案研究

**日期**：2026-03-07  
**目的**：解决泰国 TikTok 趋势日报数据源问题

---

## 问题背景

当前 `tiktok-thailand-trends` skill 使用静态备份数据：
- Lazada 有反爬虫保护（406/403错误）
- 备份数据不会更新
- 无法获取实时趋势

---

## 方案对比

### 1. TikTok Research API（官方）

**API 端点**：
- Shop Info: `https://open.tiktokapis.com/v2/research/tts/shop/`
- Product Info: `https://open.tiktokapis.com/v2/research/tts/product/`

**优点**：
- 官方支持，数据准确
- 可查询店铺信息、产品数据
- 支持泰国市场

**缺点**：
- ❌ 需要申请审批（仅限学术研究机构）
- ❌ 需要证明研究目的
- ❌ 商业用途不符合资格
- ❌ 审批周期长

**申请要求**：
- 必须是认证研究机构
- 提交研究计划
- 遵守隐私准则
- 非商业用途

**结论**：❌ 不适合我们（商业选品用途）

---

### 2. Apify TikTok Shop Scraper（推荐）

**优点**：
- ✅ 无需审批，即用即付
- ✅ 支持产品搜索、店铺抓取
- ✅ 支持泰国市场
- ✅ 返回结构化数据（JSON/CSV）
- ✅ 可获取：产品名、价格、评分、销量、描述

**可用 Actor**：
1. `novi/tiktok-shop-scraper` - 产品数据抓取（最成熟）
2. `excavator/tiktok-shop-scraper` - 店铺+产品
3. `pratikdani/tiktok-shop-search-scraper` - 搜索结果
4. `salmanrajz/trending-products-scraper` - 热门产品

**定价**：
- 按使用量计费（$0.25-$2/1000次请求）
- 免费试用额度
- 每日抓取 100 个产品：$0.50-$2/天
- 月成本：$15-$60

**API 调用示例**：
```bash
curl -X POST https://api.apify.com/v2/acts/novi~tiktok-shop-scraper/runs \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startUrls": [
      {"url": "https://shop.tiktok.com/view/product/1234567890"}
    ],
    "maxItems": 100,
    "proxy": {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}
  }'
```

**数据字段（可获取）**：
- `product_name` - 产品名称
- `product_price` - 价格
- `product_rating` - 评分
- `product_review_count` - 评论数
- `product_sold_count` - 销量
- `product_description` - 描述
- `shop_name` - 店铺名
- `product_url` - 产品链接
- `image_urls` - 图片链接

**结论**：✅ 推荐方案

---

### 3. 浏览器自动化（备选）

**方案**：
- 用 OpenClaw 无头浏览器访问 TikTok Shop
- 模拟真实用户行为
- 提取页面数据

**优点**：
- 完全控制
- 可模拟真实用户
- 绕过反爬

**缺点**：
- 需要维护反爬逻辑
- 速度慢
- 容易被封
- 维护成本高

**结论**：⚠️ 备选方案（Apify 失败时使用）

---

### 4. FastMoss（待调研）

**网站**：https://www.fastmoss.com/

**功能**：
- 专门的 TikTok Shop 数据平台
- 提供产品搜索、趋势分析
- 可能有现成 API

**待确认**：
- 是否有 API
- 定价模式
- 数据覆盖范围

---

## 推荐实施方案：Apify

### 实施步骤

1. **注册 Apify 账号**
   - 访问：https://apify.com/
   - 获取 API Token

2. **选择合适的 Actor**
   - 推荐：`novi/tiktok-shop-scraper`（最成熟）
   - 备选：`salmanrajz/trending-products-scraper`（热门产品）

3. **编写 Skill**
   - 创建 `tiktok-shop-apify` skill
   - 封装 Apify API 调用
   - 支持关键词搜索
   - 支持泰国市场筛选

4. **数据处理**
   - 提取产品信息
   - 价格转换（泰铢→人民币）
   - 趋势分析
   - 生成日报

5. **替换现有逻辑**
   - 更新 `tiktok-thailand-trends` skill
   - 移除备份数据依赖
   - 接入 Apify 实时数据

---

## 技术实现

### Skill 结构

```
~/.openclaw/skills/tiktok-shop-apify/
├── SKILL.md
├── scripts/
│   ├── apify_client.py      # Apify API 客户端
│   ├── product_search.py    # 产品搜索
│   └── trend_analyzer.py    # 趋势分析
└── config/
    └── categories.json      # 类目配置
```

### API 调用流程

1. 启动 Apify Actor Run
2. 等待运行完成
3. 获取 Dataset ID
4. 下载结果（JSON）
5. 解析数据
6. 生成报告

### 数据处理

```python
# 示例：获取咖啡类产品
{
  "searchKeywords": ["coffee", "กาแฟ"],
  "region": "TH",
  "maxItems": 100,
  "sortBy": "sales"  # 按销量排序
}
```

---

## 成本分析

### Apify 定价

- **免费额度**：$5 credit（新用户）
- **按需付费**：$0.25-$2/1000次请求
- **月度套餐**：$49/月起（包含更多额度）

### 预估成本

**每日使用**：
- 咖啡类：30 个产品
- 厨房类：30 个产品
- 家居类：20 个产品
- 工具类：20 个产品
- 总计：100 个产品/天

**月度成本**：
- 低估：$15/月（$0.50/天）
- 高估：$60/月（$2/天）
- 平均：$30-40/月

---

## 风险评估

### 技术风险

1. **Apify 服务稳定性**
   - 风险：中
   - 缓解：设置重试机制，保留备份数据作为降级方案

2. **TikTok Shop 反爬升级**
   - 风险：中
   - 缓解：Apify 会持续更新反爬策略

3. **数据质量**
   - 风险：低
   - 缓解：数据验证 + 人工抽查

### 成本风险

1. **用量超预期**
   - 风险：低
   - 缓解：设置每日抓取上限

2. **价格上涨**
   - 风险：低
   - 缓解：监控成本，必要时切换方案

---

## 下一步行动

### 立即行动

1. ✅ 调研完成（本文档）
2. ⏳ 等待用户决定：
   - A. 注册 Apify，开始实施
   - B. 先测试浏览器方案
   - C. 继续用备份数据

### 实施计划（如果选 A）

**第一阶段**（1-2天）：
- 注册 Apify 账号
- 测试 `novi/tiktok-shop-scraper`
- 验证泰国市场数据

**第二阶段**（2-3天）：
- 编写 `tiktok-shop-apify` skill
- 实现产品搜索功能
- 数据解析和格式化

**第三阶段**（1天）：
- 更新 `tiktok-thailand-trends` skill
- 接入 Apify 数据源
- 测试日报生成

**第四阶段**（1天）：
- 上线测试
- 监控数据质量
- 优化报告格式

---

## 参考资料

- [Apify TikTok Shop Scraper](https://apify.com/novi/tiktok-shop-scraper)
- [TikTok Research API Docs](https://developers.tiktok.com/doc/research-api-specs-query-tiktok-shop-products)
- [TikTok Shop Thailand Best Sellers](https://www.accio.com/business/tiktok-shop-thailand-best-selling-products-2025)

---

**更新日志**：
- 2026-03-07：初始调研完成
