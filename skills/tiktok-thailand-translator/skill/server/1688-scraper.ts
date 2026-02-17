/**
 * 1688 产品爬虫服务
 * 从 1688.com 获取产品完整信息（标题、描述、规格、价格等）
 */

// ============================================
// 类型定义
// ============================================

type ProductInfo = {
  success: boolean;
  data?: {
    title: string;
    description: string;
    price: string;
    specifications: {
      category: string;
      brand?: string;
      material?: string;
      size?: string;
      color?: string;
      weight?: string;
      features: string[];
    };
    images: string[];
    details: string;
    raw?: any; // 原始数据（如果需要）
  };
  error?: string;
  timestamp: string;
};

type ScrapedProduct = {
  title: string;
  shortDescription: string;
  fullDescription: string;
  priceRange: string;
  specifications: Record<string, string>;
  features: string[];
  images: string[];
};

// ============================================
// 产品信息提取器
// ============================================

/**
 * 从产品标题提取关键信息
 */
function parseProductTitle(title: string): {
  productName: string;
  category: string;
  features: string[];
} {
  const features: string[] = [];
  let productName = title;

  // 检测常见特征
  const featurePatterns = [
    { pattern: /新款/i, feature: '新款' },
    { pattern: /加厚/i, feature: '加厚' },
    { pattern: /加绒/i, feature: '加绒' },
    { pattern: /纯棉/i, feature: '纯棉' },
    { pattern: /防水/i, feature: '防水' },
    { pattern: /防滑/i, feature: '防滑' },
    { pattern: /可拆卸/i, feature: '可拆卸' },
    { pattern: /无线/i, feature: '无线' },
    { pattern: /便携/i, feature: '便携' },
    { pattern: /折叠/i, feature: '可折叠' },
    { pattern: /自动/i, feature: '自动' },
    { pattern: /智能/i, feature: '智能' },
  ];

  for (const { pattern, feature } of featurePatterns) {
    if (pattern.test(title)) {
      features.push(feature);
    }
  }

  // 尝试提取类目（简化版）
  let category = '其他';
  const categoryPatterns = [
    { pattern: /连衣裙|裙装/i, category: '女装' },
    { pattern: /手机壳|保护套/i, category: '手机配件' },
    { pattern: /蓝牙耳机|耳机/i, category: '数码配件' },
    { pattern: /厨房|厨具/i, category: '家居厨具' },
    { pattern: /收纳|整理/i, category: '收纳用品' },
    { pattern: /美妆|化妆/i, category: '美妆护肤' },
    { pattern: /童装|儿童/i, category: '童装' },
    { pattern: /鞋|靴/i, category: '鞋靴' },
  ];

  for (const { pattern: catPattern, category: catName } of categoryPatterns) {
    if (catPattern.test(title)) {
      category = catName;
      break;
    }
  }

  return { productName, category, features };
}

/**
 * 从价格字符串提取价格范围
 */
function parsePrice(priceStr: string): { min: number; max: number; unit: string } {
  // 匹配价格格式：¥12.50-¥18.90 或 12.50-18.90
  const priceMatch = priceStr.match(/¥?(\d+\.?\d*)\s*[-~]\s*¥?(\d+\.?\d*)/);

  if (priceMatch) {
    return {
      min: parseFloat(priceMatch[1]),
      max: parseFloat(priceMatch[2]),
      unit: 'CNY'
    };
  }

  // 单个价格
  const singlePriceMatch = priceStr.match(/¥?(\d+\.?\d*)/);
  if (singlePriceMatch) {
    const price = parseFloat(singlePriceMatch[1]);
    return { min: price, max: price, unit: 'CNY' };
  }

  return { min: 0, max: 0, unit: 'CNY' };
}

/**
 * 从描述中提取规格参数
 */
function parseSpecifications(description: string): Record<string, string> {
  const specs: Record<string, string> = {};

  // 常见规格模式
  const specPatterns = [
    { pattern: /材质[：:]\s*([^\n,，]+)/, key: '材质' },
    { pattern: /尺寸[：:]\s*([^\n,，]+)/, key: '尺寸' },
    { pattern: /颜色[：:]\s*([^\n,，]+)/, key: '颜色' },
    { pattern: /重量[：:]\s*([^\n,，]+)/, key: '重量' },
    { pattern: /品牌[：:]\s*([^\n,，]+)/, key: '品牌' },
    { pattern: /型号[：:]\s*([^\n,，]+)/, key: '型号' },
    { pattern: /产地[：:]\s*([^\n,，]+)/, key: '产地' },
  ];

  for (const { pattern, key } of specPatterns) {
    const match = description.match(pattern);
    if (match) {
      specs[key] = match[1].trim();
    }
  }

  return specs;
}

/**
 * 提取产品特点列表
 */
function parseFeatures(description: string): string[] {
  const features: string[] = [];

  // 提取用 •、-、* 开头的列表项
  const listItems = description.match(/^[•\-*]\s*.+$/gm);
  if (listItems) {
    for (const item of listItems) {
      const feature = item.replace(/^[•\-*]\s*/, '').trim();
      if (feature.length > 0) {
        features.push(feature);
      }
    }
  }

  // 如果没有列表，尝试提取包含"特点"、"优势"等词的句子
  if (features.length === 0) {
    const featureSentences = description.match(/特点[：:]\s*.+|优势[：:]\s*.+|亮点[：:]\s*.+/g);
    if (featureSentences) {
      for (const sentence of featureSentences) {
        const feature = sentence.replace(/^[特点优势亮点][：:]\s*/, '').trim();
        if (feature.length > 0) {
          features.push(feature);
        }
      }
    }
  }

  return features.slice(0, 10); // 最多返回10个特点
}

// ============================================
// 主爬虫函数
// ============================================

/**
 * 从 1688 产品页面获取完整信息
 * 注意：这是一个模拟实现，实际使用时需要集成真实爬虫
 */
async function scrape1688Product(productUrl: string): Promise<ProductInfo> {
  try {
    // TODO: 实际实现应该：
    // 1. 使用 Playwright/Puppeteer 爬取页面
    // 2. 解析 HTML 获取产品信息
    // 3. 返回结构化数据

    // 模拟数据（实际使用时删除）
    const mockData = {
      title: "2024新款夏季韩式连衣裙女装 修身显瘦气质长裙",
      description: `
        这款2024新款夏季韩式连衣裙采用优质面料，透气舒适。

        特点：
        • 修身显瘦版型，展现优美曲线
        • 韩式设计风格，时尚优雅
        • 透气面料，夏天穿着清爽
        • 精致做工，品质保证

        规格：
        材质：100%棉
        尺寸：S, M, L, XL
        颜色：白色、黑色、米色
        适合：日常、约会、聚会
      `,
      price: "¥35.00-¥58.00",
      images: [],
    };

    // 解析数据
    const { productName, category, features: titleFeatures } = parseProductTitle(mockData.title);
    const { min, max, unit } = parsePrice(mockData.price);
    const specs = parseSpecifications(mockData.description);
    const features = parseFeatures(mockData.description);

    return {
      success: true,
      data: {
        title: productName,
        description: mockData.description,
        price: `${min}-${max} ${unit}`,
        specifications: {
          category,
          material: specs['材质'],
          size: specs['尺寸'],
          color: specs['颜色'],
          features: [...titleFeatures, ...features].slice(0, 8)
        },
        images: mockData.images,
        details: mockData.description
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
 * 批量爬取产品（用于1688商品列表）
 */
async function scrape1688Products(productUrls: string[]): Promise<ProductInfo[]> {
  return Promise.all(productUrls.map(url => scrape1688Product(url)));
}

/**
 * 从产品ID构建URL
 */
function build1688Url(productId: string): string {
  return `https://detail.1688.com/offer/${productId}.html`;
}

// ============================================
// 导出接口
// ============================================

export {
  scrape1688Product,
  scrape1688Products,
  build1688Url,
  parseProductTitle,
  parsePrice,
  parseSpecifications,
  parseFeatures,
  type ProductInfo,
  type ScrapedProduct,
};

// ============================================
// 技能处理器（如果独立使用）
// ============================================

export default async function handler(ctx: any) {
  try {
    const request = await ctx.request.json();
    const { action, url, urls, productId } = request;

    if (action === 'scrape') {
      // 单个产品爬取
      const productUrl = url || (productId ? build1688Url(productId) : '');
      if (!productUrl) {
        return ctx.json({
          success: false,
          error: 'URL or productId is required'
        });
      }

      const result = await scrape1688Product(productUrl);
      return ctx.json(result);
    }

    if (action === 'batch') {
      // 批量产品爬取
      if (!urls || !Array.isArray(urls)) {
        return ctx.json({
          success: false,
          error: 'urls array is required for batch scraping'
        });
      }

      const results = await scrape1688Products(urls);
      return ctx.json({
        success: true,
        results,
        count: results.length,
        timestamp: new Date().toISOString()
      });
    }

    if (action === 'build-url') {
      // 构建产品URL
      if (!productId) {
        return ctx.json({
          success: false,
          error: 'productId is required'
        });
      }

      const url = build1688Url(productId);
      return ctx.json({
        success: true,
        productId,
        url,
        timestamp: new Date().toISOString()
      });
    }

    // 默认返回错误
    return ctx.json({
      success: false,
      error: 'Unknown action. Supported actions: scrape, batch, build-url'
    });

  } catch (error) {
    console.error('Scraping error:', error);
    return ctx.json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
}
