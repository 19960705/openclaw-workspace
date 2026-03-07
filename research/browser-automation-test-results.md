# 浏览器自动化测试结果

**测试日期**：2026-03-07  
**目标**：用浏览器绕过 Lazada 反爬，获取实时产品数据

---

## 测试工具

### agent-browser CLI
- **版本**：最新版（npm global install）
- **浏览器**：Chromium（自动安装）
- **特点**：
  - Rust 核心，快速
  - 支持 accessibility tree snapshot
  - 提供元素引用（@e1, @e2...）
  - 支持滚动、点击、填充等交互

---

## 测试过程

### 1. 安装
```bash
npm install -g agent-browser
agent-browser install
```
✅ 成功安装

### 2. 访问 Lazada 首页
```bash
agent-browser open 'https://www.lazada.co.th/'
```
- ⚠️ 页面加载超时（25秒）
- ✅ 但部分内容已加载
- ✅ 成功获取到首页产品列表

**获取到的数据示例**：
```
- link "Certainty ผ้าอ้อมผู้ใหญ่... ฿ 1,280.00 ฿ 1,625.00 -21%" [ref=e24]
- link "Floor Mop, Mop Set... ฿ 49.00 ฿ 90.00 -46%" [ref=e25]
- link "Doi KhamHoney 100%... ฿ 140.00 ฿ 190.00 -26%" [ref=e26]
```

### 3. 搜索咖啡产品
**尝试 1**：使用元素引用填充搜索框
```bash
agent-browser fill '@e6' "coffee cup"
agent-browser click '@e7'
```
❌ 失败：`@e6` 语法错误

**尝试 2**：直接访问搜索结果页
```bash
agent-browser open 'https://www.lazada.co.th/tag/coffee/?q=coffee'
```
- ⚠️ 页面加载超时
- ⚠️ 只获取到导航元素，没有产品列表
- 原因：产品列表需要更长时间加载（JS 异步渲染）

---

## 技术分析

### Lazada 架构
- **前端框架**：React SPA
- **数据加载**：异步 API 调用
- **渲染方式**：客户端渲染（CSR）
- **反爬策略**：
  - 延迟加载
  - 动态内容
  - 可能有 bot 检测

### 加载时序
1. 初始 HTML（空壳）- 1-2秒
2. React 框架加载 - 3-5秒
3. API 请求产品数据 - 5-10秒
4. 渲染产品列表 - 2-3秒
5. **总计**：15-25秒

### agent-browser 默认超时
- **默认**：25秒
- **实际需要**：30-60秒（包括滚动加载更多）

---

## 成功案例

### Lazada 首页产品抓取
```bash
agent-browser open 'https://www.lazada.co.th/'
sleep 8
agent-browser snapshot -i
```

**结果**：
- ✅ 获取到 50+ 产品
- ✅ 包含产品名、价格、折扣、评论数
- ✅ 数据格式清晰

**示例数据**：
```
link "Lvyimao Water Bottle... ฿52.98 -37% (435)" [ref=e51]
link "Sea Iqangel Men's Trousers... ฿48.00 -33% (928)" [ref=e52]
link "VINTLOOK Fashionable... ฿10.86 -46% (5579)" [ref=e53]
```

---

## 问题与挑战

### 1. 页面加载超时
- **问题**：默认 25秒超时不够
- **解决方案**：
  - 增加等待时间（30-60秒）
  - 使用 `wait` 命令等待特定元素
  - 分步加载（先加载页面，再等待内容）

### 2. 动态内容加载
- **问题**：产品列表异步加载
- **解决方案**：
  - 等待特定元素出现
  - 滚动触发懒加载
  - 多次 snapshot 确认内容加载完成

### 3. 元素引用语法
- **问题**：`@e6` 在 shell 中需要特殊处理
- **解决方案**：用引号包裹 `'@e6'`

### 4. 数据提取
- **问题**：snapshot 输出是文本，需要解析
- **解决方案**：
  - 使用 `--json` 输出 JSON 格式
  - 用 `grep`/`jq` 提取关键信息
  - 编写解析脚本

---

## 优化方案

### 方案 A：增加等待时间
```bash
agent-browser open 'https://www.lazada.co.th/tag/coffee/'
sleep 30  # 等待 30 秒
agent-browser scroll down 1000
sleep 5
agent-browser scroll down 1000
sleep 5
agent-browser snapshot -i --json > products.json
```

### 方案 B：等待特定元素
```bash
agent-browser open 'https://www.lazada.co.th/tag/coffee/'
agent-browser wait '.product-card'  # 等待产品卡片出现
agent-browser snapshot -i
```

### 方案 C：分步加载
```bash
# 1. 打开页面
agent-browser open 'https://www.lazada.co.th/tag/coffee/'

# 2. 等待初始加载
sleep 10

# 3. 滚动触发更多内容
for i in {1..5}; do
  agent-browser scroll down 1000
  sleep 3
done

# 4. 获取数据
agent-browser snapshot -i --json
```

---

## 成本分析

### 时间成本
- **初始开发**：2-3天
  - 调试加载时序
  - 编写解析脚本
  - 测试稳定性
- **维护成本**：每月 1-2小时
  - 页面结构变化
  - 反爬策略更新

### 运行成本
- **服务器**：免费（本地运行）
- **带宽**：可忽略
- **总计**：$0/月

---

## 对比：Apify vs agent-browser

| 维度 | Apify | agent-browser |
|------|-------|---------------|
| **成本** | $15-60/月 | $0/月 |
| **开发时间** | 0（即用） | 2-3天 |
| **维护成本** | 低（Apify 负责） | 中（需自己维护） |
| **稳定性** | 高 | 中（需调优） |
| **数据质量** | 结构化 | 需解析 |
| **灵活性** | 中 | 高 |
| **反爬能力** | 强（专业代理） | 中（本地 IP） |

---

## 结论

### 技术可行性
✅ **可行**，但需要：
1. 增加等待时间（30-60秒）
2. 实现滚动加载策略
3. 编写数据解析脚本
4. 处理偶发失败（重试机制）

### 推荐方案

**短期（1-2周）**：
- 用 **Apify**（快速上线，稳定可靠）
- 月成本 $15-60

**长期（1-2个月后）**：
- 优化 **agent-browser** 作为备份
- 降低对 Apify 的依赖
- 节省长期成本

**最佳实践**：
- 主力：Apify（稳定、省时间）
- 备份：agent-browser（降级方案）
- 监控：两个数据源对比，确保质量

---

## 下一步行动

### 如果选择 Apify
1. 注册账号：https://apify.com/
2. 获取 API Token
3. 测试 `novi/tiktok-shop-scraper`
4. 编写 `tiktok-shop-apify` skill
5. 上线测试

### 如果选择 agent-browser
1. 实现优化方案 A/B/C
2. 编写数据解析脚本
3. 测试稳定性（运行 100 次）
4. 实现重试机制
5. 监控和告警

### 如果两个都做
1. 先上 Apify（快速解决问题）
2. 并行开发 agent-browser（备份方案）
3. 对比数据质量
4. 逐步切换或混合使用

---

**更新日志**：
- 2026-03-07：初始测试完成
