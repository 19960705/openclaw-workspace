
# ☕ 春季新品咖啡机 - AI Master 三步法实现计划
**日期**：2026-02-22 | **项目**：春日咖啡广告

---

## 🎯 第一步：主镜头图像

### 场景设定
- **角色**：25-30岁亚洲女生，穿着宽松米白色毛衣，睡眼惺忪但带着期待的微笑
- **场景**：明亮的现代厨房，清晨阳光从右侧45度角斜射进来
- **产品**：春日限定款咖啡机，樱花粉+薄荷绿配色
- **光线**：温暖的晨光，柔和的逆光效果
- **风格**：写实电影感，温暖治愈色调
- **构图**：侧面中景，咖啡机在画面左侧，女生在右侧走向咖啡机
- **背景**：窗外隐约可见樱花枝桠

### 主镜头提示词
```
Photorealistic cinematic shot, 25-year-old Asian woman in loose cream sweater, sleepy but with期待的 smile, walking towards a spring-limited coffee machine in bright modern kitchen, morning sunlight streaming from right 45 degrees, soft backlight, cherry blossom branches visible outside window, warm healing tones, movie still, 35mm lens, f/1.8, shallow depth of field, 8K, ultra detailed --ar 9:16 --style raw
```

---

## 🎯 第二步：无限角度生成

### 需要的角度列表（对应分镜脚本）
| 镜头 | 角度 | 叙事功能 |
|------|------|----------|
| 镜头1 | 侧面特写 + 缓慢推拉 | 专业开场，建立场景 |
| 镜头2 | 中景 + 自然手持感 | 情感连接，真实故事 |
| 镜头3 | 特写 + 高速摄影 | 产品互动，物理反馈 |
| 镜头4 | 多角度蒙太奇（俯视、侧面、微距） | 过程展示，节奏把控 |
| 镜头5 | 长镜头 + 逆光 + 缓慢拉远 | 情感升华，故事高潮 |
| 镜头6 | 固定镜头 + 产品特写 | 品牌露出，简洁有力 |
| 镜头7 | 极慢淡出 + 侧影 | 结尾，余韵悠长 |

### 角度提示词模板
```
[角度描述], same character, same coffee machine, same kitchen, same lighting, same style, reference image as main shot --ar 9:16
```

### 具体角度提示词
1. **侧面特写 + 缓慢推拉**
   ```
   Close-up shot from side, slowly pushing in to coffee machine, morning sunlight creating bright highlights on metal surface, steam rising, cherry blossom branches outside window, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

2. **中景 + 自然手持感**
   ```
   Medium shot, natural handheld feeling, slight breathing movement, woman in cream sweater walking to kitchen, sleepy smile, sunlight through blinds creating warm light spots on her face, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

3. **特写 + 高速摄影**
   ```
   Extreme close-up, slow motion, woman's finger pressing coffee machine button, soft backlight feedback on button, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

4. **俯视角度**
   ```
   Top-down shot, coffee beans falling into grinder, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

5. **侧面特写（咖啡液）**
   ```
   Side close-up, coffee slowly pouring out, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

6. **微距（奶泡）**
   ```
   Macro shot, milk foam like clouds, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

7. **长镜头 + 逆光**
   ```
   Long shot, backlight creating dreamy atmosphere, woman holding coffee cup walking to window, cherry blossoms outside, wind blowing her hair, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

8. **产品特写**
   ```
   Static shot, product close-up, logo clearly visible, steam forming elegant arc, background fading to pure cherry blossom pink, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

9. **侧影 + 微光**
   ```
   Slow fade-out, woman sitting by window holding coffee, smiling into distance, only her silhouette and coffee's warm glow visible, same character, same coffee machine, same kitchen, same lighting, same style --ar 9:16
   ```

---

## 🎯 第三步：把图像变成真正的镜头

### 层级 1：单镜头运动
- **镜头1**：主图 → 缓慢推进
- **镜头5**：主图 → 缓慢拉远

### 层级 2：首帧 + 尾帧控制
- **镜头1→镜头2**：从咖啡机特写 → 女生中景
- **镜头2→镜头3**：女生中景 → 按键特写
- **镜头3→镜头4**：按键特写 → 咖啡制作蒙太奇
- **镜头4→镜头5**：蒙太奇 → 窗边长镜头
- **镜头5→镜头6**：窗边 → 产品特写
- **镜头6→镜头7**：产品特写 → 侧影淡出

### 层级 3：多镜头模式
- 每个镜头 3-5 秒
- 完整序列：广角开场 → 切特写 → 拉到鸟瞰 → ...
- 全程角色一致，风格一致，光影稳定

---

## ✅ 检查清单

### 主镜头检查
- [ ] 角色确定（25-30岁亚洲女生，米白毛衣）
- [ ] 场景确定（明亮现代厨房）
- [ ] 光线确定（清晨右侧45度，逆光）
- [ ] 风格确定（写实电影感，温暖治愈）
- [ ] 产品确定（樱花粉+薄荷绿咖啡机）
- [ ] 自己满意这张图吗？

### 无限角度检查
- [ ] 所有角度都用主图作为参考
- [ ] 只改变角度描述
- [ ] 不重新写风格/光线描述
- [ ] 角色一致
- [ ] 衣服一致
- [ ] 环境一致
- [ ] 光线没漂移

### 视频镜头检查
- [ ] 先设计镜头结构
- [ ] 再让模型执行
- [ ] 用首帧+尾帧控制
- [ ] 多镜头模式每个3-5秒
- [ ] 不是在拼素材，是在安排镜头顺序

