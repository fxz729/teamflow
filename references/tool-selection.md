# Tool Selection Heuristics

## Subagent 工具选择

### Read-Only Tasks

**优先工具**：`Read`, `Glob`, `Grep`, `Bash`（只读命令）

**场景**：
- 代码探索
- 文档阅读
- 信息查询
- 日志分析

### Write-Heavy Tasks

**优先工具**：`Write`, `Edit`

**限制**：每个 worker 最多 2 个 write-heavy 任务（防止冲突）

**场景**：
- 文件创建
- 代码修改
- 配置更新

### Mixed Tasks

**组合模式**：Read → Analyze → Write

**流程**：
1. Read 读取上下文
2. 分析需求
3. Write 输出结果

---

## Parallel Execution Patterns

### IO-Bound (推荐并行)

```markdown
并行执行：
- @worker-a: 抓取网页 A
- @worker-b: 抓取网页 B
- @worker-c: 抓取网页 C

结果汇总 → reviewer 审查
```

### CPU-Bound (谨慎并行)

```markdown
按批次执行：
- Batch 1: [worker-a, worker-b, worker-c] 各自编译
- 等待全部完成
- Batch 2: [worker-d, worker-e] 各自测试

原因：编译产物可能被其他 worker 需要
```

---

## Conflict Prevention

### 同一文件多人编辑

**规则**：同一文件最多 1 个 worker 处理

**检测**：
```
任务拆分时检查：
if (file in multiple_tasks) → 合并到同一 worker
```

### 竞态条件

**场景**：Worker A 读文件 → Worker B 写同一文件

**解决**：
1. 读任务在写任务前完成
2. 或者合并到同一 worker

---

## Tool Capability Matrix

| 任务类型 | 推荐工具 | 限制 |
|---------|---------|------|
| 搜索代码 | Grep, Glob | 无 |
| 读取文件 | Read | 无 |
| 执行命令 | Bash | 只读命令优先 |
| 创建文件 | Write | 最多 2 个/worker |
| 修改文件 | Edit | 最多 2 个/worker |
| 网络请求 | fetch, firecrawl | 无 |
| 浏览器操作 | playwright | 无 |
