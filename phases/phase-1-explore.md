# Phase 1: 并行探索

## 概述

Phase 1 是 Teamflow 工作流的第一个执行阶段，核心目标是**多视角独立探索**。

## 触发条件

- 任务被分类为 B 类（信息整合）或 C 类（可执行规划）
- 用户未要求跳过 Phase 2

## 执行模型

```
Phase 1: Worker-A → 初步结论 A
Phase 1: Worker-B → 初步结论 B
Phase 1: Worker-C → 初步结论 C
         ↓（并行，≤3 个 worker）
```

## Worker 分配规则

### 分配原则

1. **文件级锁定**：同一文件最多分配给 1 个 worker
2. **依赖优先**：有依赖关系的子任务，分配给同一 worker 或串行执行
3. **专业匹配**：根据子任务的专业领域匹配 worker 角色
4. **负载均衡**：尽量让各 worker 的工作量均衡

### 分配算法

```
输入：子任务列表 T = [t1, t2, ..., tn]
输入：worker 列表 W = [worker-a, worker-b, worker-c]

1. 分析每个子任务的：
   - 涉及文件（用于检测冲突）
   - 专业领域（用于匹配）
   - 依赖关系（用于排序）

2. 冲突检测：
   for each file in all_task_files:
       if file appears in multiple tasks:
           merge these tasks into single worker

3. 分配执行：
   available_workers = W
   for task in sorted_by_dependencies(T):
       worker = select_least_loaded_worker(available_workers)
       assign task to worker
```

## Worker 执行要求

### 执行日志格式

```markdown
## Execution Log

### 元信息
- **时间戳**：ISO 8601 格式
- **Worker ID**：worker-a / worker-b / worker-c
- **任务 ID**：唯一标识符
- **Phase**：Phase 1
- **状态**：STARTED / PROGRESS / COMPLETED / FAILED

### 执行记录
| 时间 | 事件 | 详情 |
|------|------|------|
| HH:MM:SS | 任务开始 | 接收到任务描述 |
| HH:MM:SS | 关键决策 | [决策内容] |
| HH:MM:SS | 任务完成 | [输出摘要] |

### 错误记录（如果有）
| 时间 | 错误类型 | 详情 | 重试次数 |
|------|---------|------|----------|
| HH:MM:SS | [类型] | [详情] | [n] |
```

### Worker Prompt 模板

```
你是执行专家。完成分配给你的子任务：

任务：{assigned_task}
验收标准：{acceptance_criteria}
任务类型：{B/C}

执行要求：
1. 直接执行，不调用 subagent
2. **必须包含推理链条**——输出你的思考过程，而非只给结论
3. 完成后报告结果和输出摘要
4. 遇到阻塞时说明原因
5. 不要修改其他 worker 的输出文件

输出格式：
## 推理链条
[你的思考过程，从接收到任务的第一个想法到最终结论]

## 执行结果
[你完成了什么]

## 关键洞察
[在这个过程中发现的核心洞见]
```

## 批次调度

### Barrier 规则

批次间的 barrier 同步条件：

| Barrier 类型 | 触发条件 | 超时动作 | 超时时间 |
|-------------|---------|----------|----------|
| All-complete | 批次内所有 worker 完成 | 强制进入下一批次 | 5 分钟 |
| 文件锁释放 | 所有文件锁释放 | 警告并继续 | 2 分钟 |

### 批次执行伪代码

```
batches = partition_tasks(tasks, max_size=3)
for batch in batches:
    start_time = now()

    # 并行执行批次内任务
    parallel_execute(batch.workers)

    # 等待 barrier 条件
    wait_for_barrier(batch, timeout=batch_timeout)

    if barrier_timeout:
        log_warning(f"Batch {batch.id} barrier timeout")
        force_proceed_to_next_batch()

# 如果批次总数超时
if total_timeout:
    force_convergence()
```

## 超时处理

| 场景 | 超时阈值 | 超时后动作 |
|------|----------|------------|
| 单个 Worker | 5 分钟 | 重试一次，仍失败则 solo 接手 |
| 批次执行 | 5 分钟 | 强制进入下一批次 |
| 整体 Phase 1 | 15 分钟 | 强制进入 Phase 2 |

## 输出要求

Phase 1 完成后，每个 Worker 应输出：

1. **推理链条**：完整的思考过程
2. **执行结果**：具体完成了什么
3. **关键洞察**：核心发现
4. **状态报告**：STARTED → PROGRESS → COMPLETED

## 与 Phase 2 的衔接

Phase 1 输出将传递给 Phase 2（对抗质疑）：

```
Phase 1 输出
    ↓
Phase 2 Challenger 读取
    ↓
Challenger 提出质疑
    ↓
原 Worker 回应
```

## 相关文档

- Agent Prompt 模板：[../references/agent-prompts.md](../references/agent-prompts.md)
- 工作流示例：[../references/workflow-examples.md](../references/workflow-examples.md)
