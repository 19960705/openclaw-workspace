---
name: swebench-evaluator
description: 使用 SWE-Bench 评估生成的代码质量 - 自动测试生成的 extension/skill/hook 是否能正确运行
metadata: {"openclaw":{"requires":{"bins":["docker","python3"]}, "skillKey": "swebench"}}
commandTool: exec
commandArgMode: raw
---

# SWE-Bench Evaluator

使用 SWE-Bench 评估生成的代码质量。

## 使用场景

```
User: 评估刚才生成的代码
→ exec command="python3 ~/.openclaw/skills/swebench-evaluator/evaluate.py --code '...' --test-type syntax"
→ Returns evaluation results
```

## 功能

1. **语法检查** - Python 语法验证
2. **导入测试** - 验证依赖是否正确
3. **单元测试** - 运行基本测试用例
4. **评分系统** - 0-100 分，70 分及格

## 使用方法

```bash
# 语法检查
python3 skills/swebench-evaluator/evaluate.py --code "print('hello')" --test-type syntax

# 完整检查
python3 skills/swebench-evaluator/evaluate.py --file /path/to/code.py --test-type full

# 从 stdin 读取
cat code.py | python3 skills/swebench-evaluator/evaluate.py --codex --test-type full
```

## 输出格式

```json
{
  "pass": true,
  "score": 85,
  "issues": [
    { "type": "warning", "message": "Unused import", "line": 10 }
  ],
  "test_type": "full",
  "passed": 8,
  "failed": 1
}
```
