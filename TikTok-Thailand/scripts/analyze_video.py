#!/usr/bin/env python3
"""
TikTok 视频元数据分析脚本
分析 yt-dlp 下载的 info.json 文件，提取关键信息
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def analyze_video(info_json_path):
    """分析单个视频的元数据"""
    with open(info_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取关键指标
    analysis = {
        "video_id": data.get("id"),
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "creator": data.get("uploader", ""),
        "creator_id": data.get("uploader_id", ""),
        "upload_date": data.get("upload_date", ""),
        "duration": data.get("duration", 0),
        "view_count": data.get("view_count", 0),
        "like_count": data.get("like_count", 0),
        "comment_count": data.get("comment_count", 0),
        "share_count": data.get("repost_count", 0),
        "tags": data.get("tags", []),
        "url": data.get("webpage_url", ""),
    }
    
    # 计算互动率
    if analysis["view_count"] > 0:
        engagement_rate = (
            (analysis["like_count"] + analysis["comment_count"] + analysis["share_count"]) 
            / analysis["view_count"] * 100
        )
        analysis["engagement_rate"] = round(engagement_rate, 2)
    else:
        analysis["engagement_rate"] = 0
    
    # 生成分析报告
    report = f"""# TikTok 视频分析报告

## 基本信息
- **视频ID**: {analysis['video_id']}
- **标题**: {analysis['title']}
- **创作者**: {analysis['creator']} (@{analysis['creator_id']})
- **上传日期**: {analysis['upload_date']}
- **时长**: {analysis['duration']}秒

## 数据表现
- **播放量**: {analysis['view_count']:,}
- **点赞数**: {analysis['like_count']:,}
- **评论数**: {analysis['comment_count']:,}
- **分享数**: {analysis['share_count']:,}
- **互动率**: {analysis['engagement_rate']}%

## 内容标签
{', '.join(analysis['tags']) if analysis['tags'] else '无标签'}

## 视频描述
{analysis['description']}

## 链接
{analysis['url']}

---
*分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return report, analysis

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_video.py <info.json路径>")
        sys.exit(1)
    
    info_json_path = Path(sys.argv[1])
    if not info_json_path.exists():
        print(f"错误: 文件不存在 {info_json_path}")
        sys.exit(1)
    
    # 分析视频
    report, analysis = analyze_video(info_json_path)
    
    # 保存报告
    output_dir = Path(__file__).parent.parent / "analysis"
    output_file = output_dir / f"{analysis['video_id']}_analysis.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 分析完成！报告已保存到: {output_file}")
    print(f"\n互动率: {analysis['engagement_rate']}%")
    print(f"播放量: {analysis['view_count']:,}")
