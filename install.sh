#!/bin/bash

# Teamflow 安装脚本 - 一键安装到本地 Claude Code skills 目录

set -e

REPO_URL="https://github.com/fxz729/teamflow.git"
REPO_NAME="teamflow"
SKILL_NAME="teamflow"

# 检测 OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# 查找 Claude Code skills 目录
find_skills_dir() {
    local os=$(detect_os)

    case "$os" in
        macos|linux)
            local home="$HOME"
            local dir="$home/.claude/skills/$SKILL_NAME"
            if [ -d "$home/.claude/skills" ]; then
                echo "$dir"
            else
                echo ""
            fi
            ;;
        windows)
            local home="$USERPROFILE"
            local dir="$home/.claude/skills/$SKILL_NAME"
            if [ -d "$home/.claude/skills" ]; then
                echo "$dir"
            else
                echo ""
            fi
            ;;
        *)
            echo ""
            ;;
    esac
}

# 获取 Claude Code 安装目录（向上查找）
find_claude_dir() {
    local os=$(detect_os)
    local candidates=""

    case "$os" in
        macos)
            candidates="$HOME/.claude /Applications/Claude.app/Contents/Resources"
            ;;
        linux)
            candidates="$HOME/.claude"
            ;;
        windows)
            candidates="$USERPROFILE/.claude"
            ;;
    esac

    for dir in $candidates; do
        if [ -d "$dir" ]; then
            echo "$dir"
            return 0
        fi
    done

    echo ""
}

# 主安装逻辑
main() {
    echo "🔧 Teamflow 安装脚本"
    echo ""

    local os=$(detect_os)
    echo "📂 检测到系统: $os"

    # 方法 1: 直接克隆到 skills 目录
    local skills_dir=$(find_skills_dir)
    local claude_dir=$(find_claude_dir)

    if [ -n "$skills_dir" ]; then
        echo "✅ 找到 Claude Code skills 目录: $skills_dir"
        echo ""

        # 如果已存在，先删除
        if [ -d "$skills_dir" ]; then
            echo "⚠️  已存在旧版本，正在删除..."
            rm -rf "$skills_dir"
        fi

        echo "📥 正在克隆仓库..."
        git clone "$REPO_URL" "$skills_dir"
        echo ""
        echo "✅ 安装成功！"
        echo ""
        echo "📍 安装路径: $skills_dir"
        echo ""
        echo "🚀 重启 Claude Code 后即可使用:"
        echo "   使用 teamflow [你的任务]"

    # 方法 2: 找不到 skills 目录，但 Claude Code 已安装
    elif [ -n "$claude_dir" ]; then
        echo "⚠️  未找到 skills 目录，正在 Claude Code 目录下创建..."
        local new_skills_dir="$claude_dir/skills/$SKILL_NAME"
        mkdir -p "$(dirname "$new_skills_dir")"
        git clone "$REPO_URL" "$new_skills_dir"
        echo ""
        echo "✅ 安装成功！"
        echo ""
        echo "📍 安装路径: $new_skills_dir"
        echo ""
        echo "🚀 重启 Claude Code 后即可使用:"
        echo "   使用 teamflow [你的任务]"

    # 方法 3: 完全找不到 Claude Code
    else
        echo "❌ 未找到 Claude Code 安装目录"
        echo ""
        echo "请确保已安装 Claude Code: https://claude.com/download"
        echo "安装后重启终端，再次运行此脚本"
        exit 1
    fi
}

main
