# Teamflow

**智能 Agent Team 编排框架 for Claude Code** — 一句话，启动专业团队。

```
🤖 Claude Code Skill    📦 11 Files    🔀 3-Phase Agent Team
```

> 只需说"使用 teamflow + 你的任务"，剩下的交给框架。

---

## 一句话说明

Teamflow 让 Claude Code 的 agent team 从"能用"变成"用好"：
- 输入模糊？→ 自动拆解任务
- 并行冲突？→ Phase 2 对抗质疑
- 结论散乱？→ Phase 3 收敛整合

**不需要懂 agent、懂并行、懂调度——只需要一个任务描述。**

---

## 任务类型分类

| 类型 | 名称 | 特征关键词 | 正确策略 |
|:---:|------|-----------|----------|
| **A** | 开放性思辨 | 意义、价值、伦理、哲学、观点、感受 | **Solo-Deep** — 禁用并行，单 agent 深度推理 |
| **B** | 信息整合 | 分析、对比、综述、调研、收集、整理 | **渐进式并行** — 收集后收敛 |
| **C** | 可执行规划 | 开发、设计、实现、构建、修复、重构 | **标准 teamflow** — 工程任务才用 team |
| **D** | 简单执行 | 单文件、<50行修改、直接答案 | **Solo** — 直接搞定 |

### 分类决策树

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

## 三阶段执行模型

### Solo-Deep（适合 A 类任务）

主 agent 深度推理，不拆分，不预设框架，保留完整推理链。

### 渐进式并行（适合 B 类任务）

三阶段递进结构，不是简单的平面并行。

```
Phase 1（并行）：多视角独立探索
    ├── Agent-A → 初步结论 A
    ├── Agent-B → 初步结论 B
    └── Agent-C → 初步结论 C
        ↓
Phase 2（对抗）：交叉质疑
    ├── Challenger → 质疑 A/B/C 的漏洞
    └── Agent-A/B/C 回应
        ↓
Phase 3（收敛）：综合洞见
    └── 主 agent 整合交锋，输出超越原始视角的洞见
```

**Phase 2 的价值**：让结论互相碰撞，在裂缝中诞生真正的洞见。

### 标准 Teamflow（适合 C 类任务）

Plan → Worker（≤3 并发）→ Phase 2（可选）→ Reviewer，适合工程任务。

---

## 安装

### macOS / Linux / Git Bash（Windows）

```bash
curl -fsSL https://raw.githubusercontent.com/fxz729/teamflow/master/install.sh | bash
```

或克隆到本地：

```bash
git clone https://github.com/fxz729/teamflow.git ~/.claude/skills/teamflow
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/fxz729/teamflow/master/install.ps1 | iex
```

### 手动安装

1. 点击本仓库右上角 **Code → Download ZIP**
2. 解压到 Claude Code skills 目录：

| 系统 | 路径 |
|------|------|
| Windows | `C:\Users\<用户名>\.claude\skills\teamflow` |
| macOS | `~/.claude/skills/teamflow` |
| Linux | `~/.claude/skills/teamflow` |

---

## 使用方式

安装完成后，在 Claude Code 中直接说：

```
使用 teamflow [你的任务]
```

框架会自动判断任务类型并选择最佳模式。

### 示例

| 输入 | 触发的模式 |
|------|-----------|
| `使用 teamflow 思考人生意义` | Solo-Deep |
| `使用 teamflow 分析竞品产品的差异化策略` | 渐进式并行 |
| `使用 teamflow 重构项目中认证模块` | 标准 teamflow |
| `使用 teamflow 修复 config.json 中的拼写错误` | Solo |

---

## 文件结构

```
teamflow/
├── SKILL.md                        # 主 skill 文件
├── README.md                        # 本文件
├── install.sh                       # 一键安装脚本 (macOS/Linux/Git Bash)
├── install.ps1                      # 一键安装脚本 (Windows PowerShell)
├── .gitignore                      # Git 忽略配置
│
├── phases/                          # Phase 详细文档
│   ├── phase-1-explore.md          # Phase 1: 并行探索
│   ├── phase-2-challenge.md        # Phase 2: 对抗质疑
│   └── phase-3-converge.md         # Phase 3: 收敛整合
│
├── lib/                             # Python 实现
│   ├── __init__.py
│   └── routing_rules.py             # 任务分类逻辑（可独立运行测试）
│
├── references/                      # 参考文档
│   ├── routing-rules.md            # 任务分类规则（含 Python 实现引用）
│   ├── agent-prompts.md            # Agent 提示词模板
│   ├── tool-selection.md           # 工具选择策略
│   ├── workflow-examples.md        # B/C/D 类工作流示例库
│   └── validate_output.py           # Output Contract 验证脚本
│
└── benchmark/                       # 性能基准测试
    └── benchmark.py                # 基准测试脚本
```

---

## 核心特性

### 一句话启动团队

```
使用 teamflow 分析竞品数据
```

只需描述任务，框架自动完成：
1. 任务分类和拆解
2. Worker 并行执行
3. Challenger 对抗质疑
4. 收敛成最终结论

### Phase 2 对抗质疑

普通 agent team 的问题：三个 agent 各说各话，最后"礼貌性整合"。

Teamflow 的解法：让结论真正碰撞。
- Challenger 质疑每个结论的漏洞
- Worker 必须正面回应
- 最终结论经得起推敲

### 完整 Failure Recovery

| 场景 | 超时阈值 | 自动处理 |
|------|----------|----------|
| Worker 失败 | 5 分钟 | 重试 → solo 接手 |
| Plan 超时 | 2 分钟 | 主 agent 直接规划 |
| Challenger 无响应 | 3 分钟 | 跳过 Phase 2 |
| 整体卡住 | 15 分钟 | 强制收敛输出 |

### 标准化输出

每个阶段都有完整的推理链条，确保结论可追溯、可验证。

---

## 开发者工具

### 验证输出

```bash
python references/validate_output.py --file output.md
python references/validate_output.py --dir ./outputs/
```

### 运行基准测试

```bash
python benchmark/benchmark.py --type compare
```

---

## 什么时候用

| 场景 | 示例 |
|------|------|
| 需要多角度分析时 | "分析竞品数据"、"调研市场" |
| 需要开发功能时 | "实现用户认证"、"重构模块" |
| 需要深度思考时 | "思考这个架构的价值" |
| 简单任务 | "修复这个 bug"、"查一下这个错误" |

**通用规则**：不知道用什么模式时，直接说 `使用 teamflow + 你的任务`，框架会自动选择。

---

## License

MIT
