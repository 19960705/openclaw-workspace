# Seedance 2.0 分镜头脚本终极优化版（基于 CSV 详细提示词）

> 基于《5盘录像带_详细视觉描述脚本_v0.1》+ CSV 详细提示词表格优化
>
> **核心改进**：完整 Image Prompt（超详细）+ Motion Prompt（含 SFX+VFX）+ 统一格式

---

## 0) 全局统一格式（必看！）

### 0.1 Image Prompt 统一开头（每条都保留前 150 词！）

```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition
```

### 0.2 Image Prompt 统一结尾（每条都加！）

```
--ar 16:9 --stylize 170 --q 2
```

### 0.3 Motion Prompt 格式（图生视频用）

```
[镜头运动描述], with realistic SFX: [具体音效], no background music, no BGM
```

### 0.4 统一负向提示词（所有镜头通用）

```
鸟居, 和服, 神社, 富士山, 东京塔, 日本地标, shrine, torii, kimono, geisha, samurai, Mt. Fuji, Tokyo Tower, Shibuya, religious ritual, altar, worship, sacrifice, national flag, military insignia, clean CGI, anime, cartoon, overly futuristic UI, perfect symmetry
```

---

## Prompt 结构说明

### 每个镜头包含：
1. **KF** - 镜头编号
2. **时码** - 时间范围
3. **完整 Image Prompt** - 直接复制到文生图工具
4. **Motion Prompt** - 图生视频，主 Prompt，含 SFX+VFX
5. **备注** - 镜头说明

---

# TAPE 01｜岸柏工业（机甲制造链条）约 20s

**视觉核心**：工厂真实、脏、噪、压抑；机甲只露"局部/剪影"。

---

## KF 1｜00:00-00:02｜黑场入带

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition black CRT monitor screen with flickering white Chinese characters ""TAPE 01 / INDUSTRIAL ZONE / DATE UNKNOWN"" in retro digital font, strong VHS glitch distortion, horizontal scanlines rolling slowly, color bleed on edges, pure black background, static title card, VFX: heavy glitch distortion and tracking error --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static VHS title jitter, with synchronized SFX: VHS crackle, no background music, no BGM
```

### 备注
标题卡

---

## KF 2｜00:02-00:06｜走廊偷拍推进

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition old industrial factory corridor, fluorescent lights flickering on and off, peeling paint on walls, metal door signs with only numbers, low angle handheld documentary perspective, slight motion blur --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
low angle handheld slow push forward, with realistic SFX: distant factory hum, fluorescent light buzz, no background music, no BGM
```

### 备注
走廊偷拍推进

---

## KF 3｜00:06-00:10｜传送带零件微距

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition close-up macro shot of oily metal mechanical parts on conveyor belt, stamped serial numbers and geometric red inspection stamps on part surfaces, industrial cold lighting, shallow depth of field, focus breathing --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
macro tracking shot following parts, with realistic SFX: conveyor belt whir, metal clink, no background music, no BGM
```

### 备注
传送带零件微距

---

## KF 4｜00:10-00:14｜工人背影操作

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition medium close-up of worker's back operating metal clamps, gloves covered in oil, face hidden in shadow unrecognizable, plain work uniform with no logos, cold fluorescent lighting, slight handheld shake --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
medium close-up slow push-in, with realistic SFX: metal clamp clank, factory ambient, no background music, no BGM
```

### 备注
工人背影操作

---

## KF 5｜00:14-00:16｜静帧#01 检验单扫描件

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition evidence photo scan still frame, photocopy texture and yellowed paper, industrial inspection form, large black redaction bars covering sensitive information, only readable fields "MODULE: HIP-JOINT" "STATUS: PASS", corner timecode and "SCAN / QUALITY LOG" small text, realistic tiny smudges --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: paper scan hum, no background music, no BGM
```

### 备注
检验单扫描件静帧

---

## KF 6｜00:16-00:19｜焊接/车床火花

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition close-up of industrial welding work, sparks flying but realistically restrained, oil dripping on metal surface, slight edge overexposure --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
fixed angle slight shake like on toolbox, with realistic SFX: welding spark crackle, oil drip, no background music, no BGM
```

### 备注
焊接/车床火花

---

## KF 7｜00:19-00:20｜静帧#02 遮挡版关节结构图

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition archive still frame, partial view of mecha joint structure engineering blueprint, line art and annotation numbers clear but core outline obscured by black redaction bars, slightly wrinkled paper, geometric red stamp in corner, overlay text "REDACTED / DESIGN DRAFT", realistic scan texture --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: paper rustle, no background music, no BGM
```

### 备注
关节结构图静帧

---

# TAPE 02｜飞骨图书馆（设计图纸/检索狂热）约 20s

**视觉核心**：异常事件纪录；长焦偷拍；纸张、复印、争抢；被干预拍摄。

---

## KF 1｜00:00-00:03｜静帧 借阅卡/档案盒

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition evidence photo still frame, close-up of vintage public library archive box labels and checkout cards, yellowed paper, label reading "F-08 / STACK 3 / ACCESS LIMITED", corner timecode overlay, slight scan texture and smudges, multiple redaction bars --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: archive room ambient, no background music, no BGM
```

### 备注
借阅卡/档案盒静帧

---

## KF 2｜00:03-00:07｜长焦偷拍 人群涌入

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition telephoto spy shot compressing space, vintage library reading room crowded with people, rushing through carrying stacks of books, slight camera shake and grain --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
telephoto spy handheld tracking, with realistic SFX: page rustle, hurried footsteps, no background music, no BGM
```

### 备注
长焦偷拍人群涌入

---

## KF 3｜00:07-00:11｜复印机吐纸 排队

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition old photocopier spitting out paper, line of people waiting anxiously, abstract engineering line art and parameter tables on paper (no real language), cold fluorescent lighting --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
medium shot of copier area, with realistic SFX: photocopier whir, paper feed, no background music, no BGM
```

### 备注
复印机吐纸排队

---

## KF 4｜00:11-00:15｜书页被疯狂圈画

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition close-up of book pages, fictional typeset technical text and formulas heavily circled and underlined in red pen, sticky notes with codenames and numbers, hand flipping pages quickly, shallow depth of field, focus breathing --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
close-up handheld following pages, with realistic SFX: frantic page turning, pen scribble, no background music, no BGM
```

### 备注
书页被疯狂圈画

---

## KF 5｜00:15-00:17｜静帧 工程图纸一角

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition archive still frame, partial close-up of engineering blueprint corner, only English and numbers "ACTUATOR / TORQUE LIMIT" "REV 12" visible, rest obscured by fingers or black redaction bars, creased paper, corner timecode and "FRAME GRAB / UNKNOWN SOURCE" --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: paper rustle, no background music, no BGM
```

### 备注
工程图纸一角静帧

---

## KF 6｜00:17-00:20｜书架缝隙窥视 翻找

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition peeking through bookshelf gap perspective, hand violently pulling book, worn spine numbers, dust floating, slight obstruction feeling --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
peeking perspective handheld, with realistic SFX: book pull yank, dust particles, no background music, no BGM
```

### 备注
书架缝隙窥视翻找

---

# TAPE 03｜美术馆（符号化宣传/审美异化）约 20s

**视觉核心**：把符号变成潮流与赞助；展览、媒体报道、周边礼品店；不神圣化。

---

## KF 1｜00:00-00:02｜标题卡

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition black CRT monitor screen with flickering white text "TAPE 03 / GALLERY / DATE UNKNOWN" in retro digital font, strong VHS glitch distortion, horizontal scanlines rolling slowly, color bleed on edges, pure black background, static title card, VFX: heavy glitch distortion and tracking error --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static VHS title jitter, with synchronized SFX: VHS crackle, no background music, no BGM
```

### 备注
标题卡

---

## KF 2｜00:02-00:06｜走入展厅 人群安静密集

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition wide slow pan of empty white museum hall with giant abstract paintings on walls featuring bold geometric symbols, dramatic spotlight flares, modern but retro gallery with old-style track lighting, dense silent crowd standing and staring at same abstract painting --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
slow pan across the hall, with realistic SFX: echoing footsteps, faint air conditioning hum, no background music, no BGM
```

### 备注
大厅摇镜

---

## KF 3｜00:06-00:09｜抽象画特写 符号重复

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition extreme detail close-up on abstract oil painting canvas, paint texture clearly visible, repeating geometric placeholder symbols across the surface, realistic light reflection, shallow depth of field, focus breathing --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
slow push-in to painting detail, with realistic SFX: deep resonant hum, breathing sync, no background music, no BGM
```

### 备注
抽象画特写符号重复

---

## KF 4｜00:09-00:11｜观众临摹符号

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition close-up of visitor hands tracing abstract geometric symbols with pencil on exhibition booklet, scattered exhibition brochures on table, restrained deliberate movements, soft but realistic lighting --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
close-up handheld slight drift, with realistic SFX: pencil scratch on paper, page turn, no background music, no BGM
```

### 备注
观众临摹符号（非宗教动作）

---

## KF 5｜00:11-00:13｜静帧 媒体报道截图

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition media report screenshot still frame, old TV news broadcast or newspaper layout screenshot, headline "NEW INDUSTRIAL AESTHETIC SPREADS", blurry gallery crowd photo as illustration, corner "MEDIA ARCHIVE" and timecode, realistic compression artifacts --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: old TV static hiss, no background music, no BGM
```

### 备注
媒体报道截图静帧

---

## KF 6｜00:13-00:17｜礼品店周边（符号商品化）

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition museum gift shop checkout counter close-up, postcards badges and poster tubes featuring same geometric placeholder symbol, queuing crowd partially in frame but blurry, realistic barcode scan beep feeling --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
handheld pan across merchandise, with realistic SFX: cash register beep, crowd murmur, no background music, no BGM
```

### 备注
礼品店周边（符号商品化）

---

## KF 7｜00:17-00:20｜朴素叠化：符号↔金属结构 + 过曝白闪

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition double exposure overlay effect, one layer abstract painting geometric symbols, another layer industrial metal structure and bolt close-up, restrained effect like editing evidence correlation, ending with strong overexposure white flash from spotlight --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
double exposure dissolve then overexposure flash, with realistic SFX: glowing hum intensifying, VHS distortion crackle, no background music, no BGM
```

### 备注
朴素叠化 + 过曝白闪转场

---

# TAPE 04｜狂悖街区（演唱会/极端粉丝文化）约 20s

**硬规则**：只能是商业演唱会/街区live；**不做祭祀**。

---

## KF 1｜00:00-00:02｜入带字幕

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition night street scene recording title card "TAPE 04 / STREET LIVE RECORDING", distant blurry stage lights, VHS glitch distortion, timecode --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static VHS title jitter, with synchronized SFX: distant crowd roar, VHS crackle, no background music, no BGM
```

### 备注
入带字幕

---

## KF 2｜00:02-00:06｜远景建立：临时舞台+霓虹

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition wide establishing shot of night street temporary concert stage, lighting truss and speaker arrays clearly visible, surrounding vintage neon signs all in fictional glyphs or graphic logos, dense crowd, slight handheld sway --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
wide handheld establishing shot with slight sway, with realistic SFX: crowd cheer, bass thump, neon buzz, no background music, no BGM
```

### 备注
远景建立：临时舞台+霓虹

---

## KF 3｜00:06-00:09｜穿行人群：汗水/闪光灯/安保推挤

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition shoulder-mounted POV pushing through packed crowd, sweat on faces and phone flashlights, security guards shoving people creating real chaos, motion blur and compression blocks --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
shoulder-mounted POV push through crowd, with synchronized SFX: crowd crush, phone camera clicks, shouting, no background music, no BGM
```

### 备注
穿行人群

---

## KF 4｜00:09-00:11｜舞台侧拍：歌手剪影

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition side-rear stage angle of singer backlit silhouette, microphone and in-ear monitor details, sweat reflection, realistic stage light glare, face unrecognizable --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
side angle slight drift, with realistic SFX: distorted vocal reverb, stage monitor feedback, no background music, no BGM
```

### 备注
舞台侧拍：歌手剪影

---

## KF 5｜00:11-00:13｜静帧：手机直播截图/弹幕

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition phone livestream screenshot still frame, vertical phone interface, "LIVE" badge, time "04:12:xx", scrolling comments in fictional glyphs, hashtags "#ENCORE #NOBREAK", blurry stage lights and crowd as content, heavy compression artifacts, corner "SCREEN CAPTURE" --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: phone notification ding, livestream audio crackle, no background music, no BGM
```

### 备注
手机直播截图/弹幕静帧

---

## KF 6｜00:13-00:16｜粉丝手举物 + 身体极限暗示

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition audience hands holding light signs and posters with fictional symbols resembling trendy logos not religious totems, stage light illuminating arms and sweat, singer in side light gasping exhausted with cracking voice (no gore), medics and stretcher visible at stage edge as realistic detail --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
handheld tracking across crowd then to stage edge, with synchronized SFX: crowd chant, heavy breathing, walkie-talkie crackle, no background music, no BGM
```

### 备注
粉丝手举物 + 身体极限暗示（合规版）

---

## KF 7｜00:16-00:20｜设备故障 + 卡顿切黑

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition stage lights flickering, digital mosaic compression blocks and dropped sample artifacts, audience silhouettes torn by glitch, frame frozen on blinding stage light glare then cut to black, timecode jumping erratically --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
glitch freeze on light flare then black, with realistic SFX: audio cut, power down whine, VHS distortion crackle, no background music, no BGM
```

### 备注
设备故障 + 卡顿停在灯光帧→切黑

---

# TAPE 05｜最终录像带（启动实况/事故）约 20s

**视觉核心**：监控视角+局部证据+克制灾难；不血腥、靠信息恐惧。

---

## KF 1｜00:00-00:02｜静帧：封条/红章

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition archive cover still frame, old file folder cover, typewriter font "TEST FOOTAGE / RESTRICTED", geometric red seal stamp, institution name obscured by thick black redaction bar, corner serial number and timecode, worn paper with smudges, realistic scan texture --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: paper handling rustle, no background music, no BGM
```

### 备注
封条/红章静帧

---

## KF 2｜00:02-00:06｜监控视角：测试场入口

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition low-resolution security camera perspective, test facility entrance corridor or factory gate, rotating warning beacon flashing, human figures rushing in and out with unrecognizable faces, heavy compression artifacts and timecode overlay --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
fixed security camera angle, with realistic SFX: warning beacon alarm, distant radio chatter, heavy door slam, no background music, no BGM
```

### 备注
监控视角：测试场入口

---

## KF 3｜00:06-00:10｜启动局部：液压管/锁扣

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition extreme close-up of massive mechanical device starting up: hydraulic lines pressurizing, metal joints, locking clamps releasing, cold light reflection, shallow depth of field, focus breathing --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
close-up with focus pull, with realistic SFX: hydraulic hiss, metal clank, pressurization whine, no background music, no BGM
```

### 备注
启动局部：液压管/锁扣

---

## KF 4｜00:10-00:12｜仪表异常+地面震动

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition analog gauge dials with needles jumping erratically (no readable real language), warning lights flashing, desk papers vibrating and sliding off, slight camera shake, timecode jumping --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
fixed angle with vibration shake, with realistic SFX: alarm klaxon, gauge needle ticking, papers sliding, no background music, no BGM
```

### 备注
仪表异常+地面震动

---

## KF 5｜00:12-00:14｜静帧：测试记录片段（打码）

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition test log document still frame, yellowed paper, readable key fields "PHASE 1: ONLINE" "UNAUTHORIZED TORQUE" "ABORT?", rest covered by large black redaction bars, corner "LOG EXTRACT" and timecode, realistic scan texture --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: paper scan hum, no background music, no BGM
```

### 备注
测试记录片段静帧（打码）

---

## KF 6｜00:14-00:17｜事故瞬间（克制）

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition accident moment: intense overexposure white flash and smoke dust obscuring view, violent camera shake, partially blocked by debris or obstruction, compression artifacts and noise intensifying, timecode jumping --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
violent shake then partial obstruction, with synchronized SFX: massive impact boom, glass shatter, alarm blare, no background music, no BGM
```

### 备注
事故瞬间（克制，不血腥）

---

## KF 7｜00:17-00:18｜静帧：事故后残骸快拍

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition aftermath evidence photo still frame, twisted steel beams and charred cables and collapsed supports, press quick-snap style, mecha body unrecognizable only unidentifiable metal chunks, dust and smoke residue, corner timecode and "AFTERMATH PHOTO / SOURCE UNKNOWN" --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
static freeze frame, with realistic SFX: distant sirens, settling debris, no background music, no BGM
```

### 备注
事故后残骸快拍静帧

---

## KF 8｜00:18-00:20｜黑场收束：停止键

### 完整 Image Prompt
```
late-era authentic VHS found-footage still frame, hyper-realistic, extremely detailed photorealistic, heavy analog film grain, strong horizontal scanlines, color bleed, tracking jitter, slight motion blur, cinematic VFX: sparks with motion blur, oil flying in extreme detail, screen tearing at edges, light flares and bloom, particle effects, cool desaturated blue-gray industrial tones with orange accent lights and red warning glows, gritty dark realistic pseudo-documentary, oppressive eerie biomechanical horror atmosphere, inspired by Prototype game dark tone + Poppy Playtime creepy factory aesthetic, decaying anonymous bygone bubble-economy metropolis, old camcorder footage, no Japanese cultural elements whatsoever, no text except neon signs, cinematic composition black frame with brief close-up of a hand pressing VCR stop button (only hand visible no face), then pure black, background noise disappears, timecode makes one final jump --ar 16:9 --stylize 170 --q 2
```

### Motion Prompt
```
hand press stop then black silence, with synchronized SFX: VCR mechanical click, tape stop whir, then silence, no background music, no BGM
```

### 备注
黑场收束：停止键

---

# 交付建议（终极版）

## 1. 操作顺序（严格执行！）

### 第一步：先生成 Image Prompt（文生图）
1. 选择图片生成模型（图片 4.1 或其他）
2. 复制完整 Image Prompt（包含统一开头 + 具体内容 + 统一结尾）
3. 生成静帧参考图
4. 确保 2-3 个静帧的风格一致
5. 保存到资产库

### 第二步：再生成 Motion Prompt（图生视频）
1. 选择 Seedance 2.0 模型
2. 选择「主体参考」模式（不是「首帧」！）
3. 上传对应的静帧作为参考图
4. 复制 Motion Prompt（含 SFX+VFX）
5. 设置 16:9 画幅，15-20 秒时长
6. 生成视频

## 2. 占位符号/LOGO/机甲原型策略

**先用占位符号跑通，后续再替换**

- 符号：几何图形占位，不做具体描述
- 机甲：只露局部/剪影，不做全身
- LOGO：留白或模糊占位区域

**你把LOGO/机甲原型给我后，我会做的升级**：
- 给每条Prompt加上"占位符号的精确描述"（形状、比例、边角、线宽）
- 为机甲补齐"局部特写库"（关节/液压/脚步/装甲编号）以保证不同镜头仍像同一台机甲

## 3. 终极检查清单

生成前检查：
- ✅ Image Prompt 包含完整统一开头（前 150 词）
- ✅ Image Prompt 包含统一结尾（--ar 16:9 --stylize 170 --q 2）
- ✅ Motion Prompt 包含镜头运动 + SFX
- ✅ 负向提示词统一复制全局版本
- ✅ 画幅 16:9，时长 15-20 秒
- ✅ 模式选择「主体参考」，不是「首帧」

---

**优化版本**：v2.0（终极优化版）
**优化日期**：2026-02-26
**基于**：《5盘录像带_详细视觉描述脚本_v0.1》+ CSV 详细提示词表格
**核心改进**：完整 Image Prompt（150词统一开头+具体内容+统一结尾）+ Motion Prompt（含 SFX+VFX）+ CSV 格式对齐
