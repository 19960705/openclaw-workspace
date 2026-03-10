import json
import re
from collections import Counter

# 读取数据
with open('car-spray-products-2026-03-10.json', 'r', encoding='utf-8') as f:
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

# 提取产品品牌和名称
product_mentions = Counter()
brand_keywords = [
    'stoner', 'invisible glass', 'rain-x', 'turtle wax', 'meguiar', 
    'sonax', 'chemical guys', '3m', 'armor all', 'mothers',
    'soft99', 'willson', 'prostaff', 'glaco', 'rain brella',
    # 泰国本地品牌
    'plean dee', 'bietheska', 'mr.diy', 'lotus', 'homepro'
]

for v in videos:
    text = v.get('text', '').lower()
    author = v.get('authorMeta', {}).get('name', '').lower()
    
    # 检查品牌提及
    for brand in brand_keywords:
        if brand in text or brand in author:
            product_mentions[brand] += 1

# 按互动率排序
videos_sorted = sorted([v for v in videos if v.get('playCount', 0) > 5000], 
                       key=lambda x: x.get('engagementRate', 0), reverse=True)

print("=" * 80)
print("🏆 TOP 15 高互动率产品视频")
print("=" * 80)

for i, v in enumerate(videos_sorted[:15], 1):
    author = v.get('authorMeta', {}).get('name', 'Unknown')
    plays = v.get('playCount', 0)
    likes = v.get('diggCount', 0)
    comments = v.get('commentCount', 0)
    shares = v.get('shareCount', 0)
    engagement = v.get('engagementRate', 0)
    text = v.get('text', '')[:150]
    url = v.get('webVideoUrl', '')
    is_ad = v.get('isAd', False) or v.get('isSponsored', False)
    
    # 尝试提取产品名称
    product_name = "未识别"
    text_lower = text.lower()
    for brand in brand_keywords:
        if brand in text_lower:
            product_name = brand.title()
            break
    
    print(f"\n【第 {i} 名】")
    print(f"作者: @{author}")
    print(f"产品: {product_name}")
    print(f"播放: {plays:,} | 点赞: {likes:,} | 评论: {comments:,} | 分享: {shares:,}")
    print(f"互动率: {engagement:.2f}% | 广告: {'是' if is_ad else '否'}")
    print(f"文案: {text}")
    print(f"链接: {url}")

print("\n" + "=" * 80)
print("📊 品牌提及统计")
print("=" * 80)

if product_mentions:
    print("\n🏷️ 最常提及的品牌:")
    for brand, count in product_mentions.most_common(10):
        print(f"  {brand.title()}: {count}次")
else:
    print("\n未检测到明确的品牌提及，需要手动分析视频内容")

# 产品类型分类
print("\n" + "=" * 80)
print("🔍 产品类型分析")
print("=" * 80)

product_types = {
    '车窗清洗剂': ['กระจก', 'glass', 'window', 'windshield'],
    '镀膜剂': ['เคลือบ', 'coating', 'wax', 'polish'],
    '清洁喷雾': ['ทำความสะอาด', 'clean', 'wash'],
    '防雨剂': ['กันน้ำ', 'rain', 'water repellent']
}

type_counts = {k: 0 for k in product_types.keys()}

for v in videos_sorted[:50]:
    text = v.get('text', '').lower()
    for ptype, keywords in product_types.items():
        if any(kw in text for kw in keywords):
            type_counts[ptype] += 1

print("\n产品类型分布 (TOP 50视频):")
for ptype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {ptype}: {count}个视频")

