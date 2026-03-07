# 🔄 Evolution Loop - 自进化探索系统

基于 OpenClaw Evolution Framework 实现的自触发探索循环。

## 🎯 核心特性

- **自触发机制**: Agent 完成探索后自动启动下一轮，无需等待 cron
- **主题轮换**: 5 个主题加权随机选择，避免重复探索
- **HITL 检查点**: 第 10、20 轮暂停，等待人工确认
- **夜间静默**: 23:00-07:00 静默运行，不发送通知
- **配置驱动**: 通过 JSON 配置文件灵活调整

## 📦 安装

Hook 已创建在 `~/.openclaw/hooks/evolution-loop/`

```bash
# 启用 hook
openclaw hooks enable evolution-loop

# 验证
openclaw hooks list
```

## 🚀 使用

### 开始探索

```bash
# 在 OpenClaw 中发送命令
/evolve
```

### 配置主题

编辑 `evolution-config.json`:

```json
{
  "themes": [
    {
      "name": "主题名称",
      "description": "详细描述",
      "weight": 30
    }
  ],
  "max_duration_hours": 8,
  "interval_minutes": 10,
  "hitl_checkpoints": [
    { "round": 10, "pause": true }
  ],
  "night_mode": {
    "enabled": true,
    "quiet_hours": "23:00-07:00",
    "silent_delivery": true
  }
}
```

### 查看进度

```bash
# 查看当前状态
cat .evolution-state.json

# 查看探索结果
ls -la memory/evolution-round-*.md

# 查看最新一轮
cat memory/evolution-round-001.md
```

## 📊 工作流程

```
┌─────────────────────────────────────────┐
│ 用户发送 /evolve                         │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 1. 检查是否超时 (max_duration_hours)     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 2. 检查 HITL 检查点                      │
│    (如果到达检查点，暂停等待确认)         │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 3. 选择主题 (加权随机 + 避免重复)        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 4. 执行探索 (web_search + web_fetch)    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 5. 保存结果到 memory/evolution-round-*.md│
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 6. 自触发下一轮 (延迟 interval_minutes)  │
└─────────────────────────────────────────┘
```

## 🎨 主题配置

默认 5 个主题：

1. **AI Agent 架构** (30%) - 自进化架构、元编程、多 agent 协作
2. **工具生态** (25%) - MCP、A2A、工具集成
3. **安全机制** (20%) - 沙箱、审计、威胁检测
4. **实战案例** (15%) - GitHub workflows、OSINT、内容生成
5. **自由探索** (10%) - 未来趋势、跨领域应用

## 📈 输出格式

每轮探索生成一个 Markdown 文件：

```
memory/evolution-round-001.md
memory/evolution-round-002.md
...
```

文件结构：

```markdown
# 主题名称 (轮次 X)

## 探索提示

[Agent 收到的探索指令]

---

## 探索结果

[Agent 生成的洞察]
```

## 🔧 故障排除

### Hook 未触发

```bash
# 检查 hook 是否启用
openclaw hooks list

# 重新启用
openclaw hooks enable evolution-loop
```

### 配置文件错误

```bash
# 验证 JSON 格式
cat evolution-config.json | jq .

# 重置为默认配置
rm evolution-config.json
# 下次运行 /evolve 会自动创建
```

### 自触发失败

检查 `openclaw` CLI 是否在 PATH 中：

```bash
which openclaw
```

## 📚 参考

- [OpenClaw Evolution Framework](https://github.com/TerryFYL/openclaw-evolution-framework)
- [研究报告](memory/ai-evolution-research-2026-03-07.md)
- [配置文件](evolution-config.json)

## 🤝 贡献

欢迎提交改进建议！

---

**创建时间**: 2026-03-07  
**版本**: 1.0.0  
**状态**: ✅ 可用
