# 泰国香水类内容采集计划

## 采集目标

### 内容类型
1. **测评类** - 香水开箱、试香、对比测评
2. **教程类** - 香水使用技巧、搭配建议
3. **种草类** - 香水推荐、好物分享
4. **品牌类** - 品牌故事、新品发布

### 目标指标
- 播放量：>50,000
- 互动率：>5%
- 发布时间：最近 30 天
- 地区：泰国

## 搜索关键词（泰语）

### 主要标签
- #น้ำหอม (香水)
- #รีวิวน้ำหอม (香水测评)
- #perfumethailand
- #กลิ่นหอม (香味)
- #น้ำหอมแนะนำ (香水推荐)

### 品牌标签
- #chanelperfume
- #diorperfume
- #gucciperfume
- #tomfordperfume

## 采集步骤

### 1. 手动搜索（在 TikTok App 中）
```
1. 打开 TikTok
2. 搜索 "#น้ำหอม" 或 "#รีวิวน้ำหอม"
3. 筛选：最近、最热门
4. 复制视频链接（点击分享 → 复制链接）
```

### 2. 创建 URL 列表
将复制的链接保存到 `perfume_urls.txt`：
```
https://www.tiktok.com/@user1/video/123...
https://www.tiktok.com/@user2/video/456...
https://www.tiktok.com/@user3/video/789...
```

### 3. 批量采集
```bash
cd ~/.openclaw/workspace/TikTok-Thailand
./scripts/batch_collect.sh perfume_urls.txt
```

### 4. 批量分析
```bash
for file in raw/*.info.json; do
    python3 scripts/analyze_video.py "$file"
done
```

## 分析重点

### 内容维度
- 视频时长（最佳时长）
- 开场方式（前 3 秒）
- 展示形式（特写、全景、对比）
- 文案风格（种草、测评、教程）

### 数据维度
- 互动率排名
- 热门标签组合
- 最佳发布时间
- 用户评论关键词

## 下一步行动

1. **立即执行**：在 TikTok 搜索并复制 10-20 个视频链接
2. **批量采集**：使用 batch_collect.sh 采集元数据
3. **深度分析**：识别高互动率视频的共同特征
4. **内容创作**：基于分析结果，使用 ContentFactory 创作

---

*创建时间: 2026-03-09 08:34*
