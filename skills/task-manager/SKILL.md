# Task Manager - 任务管理系统

本地文件驱动的任务管理系统，让 AI 助理像员工一样领任务、执行、汇报。

## 触发条件

当用户需要：
- 添加/查看/管理任务
- 执行定时任务
- 查看任务执行历史

## 数据文件

```
workspace/tasks/
├── tasks.json    # 任务数据库
└── log.md        # 执行日志
```

## tasks.json 结构

```json
{
  "tasks": [
    {
      "id": "task-001",
      "name": "任务名称",
      "type": "seedance|news|tiktok|message|custom",
      "description": "任务描述",
      "schedule": "once|daily|hourly|weekly",
      "scheduleTime": "09:00",
      "status": "pending|running|completed|failed",
      "enabled": true,
      "createdAt": "2026-02-14",
      "lastRun": "2026-02-14 09:00",
      "lastResult": "执行结果摘要",
      "config": {}
    }
  ]
}
```

## 任务类型

| 类型 | 说明 | 执行方式 |
|------|------|----------|
| `seedance` | 生成 Seedance 视频提示词 | 调用 seedance-prompt-generator skill |
| `news` | 采集 AI/科技新闻 | 调用 technews 或 web_search |
| `tiktok` | TikTok 趋势监控 | 调用 tiktok-thailand-trends skill |
| `message` | 发送通知消息 | 直接发送 Discord 消息 |
| `custom` | 自定义任务 | 根据 config 执行 |

## 操作指南

### 查看所有任务

读取 `tasks/tasks.json`，列出所有任务及状态。

### 添加新任务

1. 读取 `tasks/tasks.json`
2. 生成新任务 ID（格式：`task-XXX`）
3. 添加任务对象到 `tasks` 数组
4. 写回文件

**必填字段：**
- `id`: 唯一标识
- `name`: 任务名称
- `type`: 任务类型
- `schedule`: 执行频率
- `status`: 初始为 `pending`
- `enabled`: 是否启用

### 执行任务

1. 检查 `status === "pending"` 且 `enabled === true`
2. 检查是否到达执行时间
3. 更新 `status` 为 `running`
4. 执行对应类型的操作
5. 更新 `status` 为 `completed` 或 `failed`
6. 记录 `lastRun` 和 `lastResult`
7. 写入 `log.md`

### 定时检查（Heartbeat/Cron）

在 heartbeat 或 cron 中：

1. 读取 `tasks/tasks.json`
2. 筛选需要执行的任务：
   - `enabled === true`
   - `status === "pending"`
   - 到达执行时间
3. 依次执行
4. 汇报结果

## 执行时间判断

### daily（每天）
```javascript
// 检查今天是否已执行
const today = new Date().toISOString().split('T')[0]
const needsRun = !task.lastRun || !task.lastRun.startsWith(today)
```

### hourly（每小时）
```javascript
// 检查本小时是否已执行
const now = new Date()
const currentHour = now.toISOString().slice(0, 13) // "2026-02-14T09"
const needsRun = !task.lastRun || !task.lastRun.startsWith(currentHour)
```

### weekly（每周）
```javascript
// 检查本周是否已执行（周一为起点）
const getWeekStart = (date) => {
  const d = new Date(date)
  const day = d.getDay()
  const diff = d.getDate() - day + (day === 0 ? -6 : 1)
  return new Date(d.setDate(diff)).toISOString().split('T')[0]
}
const needsRun = !task.lastRun || getWeekStart(task.lastRun) !== getWeekStart(new Date())
```

### once（单次）
```javascript
const needsRun = !task.lastRun && task.status === "pending"
```

## 日志记录

每次执行后，追加到 `log.md`：

```markdown
### [2026-02-14 09:00] 任务执行
- **任务：** 每日 AI 新闻采集
- **类型：** news
- **状态：** ✅ 成功
- **结果：** 采集 10 条新闻，已推送到 Discord
```

## 汇报格式

执行完所有任务后，汇总发送：

```markdown
## 📋 任务执行报告

**执行时间：** 2026-02-14 09:00

### ✅ 已完成
- [task-001] 每日 AI 新闻采集
- [task-002] TikTok 趋势监控

### ⏳ 待执行
- [task-003] 周报生成（下次：周一）

### ❌ 失败
- （无）
```

## 与 Cron 集成

可以设置 cron 定时触发任务检查：

```json
{
  "name": "任务系统检查",
  "schedule": { "kind": "cron", "expr": "0 * * * *" },
  "payload": { 
    "kind": "agentTurn", 
    "message": "检查并执行待办任务，完成后汇报结果" 
  },
  "sessionTarget": "isolated"
}
```

## 示例任务配置

### Seedance 视频脚本任务
```json
{
  "id": "task-seedance-001",
  "name": "生成产品展示视频脚本",
  "type": "seedance",
  "description": "为新产品生成 Seedance 视频提示词",
  "schedule": "once",
  "status": "pending",
  "enabled": true,
  "config": {
    "topic": "智能手表产品展示",
    "style": "科技感",
    "duration": 15
  }
}
```

### 每日新闻采集任务
```json
{
  "id": "task-news-001",
  "name": "每日 AI 新闻",
  "type": "news",
  "description": "采集 AI 领域最新资讯",
  "schedule": "daily",
  "scheduleTime": "09:00",
  "status": "pending",
  "enabled": true,
  "config": {
    "sources": ["technews"],
    "count": 5
  }
}
```
