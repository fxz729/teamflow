#!/usr/bin/env python3
"""
Teamflow Output Validation Script
验证 Team 模式输出是否符合 Output Contract

Usage:
    python validate_output.py --file output.md
    python validate_output.py --content "## Team Execution Summary..."
    python validate_output.py --dir ./outputs/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple, List, Optional


class ValidationResult:
    def __init__(self):
        self.passed: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, msg: str):
        self.passed = False
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lines = [f"\n{'='*60}", f"Validation Result: {status}", f"{'='*60}"]
        if self.errors:
            lines.append("\nErrors:")
            for e in self.errors:
                lines.append(f"  - {e}")
        if self.warnings:
            lines.append("\nWarnings:")
            for w in self.warnings:
                lines.append(f"  - {w}")
        lines.append(f"{'='*60}\n")
        return "\n".join(lines)


def validate_team_output(content: str) -> ValidationResult:
    """验证 Team 模式输出"""
    result = ValidationResult()

    required_sections = [
        ("## Team Execution Summary", "缺少 ## Team Execution Summary"),
        ("### 任务类型", "缺少 ### 任务类型"),
        ("### 执行阶段", "缺少 ### 执行阶段"),
        ("### Phase 1", "缺少 Phase 1 相关内容"),
        ("### 最终结论", "缺少 ### 最终结论"),
    ]

    for section, error_msg in required_sections:
        if section not in content:
            result.add_error(error_msg)

    # 检查推理链条
    if "推理" not in content and "推理链条" not in content:
        result.add_warning("输出缺少推理链条（建议包含）")

    # 检查 Reviewer 输出
    if "Reviewer" not in content and "reviewer" not in content.lower():
        result.add_warning("输出缺少 Reviewer 相关内容（建议包含）")

    # 检查 Phase 完整性
    if "Phase 1" in content and "Phase 2" not in content:
        result.add_warning("Phase 2 缺失（可能不需要对抗阶段）")

    if "Phase 3" not in content and "收敛" not in content:
        result.add_warning("Phase 3/收敛阶段缺失")

    return result


def validate_solo_deep_output(content: str) -> ValidationResult:
    """验证 Solo-Deep 模式输出"""
    result = ValidationResult()

    required_sections = [
        ("## 深度思考", "缺少 ## 深度思考（或 ## Solo-Deep）"),
        ("### 推理轨迹", "缺少 ### 推理轨迹"),
        ("### 核心洞察", "缺少 ### 核心洞察（或 ### 洞察）"),
    ]

    for section, error_msg in required_sections:
        if section not in content:
            result.add_error(error_msg)

    # 检查是否包含推理原因
    if "为什么" not in content and "原因" not in content and "因为" not in content:
        result.add_warning("Solo-Deep 输出应包含推理原因（为什么这样想）")

    return result


def detect_output_type(content: str) -> str:
    """自动检测输出类型"""
    if "## Team Execution Summary" in content:
        return "team"
    elif "## 深度思考" in content or "## Solo-Deep" in content:
        return "solo-deep"
    else:
        return "unknown"


def validate_file(filepath: str) -> Tuple[bool, str]:
    """验证单个文件"""
    path = Path(filepath)
    if not path.exists():
        return False, f"File not found: {filepath}"

    content = path.read_text(encoding="utf-8")
    output_type = detect_output_type(content)

    if output_type == "unknown":
        result = ValidationResult()
        result.add_warning("无法自动识别输出类型，尝试通用验证...")
        return True, result.summary()

    if output_type == "team":
        result = validate_team_output(content)
    else:
        result = validate_solo_deep_output(content)

    return result.passed, result.summary()


def validate_content(content: str) -> Tuple[bool, str]:
    """验证内容字符串"""
    output_type = detect_output_type(content)

    if output_type == "team":
        result = validate_team_output(content)
    elif output_type == "solo-deep":
        result = validate_solo_deep_output(content)
    else:
        result = ValidationResult()
        result.add_warning("无法识别输出类型，请确保输出包含 ## Team Execution Summary 或 ## 深度思考")

    return result.passed, result.summary()


def validate_directory(dirpath: str) -> Tuple[int, int, str]:
    """验证目录下所有 .md 文件"""
    path = Path(dirpath)
    if not path.is_dir():
        return 0, 0, f"Directory not found: {dirpath}"

    md_files = list(path.glob("*.md"))
    if not md_files:
        return 0, 0, f"No .md files found in {dirpath}"

    passed = 0
    failed = 0
    results = [f"\n{'='*60}", f"Validating {len(md_files)} files in {dirpath}", f"{'='*60}\n"]

    for f in md_files:
        content = f.read_text(encoding="utf-8")
        output_type = detect_output_type(content)

        if output_type == "unknown":
            results.append(f"  {f.name}: ⚠️ SKIP (unknown type)")
            continue

        if output_type == "team":
            result = validate_team_output(content)
        else:
            result = validate_solo_deep_output(content)

        status = "✅" if result.passed else "❌"
        results.append(f"  {f.name}: {status} ({output_type})")
        if result.passed:
            passed += 1
        else:
            failed += 1
            for err in result.errors:
                results.append(f"    - {err}")

    results.append(f"\n{'='*60}")
    results.append(f"Summary: {passed} passed, {failed} failed out of {len(md_files)} files")
    results.append(f"{'='*60}\n")

    return passed, failed, "\n".join(results)


def main():
    # 处理 Windows GBK 编码问题
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Teamflow Output Validation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_output.py --file output.md
  python validate_output.py --content "## Team Execution Summary..."
  python validate_output.py --dir ./outputs/
  python validate_output.py --file output.md --verbose
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", "-f", help="Path to output file to validate")
    group.add_argument("--content", "-c", help="Content string to validate")
    group.add_argument("--dir", "-d", help="Directory containing multiple .md files")

    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.file:
        passed, summary = validate_file(args.file)
        print(summary)
        sys.exit(0 if passed else 1)

    elif args.content:
        passed, summary = validate_content(args.content)
        print(summary)
        sys.exit(0 if passed else 1)

    elif args.dir:
        passed, failed, summary = validate_directory(args.dir)
        print(summary)
        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
