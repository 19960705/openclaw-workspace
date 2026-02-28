#!/usr/bin/env python3
"""
分镜头脚本生成器 (Storyboard Generator)
为 TikTok 短视频自动生成分镜头脚本
"""
import json
from datetime import datetime
from pathlib import Path

# 配置
XIAMAI_KEY = "sk-176ecb0ce05675d8fb2d55bda5da2524900a88392d92ecde4a83401a1defd48e"
XIAMAI_BASE = "http://ai.xiamai.top/v1"

def generate_storyboard(product_name, product_features, duration=30):
    """
    生成分镜头脚本
    
    Args:
        product_name: 产品名称
        product_features: 产品特点
        duration: 视频时长(秒)
    
    Returns:
        分镜头脚本 (JSON)
    """
    import requests
    
    prompt = f"""你是一个专业的 TikTok 短视频编导。请为以下产品生成分镜头脚本：

产品名称: {product_name}
产品特点: {product_features}
视频时长: {duration} 秒

要求：
1. 每个镜头 3-5 秒
2. 包含：镜头序号、时长、画面描述、台词/文案、配乐建议
3. 前 3 秒必须抓住注意力 (hook)
4. 结尾要有 CTA (行动号召)
5. 输出 JSON 格式

JSON 格式：
{{
  "title": "视频标题",
  "total_duration": {duration},
  "hooks": ["钩子文案1", "钩子文案2"],
  "shots": [
    {{
      "shot": 1,
      "duration": 3,
      "scene": "画面描述",
      "dialogue": "台词",
      "music": "配乐建议"
    }}
  ],
  "cta": "行动号召"
}}"""

    url = f"{XIAMAI_BASE}/responses"
    headers = {
        "Authorization": f"Bearer {XIAMAI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-5.3-codex",
        "input": [{
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": prompt}]
        }]
    }
    
    try:
        r = requests.post(url, json=data, headers=headers, timeout=60)
        result = r.json()
        
        if "output" in result:
            content = result["output"][0].get("content", [{}])[0].get("text", "")
            
            # 尝试解析 JSON
            try:
                # 提取 JSON 部分
                import re
                json_match = re.search(r'\{[\s\S]*\}', content)
                if json_match:
                    storyboard = json.loads(json_match.group())
                    return storyboard
            except:
                pass
            
            return {"raw": content}
        return {"error": result}
    except Exception as e:
        return {"error": str(e)}

def format_storyboard(storyboard):
    """格式化分镜头脚本为可读文本"""
    if "error" in storyboard:
        return f"❌ Error: {storyboard['error']}"
    
    if "raw" in storyboard:
        return f"📝 Generated Script:\n{storyboard['raw']}"
    
    lines = [
        f"🎬 {storyboard.get('title', 'Untitled')}",
        f"⏱️ 时长: {storyboard.get('total_duration', 30)}秒",
        "",
        "🔥 Hooks (开头钩子):",
    ]
    
    for i, hook in enumerate(storyboard.get('hooks', []), 1):
        lines.append(f"  {i}. {hook}")
    
    lines.append("")
    lines.append("📹 分镜头:")
    
    for shot in storyboard.get('shots', []):
        lines.append(f"\n  镜头 {shot.get('shot', '?')}: {shot.get('duration', '?')}秒")
        lines.append(f"    画面: {shot.get('scene', '')}")
        lines.append(f"    台词: {shot.get('dialogue', '')}")
        lines.append(f"    配乐: {shot.get('music', '')}")
    
    lines.append("")
    lines.append(f"📢 CTA: {storyboard.get('cta', '')}")
    
    return '\n'.join(lines)

# 测试
if __name__ == "__main__":
    print("🎬 分镜头脚本生成器测试\n")
    
    product = "咖啡磨豆机"
    features = "便携、自动研磨、可调节粗细、不锈钢刀头"
    
    print(f"产品: {product}")
    print(f"特点: {features}\n")
    
    result = generate_storyboard(product, features, duration=30)
    print(format_storyboard(result))
