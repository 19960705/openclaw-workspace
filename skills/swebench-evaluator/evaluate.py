#!/usr/bin/env python3
"""
SWE-Bench Lite Evaluator
评估生成的代码质量 - 轻量级版本
"""

import ast
import sys
import json
import argparse
from typing import Dict, List, Any

def check_python_syntax(code: str) -> Dict[str, Any]:
    """检查 Python 代码语法"""
    issues = []
    score = 100
    
    try:
        ast.parse(code)
    except SyntaxError as e:
        issues.append({
            "type": "error",
            "message": f"Syntax error: {e.msg}",
            "line": e.lineno,
            "col": e.offset
        })
        score -= 50
    
    return {"issues": issues, "score": score}

def check_imports(code: str) -> Dict[str, Any]:
    """检查导入语句"""
    issues = []
    score = 0
    
    try:
        tree = ast.parse(code)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        # Check for suspicious imports
        for imp in imports:
            if imp.startswith("..") or imp.startswith("/"):
                issues.append({
                    "type": "warning",
                    "message": f"Suspicious import path: {imp}"
                })
                score -= 10
        
        score = 100 - len(issues) * 10
        
    except:
        score = 0
        
    return {"issues": issues, "score": max(0, score)}

def run_simple_tests(code: str, test_cases: List[Dict]) -> Dict[str, Any]:
    """运行简单测试"""
    issues = []
    passed = 0
    failed = 0
    
    # Create a safe execution environment
    safe_globals = {
        "__builtins__": {
            "print": print,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
        }
    }
    
    for tc in test_cases:
        try:
            # Compile the code first
            compiled = compile(code, "<test>", "exec")
            
            # Create a local namespace for execution
            local_ns = {}
            
            # Execute the code
            exec(compiled, safe_globals, local_ns)
            
            # Try to find and run a test function
            if "test" in local_ns:
                result = local_ns["test"](tc.get("input"))
                if result == tc.get("expected"):
                    passed += 1
                else:
                    failed += 1
                    issues.append({
                        "type": "error",
                        "message": f"Test failed: expected {tc.get('expected')}, got {result}"
                    })
            else:
                passed += 1  # No test function, assume pass
                
        except Exception as e:
            failed += 1
            issues.append({
                "type": "error",
                "message": f"Runtime error: {str(e)}"
            })
    
    score = 100 - failed * 20
    return {
        "issues": issues, 
        "score": max(0, score),
        "passed": passed,
        "failed": failed
    }

def evaluate_code(code: str, test_type: str = "syntax", test_cases: List = None) -> Dict[str, Any]:
    """主评估函数"""
    results = {
        "pass": False,
        "score": 0,
        "issues": [],
        "test_type": test_type
    }
    
    total_score = 0
    weights = {"syntax": 1.0, "import": 0.5, "unit": 1.0}
    
    if test_type in ["syntax", "full"]:
        syntax_result = check_python_syntax(code)
        results["issues"].extend(syntax_result["issues"])
        total_score += syntax_result["score"] * weights["syntax"]
    
    if test_type in ["import", "full"]:
        import_result = check_imports(code)
        results["issues"].extend(import_result["issues"])
        total_score += import_result["score"] * weights["import"]
    
    if test_type in ["unit", "full"] and test_cases:
        unit_result = run_simple_tests(code, test_cases)
        results["issues"].extend(unit_result["issues"])
        results["passed"] = unit_result.get("passed", 0)
        results["failed"] = unit_result.get("failed", 0)
        total_score += unit_result["score"] * weights["unit"]
    
    # Normalize score
    weight_sum = 0
    if test_type in ["syntax", "full"]: weight_sum += weights["syntax"]
    if test_type in ["import", "full"]: weight_sum += weights["import"]
    if test_type in ["unit", "full"] and test_cases: weight_sum += weights["unit"]
    
    results["score"] = int(total_score / weight_sum) if weight_sum > 0 else 0
    results["pass"] = results["score"] >= 70
    
    return results

def main():
    parser = argparse.ArgumentParser(description="SWE-Bench Lite Code Evaluator")
    parser.add_argument("--code", type=str, help="Code to evaluate")
    parser.add_argument("--file", type=str, help="File containing code to evaluate")
    parser.add_argument("--test-type", type=str, default="syntax", 
                       choices=["syntax", "import", "unit", "full"],
                       help="Type of test to run")
    parser.add_argument("--test-cases", type=str, help="JSON array of test cases")
    parser.add_argument("--codex", action="store_true", help="Codex mode - accept code from stdin")
    
    args = parser.parse_args()
    
    # Get code
    code = args.code
    if args.file:
        with open(args.file, "r") as f:
            code = f.read()
    elif args.codex:
        code = sys.stdin.read()
    
    if not code:
        print(json.dumps({"error": "No code provided"}))
        sys.exit(1)
    
    # Parse test cases
    test_cases = None
    if args.test_cases:
        try:
            test_cases = json.loads(args.test_cases)
        except:
            test_cases = None
    
    # Run evaluation
    result = evaluate_code(code, args.test_type, test_cases)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
