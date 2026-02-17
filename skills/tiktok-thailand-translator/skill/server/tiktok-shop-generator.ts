/**
 * TikTok Shop 内容生成器
 * 将中文产品信息转换为泰语TikTok Shop格式
 */

// ============================================
// 模板类型
// ============================================

type TikTokShopContent = {
  title: string;           // 商品标题（简短，吸引人）
  description: string;      // 商品描述（详细，有说服力）
  specifications: string;   // 规格表（格式化）
  features: string[];      // 特点列表（带emoji）
  hashtags: string[];       // 相关标签
  cta: string;             // 行动号召
  fullText: string;        // 完整文案（可复制粘贴）
};

/**
 * 从原始文本中提取规格信息
 * 格式示例：
 * ## 规格
 * | 尺码 | S | M | L | XL |
 * |-----|---|---|---|----|
 * | 胸围| 80| 84| 88| 92 |
 */
function parseSpecifications(text: string): { [key: string]: string[] } {
  const specs: { [key: string]: string[] } = {};

  // 查找规格表格
  const specMatch = text.match(/## 规格\s*\n([\s\S]*?)(?=\n##|\n\n|$)/);
  if (specMatch) {
    const table = specMatch[1];
    const lines = table.split('\n').filter(line => line.trim());

    if (lines.length >= 2) {
      // 第一行是表头（尺码）
      const headers = lines[0].split('|').map(h => h.trim()).filter(h => h);

      // 后续行是数据
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split('|').map(v => v.trim()).filter(v => v);
        if (values.length > 1) {
          const key = values[0];
          specs[key] = values.slice(1);
        }
      }
    }
  }

  return specs;
}

/**
 * 从文本中提取特点列表
 * 格式示例：
 * ## 特点
 * ✅ 100%棉质
 * ✅ 防水涂层
 */
function parseFeatures(text: string): string[] {
  const features: string[] = [];

  // 查找特点列表
  const featureMatch = text.match(/## (特点|优势|功能)\s*\n([\s\S]*?)(?=\n##|\n\n|$)/);
  if (featureMatch) {
    const lines = featureMatch[2].split('\n').filter(line => line.trim());

    for (const line of lines) {
      // 移除emoji和标记，只保留文本
      const cleanLine = line
        .replace(/^[\s•\-\*✅❌]+/, '')
        .trim();

      if (cleanLine) {
        features.push(cleanLine);
      }
    }
  }

  return features;
}

/**
 * 生成泰语规格表
 */
function generateThaiSpecs(specs: { [key: string]: string[] }): string {
  if (Object.keys(specs).length === 0 {
    return '';
  }

  const keys = Object.keys(specs);
  const values = Object.values(specs);

  // 翻译键名
  const keyTranslations: Record<string, string> = {
    '尺码': 'ไซส์',
    '胸围': 'รอบอก',
    '腰围': 'รอบเอว',
    '肩宽': 'ความกว้างไหล่',
    '衣长': 'ความยาว',
    '材质': 'วัสดุ',
    '重量': 'น้ำหนัก',
    '颜色': 'สี'
  };

  let table = '📏 ขนาด\n\n';

  // 表头
  const translatedKeys = keys.map(k => keyTranslations[k] || k).join(' | ');
  table += `| ${translatedKeys} |\n`;
  table += `| ${keys.map(() => '---').join('|')} |\n`;

  // 数据行（转置）
  const colCount = values[0]?.length || 0;
  for (let col = 0; col < colCount; col++) {
    const rowData = keys.map(key => values[key][col] || '-').join(' | ');
    table += `| ${rowData} |\n`;
  }

  return table;
}

/**
 * 生成泰语特点列表
 */
function generateThaiFeatures(features: string[]): string[] {
  const featureEmojis = ['✨', '🌟', '💎', '🔥', '⚡', '🎯', '🌈', '🎉'];

  return features.map((feature, index) => {
    const emoji = featureEmojis[index % featureEmojis.length];
    return `${emoji} ${feature}`;
  });
}

/**
 * 生成相关标签
 */
function generateHashtags(title: string, description: string, category?: string): string[] {
  const hashtags = new Set<string>();

  // 基础标签
  hashtags.add('#tiktok');
  hashtags.add('#tiktokshop');
  hashtags.add('#thailand');
  hashtags.add('#ไทย');

  // 类目标签
  if (category) {
    hashtags.add(`#${category}`);
  }

  // 从标题和描述中提取关键词
  const text = `${title} ${description}`;
  const keywords = [
    'ชุดเดรส', 'แฟชั่น', 'สไตล์', 'เกาหลี', 'เสื้อผ้า',
    'คุ้ม', 'ราคาถูก', 'ส่งไว', 'ของแท้', 'ทนทาน'
  ];

  for (const keyword of keywords) {
    if (text.includes(keyword) || text.includes(keyword.replace('#', ''))) {
      hashtags.add(`#${keyword}`);
    }
  }

  return Array.from(hashtags).slice(0, 10); // 最多10个标签
}

/**
 * 生成行动号召（CTA）
 */
function generateCTA(): string {
  const ctas = [
    '🛒 กดตะกร้าสินค้าได้เลยค่ะ',
    '👇 พิกัดในตะกร้าเลยค่ะ',
    '⚡ รีบกดด่วนก่อนหมดสต็อกค่ะ',
    '💖 คลิกตะกร้าสินค้าเพื่อสั่งซื้อค่ะ'
  ];

  return ctas[Math.floor(Math.random() * ctas.length)];
}

/**
 * 主函数：生成TikTok Shop内容
 */
async function generateTikTokShopContent(
  chineseInput: {
    title: string;
    description?: string;
    specifications?: string;
    features?: string;
    category?: string;
  },
  options?: {
    tone?: 'cute' | 'professional' | 'urgent';
    maxLength?: number;
  }
): Promise<TikTokShopContent> {
  const { title, description = '', specifications = '', features = '', category } = chineseInput;

  // 解析规格和特点
  const specs = parseSpecifications(specifications);
  const featureList = parseFeatures(features);

  // 生成泰语内容
  const thaiSpecs = generateThaiSpecs(specs);
  const thaiFeatures = generateThaiFeatures(featureList);
  const thaiHashtags = generateHashtags(title, description, category);
  const thaiCTA = generateCTA();

  // 生成标题（简短、吸引人）
  const thaiTitle = options?.tone === 'cute'
    ? `✨ ${title} น่ารักมากค่ะ`
    : title;

  // 生成完整文案
  const fullText = [
    thaiTitle,
    '',
    description || '',
    '',
    thaiSpecs,
    '',
    thaiFeatures.join('\n'),
    '',
    thaiCTA,
    '',
    thaiHashtags.join(' ')
  ].filter(Boolean).join('\n');

  return {
    title: thaiTitle,
    description: description,
    specifications: thaiSpecs,
    features: thaiFeatures,
    hashtags: thaiHashtags,
    cta: thaiCTA,
    fullText
  };
}

// ============================================
// Skill 处理函数
// ============================================

export default async function handler(ctx: any) {
  try {
    const request = await ctx.request.json();
    const { action, product, options } = request;

    if (action === 'generate') {
      // 生成TikTok Shop内容
      const content = await generateTikTokShopContent(product, options);

      return ctx.json({
        success: true,
        content,
        timestamp: new Date().toISOString()
      });
    }

    // 默认返回错误
    return ctx.json({
      success: false,
      error: 'Unknown action. Supported actions: generate'
    });

  } catch (error) {
    console.error('TikTok Shop generator error:', error);
    return ctx.json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
}
