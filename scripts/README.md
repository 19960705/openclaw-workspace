# Scripts 目录说明

这个目录包含各种自动化脚本和工具。

## 🌟 推荐使用

### AI日报增强版
- **`ai-daily-enhanced-v2.sh`** ⭐⭐⭐⭐⭐
  - 最新版本，包含重要性分析 + 智能去重
  - 使用：`bash scripts/ai-daily-enhanced-v2.sh`
  - 文档：`docs/ai-daily-enhancement-guide.md`

- **`ai-daily-enhanced.sh`**
  - v1.0 版本，仅包含重要性分析
  - 推荐使用 v2.0

### 系统维护
- **`workspace-health-check.sh`**
  - 检查 workspace 健康状态
  - 使用：`bash scripts/workspace-health-check.sh`

- **`recurring-failure-guard.sh`**
  - 检测和处理重复失败
  - 使用：`bash scripts/recurring-failure-guard.sh gateway`
  - 使用：`bash scripts/recurring-failure-guard.sh browser`

## 📁 完整列表

### AI 相关
- `ai-daily-enhanced.sh` - AI日报增强版 v1.0
- `ai-daily-enhanced-v2.sh` - AI日报增强版 v2.0 (推荐)
- `integrate-ai-daily-enhancement.sh` - AI日报集成脚本

### 系统工具
- `workspace-health-check.sh` - Workspace 健康检查
- `recurring-failure-guard.sh` - 重复失败检测

### 其他
- 其他脚本根据需要使用

## 🔧 使用技巧

### 给脚本添加执行权限
```bash
chmod +x scripts/your-script.sh
```

### 查看脚本内容
```bash
cat scripts/your-script.sh
```

### 测试脚本
```bash
bash scripts/your-script.sh  # 直接运行
```

## 📝 添加新脚本

1. 创建脚本文件：`scripts/your-script.sh`
2. 添加 shebang：`#!/bin/bash`
3. 添加说明注释
4. 添加执行权限：`chmod +x scripts/your-script.sh`
5. 更新这个 README

## 🆘 故障排除

### 权限错误
```bash
chmod +x scripts/your-script.sh
```

### 找不到命令
确保脚本路径正确：
```bash
bash /Users/mac/.openclaw/workspace/scripts/your-script.sh
```

---

**最后更新**：2026-03-11  
**维护者**：Keonho (自由时间自动化)
