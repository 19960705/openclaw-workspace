# HEARTBEAT.md

## 任务检查

每次 heartbeat 时：

1. 读取 `tasks/tasks.json`
2. 检查是否有待执行的任务（enabled + pending + 到达执行时间）
3. 如果有，执行并汇报
4. 如果没有，回复 HEARTBEAT_OK
