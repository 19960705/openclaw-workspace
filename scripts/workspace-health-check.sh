#!/bin/bash
# workspace-health-check.sh — 自动检查 workspace 健康状态
# 用于自由活动时间或定期维护

echo "🔍 Workspace Health Check - $(date '+%Y-%m-%d %H:%M')"
echo "================================================"

# 1. Cron 任务检查
echo ""
echo "📋 Cron 任务状态:"
if [ -f ~/.openclaw/cron/jobs.json ]; then
    python3 -c "
import json
with open('$HOME/.openclaw/cron/jobs.json') as f:
    data = json.load(f)
errors = 0
for j in data['jobs']:
    if not j.get('enabled', False):
        continue
    state = j.get('state', {})
    if state.get('consecutiveErrors', 0) > 0:
        errors += 1
        print(f'  ❌ {j[\"name\"]}: {state[\"consecutiveErrors\"]}x errors - {str(state.get(\"lastError\",\"\"))[:60]}')
    elif state.get('lastStatus') == 'error':
        errors += 1
        print(f'  ⚠️  {j[\"name\"]}: last run failed - {str(state.get(\"lastError\",\"\"))[:60]}')
if errors == 0:
    print('  ✅ 所有活跃任务正常')
print(f'  总计: {sum(1 for j in data[\"jobs\"] if j.get(\"enabled\", False))} 活跃 / {len(data[\"jobs\"])} 总计')
"
fi

# 2. 磁盘空间
echo ""
echo "💾 磁盘空间:"
du -sh ~/.openclaw/workspace 2>/dev/null | awk '{print "  Workspace: " $1}'
du -sh ~/.openclaw/workspace/memory 2>/dev/null | awk '{print "  Memory: " $1}'
du -sh ~/.openclaw/workspace/knowledge 2>/dev/null | awk '{print "  Knowledge: " $1}'
du -sh ~/.openclaw/workspace/archive 2>/dev/null | awk '{print "  Archive: " $1}'

# 3. Memory 文件数量
echo ""
echo "🧠 Memory 状态:"
echo "  主日志: $(ls ~/.openclaw/workspace/memory/2026-*.md 2>/dev/null | grep -v session-transcripts | wc -l | tr -d ' ') 个"
echo "  Transcripts: $(ls ~/.openclaw/workspace/memory/session-transcripts/*.md 2>/dev/null | wc -l | tr -d ' ') 个"
echo "  MEMORY.md: $(wc -l < ~/.openclaw/workspace/MEMORY.md 2>/dev/null | tr -d ' ') 行"

# 4. Git 状态
echo ""
echo "📦 Git 状态:"
cd ~/.openclaw/workspace
AHEAD=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "?")
echo "  未推送 commits: $AHEAD"
DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
echo "  未提交文件: $DIRTY"

# 5. 敏感文件检查
echo ""
echo "🔒 安全检查:"
if git log --all --diff-filter=A --name-only --pretty=format: 2>/dev/null | grep -q "\.env"; then
    echo "  ⚠️  .env 文件在 git history 中"
else
    echo "  ✅ 无敏感文件泄露"
fi

echo ""
echo "================================================"
echo "✅ 检查完成"
