# OpenClaw Recurring Failures — 解决套路（待 crystallize）

> Last updated: 2026-03-02

本文件把近期高频失败（cron / browser）整理成“可执行的排障与修复步骤”，用于后续 `foundry_crystallize` 固化为自动化 hook/pattern。

---

## 1) cron:gateway closed → unauthorized: device token mismatch

### 典型现象
- cron 任务执行时，Gateway 连接目标 `ws://<ip>:<port>` 失败
- 报错包含：`unauthorized: device token mismatch`

### 常见原因
- Gateway 使用的 device token 与实际设备/节点 token 不一致（被旋转、重装、或配置文件被覆盖）
- 多环境/多实例导致 token 引用错位（旧 token 仍在 cron 环境里）

### 修复步骤（人工）
1. **定位 token 来源**
   - 检查 OpenClaw 配置（通常在 `~/.openclaw/openclaw.json`）里与 gateway/device 相关字段。
   - 如果有多个配置文件/多用户运行，确认 cron 使用的是同一用户、同一 HOME。
2. **rotate / reissue device token**
   - 重新签发并写回配置（以当前 Gateway 实例为准）。
3. **重启 gateway**
   - `openclaw gateway restart`
4. **验证**
   - 立刻手动跑一次对应 cron 的核心命令/脚本，确保不再出现 mismatch。

### 预防措施
- 统一 cron 的环境变量（HOME/PATH）与交互式 shell 保持一致。
- token 变更后，确保相关 cron 任务使用的配置文件同步更新。

---

## 2) browser: Can't reach the OpenClaw browser control service (timeout)

### 典型现象
- browser 工具超时：`Can't reach the OpenClaw browser control service (timed out ...)`

### 常见原因
- browser control server 未启动/已崩溃
- 本机端口被占用、被代理拦截或网络栈异常
- profile 使用错误（原则：优先 profile=`openclaw`）

### 修复步骤（人工）
1. **检查 browser 服务状态**
   - 先跑一次最小化调用：`browser status`（或在工具里直接 status）
2. **重启 browser 服务**
   - 若你有 watchdog：触发 watchdog 重启；否则手动 restart。
3. **验证 profile**
   - 统一用 `profile="openclaw"`，避免 chrome relay 不稳定。
4. **复测**
   - `browser open` 打开一个轻量 URL（如 about:blank 或 docs 页面）确认能 snapshot。

### 预防措施
- 保持 browser-watchdog 处于启用状态（自动恢复）。
- 对所有 browser 自动化：失败后先走“status→restart→retry（带 backoff）”固定策略。

---

## 下一步（建议）
- 先把上面两条按“可执行步骤 + 触发条件 + 验证方式”补齐到足够稳定。
- 然后用 `foundry_crystallize` 固化为 pattern/hook，避免未来反复出现同类故障。
