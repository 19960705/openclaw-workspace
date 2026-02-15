# Antigravity Image Generator (Nano Banana Pro)

直接调用本地 Antigravity Manager 的 Imagen 3 引擎，生成 4K 高画质 (Pro) 图片。

## 触发条件

当用户需要：
- 使用 Nano Banana Pro 生成图片
- 生成 4K 高清 AI 绘画
- 使用 Google Imagen 3 模型

## 核心配置

- **Model:** `gemini-3-pro-image`
- **Quality:** `hd` (强制)
- **ImageSize:** `4K` (强制)
- **API Base:** `http://127.0.0.1:8045/v1`

## 使用方式

### 直接触发
> “帮我用 Nano Banana Pro 画一个...”

### 脚本调用
```bash
./scripts/generate.sh "prompt" "size"
```

## 输出路径
生成的图片保存在 `~/.openclaw/media/generated_images/` 目录下。

## 示例
```markdown
帮我生成一张 16:9 的赛博朋克风格安乾镐，站在雨中的首尔街头。
```

## 注意事项
1. 必须确保本地 **Antigravity-Manager** 已启动并运行在 8045 端口。
2. 该 Skill 强制开启了 4K 高级画质模式，会消耗较高的账号配额。
