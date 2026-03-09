# TikTok 泰区内容自动化管道 - 使用指南

## 快速开始

### 1. 采集单个视频
```bash
cd ~/.openclaw/workspace/TikTok-Thailand
yt-dlp --write-info-json --skip-download \
  "https://www.tiktok.com/@username/video/1234567890" \
  -o "raw/%(id)s.%(ext)s"
```

### 2. 批量采集视频
创建 URL 列表文件 `urls.txt`：
```
https://www.tiktok.com/@user1/video/123
https://www.tiktok.com/@user2/video/456
https://www.tiktok.com/@user3/video/789
```

执行批量采集：
```bash
./scripts/batch_collect.sh urls.txt
```

### 3. 分析视频
```bash
python3 scripts/analyze_video.py raw/1234567890.info.json
```

分析报告会自动保存到 `analysis/` 目录。

### 4. 生成内容灵感
基于分析报告，使用 ContentFactory 工作流：

1. 将分析报告复制到 ContentFactory 收件箱
2. 使用 Perplexity 深度研究
3. 生成选题和大纲
4. 创作终稿

## 工作流示例

### 场景：研究泰国美妆类爆款视频

**步骤 1：采集热门视频**
```bash
# 创建美妆类视频列表
cat > beauty_urls.txt << EOF
https://www.tiktok.com/@thaibeauty1/video/xxx
https://www.tiktok.com/@thaibeauty2/video/yyy
https://www.tiktok.com/@thaibeauty3/video/zzz
EOF

# 批量采集
./scripts/batch_collect.sh beauty_urls.txt
```

**步骤 2：分析所有视频**
```bash
for file in raw/*.info.json; do
    python3 scripts/analyze_video.py "$file"
done
```

**步骤 3：汇总分析**
查看 `analysis/` 目录下的所有报告，识别：
- 高互动率的视频特征
- 热门标签和话题
- 成功的内容结构
- 用户偏好

**步骤 4：生成内容方案**
基于分析结果，在 ContentFactory 中创建：
- 选题：模仿高互动率视频的主题
- 大纲：借鉴成功的内容结构
- 脚本：融入热门标签和元素

## 目录结构
```
TikTok-Thailand/
├── README.md              # 工作流说明
├── GUIDE.md              # 本使用指南
├── raw/                  # 原始元数据
│   ├── 123456.info.json
│   └── 789012.info.json
├── analysis/             # 分析报告
│   ├── 123456_analysis.md
│   └── 789012_analysis.md
├── ideas/                # 内容灵感库
│   └── beauty_content_ideas.md
└── scripts/              # 自动化脚本
    ├── analyze_video.py
    └── batch_collect.sh
```

## 进阶功能（未来）

### 集成 Apify TikTok Scraper
- 自动采集话题下的热门视频
- 批量分析竞品账号
- 追踪趋势变化

### AI 自动分析
- 使用 Claude 自动提取创意点
- 生成内容建议
- 预测爆款潜力

### ContentFactory 深度集成
- 一键从分析到终稿
- 自动化内容生产流程
- 多平台内容适配

## 注意事项
- 遵守 TikTok 使用条款
- 尊重原创内容版权
- 仅用于学习和灵感参考
- 不要过度采集导致 IP 被封
