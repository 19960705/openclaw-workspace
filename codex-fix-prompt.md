# 任务：修复 OpenClaw 中 codex 工具调用问题

## 问题
在 OpenClaw 中使用 `xiamai/gpt-5.3-codex` 模型时，模型只回复纯文本，不调用任何工具。

## 已知
- codex API 本身支持工具调用（直接 curl 测试成功）
- OpenClaw 配置已正确（无 Invalid input 错误）
- 问题：OpenClaw 发送的请求格式不对

## 你的任务
1. 查看 OpenClaw 源码（位于 `/Users/mac/.nvm/versions/node/v22.12.0/lib/node_modules/openclaw/dist/`）
2. 找到处理 `openai-responses` API 类型的代码
3. 找出它发送的请求格式
4. 对比官方文档要求的格式（`input` 数组 + `type` 字段）
5. 修复问题

## 官方文档
http://ai.xiamai.top/docs/codex#sec-lfdolrk

## 官方文档要求的请求格式
```json
{
  "model": "gpt-5.2",
  "input": [
    {
      "type": "message",
      "role": "developer",
      "content": [
        { "type": "input_text", "text": "123" }
      ]
    },
    {
      "type": "message",
      "role": "user",
      "content": [
        { "type": "input_text", "text": "456" }
      ]
    }
  ]
}
```

## 关键
- 使用 `input` 数组，不是 `messages`
- 每个消息有 `type` 字段（`"type": "message"`）
- `content` 是数组，每个内容块有 `type` 字段（`"type": "input_text"`）

现在开始！
