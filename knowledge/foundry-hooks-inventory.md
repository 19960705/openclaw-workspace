# Foundry Hooks 清单

**更新日期**: 2026-02-26
**总计**: 14 个 hooks

## 当前活跃 Hooks

| # | 文件名 | 类型 | 工具 | 说明 |
|---|--------|------|------|------|
| 1 | auto-retry-fallback-handler.ts | auto | all | 自动重试 fallback 处理 |
| 2 | auto_crystallized_cron_1771399143981.ts | auto | cron | Cron 自动结晶 |
| 3 | auto_crystallized_cron_1771399164532.ts | auto | cron | Cron 自动结晶 |
| 4 | auto_crystallized_cron_1771399230329.ts | auto | cron | Cron 自动结晶 |
| 5 | auto_token_refresh.ts | auto | token | Token 刷新 |
| 6 | crystallized_browser_1772074774039.ts | manual | browser | 手动结晶 - browser 失败处理 |
| 7 | rise_crystallized_browser_1772004414206.ts | rise | browser | RISE 自动结晶 |
| 8 | rise_crystallized_edit_1771880396809.ts | rise | edit | 编辑失败处理 |
| 9 | rise_crystallized_message_1771645942217.ts | rise | message | 消息失败处理 |
| 10 | rise_crystallized_read_1771769469557.ts | rise | read | 读取失败处理 |
| 11 | rise_crystallized_web_fetch_1771668102543.ts | rise | web_fetch | Web 获取失败处理 |
| 12 | rise_crystallized_web_search_1771593863911.ts | rise | web_search | 搜索失败处理 |
| 13 | rise_crystallized_web_search_1771775759501.ts | rise | web_search | 搜索失败处理 |
| 14 | rise_crystallized_web_search_1771920973254.ts | rise | web_search | 搜索失败处理 |

## 清理记录 (2026-02-26)

删除了 12 个重复的 browser hooks:
- rise_crystallized_browser_*.ts (10个)
- auto_crystallized_browser_*.ts (1个)
- 原因: 同一错误模式被重复结晶多次

## 待处理

- Gateway token mismatch (6x) - 历史遗留错误，当前 gateway 正常运行
