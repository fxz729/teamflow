# Teamflow

**智能任务编排框架 for Claude Code** — 让正确的方式处理正确的任务。

```
🤖 Claude Code Skill    📦 4 Files    🔀 Solo / Progressive Parallel / Solo-Deep
```

> 不是所有任务都适合拆分并行。Teamflow 是你思考的路由器，不是并行工具箱。

---

## 核心问题

当你让 AI 思考"人生意义"这样的问题时，如果它拆成三个 agent 并行思考——最终只会得到三段孤立的碎片，而非连贯的深度洞见。

**原因：某些思维过程本质上是串行的、不可拆分的。**

Teamflow 的核心判断：**不是所有任务都适合拆分并行**。它根据任务类型，自动选择最合适的处理策略。

---

## 核心设计

### 任务类型分类体系

| 类型 | 名称 | 特征 | 正确策略 |
|:---:|------|------|----------|
| **A** | 开放性思辨 | 意义、价值、伦理、哲学 | **Solo-Deep** — 禁用并行，单 agent 深度推理 |
| **B** | 信息整合 | 分析、对比、综述、调研 | **渐进式并行** — 收集后收敛 |
| **C** | 可执行规划 | 开发、设计、构建、修复 | **标准 teamflow** — 工程任务才用 team |
| **D** | 简单执行 | 单文件、<50行修改 | **Solo** — 直接搞定 |

### 三种执行模式

#### Solo-Deep
主 agent 深度推理，不拆分，不预设框架，保留完整推理链。

```
用户: "使用 teamflow 思考人生意义"
    ↓
检测到 A 类关键词（意义）
    ↓
Solo-Deep 模式
• 不拆分任务
• 不预设视角框架
• 深度推理 → 输出推理链条
```

#### 渐进式并行
三阶段递进结构，不是简单的平面并行。

```
Phase 1（并行）：多视角独立探索
    ├── Agent-A → 初步结论 A
    ├── Agent-B → 初步结论 B
    └── Agent-C → 初步结论 C
        ↓
Phase 2（对抗）：交叉质疑
    ├── 挑战者 → 质疑 A/B/C 的漏洞
    └── Agent-A/B/C 回应
        ↓
Phase 3（收敛）：综合洞见
    └── 主 agent 整合交锋，输出超越原始视角的洞见
```

**Phase 2 的价值**：让结论互相碰撞，在裂缝中诞生真正的洞见。

#### 标准 Teamflow
Plan → Worker（≤3 并发）→ Reviewer，适合 C 类工程任务。

---

## 一键安装

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

---

## 文件结构

```
teamflow/
├── SKILL.md                        # 主 skill 文件
├── install.sh                      # 一键安装脚本 (macOS/Linux/Git Bash)
├── install.ps1                     # 一键安装脚本 (Windows PowerShell)
└── references/
    ├── routing-rules.md            # 任务分类与路由规则
    ├── agent-prompts.md            # Agent 指令模板
    └── tool-selection.md           # 工具选择策略
```

---

## 什么时候用

| 场景 | 推荐模式 |
|------|----------|
| 思考人生意义、伦理判断、价值观探索 | Solo-Deep |
| 市场调研、竞品分析、多方资料整合 | 渐进式并行 |
| 功能开发、bug 修复、架构设计 | 标准 teamflow |
| 单文件编辑、简单问答 | Solo |

---

## License

MIT
