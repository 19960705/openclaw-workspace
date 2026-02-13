# Seedance 2.0 Prompt Generator

为 Seedance 2.0（字节跳动即梦 AI 视频模型）生成专业级提示词。支持分镜头脚本、风格定义、主体文生图提示词的完整工作流。

## 触发条件

当用户需要：
- 生成 Seedance 2.0 视频提示词
- 创建分镜头脚本
- 设计 AI 视频的风格和主体描述
- 将创意想法转换为 Seedance 格式

## Seedance 2.0 核心概念

### 多模态输入系统

Seedance 2.0 支持四种输入模态自由组合：

| 类型 | 限制 | 用途 |
|------|------|------|
| 图片 | 最多 9 张 | 角色形象、场景风格、首尾帧、商品外观 |
| 视频 | 最多 3 个，总时长 ≤15s | 运镜参考、动作参考、转场效果 |
| 音频 | 最多 3 个 MP3，总时长 ≤15s | 背景音乐、音色参考、节奏卡点 |
| 文字 | 自然语言 | 画面描述、剧情、镜头指令 |

**总文件上限：12 个**
**生成时长：4-15 秒**

### @ 引用语法

上传素材后，必须在提示词中用 `@` 明确指定每个素材的用途：

```
@图片1 作为首帧
@图片2 的人物作为主角
@视频1 参考镜头语言和运镜
@音频1 用于配乐
```

**关键规则：** 素材不说清楚用途，模型会乱用！

## 提示词黄金公式

```
@素材引用 + 用途说明 + 具体画面描述 + 时间线（可选）
```

### 导演级提示词结构

```
主体（Subject）+ 动作（Action）+ 镜头（Camera）+ 场景（Scene）+ 风格（Style）+ 约束（Constraints）
```

## 分镜头脚本模板

### 完整格式

```markdown
# 《[项目标题]》

## 🎬 风格定位
- **视觉风格：** [整体美术风格 / 质感 / 氛围]
- **画面比例：** [16:9 / 9:16 / 1:1]
- **总时长：** [X] 秒
- **音乐建议：** [配乐风格 + 音效元素]

---

## 🎞 分镜头脚本

### 🎥 镜头 1（0–Xs）

**画面：**
[具体场景描述]
[主体动作描述]
[细节/特效描述]

**镜头：** [机位 + 运动方式]

**字幕：**
"[画面配文/旁白]"

**音效：** [此镜头的音乐/音效变化]

---

### 🎥 镜头 2（X–Ys）

**画面：**
[具体场景描述]
[主体动作描述]
[细节/特效描述]

**镜头：** [机位 + 运动方式]

**字幕：**
"[画面配文/旁白]"

**音效：** [此镜头的音乐/音效变化]

---

...（重复至所有镜头）
```

### 示例：情感叙事类分镜

```markdown
# 《当AI把广东年味变成毛毡世界》

## 🎬 风格定位
- **视觉风格：** 手工毛毡质感 / 柔软 / 微缩场景 / 暖色光
- **画面比例：** 9:16
- **总时长：** 60 秒
- **音乐建议：** 温柔钢琴 + 轻微风铃声 + 环境氛围音

---

## 🎞 分镜头脚本

### 🎥 镜头 1（0–4s）

**画面：**
一团白色羊毛在画面中央慢慢旋转，像云一样。
羊毛慢慢"戳"出红色。

**镜头：** 居中固定，微距特写

**字幕：**
"如果AI，把广东年味变成毛毡世界…"

**音效：** 音乐温柔铺开

---

### 🎥 镜头 2（4–8s）

**画面：**
红色毛毡慢慢被"戳"成立体灯笼，悬挂在毛毡街道上。
背景是微缩骑楼街景，全部都是毛毡质感。

**镜头：** 缓慢后拉，展示环境

**字幕：**
"第一缕年味，是红色的。"

**音效：** 轻微市井声

---

### 🎥 镜头 3（8–14s）

**画面：**
迷你毛毡花市出现。
小小摊位上摆着毛毡年桔、挥春、鲜花。

**镜头：** 慢速推进

**字幕：**
"行花街，是广东的仪式感。"

**音效：** 配乐持续，人声嘈杂若隐若现

---
```

### 示例：产品广告分镜

```markdown
# 《机械键盘产品展示》

## 🎬 风格定位
- **视觉风格：** 商业摄影 / 高级感 / 简约科技
- **画面比例：** 16:9
- **总时长：** 10 秒
- **音乐建议：** 电子氛围音 + 轻微机械音效

---

## 🎞 分镜头脚本

### 🎥 镜头 1（0–3s）

**画面：**
纯白无限背景，黑色哑光机械键盘静置。
RGB 灯效缓慢呼吸变化。

**镜头：** 固定机位微距，缓慢推进

**字幕：** （无）

**音效：** 轻微电流嗡嗡声

---

### 🎥 镜头 2（3–7s）

**画面：**
键盘开始顺时针 360° 平稳旋转。
键帽文字清晰可读，材质质感突出。

**镜头：** 固定机位，转盘运动

**字幕：** （无）

**音效：** 安静，偶尔机械咔嗒声

---

### 🎥 镜头 3（7–10s）

**画面：**
旋转停止，RGB 灯效达到最亮。
品牌 Logo 发光，画面定格。

**镜头：** 缓慢后拉至全景

**字幕：**
"BRAND NAME"

**音效：** 轻微升调电子音，收尾

---
```

## 🖼️ 首帧/首尾帧文生图提示词（Nano Banana Pro）

在 Seedance 2.0 生成视频前，需要先用文生图模型生成高质量的首帧（或首尾帧）来锁定整体基调。

### 首帧提示词结构

```
[主体描述], [场景/背景], [光影氛围], [艺术风格/质感], [镜头/构图], [画质参数]
```

### 首帧提示词模板

```markdown
## 🖼️ 首帧文生图提示词

### 基础信息
- **画面比例：** [16:9 / 9:16 / 1:1]
- **用途：** [首帧 / 尾帧 / 风格参考]

### 提示词构成

| 元素 | 描述 |
|------|------|
| **主体** | [画面中心的人物/物品/场景主体] |
| **场景** | [环境、背景、空间描述] |
| **光影** | [光源方向、光线质感、明暗对比] |
| **风格** | [艺术风格、材质质感、美术基调] |
| **构图** | [镜头角度、景别、视觉焦点] |
| **画质** | [分辨率、清晰度、细节程度] |

### 完整提示词
```
[英文提示词，可直接复制到 Nano Banana Pro]
```

### 负面提示词（可选）
```
[需要排除的元素]
```
```

### 示例：毛毡风格首帧

```markdown
## 🖼️ 首帧文生图提示词

### 基础信息
- **画面比例：** 9:16
- **用途：** 首帧（锁定毛毡质感基调）

### 提示词构成

| 元素 | 描述 |
|------|------|
| **主体** | 一团柔软的白色羊毛，中心微微泛红 |
| **场景** | 纯净的浅米色背景，微缩世界感 |
| **光影** | 柔和的暖色漫射光，无明显阴影 |
| **风格** | 手工毛毡质感，羊毛纤维清晰可见，治愈系 |
| **构图** | 居中构图，微距特写，浅景深 |
| **画质** | 高清细腻，纤维纹理清晰 |

### 完整提示词
```
A soft fluffy white wool ball with subtle red tint in center, miniature world aesthetic, felt craft texture, visible wool fibers, pure light beige background, warm soft diffused lighting, cozy healing atmosphere, centered composition, macro close-up shot, shallow depth of field, high detail, 4K quality
```

### 负面提示词
```
blurry, low quality, plastic texture, harsh shadows, oversaturated
```
```

### 示例：产品展示首帧

```markdown
## 🖼️ 首帧文生图提示词

### 基础信息
- **画面比例：** 16:9
- **用途：** 首帧（产品静态展示）

### 提示词构成

| 元素 | 描述 |
|------|------|
| **主体** | 黑色哑光机械键盘，RGB 灯效微亮 |
| **场景** | 纯白无限背景，倒影可见 |
| **光影** | 影棚柔光，轻微侧光勾勒轮廓 |
| **风格** | 高端商业摄影，苹果风格简约 |
| **构图** | 45度俯视，产品居中，留白充足 |
| **画质** | 超高清，材质细节锐利 |

### 完整提示词
```
A black matte mechanical keyboard with subtle RGB backlighting, pure white infinite cyclorama background, visible reflection on glossy surface, professional studio soft lighting with rim light accent, premium commercial product photography, Apple-style minimalist aesthetic, 45-degree overhead angle, centered composition with generous negative space, ultra sharp details, 4K resolution
```
```

### 示例：赛博朋克首帧

```markdown
## 🖼️ 首帧文生图提示词

### 基础信息
- **画面比例：** 9:16
- **用途：** 首帧（锁定赛博朋克氛围）

### 完整提示词
```
A young woman with neon blue short hair standing in rainy cyberpunk city street, holographic advertisements reflecting on wet pavement, pink and cyan neon signs, dense fog with volumetric lighting, dystopian night atmosphere, cinematic color grading, medium shot, looking at camera, mysterious expression, high contrast dramatic lighting, ultra detailed, 4K cinematic quality
```
```

### 首尾帧配合使用

当需要控制视频的起点和终点时，生成配对的首尾帧：

```markdown
## 🖼️ 首尾帧文生图提示词

### 首帧
```
[开始画面的提示词]
```

### 尾帧
```
[结束画面的提示词 - 保持风格一致，改变主体状态/位置/情绪]
```

### 一致性要点
- 保持相同的光影风格
- 保持相同的色彩基调
- 保持相同的画面质感
- 主体可以有动作/位置变化
```

### 风格关键词速查

| 风格类型 | 英文关键词 |
|----------|-----------|
| 毛毡/手工 | felt craft, wool texture, handmade aesthetic, cozy, miniature |
| 商业摄影 | commercial photography, product shot, studio lighting, minimalist |
| 电影感 | cinematic, film style, anamorphic, dramatic lighting |
| 赛博朋克 | cyberpunk, neon, dystopian, holographic, rain-soaked |
| 动漫风 | anime style, cel shading, vibrant colors, Japanese animation |
| 复古胶片 | vintage, film grain, retro, nostalgic, analog |
| 3D 渲染 | 3D render, Octane, C4D, CGI, photorealistic |
| 水彩插画 | watercolor, soft edges, painterly, artistic |
| 极简主义 | minimalist, clean, simple, negative space, pure |
| 奇幻梦境 | dreamlike, surreal, fantasy, ethereal, magical |

## 风格与主体的文生图提示词

### 风格提示词模板

```markdown
## 风格提示词

**整体基调：** [电影感/广告感/纪录片/动漫/写实...]
**色彩方案：** [暖色调/冷色调/高对比/柔和/霓虹...]
**光影风格：** [自然光/影棚灯/逆光/God rays/霓虹反射...]
**画面质感：** [胶片颗粒/4K 清晰/柔焦/锐利/梦幻...]
**时代感：** [现代/复古/未来/赛博朋克/古典...]

**完整风格句：**
[整体基调], [色彩方案], [光影风格], [画面质感], 2K resolution, cinematic quality
```

### 主体提示词模板

```markdown
## 主体提示词

**类型：** [人物/产品/场景/动物/抽象...]

### 人物主体
**年龄性别：** [X岁，男/女]
**外貌特征：** [发型、发色、肤色、五官特点]
**服装：** [款式、颜色、材质、图案]
**姿态表情：** [站/坐/走，情绪状态]
**配饰道具：** [手持物品、饰品]

**完整人物句：**
A [年龄] [性别] with [发型发色], wearing [服装描述], [姿态], [表情], [配饰]

### 产品主体
**产品名称：** [具体名称]
**材质质感：** [金属/塑料/木质/玻璃...]
**颜色细节：** [主色、辅色、渐变、图案]
**品牌元素：** [Logo 位置、文字]
**尺寸比例：** [相对大小]

**完整产品句：**
A [材质] [颜色] [产品名], with [细节特征], [品牌元素], sharp details, commercial photography style
```

## 常用提示词元素库

### 镜头运动词汇

| 中文 | 英文 | 效果 |
|------|------|------|
| 推镜头 | push in / dolly in | 镜头向主体靠近 |
| 拉镜头 | pull out / dolly out | 镜头远离主体 |
| 摇镜头 | pan (左右) / tilt (上下) | 镜头转动 |
| 移动镜头 | tracking shot | 镜头跟随移动 |
| 环绕镜头 | orbit shot | 绕主体旋转 |
| 俯拍 | bird's-eye view / overhead | 从上往下拍 |
| 仰拍 | low-angle shot | 从下往上拍 |
| 跟拍 | follow shot | 跟随主体移动 |
| 一镜到底 | one continuous shot | 不切镜 |
| 希区柯克变焦 | Hitchcock zoom / dolly zoom | 推拉同时变焦 |
| 手持镜头 | handheld | 轻微晃动感 |

### 光影关键词

| 效果 | 关键词 |
|------|--------|
| 自然光 | natural lighting, golden hour, soft sunlight |
| 影棚灯 | studio lighting, 3-point lighting, high-key |
| 逆光 | backlit, silhouette, rim light |
| 霓虹 | neon glow, cyberpunk lighting, neon reflections |
| 电影感 | cinematic lighting, anamorphic lens flare |
| 氛围光 | volumetric fog, God rays, atmospheric |

### 音效关键词

| 场景 | 关键词 |
|------|--------|
| 金属 | metallic clink, sharp clang |
| 水 | splashing, dripping, underwater muffled |
| 脚步 | footsteps on [材质], echoing steps |
| 环境 | ambient noise, distant sirens, wind howling |
| 动作 | whoosh, impact thud, fabric rustling |

### 一致性约束句

当需要保持角色/物品一致时，在提示词末尾添加：

```
Keep the same character, same clothing, same hairstyle, no face changes, no flicker, high consistency.
保持角色、服装、发型一致，无面部变化，无闪烁，高一致性。
```

## 输出格式

当用户提供创意需求时，按以下格式输出：

```markdown
# Seedance 2.0 提示词生成

## 📋 分镜头脚本

[按镜头拆分的详细脚本]

## 🎨 风格提示词

**文生图提示词（用于生成参考图）：**
[英文风格描述，可直接用于 Midjourney/DALL-E/Seedream]

## 👤 主体提示词

**角色/产品文生图提示词：**
[英文主体描述，可直接用于生成参考图]

## 🎬 Seedance 完整提示词

**素材准备：**
- 图片 1：[用途说明]
- 图片 2：[用途说明]
- 视频 1：[用途说明]（可选）
- 音频 1：[用途说明]（可选）

**提示词：**
```
[可直接复制使用的 Seedance 提示词]
```

## 💡 生成建议

- 推荐时长：[X 秒]
- 生成次数建议：[多次生成挑选最佳]
- 注意事项：[针对该场景的特别提示]
```

## 实战模板

### 模板 1：电商产品展示

**输入：** 我要做一个包包的产品视频

**输出：**

```markdown
# Seedance 2.0 提示词生成

## 📋 分镜头脚本

### 镜头 1 (0-5s)
**画面：** 包包在纯白无限背景中央，缓慢顺时针旋转，展示正面和侧面
**镜头：** 固定微距，转盘旋转
**音效：** 安静，轻微皮革质感声

### 镜头 2 (5-10s)
**画面：** 旋转停止，镜头推进至五金细节和材质纹理
**镜头：** 缓慢推进至特写
**音效：** 轻微金属光泽音效

## 🎨 风格提示词

**文生图提示词：**
Minimalist product photography, pure white infinite studio background, soft high-key lighting, commercial advertising style, clean and luxurious, 2K resolution, sharp details

## 👤 主体提示词

**产品文生图提示词：**
A premium leather handbag, [颜色] color, gold hardware details, elegant design, visible stitching and texture, brand logo centered, commercial product shot

## 🎬 Seedance 完整提示词

**素材准备：**
- 图片 1：包包正面高清图
- 图片 2：包包侧面图
- 图片 3：材质细节特写

**提示词：**
```
对 @图片1 的包包进行商业化摄像展示，包包的侧面参考 @图片2，包包的表面材质参考 @图片3。包包在纯白无限背景中央缓慢顺时针旋转 360 度，展示所有细节。镜头从中景缓慢推进到特写，最后定格在品牌 Logo。商业摄影风格，高级感，柔和高调打光，2K 分辨率。保持产品细节一致，Logo 清晰可读。
```

## 💡 生成建议

- 推荐时长：10 秒
- 先用 5 秒测试效果，满意后生成 10 秒版本
- 确保参考图的产品角度和光线一致
```

### 模板 2：短剧预告片

### 模板 3：运镜复刻

### 模板 4：音乐卡点视频

（详见下方完整模板库）

## 完整模板库

详细模板请参考：[templates/](./templates/) 目录

## 注意事项

1. **@ 引用必须准确**：素材多时反复检查，鼠标悬停预览确认
2. **时间线分段写**：复杂剧情按秒数分段描述，更精准
3. **镜头语言要具体**：推、拉、摇、移、环绕，写清楚
4. **多次生成**：AI 有随机性，同样输入跑 3-5 次挑最好的
5. **先简单后复杂**：新手从「一张图 + 文字」开始

## 参考资源

- 官方入口：即梦 (Jimeng / Dreamina)
- 官方模型：Seedance 2.0
- 文生图配套：Seedream 4.0（生成参考图）
