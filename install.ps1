# Teamflow 安装脚本 (Windows PowerShell)
# 使用方式: .\install.ps1

$RepoUrl = "https://github.com/fxz729/teamflow.git"
$SkillName = "teamflow"

Write-Host "🔧 Teamflow 安装脚本" -ForegroundColor Cyan
Write-Host ""

# 查找 Claude Code skills 目录
$ClaudeBase = $env:USERPROFILE + "\.claude"
$SkillsDir = $ClaudeBase + "\skills\$SkillName"

if (Test-Path $SkillsDir) {
    Write-Host "⚠️  已存在旧版本，正在删除..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $SkillsDir
}

if (Test-Path "$ClaudeBase\skills") {
    Write-Host "✅ 找到 Claude Code skills 目录" -ForegroundColor Green
    Write-Host "📍 $SkillsDir"
    Write-Host ""
    Write-Host "📥 正在克隆仓库..." -ForegroundColor Cyan
    git clone $RepoUrl $SkillsDir
} elseif (Test-Path $ClaudeBase) {
    Write-Host "⚠️  skills 目录不存在，正在创建..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "$ClaudeBase\skills\$SkillName" -Force | Out-Null
    Write-Host "📥 正在克隆仓库..." -ForegroundColor Cyan
    git clone $RepoUrl $SkillsDir
} else {
    Write-Host "❌ 未找到 Claude Code 安装目录" -ForegroundColor Red
    Write-Host ""
    Write-Host "请确保已安装 Claude Code: https://claude.com/download" -ForegroundColor Yellow
    Write-Host "安装后再次运行此脚本"
    exit 1
}

Write-Host ""
Write-Host "✅ 安装成功！" -ForegroundColor Green
Write-Host ""
Write-Host "📍 安装路径: $SkillsDir"
Write-Host ""
Write-Host "🚀 重启 Claude Code 后即可使用:" -ForegroundColor Cyan
Write-Host "   使用 teamflow [你的任务]"
