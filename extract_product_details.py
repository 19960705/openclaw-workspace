import json
import re
from collections import Counter

# 读取数据
with open('car-spray-products-2026-03-10.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

# 计算互动率
for v in videos:
    plays = v.get('playCount', 0)
    if plays > 0:
        engagement = (v.get('diggCount', 0) + v.get('commentCount', 0) + v.get('shareCount', 0)) / plays * 100
        v['engagementRate'] = engagement
    else:
        v['engagementRate'] = 0

# 扩展品牌和产品关键词
product_patterns = {
    # 国际品牌
    '3M': r'3m',
    'Stoner Invisible Glass': r'stoner|invisible\s*glass',
    'Rain-X': r'rain[-\s]*x',
    'Turtle Wax': r'turtle\s*wax',
    "Meguiar's": r"meguiar'?s?",
    'Sonax': r'sonax',
    'Chemical Guys': r'chemical\s*guys',
    'Armor All': r'armor\s*all',
    'Mothers': r'mothers',
    'Soft99': r'soft\s*99',
    'Willson': r'willson',
    'Glaco': r'glaco',
    'Rain Brella': r'rain\s*brella',
    
    # 泰国本地品牌/产品
    'Super Wash': r'super\s*wash',
    'Candy Gleam': r'candy\s*gleam',
    'Amway Car Wash': r'แอมเวย์|amway',
    'Mr.DIY': r'mr\.?\s*diy|mrdiy',
    'Plean Dee': r'plean\s*dee|เพลินดี',
    'Bie The Ska': r'bietheska|bie\s*the\s*ska',
}

brand_mentions = Counter()
product_videos = {}

# 分析每个视频
for v in videos:
    text = (v.get('text', '') + ' ' + v.get('authorMeta', {}).get('name', '')).lower()
    
    for brand, pattern in product_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            brand_mentions[brand] += 1
            if brand not in product_videos:
                product_videos[brand] = []
            product_videos[brand].append(v)

print("=" * 80)
print("🏆 热门产品品牌排行")
print("=" * 80)

for i, (brand, count) in enumerate(brand_mentions.most_common(15), 1):
    # 计算该品牌视频的平均互动率
    brand_vids = product_videos[brand]
    avg_engagement = sum(v.get('engagementRate', 0) for v in brand_vids) / len(brand_vids) if brand_vids else 0
    total_plays = sum(v.get('playCount', 0) for v in brand_vids)
    total_likes = sum(v.get('diggCount', 0) for v in brand_vids)
    
    print(f"\n【第 {i} 名】{brand}")
    print(f"  提及次数: {count}次")
    print(f"  总播放量: {total_plays:,}")
    print(f"  总点赞数: {total_likes:,}")
    print(f"  平均互动率: {avg_engagement:.2f}%")
    
    # 显示该品牌最热门的视频
    top_vid = max(brand_vids, key=lambda x: x.get('playCount', 0))
    print(f"  最热视频: {top_vid.get('webVideoUrl', '')}")
    print(f"    播放: {top_vid.get('playCount', 0):,} | 互动率: {top_vid.get('engagementRate', 0):.2f}%")

# 分析产品类型和价格区间（从文案中提取）
print("\n" + "=" * 80)
print("💰 产品特征分析")
print("=" * 80)

# 提取价格信息
price_mentions = []
for v in videos[:100]:
    text = v.get('text', '')
    # 匹配泰铢价格
    prices = re.findall(r'(\d+)(?:\s*บาท|฿|\s*baht)', text, re.IGNORECASE)
    if prices:
        price_mentions.extend([int(p) for p in prices if int(p) < 2000])  # 过滤异常值

if price_mentions:
    avg_price = sum(price_mentions) / len(price_mentions)
    print(f"\n价格区间分析 (基于 {len(price_mentions)} 个价格提及):")
    print(f"  平均价格: {avg_price:.0f} 泰铢")
    print(f"  价格范围: {min(price_mentions)} - {max(price_mentions)} 泰铢")

# 功能特点分析
features = {
    '防雨/疏水': ['กันน้ำ', 'water repellent', 'rain', 'hydrophobic'],
    '去污/清洁': ['ทำความสะอาด', 'clean', 'remove', 'ขจัด'],
    '镀膜/保护': ['เคลือบ', 'coating', 'protect', 'seal'],
    '增亮/抛光': ['เงา', 'shine', 'polish', 'gloss'],
    '防雾': ['กันฝ้า', 'anti-fog', 'fog'],
}

feature_counts = {k: 0 for k in features.keys()}
for v in videos[:100]:
    text = v.get('text', '').lower()
    for feature, keywords in features.items():
        if any(kw in text for kw in keywords):
            feature_counts[feature] += 1

print("\n产品功能特点 (TOP 100视频):")
for feature, count in sorted(feature_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {feature}: {count}个视频提及")

