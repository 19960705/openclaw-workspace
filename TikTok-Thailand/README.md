# TikTok 泰区内容自动化管道

## 工作流程

### 阶段 1：内容采集
```
输入：TikTok 视频链接 / 话题标签
  ↓
yt-dlp 下载视频 + 元数据
  ↓
输出：视频文件 + JSON 元数据
```

### 阶段 2：内容分析
```
输入：视频元数据 (标题、描述、标签、播放量、点赞数)
  ↓
AI 分析（使用 Perplexity 或 Claude）
  - 识别热门元素
  - 提取创意点
  - 分析用户反馈
  ↓
输出：分析报告
```

### 阶段 3：灵感生成
```
输入：分析报告
  ↓
ContentFactory 工作流
  - 选题生成
  - 大纲创作
  - 脚本撰写
  ↓
输出：可执行的内容方案
```

## 目录结构
```
~/.openclaw/workspace/TikTok-Thailand/
├── raw/              # 原始视频和元数据
├── analysis/         # 分析报告
├── ideas/            # 灵感库
└── scripts/          # 自动化脚本
```

## 使用示例

### 1. 采集单个视频
```bash
cd ~/.openclaw/workspace/TikTok-Thailand
yt-dlp --write-info-json --skip-download \
  "https://www.tiktok.com/@user/video/123456" \
  -o "raw/%(id)s.%(ext)s"
```

### 2. 分析视频
```bash
python3 scripts/analyze_video.py raw/123456.info.json
```

### 3. 生成内容方案
```bash
# 使用 ContentFactory 工作流
# 输入：analysis/123456_analysis.md
# 输出：ideas/content_idea_001.md
```
