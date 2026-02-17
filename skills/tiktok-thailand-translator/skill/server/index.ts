/**
 * TikTok Thailand Translator Skill
 * 中→泰翻译服务，用于TikTok电商文案生成
 */

// 泰语关键词映射（来自我们的关键词库）
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
  
  // 信任/保障词
  "保证不失望": "ไม่ผิดหวังแน่นอน",
  "正品": "ของแท้",
  "和图一致": "ตรงปก",
  "发货快": "ส่งไว",
  "品质保证": "รับประกันคุณภาพ",
  "七天无理由退货": "คืนสินค้าได้ 7 วัน",
  "售后有保障": "บริการหลังการขาย",
  "假一赔十": "ปลอมเสียเปลี่ยนคืน 10 เท่า",
  
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
  
  // 产品效果词
  "显瘦": "ทำให้ดูผอมลง",
  "显高": "ทำให้ดูสูง",
  "显白": "ทำให้ผิวขาว",
  "补水": "บำรุงความชื้น",
  "控油": "ควบความมัน",
  "美白": "ลดรอยดำ",
  "抗衰老": "ต้านอาการชราญาว",
  "祛痘": "รักษสิวอุด",
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
};

/**
 * 翻译函数：基于关键词映射 + 简单规则
 */
function translateToThai(text: string): string {
  let translated = text;
  
  // 查找关键词并替换
  for (const [chinese, thai] of Object.entries(THAI_KEYWORD_MAP)) {
    // 优先替换完整匹配
    if (text.includes(chinese)) {
      translated = translated.replace(new RegExp(chinese, 'g'), thai);
    }
  }
  
  // 简单规则：数字翻译
  translated = translated.replace(/(\d+)/g, (match, p1) => {
    const num = parseInt(p1, 10);
    const thaiNumbers = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙', '๑๐'];
    return thaiNumbers[num] || num;
  });
  
  // 规则：常用词后加语气词
  const toneWords = ['ค่ะ', 'นะค้า', 'จ้าา', 'เลย', 'มากๆ'];
  translated = translated.replace(/([。！])$/, '$1 ค่ะ');
  
  // 规则：问号结尾
  translated = translated.replace(/[?]$/, 'หรือ?');
  
  return translated;
}

/**
 * 关键词提取：从文本中提取相关关键词
 */
function extractKeywords(text: string): string[] {
  const keywords: string[] = [];
  
  // 提取提到的关键词
  for (const [chinese] of Object.keys(THAI_KEYWORD_MAP)) {
    if (text.includes(chinese)) {
      const thai = THAI_KEYWORD_MAP[chinese];
      if (thai && !keywords.includes(thai)) {
        keywords.push(thai);
      }
    }
  }
  
  return keywords;
}

/**
 * 批量翻译
 */
function batchTranslateToThai(texts: string[]): string[] {
  return texts.map(translateToThai);
}

/**
 * Skill主处理函数
 */
export default async function handler(ctx: any) {
  try {
    const request = await ctx.request.json();
    const { action, text, texts } = request;
    
    if (action === 'translate') {
      // 单个翻译
      const translated = translateToThai(text);
      const keywords = extractKeywords(text);
      
      return ctx.json({
        success: true,
        original: text,
        translated,
        keywords,
        timestamp: new Date().toISOString()
      });
    }
    
    if (action === 'batch') {
      // 批量翻译
      const translated = batchTranslateToThai(texts);
      
      return ctx.json({
        success: true,
        originals: texts,
        translated,
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
    
    // 默认返回错误
    return ctx.json({
      success: false,
      error: 'Unknown action. Supported actions: translate, batch, keywords'
    });
    
  } catch (error) {
    console.error('Translation error:', error);
    return ctx.json({
      success: false,
      error: error instanceof Error ? error.message : String(error)
    });
  }
}
