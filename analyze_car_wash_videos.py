import json
import statistics

# 读取数据
with open('tiktok-car-wash-spray-2026-03-10.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"总共采集到 {len(videos)} 个视频\n")

# 计算互动率
for v in videos:
    plays = v.get('playCount', 0)
    if plays > 0:
        engagement = (v.get('diggCount', 0) + v.get('commentCount', 0) + v.get('shareCount', 0)) / plays * 100
        v['engagementRate'] = engagement
    else:
        v['engagementRate'] = 0

# 按互动率排序
videos_sorted = sorted([v for v in videos if v.get('playCount', 0) > 1000], 
                       key=lambda x: x.get('engagementRate', 0), reverse=True)

print("=" * 80)
print("🔥 TOP 10 高转化率洗车喷雾剂带货视频")
print("=" * 80)

for i, v in enumerate(videos_sorted[:10], 1):
    author = v.get('authorMeta', {}).get('name', 'Unknown')
    plays = v.get('playCount', 0)
    likes = v.get('diggCount', 0)
    comments = v.get('commentCount', 0)
    shares = v.get('shareCount', 0)
    engagement = v.get('engagementRate', 0)
    duration = v.get('videoMeta', {}).get('duration', 0)
    text = v.get('text', '')[:100]
    url = v.get('webVideoUrl', '')
    hashtags = [h.get('name', '') for h in v.get('hashtags', [])]
    is_ad = v.get('isAd', False) or v.get('isSponsored', False)
    
    print(f"\n【第 {i} 名】")
    print(f"作者: @{author}")
    print(f"播放: {plays:,} | 点赞: {likes:,} | 评论: {comments:,} | 分享: {shares:,}")
    print(f"互动率: {engagement:.2f}%")
    print(f"时长: {duration}秒 | 广告: {'是' if is_ad else '否'}")
    print(f"文案: {text}")
    print(f"话题: {', '.join(hashtags[:5])}")
    print(f"链接: {url}")

# 统计分析
print("\n" + "=" * 80)
print("📊 数据洞察")
print("=" * 80)

high_engagement = [v for v in videos_sorted if v.get('engagementRate', 0) > 5]
print(f"\n高互动率视频(>5%): {len(high_engagement)} 个")

avg_engagement = statistics.mean([v.get('engagementRate', 0) for v in videos_sorted]) if videos_sorted else 0
print(f"平均互动率: {avg_engagement:.2f}%")

avg_duration = statistics.mean([v.get('videoMeta', {}).get('duration', 0) for v in videos_sorted]) if videos_sorted else 0
print(f"平均视频时长: {avg_duration:.1f}秒")

# 话题标签分析
all_hashtags = {}
for v in videos_sorted[:30]:
    for h in v.get('hashtags', []):
        name = h.get('name', '')
        if name:
            all_hashtags[name] = all_hashtags.get(name, 0) + 1

top_hashtags = sorted(all_hashtags.items(), key=lambda x: x[1], reverse=True)[:10]
print(f"\n🏷️ 热门话题标签:")
for tag, count in top_hashtags:
    print(f"  #{tag}: {count}次")

# 广告视频分析
ad_videos = [v for v in videos_sorted if v.get('isAd', False) or v.get('isSponsored', False)]
print(f"\n💰 广告视频: {len(ad_videos)} 个")
if ad_videos:
    avg_ad_engagement = statistics.mean([v.get('engagementRate', 0) for v in ad_videos])
    print(f"广告视频平均互动率: {avg_ad_engagement:.2f}%")

