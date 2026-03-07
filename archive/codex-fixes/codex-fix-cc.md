# 任务：修复 OpenClaw 中 codex 工具调用问题

## 背景
在 OpenClaw 中使用 `xiamai/gpt-5.3-codex` 模型时，模型只回复纯文本，不调用任何工具。

## 已知信息
### 1. codex API 本身支持工具调用
我们直接用 curl 测试过：
```bash
curl -X POST http://ai.xiamai.top/v1/responses \
  -H "Authorization: Bearer sk-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.3-codex",
    "input": [
      {
        "type": "message",
        "role": "user",
        "content": [{ "type": "input_text", "text": "Calculate 123 * 456" }]
      }
    ],
    "tools": [...]
  }'
```
可以正常返回 `function_call`。

### 2. 当前 OpenClaw 配置
- API 类型：`openai-responses`
- 模型：`xiamai/gpt-5.3-codex`
- Base URL：`http://ai.xiamai.top`
- 问题：模型只回复纯文本，不调用工具

### 3. 官方文档要求的请求格式
```json
{
  "model": "gpt-5.2",
  "input": [
    {
      "type": "message",
      "role": "developer",
      "content": [
        { "type": "input_text", "text": "..." }
      ]
    }
  ]
}
```
关键：使用 `input` 数组，每个消息有 `type` 字段，content 是数组，每个内容块有 `type` 字段。

## 你需要做的
1. 找到 OpenClaw 中处理 `openai-responses` API 类型的代码
   - 位置：`/Users/mac/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/dist/`
   - 搜索关键词：`openai-responses`
2. 查看它实际发送的请求格式
3. 修改代码，让它发送正确的格式（`input` 数组 + `type` 字段）
4. 或者确认是否应该用 `openai-codex-responses` 而不是 `openai-responses`

## 官方文档
http://ai.xiamai.top/docs/codex#sec-lfdolrk
