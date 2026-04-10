#!/usr/bin/env python3
"""
Teamflow Routing Rules - 任务分类逻辑 Python 实现

本模块实现 SKILL.md 中定义的任务分类和路由决策逻辑。
所有分类规则都源自 routing-rules.md，通过代码形式提供可执行验证。

Usage:
    from routing_rules import classify_task, TaskCategory

    category = classify_task("分析竞品数据并实现功能")
    print(category)  # TaskCategory.EXECUTABLE_PLANNING
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple


class TaskCategory(Enum):
    """任务类型枚举 - 与 SKILL.md 中的 A/B/C/D 分类对应"""
    # A 类：开放性思辨（Open-Ended Reasoning）
    OPEN_ENDED_REASONING = "A"
    # B 类：信息整合（Information Integration）
    INFO_INTEGRATION = "B"
    # C 类：可执行规划（Executable Planning）
    EXECUTABLE_PLANNING = "C"
    # D 类：简单执行（Simple Execution）
    SIMPLE_EXECUTION = "D"
    # 未知类型
    UNKNOWN = "UNKNOWN"


# ============ 关键词定义 ============

# A 类触发关键词（开放性思辨）
A_KEYWORDS = [
    "意义", "价值", "应该", "真相", "美", "灵魂",
    "伦理", "道德", "哲学", "观点", "感受",
    "判断", "评价", "好不好", "如何看待",
    "人生", "存在", "本质", "超越",
]

# A 类触发关键词（隐式，需结合语境）
A_KEYWORDS_IMPLICIT = [
    "思考", "反思", "探讨", "探索",
]

# A 类不触发场景（后面跟具体技术名词时）
A_KEYWORDS_TECH_CONTEXT = [
    "架构", "代码", "系统", "项目", "模块", "接口", "功能", "实现", "设计",
]

# B 类触发关键词（信息整合）
B_KEYWORDS = [
    "分析", "对比", "综述", "报告",
    "收集", "整理", "汇总", "多方",
    "研究", "调查", "评估",
]

# C 类触发关键词（可执行规划）
C_KEYWORDS = [
    "开发", "设计", "实现", "构建",
    "创建功能", "修复", "重构",
    "架构", "部署", "测试",
]

# D 类触发条件
D_CRITERIA = {
    "single_file": True,      # 单文件编辑
    "line_count": 50,         # <50 行代码修改
    "direct_answer": True,    # 直接答案查询
    "small_tool": True,       # 小型工具创建
}


# ============ 辅助函数 ============

def count_keyword_hits(text: str, keywords: List[str], case_sensitive: bool = False) -> int:
    """统计文本中关键词出现次数"""
    count = 0
    text_to_check = text if case_sensitive else text.lower()
    for keyword in keywords:
        keyword_to_check = keyword if case_sensitive else keyword.lower()
        count += text_to_check.count(keyword_to_check)
    return count


def has_tech_context(text: str) -> bool:
    """检测文本是否在技术上下文中（用于判断 A 类隐式关键词）"""
    for tech_term in A_KEYWORDS_TECH_CONTEXT:
        if tech_term in text:
            return True
    return False


def is_d_class_task(
    task: str = "",
    file_count: int = 0,
    line_count: int = 0,
    is_direct_answer: bool = False,
    is_small_tool: bool = False
) -> bool:
    """
    判断是否为 D 类任务

    D 类条件（满足任一）：
    - 单文件编辑
    - <50 行代码修改
    - 直接答案查询
    - 小型工具创建
    - 明确的 D 类短语（如"修复 xx 文件中的 yy"）
    """
    if file_count == 1:
        return True
    if line_count < 50:
        return True
    if is_direct_answer:
        return True
    if is_small_tool:
        return True

    # 辅助判断：识别明确的 D 类短语
    # 只有当其他分类关键词都不满足时才考虑
    import re
    d_patterns = [
        r"修复\s+\S+\s+中的",  # 修复 xx 中的 yy
        r"修改\s+\S+\s+中的",  # 修改 xx 中的 yy
        r"更正\s+\S+\s+中的",  # 更正 xx 中的 yy
    ]
    for pattern in d_patterns:
        if re.search(pattern, task):
            return True

    return False


# ============ 核心分类函数 ============

def classify_task(
    task: str,
    file_count: int = 0,
    line_count: int = 0,
    is_direct_answer: bool = False,
    is_small_tool: bool = False
) -> TaskCategory:
    """
    核心任务分类函数

    采用多标签评分机制，优先级规则：
    1. A 类命中 >= 1 → Solo-Deep（A 类最高优先级）
    2. A 类未命中，B 类和 C 类同时命中 → 比较数量
    3. 仅 B 类命中 → 渐进式并行
    4. 仅 C 类命中 → 标准 teamflow
    5. A/B/C 都不命中 → 评估 D 类或复杂度

    Args:
        task: 用户输入的任务描述
        file_count: 涉及文件数（默认 0）
        line_count: 预估代码行数（默认 0）
        is_direct_answer: 是否为直接答案查询（默认 False）
        is_small_tool: 是否为小型工具创建（默认 False）

    Returns:
        TaskCategory: 任务分类结果
    """
    # Step 1: 检测 A 类关键词
    a_count = count_keyword_hits(task, A_KEYWORDS)
    if a_count >= 1:
        return TaskCategory.OPEN_ENDED_REASONING

    # Step 2: 检测 A 类隐式关键词（需结合语境）
    implicit_a_count = 0
    for keyword in A_KEYWORDS_IMPLICIT:
        if keyword in task:
            # 检查是否在技术上下文中
            # 如果 "思考/反思" 后面跟的是技术名词，则为 C 类
            if keyword in ["思考", "反思"]:
                # 简单检测：关键词后面是否有技术术语
                idx = task.find(keyword)
                remaining = task[idx + len(keyword):]
                if has_tech_context(remaining):
                    implicit_a_count += 0  # 技术上下文，不算 A 类
                else:
                    implicit_a_count += 1
            else:
                implicit_a_count += 1

    if implicit_a_count >= 1:
        return TaskCategory.OPEN_ENDED_REASONING

    # Step 3: 统计 B 类和 C 类关键词
    b_count = count_keyword_hits(task, B_KEYWORDS)
    c_count = count_keyword_hits(task, C_KEYWORDS)

    # Step 4: 多标签共存决策
    if b_count >= 1 and c_count >= 1:
        # B 类和 C 类同时命中
        if b_count > c_count:
            return TaskCategory.INFO_INTEGRATION
        else:
            return TaskCategory.EXECUTABLE_PLANNING

    # Step 5: 单类型命中（B/C 类）
    if b_count >= 1:
        return TaskCategory.INFO_INTEGRATION
    if c_count >= 1:
        # 特殊处理：仅有"修复"关键词且匹配 D 类模式时，判定为 D 类
        if c_count == 1 and "修复" in task:
            import re
            if re.search(r"修复\s+\S+\s+中的", task):
                return TaskCategory.SIMPLE_EXECUTION
        return TaskCategory.EXECUTABLE_PLANNING

    # Step 6: A/B/C 都不满足时，才评估 D 类
    # 注意：D 类只有通过显式参数（file_count, line_count）或明确的 D 类短语才触发
    if is_d_class_task(task, file_count, line_count, is_direct_answer, is_small_tool):
        return TaskCategory.SIMPLE_EXECUTION

    # Step 7: 默认按复杂度判断
    complexity_score = calculate_complexity_score(file_count, line_count)
    if complexity_score >= 0.7:
        return TaskCategory.EXECUTABLE_PLANNING
    elif complexity_score >= 0.4:
        return TaskCategory.INFO_INTEGRATION
    else:
        return TaskCategory.SIMPLE_EXECUTION


def calculate_complexity_score(file_count: int, line_count: int) -> float:
    """
    计算任务复杂度得分（0.0 - 1.0）

    复杂度得分 =
      (文件数得分 × 0.3) +
      (代码行数得分 × 0.3) +
      (任务数得分 × 0.2) +
      (领域数得分 × 0.2)

    得分解释：
    - 0.0 - 0.3 → Solo
    - 0.4 - 0.6 → 渐进式并行（B 类）
    - 0.7 - 1.0 → 标准 teamflow（C 类）
    """
    # 文件数得分：≤1 → 0, 2-3 → 1, >3 → 2
    if file_count <= 1:
        file_score = 0
    elif file_count <= 3:
        file_score = 1
    else:
        file_score = 2

    # 代码行数得分：<50 → 0, 50-200 → 1, >200 → 2
    if line_count < 50:
        line_score = 0
    elif line_count <= 200:
        line_score = 1
    else:
        line_score = 2

    # 任务数得分（默认 1）：1 → 0, 2-4 → 1, >4 → 2
    # 这里无法从外部参数推断，使用文件数作为代理
    task_score = file_score  # 简化处理

    # 领域数得分（默认 1）：1 → 0, 2 → 1, >2 → 2
    domain_score = 1 if file_count > 1 else 0

    # 计算加权得分
    complexity = (
        (file_score * 0.3) +
        (line_score * 0.3) +
        (task_score * 0.2) +
        (domain_score * 0.2)
    ) / 2  # 归一化到 0-1

    return min(1.0, complexity)


def get_routing_decision(category: TaskCategory) -> Dict[str, any]:
    """
    根据任务分类返回路由决策

    Args:
        category: 任务分类结果

    Returns:
        Dict 包含：
        - mode: 执行模式（Solo-Deep / 渐进式并行 / 标准 teamflow / Solo）
        - phases: 应执行的阶段列表
        - phase2_required: 是否需要 Phase 2
    """
    routing_table = {
        TaskCategory.OPEN_ENDED_REASONING: {
            "mode": "Solo-Deep",
            "phases": [],
            "phase2_required": False,
            "description": "开放性思辨任务，主 agent 直接深度推理"
        },
        TaskCategory.INFO_INTEGRATION: {
            "mode": "渐进式并行",
            "phases": ["Phase 1", "Phase 2", "Phase 3"],
            "phase2_required": True,
            "description": "信息整合任务，多源并行探索后收敛"
        },
        TaskCategory.EXECUTABLE_PLANNING: {
            "mode": "标准 teamflow",
            "phases": ["Plan", "Phase 1", "Phase 2", "Phase 3"],
            "phase2_required": True,
            "description": "可执行规划任务，完整三阶段流程"
        },
        TaskCategory.SIMPLE_EXECUTION: {
            "mode": "Solo",
            "phases": [],
            "phase2_required": False,
            "description": "简单执行任务，主 agent 直接完成"
        },
        TaskCategory.UNKNOWN: {
            "mode": "标准 teamflow",
            "phases": ["Plan", "Phase 1", "Phase 2", "Phase 3"],
            "phase2_required": True,
            "description": "未知类型，默认完整流程"
        },
    }
    return routing_table.get(category, routing_table[TaskCategory.UNKNOWN])


def should_enable_phase2(
    worker_count: int,
    has_divergence: bool = False,
    is_high_risk: bool = False,
    user_requests_challenge: bool = False
) -> Tuple[bool, str]:
    """
    判断是否应该启用 Phase 2（对抗质疑）

    必须启用（满足任一）：
    - Phase 1 有 3 个或以上 agent 输出
    - 任务涉及多个专业领域
    - Phase 1 输出中存在明显矛盾或分歧
    - 任务涉及高风险决策

    可选启用：
    - 用户明确要求深度交锋
    - 任务复杂度高于阈值（子任务数 >= 5）
    - 时间敏感任务

    可跳过：
    - 任务只有 1-2 个子任务
    - Phase 1 输出高度一致（无明显分歧）
    - 时间敏感任务（快速交付优先）

    Returns:
        (should_enable, reason) 元组
    """
    # 必须启用条件
    if worker_count >= 3:
        return True, "Phase 1 有 3+ agent 输出"

    if is_high_risk:
        return True, "任务涉及高风险决策"

    if user_requests_challenge:
        return True, "用户明确要求深度交锋"

    # 可选启用条件
    optional_reasons = []
    if has_divergence:
        optional_reasons.append("Phase 1 输出存在分歧")

    if optional_reasons:
        return True, "; ".join(optional_reasons)

    # 可跳过条件
    if worker_count <= 2:
        return False, "任务只有 1-2 个子任务，跳过 Phase 2"

    return False, "未满足启用条件"


# ============ CLI 接口 ============

def main():
    """命令行接口 - 用于测试分类逻辑"""
    import sys
    import json

    # 处理 Windows GBK 编码问题
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    test_cases = [
        # A 类测试
        ("思考人生意义", "A"),
        ("思考这个系统的价值", "A"),
        ("评价这段代码的质量", "A"),

        # B 类测试
        ("分析竞品数据", "B"),
        ("对比 React 和 Vue 的优劣", "B"),
        ("收集并整理最新研究进展", "B"),

        # C 类测试
        ("实现用户认证系统", "C"),
        ("设计一个 RESTful API", "C"),
        ("开发新功能", "C"),

        # D 类测试
        ("修复 config.json 中的拼写错误", "D"),
        ("创建一个计算哈希的脚本", "D"),

        # 多标签共存测试
        ("思考这个系统的价值，并分析竞品数据", "A"),  # A+B → A
        ("分析竞品数据并实现功能", "C"),  # B+C → C (数量相等时默认 C)
        ("对比分析 React 和 Vue 并设计新功能", "B"),  # B+C → B (B > C)
    ]

    print("\n" + "=" * 60)
    print("Teamflow Routing Rules 测试")
    print("=" * 60)

    passed = 0
    failed = 0

    for task, expected in test_cases:
        result = classify_task(task)
        status = "✅" if result.value == expected else "❌"
        if status == "✅":
            passed += 1
        else:
            failed += 1

        routing = get_routing_decision(result)
        print(f"\n{status} 输入: \"{task}\"")
        print(f"   预期: {expected}, 实际: {result.value}")
        print(f"   模式: {routing['mode']}")

    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{passed + failed} 通过")
    print("=" * 60)

    # 输出 JSON 格式结果（供程序调用）
    if "--json" in sys.argv:
        task = sys.argv[2] if len(sys.argv) > 2 else ""
        result = classify_task(task)
        routing = get_routing_decision(result)
        print(json.dumps({
            "task": task,
            "category": result.value,
            "routing": routing
        }, ensure_ascii=False, indent=2))

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
