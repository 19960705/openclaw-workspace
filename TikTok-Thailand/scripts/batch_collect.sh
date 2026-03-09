#!/bin/bash
# TikTok 批量采集脚本
# 用法: ./batch_collect.sh urls.txt

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAW_DIR="$SCRIPT_DIR/../raw"

if [ ! -f "$1" ]; then
    echo "用法: ./batch_collect.sh <URL列表文件>"
    echo "URL列表文件格式：每行一个 TikTok 视频链接"
    exit 1
fi

mkdir -p "$RAW_DIR"

echo "开始批量采集 TikTok 视频元数据..."
echo "目标目录: $RAW_DIR"
echo ""

count=0
while IFS= read -r url; do
    # 跳过空行和注释
    [[ -z "$url" || "$url" =~ ^# ]] && continue
    
    count=$((count + 1))
    echo "[$count] 采集: $url"
    
    yt-dlp \
        --write-info-json \
        --skip-download \
        --no-warnings \
        -o "$RAW_DIR/%(id)s.%(ext)s" \
        "$url"
    
    if [ $? -eq 0 ]; then
        echo "  ✅ 成功"
    else
        echo "  ❌ 失败"
    fi
    
    # 避免请求过快
    sleep 2
    echo ""
done < "$1"

echo "采集完成！共处理 $count 个视频"
echo "元数据文件保存在: $RAW_DIR"
