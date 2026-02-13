# 文生图提示词模板库

## 说明

这个模板库提供用于生成 Seedance 2.0 参考图的文生图提示词。
可以直接用于 Midjourney、DALL-E、Stable Diffusion、Seedream 等图像生成模型。

---

## 人物提示词模板

### 通用结构
```
A [年龄] [性别] [种族/国籍（可选）] with [发型发色], [面部特征], wearing [服装描述], [姿势], [表情], [配饰/道具], [光线描述], [风格描述], [画质描述]
```

### 示例：现代都市女性
```
A 25-year-old Asian woman with long black hair and bangs, delicate features, wearing a white silk blouse and black high-waisted trousers, standing confidently, subtle smile, holding a coffee cup, soft natural window lighting, modern urban style, professional portrait photography, 4K, high detail
```

### 示例：古装仙侠男性
```
A 30-year-old Chinese man with long black hair tied in a topknot, sharp features, wearing flowing white hanfu robes with silver embroidery, standing on a cliff edge, calm expression, holding a jade flute, misty mountain background, volumetric fog, xianxia fantasy style, cinematic lighting, 4K
```

### 示例：赛博朋克角色
```
A young woman with neon blue short hair and cybernetic eye implant, pale skin, wearing a black leather jacket with LED strips, standing in rain, intense gaze, holographic accessories, neon city background, cyberpunk aesthetic, dramatic rim lighting, 4K
```

### 示例：复古怀旧人物
```
A 35-year-old man with slicked-back brown hair and mustache, warm features, wearing a beige trench coat and fedora hat, leaning against a vintage car, thoughtful expression, cigarette in hand, 1940s noir style, warm sepia tones, film grain, vintage photograph quality
```

---

## 场景提示词模板

### 通用结构
```
[场景类型] with [主要元素], [次要元素], [光线条件], [天气/时间], [氛围], [风格], [画质]
```

### 示例：现代城市街道
```
Modern city street at night, wet pavement reflecting neon signs, tall glass buildings, sparse pedestrians with umbrellas, light rain falling, moody atmosphere, cyberpunk urban aesthetic, cinematic composition, 4K, high detail
```

### 示例：古风建筑场景
```
Traditional Chinese courtyard in autumn, red maple leaves scattered on stone path, wooden pavilion with curved roof, lotus pond with koi fish, morning mist, peaceful atmosphere, ancient oriental style, soft diffused lighting, 4K
```

### 示例：自然风光
```
Dramatic mountain landscape at sunset, snow-capped peaks, pine forest in foreground, winding river reflecting orange sky, clouds with golden edges, epic scale, landscape photography style, golden hour lighting, 4K
```

### 示例：室内空间
```
Minimalist modern living room, large floor-to-ceiling windows, white walls, beige sofa, wooden coffee table, indoor plants, afternoon sunlight casting shadows, clean Scandinavian design, architectural photography style, 4K
```

---

## 产品提示词模板

### 通用结构
```
A [材质] [颜色] [产品名], [细节特征], [背景], [光线], [风格], [画质]
```

### 示例：电子产品
```
A sleek black matte mechanical keyboard with RGB backlighting, floating on pure white infinite background, reflection on glossy surface, soft studio lighting with blue accent, Apple-style product photography, 4K, ultra sharp
```

### 示例：美妆产品
```
A luxurious gold glass bottle of perfume, intricate Art Deco patterns, pink rose petals scattered around base, soft pink gradient background, dreamy bokeh, beauty advertisement style, soft diffused lighting, 4K
```

### 示例：时尚配饰
```
A premium Italian leather handbag in burgundy color, gold hardware details, visible stitching texture, placed on marble surface, neutral gray background, luxury fashion photography, dramatic side lighting, 4K
```

### 示例：食品饮料
```
A tall glass of iced coffee with milk swirling, condensation droplets on glass, coffee beans scattered on wooden table, rustic cafe background bokeh, warm inviting atmosphere, food photography style, natural side lighting, 4K
```

---

## 风格修饰词库

### 整体风格
| 风格 | 英文关键词 |
|------|-----------|
| 电影感 | cinematic, film style, movie-like |
| 商业广告 | commercial photography, advertisement style |
| 杂志封面 | magazine cover, editorial style |
| 纪录片 | documentary style, realistic |
| 动漫 | anime style, Japanese animation |
| 3D 渲染 | 3D render, CGI, Octane render |
| 油画 | oil painting style, painterly |
| 水彩 | watercolor style, soft edges |
| 插画 | illustration style, digital art |
| 复古 | vintage, retro, nostalgic |

### 光线描述
| 效果 | 英文关键词 |
|------|-----------|
| 自然光 | natural lighting, available light |
| 黄金时刻 | golden hour, warm sunset light |
| 蓝色时刻 | blue hour, twilight |
| 影棚灯 | studio lighting, professional lighting |
| 三点布光 | 3-point lighting |
| 高调 | high-key lighting, bright and airy |
| 低调 | low-key lighting, dramatic shadows |
| 逆光 | backlit, rim light, silhouette |
| 霓虹 | neon lighting, colorful glow |
| 月光 | moonlight, cool blue tones |

### 画质描述
| 效果 | 英文关键词 |
|------|-----------|
| 高清 | 4K, 8K, high resolution |
| 锐利 | ultra sharp, crisp details |
| 浅景深 | shallow depth of field, bokeh |
| 胶片感 | film grain, analog texture |
| 清晰 | sharp focus, high detail |
| 柔焦 | soft focus, dreamy |

---

## 负面提示词（Negative Prompts）

用于排除不想要的元素：

### 人物类
```
deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, mutated hands, fused fingers, too many fingers, long neck, cross-eyed
```

### 产品类
```
blurry, low quality, distorted, warped, text errors, misspelled, cropped, out of frame, watermark, signature
```

### 场景类
```
blurry, low quality, oversaturated, undersaturated, overexposed, underexposed, artifacts, noise, distorted
```

---

## 使用建议

1. **具体优于模糊**：「25 岁亚洲女性黑色长发」优于「一个女人」
2. **关键词顺序**：最重要的放前面，权重更高
3. **风格一致**：同一项目的所有参考图保持相同的风格关键词
4. **光线匹配**：多张参考图的光线方向和色温要一致
5. **先测试**：生成几张测试图，调整关键词后再批量生成
