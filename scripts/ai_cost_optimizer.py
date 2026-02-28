#!/usr/bin/env python3
"""
AI Cost Optimizer - xiamai 智能路由版
根据任务复杂度自动选择模型
"""
import requests

# 配置
XIAMAI_KEY = "sk-176ecb0ce05675d8fb2d55bda5da2524900a88392d92ecde4a83401a1defd48e"
XIAMAI_BASE = "http://ai.xiamai.top/v1"

# 模型配置
MODELS = {
    "mini": "gpt-5.3-codex-mini",  # 简单任务 ($0.50/1M)
    "pro": "gpt-5.3-codex",        # 复杂任务 ($3.00/1M)
}

class XiamaiRouter:
    def __init__(self):
        self.usage = {"mini": 0, "pro": 0}
    
    def classify(self, prompt):
        """分类任务"""
        p = prompt.lower()
        
        # 简单任务 → mini
        if any(k in p for k in [
            "?", "真假", "是么", "分类", "总结", "几个", "多少", "有吗",
            "是什么", "怎么样", "好不好", "哪个好", "介绍一下"
        ]):
            return "mini"
        
        # 复杂任务 → pro
        if any(k in p for k in [
            "写", "创作", "推广", "写一篇", "写一段", "如何做",
            "为什么", "分析", "设计", "开发", "代码"
        ]):
            return "pro"
        
        # 默认 → mini (省成本)
        return "mini"
    
    def ask(self, prompt, model=None):
        """智能问答"""
        # 自动选择模型
        if not model:
            task_type = self.classify(prompt)
            model = MODELS[task_type]
            self.usage[task_type] += 1
        else:
            task_type = "pro" if model == MODELS["pro"] else "mini"
        
        # 调用 API
        url = f"{XIAMAI_BASE}/responses"
        headers = {"Authorization": f"Bearer {XIAMAI_KEY}", "Content-Type": "application/json"}
        data = {
            "model": model,
            "input": [{"type": "message", "role": "user", 
                      "content": [{"type": "input_text", "text": prompt}]}]
        }
        
        try:
            r = requests.post(url, json=data, headers=headers, timeout=60)
            result = r.json()
            
            if "output" in result:
                content = result["output"][0].get("content", [{}])[0].get("text", "")
                return {"model": model, "type": task_type, "response": content}
            return {"model": model, "error": result}
        except Exception as e:
            return {"model": model, "error": str(e)}
    
    def stats(self):
        return self.usage

# 便捷函数
def ask(prompt):
    """直接调用"""
    router = XiamaiRouter()
    return router.ask(prompt)

# 测试
if __name__ == "__main__":
    router = XiamaiRouter()
    
    print("🧪 xiamai 智能路由测试\n")
    
    tests = [
        ("这是咖啡磨豆机吗？", "简单"),
        ("写一段推广文案", "复杂"),
        ("这个产品怎么样？", "简单"),
        ("帮我分析市场", "复杂"),
    ]
    
    for prompt, desc in tests:
        result = router.ask(prompt)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"Q: {prompt}")
            print(f"   → {result['model']} ({result['type']})")
            print(f"   → {result['response'][:60]}...")
            print()
    
    print(f"📊 使用统计: {router.stats()}")
    print(f"\n💡 简单任务用 mini，复杂任务用 pro")
