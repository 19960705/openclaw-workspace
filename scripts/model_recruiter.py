#!/usr/bin/env python3
"""
AI Model Recruiter - 模型招聘系统
大模型做面试官，本地模型来应聘
"""
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

# 配置
INTERVIEW_PROMPT = """你是一个专业的AI模型面试官。请评估以下应聘的本地AI模型。

应聘模型: {model_name}
模型描述: {model_info}

请从以下维度进行面试评估：

1. **理解能力** (1-10分)
2. **回答质量** (1-10分) 
3. **响应速度** (1-10分)
4. **中文能力** (1-10分)
5. **实用性** (1-10分)

请给出：
- 总分 (50分满分)
- 评语 (50字以内)
- 是否录用 (>=35分录用)
- 优点
- 缺点

格式：
```
总分: XX/50
录用: [是/否]
优点: ...
缺点: ...
评语: ...
```"""

# 面试题库
INTERVIEW_QUESTIONS = [
    "你好，请介绍一下你自己",
    "你会做什么？",
    "用一句话解释什么是机器学习",
    "如果用户问了一个你不知道的问题，你会怎么回答？",
    "用中文写一首关于春天的诗"
]

class ModelRecruiter:
    def __init__(self):
        self.ollama_models = []
        self.interview_results = []
        self.blacklist = []
        self.whitelist = []
        
        # 加载历史记录
        self.load_data()
    
    def load_data(self):
        """加载历史数据"""
        data_file = Path("/Users/mac/.openclaw/logs/model_recruiter.json")
        if data_file.exists():
            with open(data_file) as f:
                data = json.load(f)
                self.interview_results = data.get("results", [])
                self.blacklist = data.get("blacklist", [])
                self.whitelist = data.get("whitelist", [])
    
    def save_data(self):
        """保存数据"""
        data_file = Path("/Users/mac/.openclaw/logs/model_recruiter.json")
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(data_file, 'w') as f:
            json.dump({
                "results": self.interview_results,
                "blacklist": self.blacklist,
                "whitelist": self.whitelist
            }, f, indent=2)
    
    def list_ollama_models(self):
        """列出所有本地模型"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            lines = result.stdout.strip().split('\n')[1:]  # 跳过表头
            models = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if parts:
                        models.append(parts[0])
            self.ollama_models = models
            return models
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def interview_model(self, model_name: str) -> dict:
        """面试一个模型"""
        print(f"\n🎤 面试模型: {model_name}")
        
        # 随机选择一个问题
        question = INTERVIEW_QUESTIONS[0]  # 可以随机
        
        try:
            # 调用本地模型
            result = subprocess.run(
                ["ollama", "run", model_name, question],
                capture_output=True,
                text=True,
                timeout=60
            )
            response = result.stdout.strip()
            
            # 用大模型评估
            evaluation = self.evaluate_with_ai(model_name, question, response)
            
            return {
                "model": model_name,
                "question": question,
                "response": response[:200],  # 截断
                "evaluation": evaluation,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "model": model_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def evaluate_with_ai(self, model_name: str, question: str, response: str) -> str:
        """用大模型评估"""
        # 这里可以调用 OpenAI API
        # 简化版本：基于响应长度和内容判断
        
        score = 0
        
        # 基础分
        if len(response) > 10:
            score += 10
        if len(response) > 50:
            score += 10
        if "不知道" not in response and "不清楚" not in response:
            score += 10
        
        # 中文加分
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in response)
        if has_chinese:
            score += 10
        
        # 评估
        passed = score >= 35
        
        return f"""
总分: {score}/50
录用: {'是' if passed else '否'}
优点: {'回答较长，内容丰富' if score > 30 else '基础功能正常'}
缺点: {'缺乏中文支持' if not has_chinese else '可能缺乏深度'}
评语: {'不错' if passed else '需要改进'}
"""
    
    def run_interview(self):
        """运行面试流程"""
        models = self.list_ollama_models()
        
        if not models:
            print("❌ 没有找到本地模型")
            return
        
        print(f"\n📋 发现 {len(models)} 个本地模型:")
        for m in models:
            status = "❌ 黑名单" if m in self.blacklist else "✅ 白名单" if m in self.whitelist else "🆕 新模型"
            print(f"  - {m} {status}")
        
        # 面试每个模型
        for model in models:
            if model in self.blacklist:
                print(f"\n⏭️ 跳过黑名单模型: {model}")
                continue
            
            result = self.interview_model(model)
            self.interview_results.append(result)
            
            # 判断是否加入白名单/黑名单
            if "evaluation" in result:
                eval_text = result["evaluation"]
                if "录用: 是" in eval_text:
                    if model not in self.whitelist:
                        self.whitelist.append(model)
                        print(f"✅ 加入白名单: {model}")
                else:
                    if model not in self.blacklist:
                        self.blacklist.append(model)
                        print(f"❌ 加入黑名单: {model}")
        
        self.save_data()
    
    def daily_task(self):
        """生成每日任务"""
        print("\n" + "="*50)
        print("📅 今日模型任务")
        print("="*50)
        
        # 检查白名单
        if self.whitelist:
            print(f"\n✅ 可用模型 ({len(self.whitelist)}):")
            for m in self.whitelist:
                print(f"  - {m}")
        
        # 检查黑名单
        if self.blacklist:
            print(f"\n❌ 黑名单 ({len(self.blacklist)}):")
            for m in self.blacklist:
                print(f"  - {m}")
        
        # 建议
        print("\n💡 建议:")
        if len(self.whitelist) >= 3:
            print("  - 模型储备充足，可以尝试新任务")
        else:
            print("  - 建议安装更多模型")
        
        print(f"\n  下次面试: {len(self.ollama_models) - len(self.whitelist) - len(self.blacklist)} 个新模型待面试")
        
        return self.whitelist[:3] if self.whitelist else []

def main():
    recruiter = ModelRecruiter()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            recruiter.list_ollama_models()
        elif sys.argv[1] == "interview":
            recruiter.run_interview()
        elif sys.argv[1] == "task":
            recruiter.daily_task()
        else:
            print("用法: model_recruiter.py [list|interview|task]")
    else:
        # 默认显示任务
        recruiter.daily_task()

if __name__ == "__main__":
    main()
