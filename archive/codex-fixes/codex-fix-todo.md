# Codex 工具调用问题修复任务

## 问题现象
- 在 OpenClaw 中切换到 `xiamai/gpt-5.3-codex` 后，模型只回复纯文本，不调用任何工具
- 但直接通过 curl 调用 xiamai 的 `/v1/responses` API 时，codex 可以正常返回 `function_call`

## 当前配置（openclaw.json）
```json
{
  "models": {
    "providers": {
      "xiamai": {
        "baseUrl": "http://ai.xiamai.top/v1",
        "apiKey": "sk-...",
        "auth": "api-key",
        "api": "openai-responses",
        "authHeader": true,
        "models": [
          {
            "id": "gpt-5.3-codex",
            "name": "GPT 5.3 Codex",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 400000,
            "maxTokens": 128000
          }
        ],
        "headers": {
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) OpenClaw/2026.2.14",
          "Accept": "application/json"
        }
      }
    }
  }
}
```

## 官方文档要求的请求格式（Responses API）
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

## 可能的问题
- OpenClaw 在用 `openai-responses` API 类型时，可能发送的是 Chat Completions 格式（`messages` 数组），而不是 codex 期望的 Responses API 格式（`input` 数组，带 `type` 字段）

## 官方文档地址
http://ai.xiamai.top/docs/codex#sec-lfdolrk

## 你需要做的
1. 研究 OpenClaw 源码中 `openai-responses` API 类型的实现
2. 找出它发送的请求格式
3. 修改代码，让它对 codex 发送正确的 Responses API 格式（`input` 数组 + `type` 字段）
4. 或者确认是否应该用其他 API 类型（`openai-codex-responses`？）
