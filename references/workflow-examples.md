# Teamflow 工作流示例库

> 收录 B/C 类任务的完整工作流示例，供实际执行参考。

---

## B 类示例（信息整合）

### B-1: 竞品分析报告

**输入**: `"使用 teamflow 对比分析竞品 A、B、C 的差异化策略"`

```yaml
/workflow competitive_analysis {
  metadata:
    type: B
    mode: parallel
  
  phase classify {
    // 主 agent 自动分类：B 类（对比分析）
  }
  
  phase explore {
    concurrent: 3
    timeout: 300
    
    /spawn worker-a:general-purpose """
      任务：分析竞品 A 的核心差异化策略
      
      要求：
      1. 识别竞品 A 的市场定位
      2. 分析其核心竞争优势
      3. 评估其定价策略
      4. 输出结构化分析报告
    """
    
    /spawn worker-b:general-purpose """
      任务：分析竞品 B 的核心差异化策略
      
      要求：
      1. 识别竞品 B 的市场定位
      2. 分析其核心竞争优势
      3. 评估其定价策略
      4. 输出结构化分析报告
    """
    
    /spawn worker-c:general-purpose """
      任务：分析竞品 C 的核心差异化策略
      
      要求：
      1. 识别竞品 C 的市场定位
      2. 分析其核心竞争优势
      3. 评估其定价策略
      4. 输出结构化分析报告
    """
    
    /await all
  }
  
  phase challenge {
    concurrent: 1
    timeout: 180
    
    /spawn challenger:security-reviewer """
      任务：质疑竞品分析中的假设和漏洞
      
      审查要点：
      1. 数据来源是否可靠？
      2. 竞争优势是否可持续？
      3. 定价策略是否考虑了成本结构？
      4. 是否有遗漏的关键维度？
    """
  }
  
  phase converge {
    /delegate reviewer:code-reviewer """
      任务：整合竞品分析，输出差异化策略报告
      
      输入：竞品 A/B/C 分析 + 质疑回应
      输出要求：
      1. 三者对比矩阵
      2. 各竞品优劣势总结
      3. 差异化策略建议
      4. 市场机会分析
    """
  }
}
```

**预期输出结构**:
```markdown
## Team Execution Summary

### 任务类型
B 类：信息整合

### 执行阶段
- [x] Phase 1: worker-a / worker-b / worker-c（并行探索）
- [x] Phase 2: challenger（对抗质疑）
- [x] Phase 3: 收敛整合

### Phase 1 输出摘要
| Worker | 核心推理路径 | 关键洞察 |
|--------|-------------|----------|
| @worker-a | [竞品A分析] | [定位：高端市场...] |
| @worker-b | [竞品B分析] | [定价：差异化策略...] |
| @worker-c | [竞品C分析] | [技术：开源路线...] |

### Phase 2 质疑与回应
| 质疑点 | 来源 | 回应摘要 |
|--------|------|----------|
| 数据来源 | @challenger | [回应1] |
| 可持续性 | @challenger | [回应2] |

### 最终结论
---
**Reviewer 最终整合**：
[差异化策略报告]
```

---

### B-2: 技术选型对比

**输入**: `"使用 teamflow 对比 React、Vue、Angular 三种前端框架的优劣"`

```yaml
/workflow tech_stack_comparison {
  metadata:
    type: B
    mode: parallel
  
  phase explore {
    concurrent: 3
    timeout: 300
    
    /spawn worker-a:general-purpose """
      任务：深度分析 React 框架
      
      分析维度：
      1. 学习曲线与入门门槛
      2. 生态系统成熟度
      3. 性能特点
      4. 适用场景
      5. 社区活跃度
    """
    
    /spawn worker-b:general-purpose """
      任务：深度分析 Vue 框架
      
      分析维度：
      1. 学习曲线与入门门槛
      2. 生态系统成熟度
      3. 性能特点
      4. 适用场景
      5. 社区活跃度
    """
    
    /spawn worker-c:general-purpose """
      任务：深度分析 Angular 框架
      
      分析维度：
      1. 学习曲线与入门门槛
      2. 生态系统成熟度
      3. 性能特点
      4. 适用场景
      5. 社区活跃度
    """
    
    /await all
  }
  
  phase challenge {
    concurrent: 1
    timeout: 180
    
    /spawn challenger:security-reviewer """
      质疑点：
      1. 是否考虑了 TypeScript 原生支持的重要性？
      2. 企业级应用场景下哪个更有优势？
      3. 移动端开发支持是否评估？
    """
  }
  
  phase converge {
    /delegate reviewer:code-reviewer """
      整合三个框架的分析，输出：
      1. 多维对比矩阵
      2. 各框架核心优势
      3. 选择建议（按场景）
    """
  }
}
```

---

### B-3: 多源资料收集

**输入**: `"使用 teamflow 收集并整理 AI 安全领域的最新研究进展"`

```yaml
/workflow research_collection {
  metadata:
    type: B
    mode: parallel
  
  phase explore {
    concurrent: 3
    timeout: 300
    
    /spawn worker-a:general-purpose """
      任务：收集 AI 安全学术研究
      来源：arXiv、学术会议论文
    """
    
    /spawn worker-b:general-purpose """
      任务：收集 AI 安全工业实践
      来源：Google、Microsoft、OpenAI 博客
    """
    
    /spawn worker-c:general-purpose """
      任务：收集 AI 安全法规政策
      来源：政府文件、行业报告
    """
    
    /await all
  }
  
  # B-3 跳过 Phase 2（资料收集不需要对抗）
  // Phase 2: 跳过
  
  phase converge {
    /delegate reviewer:code-reviewer """
      整合三个来源的资料，输出：
      1. 研究趋势总结
      2. 关键技术方向
      3. 实践建议
      4. 知识缺口分析
    """
  }
}
```

---

## C 类示例（可执行规划）

### C-1: 用户认证系统

**输入**: `"使用 teamflow 实现一个用户认证系统"`

```yaml
/workflow user_auth_system {
  metadata:
    type: C
    mode: standard
  
  phase plan {
    /delegate planner:everything-claude-code:planner """
      任务：拆分用户认证系统
      
      子任务：
      1. 用户注册模块
      2. 用户登录模块
      3. Token 管理模块
      4. 权限控制模块
      
      约束：
      - 使用 JWT 进行身份验证
      - 密码需要加密存储
      - 支持第三方登录（OAuth）
    """
  }
  
  phase explore {
    concurrent: 3
    timeout: 300
    
    /spawn worker-a:general-purpose """
      任务：实现用户注册和登录模块
      
      要求：
      1. POST /api/register - 用户注册
      2. POST /api/login - 用户登录
      3. 密码 bcrypt 加密
      4. 输入验证
    """
    
    /spawn worker-b:general-purpose """
      任务：实现 Token 管理模块
      
      要求：
      1. JWT token 生成
      2. Token 刷新机制
      3. Token 过期处理
      4. Refresh token 存储
    """
    
    /spawn worker-c:general-purpose """
      任务：实现权限控制模块
      
      要求：
      1. 基于角色的访问控制（RBAC）
      2. 中间件验证
      3. 权限层级设计
    """
    
    /await all
  }
  
  phase challenge {
    concurrent: 1
    timeout: 180
    
    /spawn challenger:everything-claude-code:tdd-guide """
      质疑：
      1. 测试覆盖率是否达标？
      2. 是否有安全漏洞？
      3. 错误处理是否完善？
    """
  }
  
  phase converge {
    /delegate reviewer:everything-claude-code:code-reviewer """
      最终代码审查：
      1. 代码质量评估
      2. 安全审查
      3. 集成测试
      4. 文档完整性
    """
  }
}
```

---

### C-2: RESTful API 设计

**输入**: `"使用 teamflow 设计一个电商系统的订单管理 RESTful API"`

```yaml
/workflow order_management_api {
  metadata:
    type: C
    mode: standard
  
  phase plan {
    /delegate planner:everything-claude-code:planner """
      拆分订单管理 API
      
      端点设计：
      1. 订单创建
      2. 订单查询（单个/列表）
      3. 订单更新
      4. 订单取消
      5. 订单状态流转
    """
  }
  
  phase explore {
    concurrent: 3
    timeout: 300
    
    /spawn worker-a:general-purpose """
      任务：设计订单核心 API
      
      端点：
      - POST /orders
      - GET /orders/{id}
      - PUT /orders/{id}
      - DELETE /orders/{id}
      
      包括请求/响应格式、状态码设计
    """
    
    /spawn worker-b:general-purpose """
      任务：设计订单查询 API
      
      端点：
      - GET /orders (列表)
      - GET /orders?status=pending
      - GET /orders?user_id=123
      
      包括分页、过滤、排序设计
    """
    
    /spawn worker-c:general-purpose """
      任务：设计订单状态流转 API
      
      状态：pending → confirmed → shipped → delivered → cancelled
      包括状态机设计、事件驱动
    """
    
    /await all
  }
  
  phase challenge {
    concurrent: 1
    timeout: 180
    
    /spawn challenger:security-reviewer """
      质疑：
      1. 幂等性设计？
      2. 并发控制？
      3. 权限控制是否完善？
    """
  }
  
  phase converge {
    /delegate reviewer:everything-claude-code:code-reviewer """
      整合 API 设计，输出：
      1. 完整 API 规范（OpenAPI 格式）
      2. 数据库设计
      3. 错误处理规范
    """
  }
}
```

---

### C-3: 数据库迁移

**输入**: `"使用 teamflow 设计一个用户系统的数据库迁移方案"`

```yaml
/workflow database_migration {
  metadata:
    type: C
    mode: standard
  
  phase plan {
    /delegate planner:everything-claude-code:planner """
      拆分数据库迁移任务
      
      阶段：
      1. 现状分析
      2. 迁移方案设计
      3. 回滚方案
      4. 实施步骤
    """
  }
  
  phase explore {
    concurrent: 2
    timeout: 300
    
    /spawn worker-a:general-purpose """
      任务：设计迁移方案
      
      内容：
      1. 源数据库结构分析
      2. 目标数据库设计
      3. 数据迁移脚本
      4. 性能优化策略
    """
    
    /spawn worker-b:general-purpose """
      任务：设计回滚方案
      
      内容：
      1. 回滚触发条件
      2. 回滚脚本
      3. 数据一致性保证
      4. 演练计划
    """
    
    /await all
  }
  
  // C-3 合并 Phase 2/3
  phase converge {
    /delegate reviewer:everything-claude-code:code-reviewer """
      整合迁移方案，输出：
      1. 完整迁移文档
      2. 风险评估
      3. 实施时间线
      4. 验收标准
    """
  }
}
```

---

## D 类示例（简单执行）

### D-1: 单文件修复

**输入**: `"使用 teamflow 修复 config.json 中的拼写错误"`

```yaml
/workflow fix_typo {
  metadata:
    type: D
    mode: solo
  
  // D 类任务直接执行，无需阶段
  /delegate solo:general-purpose """
    任务：修复 config.json 中的拼写错误
    
    文件：config.json
    错误：conifg → config
    
    操作：
    1. 读取文件
    2. 修复拼写错误
    3. 保存文件
  """
}
```

---

### D-2: 小工具创建

**输入**: `"使用 teamflow 创建一个计算文件哈希的脚本"`

```yaml
/workflow file_hash_tool {
  metadata:
    type: D
    mode: solo
  
  /delegate solo:general-purpose """
    任务：创建文件哈希计算脚本
    
    要求：
    1. 支持 MD5、SHA1、SHA256
    2. 支持拖拽文件
    3. 输出格式清晰
    
    输出：hash_tool.py
  """
}
```

---

## 多标签共存示例

### M-1: A+B 共存

**输入**: `"使用 teamflow 思考这个 AI 项目的价值，并分析竞品数据"`

```yaml
/workflow ai_value_analysis {
  metadata:
    type: A  # A 类优先级最高
    mode: solo-deep
  
  // A 类任务不拆分，主 agent 直接深度推理
  /delegate solo-deep:general-purpose """
    任务：深度思考 AI 项目的价值
    
    思考维度：
    1. 技术价值
    2. 商业价值
    3. 社会影响
    4. 潜在风险
    
    注意：保留完整推理链条
  """
  
  // 可选：独立执行 B 类分析
  /branch with_analysis == true {
    /spawn worker-b:general-purpose """
      任务：分析竞品数据
    """
  }
}
```

---

### M-2: B+C 共存

**输入**: `"使用 teamflow 分析竞品并实现一个差异化功能"`

```yaml
/workflow analyze_and_implement {
  metadata:
    type: B  # B:C 数量相等，默认 C 类
    mode: standard
  
  phase analyze {
    concurrent: 3
    /spawn worker-a:general-purpose "分析竞品 A"
    /spawn worker-b:general-purpose "分析竞品 B"
    /spawn worker-c:general-purpose "分析竞品 C"
    /await all
  }
  
  phase implement {
    /spawn worker-implement:general-purpose """
      任务：基于竞品分析，实现差异化功能
      
      输入：竞品分析结果
      要求：突出差异化优势
    """
  }
  
  phase converge {
    /delegate reviewer:everything-claude-code:code-reviewer """
      整合分析和实现结果
    """
  }
}
```

---

## 示例使用指南

### 如何使用本示例库

1. **匹配任务类型**：根据输入识别 A/B/C/D 类型
2. **选择相似示例**：从示例库中选择最接近的场景
3. **按需调整**：根据具体需求修改任务描述和参数
4. **执行验证**：使用 `validate_output.py` 验证输出

### 示例执行检查清单

```markdown
- [ ] 任务类型识别正确
- [ ] Worker 数量 ≤ 3
- [ ] Phase 2 启用条件满足（可选跳过）
- [ ] 输出符合 Output Contract
- [ ] 推理链条保留完整
```

---

*最后更新：2026-04-10*
