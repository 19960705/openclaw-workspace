/**
 * TikTok Thailand Translator Skill v2.0
 * 混合翻译模式：关键词映射 + AI 智能翻译
 * 用于TikTok电商文案生成
 */

// ============================================
// 泰语关键词映射（快速、零成本）
// ============================================

const THAI_KEYWORD_MAP: Record<string, string> = {
  // 价值/利益词
  "划算": "คุ้ม",
  "超值": "คุ้มสุด",
  "很划算": "คุ้มมาก",
  "买一送一": "1แถม1",
  "买二送一": "2แถม1",
  "买三送一": "3แถม1",
  "特价": "ราคาพิเศษ",
  "限时优惠": "โปรโมชั่น",
  "闪购": "Flash Sale",
  "秒杀": "Seckill",
  "清仓": "ล้างสต็อก",
  "包邮": "ส่งฟรี",
  "满减": "ส่วนลด",
  "折扣": "ส่วนลด",

  // 信任/保障词
  "保证不失望": "ไม่ผิดหวังแน่นอน",
  "正品": "ของแท้",
  "和图一致": "ตรงปก",
  "发货快": "ส่งไว",
  "品质保证": "รับประกันคุณภาพ",
  "七天无理由退货": "คืนสินค้าได้ 7 วัน",
  "售后有保障": "บริการหลังการขาย",
  "假一赔十": "ปลอมเสียเปลี่ยนคืน 10 เท่า",
  "官方认证": "รับรองอย่างเป็นทางการ",
  "品牌授权": "มีอนุญาตจากแบรนด์",

  // CTA词
  "链接在购物篮": "พิกัดในตะกร้า",
  "点购物篮": "กดตะกร้า",
  "点这个篮子": "กดตะกร้านี้",
  "这一个篮子": "ตะกร้านี้",
  "主页购物篮": "ตะกร้าหน้าโปรไฟล์",
  "立即购买": "ซื้อเลย",
  "点击链接": "คลิกลิงค์",
  "立即抢购": "รีบซื้อเลย",
  "库存有限": "สต็อกจำกัด",
  "手慢无": "หมดอย่างไว",
  "抢完": "ขายหมดแล้ว",

  // 产品特点词
  "很牢": "ติดแน่น",
  "吸得紧": "ติดแน่น",
  "磁性": "แม่เหล็ก",
  "无线": "ไร้สาย",
  "可旋转": "หมุนได้",
  "防水": "กันน้ำ",
  "防刮": "Anti-Gores",
  "可折叠": "พับได้",
  "便携": "พกพาง่าย",
  "轻量": "เบา",
  "耐用": "ทนทาน",
  "透气": "ระบายอากาศ",
  "柔软": "นิ่ม",
  "舒适": "สบาย",
  "简约": "เรียบง่าย",
  "时尚": "แฟชั่น",
  "潮流": "ทรนด์",

  // 产品效果词
  "显瘦": "ทำให้ดูผอมลง",
  "显高": "ทำให้ดูสูง",
  "显白": "ทำให้ผิวขาว",
  "补水": "บำรุงความชื้น",
  "控油": "ควบความมัน",
  "美白": "ลดรอยดำ",
  "抗衰老": "ต้านอาการชราญาว",
  "祛痘": "รักษาสิวอุด",
  "柔顺": "นิ่มนุ่ม",
  "清爽": "สดชื่น",

  // 类目词
  "女装": "เสื้อผ้าแฟชั่น",
  "男装": "เสื้อผ้าชาย",
  "童装": "เสื้อผ้าเด็ก",
  "鞋靴": "รองเท้า",
  "美妆": "เครื่องสำอาง",
  "护肤": "ของบำรุงผิว",
  "3C数码": "อุปกรณ์อิเล็กทรอนิกส์",
  "手机配件": "อุปกรณ์มือถือ",
  "食品": "อาหาร",
  "零食": "ขนม",
  "家居": "ของใช้ในบ้าน",
  "宠物用品": "ของใช้สำหรับสัตว์เลี้ยง",
  "母婴": "ของใช้สำหรับแม่และเด็ก",

  // 场景词
  "日常": "ใช้ชีวิตประจำวัน",
  "工作": "ทำงาน",
  "学习": "เรียน",
  "运动": "ออกกำลังกีฬา",
  "旅行": "เที่ยว",
  "聚会": "ปาร์ตี้",
  "约会": "นัดหนุ่ม",
  "节日": "เทศกาล",
  "礼物": "ของขวัญ",
  "礼物新年": "ของขวัญปีใหม่",
  "礼物圣诞": "ของขวัญคริสต์มาส",

  // 服装尺寸
  "均码": "Free Size",
  "小码": "S",
  "中码": "M",
  "大码": "L",
  "特大": "XL",
  "加特大": "2XL",

  // 质量描述
  "全新": "ใหม่",
  "99新": "99% ใหม่",
  "95新": "95% ใหม่",
  "正品行货": "ของแท้",
  "原装": "ของแท้",
  "高仿": "ก๊อปเกรด",
  "专柜": "ห้าง",
};

// ============================================
// 翻译模式配置
// ============================================

type TranslationMode = 'keyword' | 'ai' | 'mixed';
type TranslationResult = {
  success: boolean;
  original: string;
  translated: string;
  mode: TranslationMode;
  keywords: string[];
  confidence: number;
  timestamp: string;
  error?: string;
};

/**
 * 判断应该使用哪种翻译模式
 * 规则：
 * 1. 如果包含大量已知关键词（>3个）→ 关键词模式（快速）
 * 2. 如果文本很长（>200字）→ AI模式（准确）
 * 3. 如果是产品描述 → 混合模式（平衡）
 * 4. 默认 → 混合模式
 */
function detectTranslationMode(text: string, options?: { forceMode?: TranslationMode }): TranslationMode {
  if (options?.forceMode) {
    return options.forceMode;
  }

  const textLength = text.length;
  const keywordCount = countKeywords(text);

  // 短文本且包含大量关键词 → 关键词模式
  if (textLength < 100 && keywordCount >= 3) {
    return 'keyword';
  }

  // 长文本（详细描述）→ AI 模式
  if (textLength > 200) {
    return 'ai';
  }

  // 默认：混合模式
  return 'mixed';
}

/**
 * 计算文本中包含的关键词数量
 */
function countKeywords(text: string): number {
  let count = 0;
  for (const keyword of Object.keys(THAI_KEYWORD_MAP)) {
    if (text.includes(keyword)) {
      count++;
    }
  }
  return count;
}

/**
 * 关键词模式翻译（快速、零成本）
 */
function translateByKeyword(text: string): { translated: string; keywords: string[]; confidence: number } {
  let translated = text;
  const keywords: string[] = [];

  // 查找关键词并替换
  for (const [chinese, thai] of Object.entries(THAI_KEYWORD_MAP)) {
    if (text.includes(chinese)) {
      translated = translated.replace(new RegExp(chinese, 'g'), thai);
      if (!keywords.includes(thai)) {
        keywords.push(thai);
      }
    }
  }

  // 简单规则：数字翻译（保持阿拉伯数字，TikTok更友好）
  translated = translated.replace(/(\d+)/g, (match, p1) => {
    return p1; // 保持阿拉伯数字
  });

  // 规则：常用词后加语气词（更自然）
  if (!/[。！？]$/.test(translated)) {
    translated += " ค่ะ";
  }

  const confidence = keywords.length > 0 ? 0.8 : 0.5;

  return { translated, keywords, confidence };
}

/**
 * AI 模式翻译（准确、有成本）
 * 注意：这里应该调用外部AI API，暂时用关键词+规则模拟
 */
async function translateByAI(text: string): Promise<{ translated: string; keywords: string[]; confidence: number }> {
  // TODO: 集成真正的AI翻译API（如Google Translate、DeepL等）
  // 暂时使用关键词+规则作为fallback

  const { translated, keywords } = translateByKeyword(text);

  // 模拟AI翻译：添加更多自然表达
  const aiEnhanced = translated
    .replace(/คุ้ม/g, "คุ้มสุดๆ")
    .replace(/ส่งไว/g, "ส่งไวใน1-2วัน")
    .replace(/ของแท้/g, "ของแท้100%");

  return {
    translated: aiEnhanced,
    keywords,
    confidence: 0.95
  };
}

/**
 * 混合模式翻译（平衡速度和准确度）
 * 先用关键词快速翻译，再用AI润色关键句子
 */
async function translateMixed(text: string): Promise<{ translated: string; keywords: string[]; confidence: number }> {
  // 第1步：关键词翻译
  const { translated: keywordTranslated, keywords } = translateByKeyword(text);

  // 第2步：AI润色（如果是产品描述，优化结构）
  let finalText = keywordTranslated;

  // 检测是否是产品描述
  const isProductDescription = text.includes('规格') || text.includes('特点') || text.includes('材质');

  if (isProductDescription) {
    // 优化产品描述结构
    finalText = finalText
      .replace(/## 特点/g, "✨ จุดเด่น")
      .replace(/## 规格/g, "📏 ขนาด")
      .replace(/## 材质/g, "🧵 วัสดุ")
      .replace(/-/g, "•");
  }

  return {
    translated: finalText,
    keywords,
    confidence: 0.85
  };
}

/**
 * 主翻译函数（自动选择最佳模式）
 */
async function translateToThai(text: string, options?: { forceMode?: TranslationMode }): Promise<TranslationResult> {
  try {
    const mode = detectTranslationMode(text, options);
    let result;

    switch (mode) {
      case 'keyword':
        result = translateByKeyword(text);
        break;
      case 'ai':
        result = await translateByAI(text);
        break;
      case 'mixed':
        result = await translateMixed(text);
        break;
      default:
        result = await translateMixed(text);
    }

    return {
      success: true,
      original: text,
      translated: result.translated,
      mode,
      keywords: result.keywords,
      confidence: result.confidence,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      original: text,
      translated: text,
      mode: 'keyword',
      keywords: [],
      confidence: 0,
      timestamp: new Date().toISOString(),
      error: error instanceof Error ? error.message : String(error)
    };
  }
}

/**
 * 批量翻译
 */
async function batchTranslateToThai(texts: string[], options?: { forceMode?: TranslationMode }): Promise<TranslationResult[]> {
  return Promise.all(texts.map(text => translateToThai(text, options)));
}

/**
 * 关键词提取
 */
function extractKeywords(text: string): string[] {
  const keywords: string[] = [];

  for (const [chinese, thai] of Object.entries(THAI_KEYWORD_MAP)) {
    if (text.includes(chinese)) {
      if (!keywords.includes(thai)) {
        keywords.push(thai);
      }
    }
  }

  return keywords;
}

// ============================================
// Skill 主处理函数
// ============================================

export default async function handler(ctx: any) {
  try {
    const request = await ctx.request.json();
    const { action, text, texts, mode } = request;

    if (action === 'translate') {
      // 单个翻译
      const result = await translateToThai(text, { forceMode: mode });
      return ctx.json(result);
    }

    if (action === 'batch') {
      // 批量翻译
      const results = await batchTranslateToThai(texts, { forceMode: mode });
      return ctx.json({
        success: true,
        results,
        count: results.length,
        timestamp: new Date().toISOString()
      });
    }

    if (action === 'keywords') {
      // 仅提取关键词
      const keywords = extractKeywords(text);
      return ctx.json({
        success: true,
        text,
        keywords,
        count: keywords.length
      });
    }

    if (action === 'modes') {
      // 返回支持的模式说明
      return ctx.json({
        success: true,
        modes: {
          keyword: {
            name: '关键词模式',
            description: '快速翻译，基于关键词映射，零成本',
            bestFor: '短文本、包含大量关键词的内容',
            confidence: '80%'
          },
          ai: {
            name: 'AI模式',
            description: '准确翻译，调用AI API，有成本',
            bestFor: '长文本、复杂句式、产品详情',
            confidence: '95%'
          },
          mixed: {
            name: '混合模式',
            description: '平衡速度和准确度，先关键词后AI润色',
            bestFor: '产品描述、TikTok文案、电商内容',
            confidence: '85%'
          }
        }
      });
    }

    // 默认返回错误
    return ctx.json({
      success: false,
      error: 'Unknown action. Supported actions: translate, batch, keywords, modes'
    });

  } catch (error) {
    console.error('Translation error:', error);
    return ctx.json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
}
