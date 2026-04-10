---
name: teamflow
description: "协调是否单兵作战还是使用subagent团队处理复杂任务。智能识别任务类型，优先为开放性思辨任务启用solo模式，为可拆分任务启用渐进式team模式。"
---

# Teamflow

## 核心设计原则

Teamflow 不是"强制并行框架"，而是"思考策略路由器"。其核心判断：**不是所有任务都适合拆分并行。**

---

## 任务类型分类

| 类型 | 特征关键词 | 适合模式 |
|------|-----------|---------|
| **A. 开放性思辨** | 意义、价值、应该、真相、美、灵魂、伦理、哲学、观点、感受 | **Solo-Deep** |
| **B. 信息整合** | 分析、对比、综述、报告、收集、整理、多方汇总 | **渐进式并行** |
| **C. 可执行规划** | 开发、设计、实现、构建、修复、创建功能 | **标准teamflow** |
| **D. 简单执行** | 单文件编辑、<50行修改、直接答案、小工具 | **Solo** |

### 分类决策规则

```
统计所有类型关键词命中数量：
├── A 类命中 ≥ 1 → Solo-Deep（A 类最高优先级）
├── A 类未命中，B 类和 C 类同时命中
│   ├── B 类命中数 > C 类命中数 → 渐进式并行
│   └── B 类命中数 ≤ C 类命中数 → 标准 teamflow
├── 仅 B 类命中 → 渐进式并行
├── 仅 C 类命中 → 标准 teamflow
└── A/B/C 都不命中 → 评估 D 类或复杂度
```

---

## 执行流程

### Solo-Deep 模式（A 类）
```
用户输入 → 检测到 A 类关键词 → 主 agent 深度推理 → 输出推理链条
```

### Team 模式（B/C 类）
```
用户输入
    ↓
任务分类（自动判断）
    ↓
Prompt-Engineer 生成专业提示词（替换原始输入）
    ↓
任务拆分 + 批次规划
    ↓
Phase 1: Worker-A / B / C 并行探索
    ↓
Phase 2: Challenger 对抗质疑（可选）
    ↓
Phase 3: Reviewer 收敛整合
    ↓
最终结论
```

---

## 三阶段模型

### Phase 1：并行探索
- 最多 3 个 Worker 并行
- 每个 Worker 独立执行子任务
- 必须保留推理链条

### Phase 2：对抗质疑
- 1 个 Challenger 质疑 Phase 1 输出
- 原 Worker 回应
- **启用条件**：
  - Phase 1 有 3+ agent 输出
  - 任务涉及多个专业领域
  - Phase 1 输出存在明显分歧
  - 任务涉及高风险决策

### Phase 3：收敛整合
- Reviewer 最终审查
- 主 agent 综合所有交锋
- 输出超越原始视角的洞见

---

## 并发设计

| Phase | Agent 类型 | 并发数 |
|-------|-----------|--------|
| Phase 1 | Worker-A/B/C | ≤ 3 |
| Phase 2 | Challenger | 1（独立 pool）|
| Phase 3 | 主 agent | N/A |

---

## Failure Recovery

| 场景 | 超时阈值 | 超时后动作 |
|------|----------|------------|
| 单个 Worker | 5 分钟 | 重试一次，失败则 solo 接手 |
| Plan agent | 2 分钟 | 降级为直接执行 |
| Phase 2 Challenger | 3 分钟 | 跳过 Phase 2 |
| 整体执行 | 15 分钟 | 强制收敛 |

---

## Output Contract

### Solo-Deep 模式输出
```markdown
## 深度思考
### 推理链条
### 核心洞察
### 可能的争议点
```

### Team 模式输出
```markdown
## Team Execution Summary
### 任务类型
### 执行阶段
### Phase 1 输出摘要
### Phase 2 质疑与回应
### 最终结论
---
**Reviewer 最终整合**
```

---

## 引用文档

| 文档 | 说明 |
|------|------|
| [phases/phase-1-explore.md](phases/phase-1-explore.md) | Phase 1 详细流程 |
| [phases/phase-2-challenge.md](phases/phase-2-challenge.md) | Phase 2 详细流程 |
| [phases/phase-3-converge.md](phases/phase-3-converge.md) | Phase 3 详细流程 |
| [references/routing-rules.md](references/routing-rules.md) | 任务分类规则 |
| [references/agent-prompts.md](references/agent-prompts.md) | Agent 提示词模板 |
| [references/workflow-examples.md](references/workflow-examples.md) | 工作流示例库 |
| [references/tool-selection.md](references/tool-selection.md) | 工具选择策略 |
| [references/validate_output.py](../references/validate_output.py) | 输出验证脚本 |
| [lib/routing_rules.py](../lib/routing_rules.py) | 分类逻辑 Python 实现 |

---

## 自检清单

使用 teamflow 前，请确认：
- [ ] 任务是否包含 A 类关键词？（如果是，强制 Solo-Deep）
- [ ] 任务是否同时包含 B 类和 C 类关键词？（如果是的，进行计数比较）
- [ ] 子任务数是否 ≤ 3？（如果否，需要批次调度）
- [ ] Phase 2 启用条件是否满足？

---

**最后更新**：2026-04-11（模块化重构）
