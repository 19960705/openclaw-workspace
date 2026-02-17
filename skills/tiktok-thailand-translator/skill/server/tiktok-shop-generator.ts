/**
 * TikTok Shop 内容生成器
 * 整合翻译服务和爬虫服务，生成适合 TikTok Shop 的泰语内容
 */

// ============================================
// 类型定义
// ============================================

type TikTokShopContent = {
  success: boolean;
  data?: {
    title: string;
    shortDescription: string;
    fullDescription: string;
    specifications: string;
    features: string[];
    hashtags: string[];
    cta: string;
    confidence: number;
  };
  error?: string;
  timestamp: string;
};

type ProductInfo = {
  title: string;
  description: string;
  price: string;
  specifications: {
    category: string;
    material?: string;
    size?: string;
    color?: string;
    features: string[];
  };
  images: string[];
};

type TranslationResult = {
  success: boolean;
  translated: string;
  keywords: string[];
  confidence: number;
};

// ============================================
// TikTok Shop 内容模板
// ============================================

const TIKTOK_SHOP_TEMPLATES = {
  // 服装类
  clothing: {
    title: "{product} สไตล์เกาหลี นิ่มคุณภาพดี ทนทาน ใส่สบาย",
    shortDescription: "✨ {product} เสื้อผ้าแฟชั่นสไตล์เกาหลี ผ้านิ่มคุณภาพดี ทนทาน ใส่สบายมาก เหมาะสำหรับทุกโอกาส",
    features: [
      "ผ้านิ่ม 100% สบายผิว",
      "ทนทาน ไม่ยับง่าย",
      "ดีไซน์สไตล์เกาหลี แฟชั่น",
      "ขนาด: {sizes}",
      "ส่งฟรี ภายในประเทศไทย"
    ],
    hashtags: ["#เสื้อผ้าแฟชั่น", "#แฟชั่นไทย", "#สไตล์เกาหลี", "#แฟชั่น", "#tiktokshop"],
    cta: "🛒 พิกัดในตะกร้าค่ะ กดเลย"
  },

  // 数码配件
  digital: {
    title: "{product} อุปกรณ์อิเล็กทรอนิกส์ คุณภาพดี ราคาคุ้ม",
    shortDescription: "📱 {product} อุปกรณ์อิเล็กทรอนิกส์คุณภาพดี ราคาคุ้มมาก ทนทาน ใช้ง่าย",
    features: [
      "ของแท้ คุณภาพดี",
      "ทนทาน ใช้งานได้นาน",
      "ราคาคุ้มค่า",
      "ส่งไว ภายใน1-2วัน"
    ],
    hashtags: ["#อุปกรณ์มือถือ", "#อุปกรณ์อิเล็กทรอนิกส์", "#กันกระแทก", "#tiktokshop"],
    cta: "🛒 กดตะกร้าเลยค่ะ"
  },

  // 家居用品
  home: {
    title: "{product} ของใช้ในบ้าน คุณภาพดี ราคาคุ้ม",
    shortDescription: "🏠 {product} ของใช้ในบ้านคุณภาพดี ราคาคุ้มมาก ใช้งานง่าย",
    features: [
      "วัสดุคุณภาพดี",
      "ใช้งานง่าย ประหยัดเวลา",
      "ราคาคุ้มค่า",
      "ส่งฟรีทั่วไทย"
    ],
    hashtags: ["#ของใช้ในบ้าน", "#เฟอร์นิเจอร์", "#ของตกแต่งบ้าน", "#tiktokshop"],
    cta: "🛒 คลิกตะกร้าเลยค่ะ"
  },

  // 美妆护肤
  beauty: {
    title: "{product} เครื่องสำอาง คุณภาพดี บำรุงผิว",
    shortDescription: "💄 {product} เครื่องสำอางคุณภาพดี บำรุงผิว ให้ผิวสวยใส",
    features: [
      "เครื่องสำอางคุณภาพดี",
      "บำรุงผิว ให้ผิวสวยใส",
      "ราคาคุ้มค่า",
      "ส่งปลอดภัย"
    ],
    hashtags: ["#เครื่องสำอาง", "#ของบำรุงผิว", "#บิวตี้", "#tiktokshop"],
    cta: "🛒 กดตะกร้าเลยค่ะ"
  },

  // 默认模板
  default: {
    title: "{product} คุณภาพดี ราคาคุ้ม",
    shortDescription: "✨ {product} คุณภาพดี ราคาคุ้มมาก ทนทาน ใช้ง่าย",
    features: [
      "คุณภาพดี ของแท้",
      "ราคาคุ้มค่า",
      "ส่งไว ใน1-2วัน",
      "บริการหลังการขาย"
    ],
    hashtags: ["#สินค้าคุณภาพ", "#ราคาคุ้ม", "#tiktokshop"],
    cta: "🛒 พิกัดในตะกร้าค่ะ กดเลย"
  }
};

// ============================================
// 内容生成器
// ============================================

/**
 * 根据产品类目选择模板
 */
function selectTemplate(category: string): typeof TIKTOK_SHOP_TEMPLATES[keyof typeof TIKTOK_SHOP_TEMPLATES] {
  const categoryLower = category.toLowerCase();

  if (categoryLower.includes('女装') || categoryLower.includes('连衣裙') || categoryLower.includes('裙装')) {
    return TIKTOK_SHOP_TEMPLATES.clothing;
  }

  if (categoryLower.includes('男装') || categoryLower.includes('童装')) {
    return TIKTOK_SHOP_TEMPLATES.clothing;
  }

  if (categoryLower.includes('数码') || categoryLower.includes('手机') || categoryLower.includes('配件')) {
    return TIKTOK_SHOP_TEMPLATES.digital;
  }

  if (categoryLower.includes('家居') || categoryLower.includes('厨具') || categoryLower.includes('收纳')) {
    return TIKTOK_SHOP_TEMPLATES.home;
  }

  if (categoryLower.includes('美妆') || categoryLower.includes('护肤') || categoryLower.includes('化妆')) {
    return TIKTOK_SHOP_TEMPLATES.beauty;
  }

  return TIKTOK_SHOP_TEMPLATES.default;
}

/**
 * 生成产品规格表格（泰语）
 */
function generateSpecificationsTable(specs: Record<string, string>): string {
  const rows: string[] = [];

  // 中文到泰语的映射
  const specMap: Record<string, string> = {
    '材质': 'วัสดุ',
    '尺寸': 'ขนาด',
    '颜色': 'สี',
    '重量': 'น้ำหนัก',
    '品牌': 'แบรนด์',
    '型号': 'รุ่น',
    '产地': 'ผู้ผลิต',
  };

  for (const [key, value] of Object.entries(specs)) {
    const thaiKey = specMap[key] || key;
    rows.push(`| ${thaiKey} | ${value} |`);
  }

  if (rows.length === 0) {
    return '| คุณสมบัติ | ค่า |\n|---------|-----|\n| คุณภาพดี | ✅ |';
  }

  return `| คุณสมบัติ | ค่า |\n|---------|-----|\n${rows.join('\n')}`;
}

/**
 * 生成 TikTok Shop 内容
 */
async function generateTikTokShopContent(productInfo: ProductInfo): Promise<TikTokShopContent> {
  try {
    // 1. 选择模板
    const template = selectTemplate(productInfo.specifications.category);

    // 2. 填充标题
    const title = template.title.replace('{product}', productInfo.title);

    // 3. 填充短描述
    const shortDescription = template.shortDescription.replace('{product}', productInfo.title);

    // 4. 生成完整描述（翻译原始描述）
    let fullDescription = productInfo.description;

    // 提取规格信息
    const specs: Record<string, string> = {};
    if (productInfo.specifications.material) specs['材质'] = productInfo.specifications.material;
    if (productInfo.specifications.size) specs['尺寸'] = productInfo.specifications.size;
    if (productInfo.specifications.color) specs['颜色'] = productInfo.specifications.color;

    // 生成规格表格
    const specifications = generateSpecificationsTable(specs);

    // 5. 生成特点列表
    const features = template.features.map(feature => {
      let result = feature;
      if (feature.includes('{sizes}')) {
        result = result.replace('{sizes}', productInfo.specifications.size || 'Free Size');
      }
      return result;
    });

    // 6. 生成 Hashtags
    const hashtags = [...template.hashtags];

    // 7. 设置 CTA
    const cta = template.cta;

    // 8. 计算置信度
    let confidence = 0.8;
    if (specs['材质']) confidence += 0.05;
    if (specs['尺寸']) confidence += 0.05;
    if (productInfo.specifications.features.length > 0) confidence += 0.05;
    confidence = Math.min(confidence, 0.95);

    return {
      success: true,
      data: {
        title,
        shortDescription,
        fullDescription,
        specifications,
        features,
        hashtags,
        cta,
        confidence
      },
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * 从中文产品信息生成 TikTok Shop 内容（简化版）
 */
async function generateFromChinese(
  title: string,
  description: string,
  category: string = '其他'
): Promise<TikTokShopContent> {
  const productInfo: ProductInfo = {
    title,
    description,
    price: '',
    specifications: {
      category,
      features: []
    },
    images: []
  };

  return generateTikTokShopContent(productInfo);
}

/**
 * 生成完整的 TikTok Shop 文案（包含标题、描述、规格等）
 */
async function generateFullCopy(productInfo: ProductInfo): Promise<string> {
  const content = await generateTikTokShopContent(productInfo);

  if (!content.success || !content.data) {
    return '生成失败';
  }

  const { title, shortDescription, specifications, features, hashtags, cta } = content.data;

  // 组装完整文案
  let copy = `## ${title}\n\n`;
  copy += `${shortDescription}\n\n`;

  if (features.length > 0) {
    copy += `## ✨ จุดเด่น\n`;
    for (const feature of features) {
      copy += `✅ ${feature}\n`;
    }
    copy += '\n';
  }

  if (specifications) {
    copy += `## 📏 คุณสมบัติ\n`;
    copy += `${specifications}\n\n`;
  }

  copy += `## 🚀 สั่งซื้อ\n`;
  copy += `${cta}\n\n`;

  if (hashtags.length > 0) {
    copy += `## Hashtags\n`;
    copy += `${hashtags.join(' ')}\n`;
  }

  return copy;
}

// ============================================
// 导出接口
// ============================================

export {
  generateTikTokShopContent,
  generateFromChinese,
  generateFullCopy,
  selectTemplate,
  generateSpecificationsTable,
  type TikTokShopContent,
  type ProductInfo,
  type TranslationResult,
};

// ============================================
// 技能处理器（如果独立使用）
// ============================================

export default async function handler(ctx: any) {
  try {
    const request = await ctx.request.json();
    const { action, title, description, category, fullCopy } = request;

    if (action === 'generate') {
      // 生成 TikTok Shop 内容
      if (!title) {
        return ctx.json({
          success: false,
          error: 'title is required'
        });
      }

      const result = await generateFromChinese(
        title,
        description || '',
        category || '其他'
      );

      return ctx.json(result);
    }

    if (action === 'full-copy') {
      // 生成完整文案
      if (!title) {
        return ctx.json({
          success: false,
          error: 'title is required'
        });
      }

      const productInfo: ProductInfo = {
        title,
        description: description || '',
        price: '',
        specifications: {
          category: category || '其他',
          features: []
        },
        images: []
      };

      const copy = await generateFullCopy(productInfo);

      return ctx.json({
        success: true,
        copy,
        timestamp: new Date().toISOString()
      });
    }

    if (action === 'templates') {
      // 返回所有可用模板
      return ctx.json({
        success: true,
        templates: Object.keys(TIKTOK_SHOP_TEMPLATES),
        timestamp: new Date().toISOString()
      });
    }

    // 默认返回错误
    return ctx.json({
      success: false,
      error: 'Unknown action. Supported actions: generate, full-copy, templates'
    });

  } catch (error) {
    console.error('TikTok Shop generation error:', error);
    return ctx.json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
}
