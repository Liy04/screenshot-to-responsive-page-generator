param(
    [string]$Task = "请为 Codex 生成当前任务的最小上下文包",
    [string]$OutputPath = ".context/codex-context-pack.md",
    [int]$MaxTurns = 8
)

$ErrorActionPreference = "Stop"

$MinTurns = 3
$MaxAllowedTurns = 16
if ($MaxTurns -lt $MinTurns -or $MaxTurns -gt $MaxAllowedTurns) {
    Write-Error "MaxTurns 必须在 $MinTurns 到 $MaxAllowedTurns 之间。超大任务应优先拆成多个 context-pack，而不是无限提高 turns。"
    exit 1
}

$ClaudeCommand = Get-Command claude -ErrorAction SilentlyContinue
if (-not $ClaudeCommand) {
    Write-Error "Claude Code CLI 未找到，请先确认 claude 命令可用。"
    exit 1
}

if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    Write-Error "OutputPath 必须是 .context/ 下的相对路径，不允许绝对路径。"
    exit 1
}

$ProjectRoot = (Get-Location).ProviderPath
$ContextRoot = [System.IO.Path]::GetFullPath((Join-Path $ProjectRoot ".context"))
$OutputFullPath = [System.IO.Path]::GetFullPath((Join-Path $ProjectRoot $OutputPath))
$ContextRootWithSeparator = $ContextRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

if (-not $OutputFullPath.StartsWith($ContextRootWithSeparator, [System.StringComparison]::OrdinalIgnoreCase)) {
    Write-Error "OutputPath 必须位于 .context/ 目录内部，且不允许路径穿越。"
    exit 1
}

$OutputDirectory = Split-Path -Parent $OutputFullPath
if (-not (Test-Path $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}

$Prompt = @"
请使用 context-scout Skill 为 Codex 生成最小上下文包。

当前任务：
$Task

严格要求：
1. 只读取项目上下文，不修改任何文件。
2. 不执行构建、测试、安装依赖、数据库命令。
3. 不读取或输出敏感文件内容。
4. 不读取构建产物、缓存目录、副产物目录。
5. 不输出完整大文件内容。
6. 不输出超过 30 行的连续文件片段。
7. 必须列出相关文件路径。
8. 必须区分 Facts 和 Suggestions。
9. 必须列出 Must Not Touch。
10. 必须列出 Uncertainties。
11. 输出 Markdown。
12. 控制在 150 行以内。
13. 不要把猜测写成事实。
14. 没有证据就写“不确定”。
15. 输出必须直接从 "# Codex Context Pack" 开始，不要输出任何前言、解释、寒暄或后记。
16. 如果当前任务范围过大，无法在 150 行内可靠覆盖，请在 Uncertainties 中建议拆成多个 context-pack；不要强行覆盖全部内容。

必须优先读取当前阶段约束文件：
- docs/context/current-phase.md

如果 docs/context/current-phase.md 存在，必须在 context-pack 中总结：
- 当前阶段目标
- 当前阶段禁止项
- 当前阶段推荐实现方式
- 当前阶段允许修改范围

如果 docs/context/current-phase.md 不存在，必须在 Uncertainties 中说明未找到。

禁止读取或输出以下敏感文件或内容：
- .claude/settings.local.json
- .claude/*.local.json
- .env
- .env.*
- *.pem
- *.key
- *.p12
- *.jks
- application-prod.yml
- application-prod.yaml
- 任何包含 password / secret / token / apiKey / privateKey 的文件或内容

如果发现敏感文件，只能报告：
发现敏感配置文件路径，但未读取内容。

禁止读取以下低价值目录和副产物：
- .context/
- frontend/dist/
- frontend/node_modules/
- backend/target/
- backend/uploads/
- backend/mock-data/
- worker/__pycache__/
- *.log

优先查看：
- AGENTS.md
- docs/context/current-phase.md
- README.md
- docs/
- schema/
- worker/
- package.json
- pom.xml
- 与当前任务直接相关的文件

context-pack 使用和流转规则：
1. context-pack 是临时上下文包，不是正式项目文档，不得提交 Git。
2. 哪个线程调用 context-scout，哪个线程必须先验收 context-pack。
3. 验收通过前，调用线程不得把 context-pack 当成事实依据。
4. context-pack 不会被项目经理线程自动处理。
5. 如果涉及阶段边界、跨线程、数据库、Entity、Mapper、Redis、RabbitMQ、AI、Figma、任务扩大、周计划、任务卡、技术方案、下一天或下一周任务，必须建议调用线程交给项目经理最终确认。
6. 如果只涉及调用线程自己的局部上下文，且不涉及阶段边界、跨线程范围、敏感模块或任务扩大，可以建议该线程自检验收通过后继续。
7. 相关文件已修改、当前阶段变化、任务目标变化、线程切换、用户新增限制、或与正式文档冲突时，context-pack 视为过期。
8. 如果 context-pack 与 AGENTS.md、docs/context/current-phase.md、当前任务卡或专项设计文档冲突，以正式文档为准。

输出格式必须严格使用：

# Codex Context Pack

## 1. Task

## 2. Phase Constraints

## 3. Relevant Files
| 文件路径 | 相关原因 |
|---|---|

## 4. Facts

## 5. Suggestions

## 6. Must Not Touch

## 7. Risk Notes

## 8. Recommended Codex Next Step

## 9. Uncertainties
"@

$ContextPackPath = $OutputFullPath

claude -p $Prompt --output-format text --max-turns $MaxTurns | Out-File -FilePath $ContextPackPath -Encoding utf8

$ContextPack = Get-Content -Raw -Encoding utf8 $ContextPackPath
if ([string]::IsNullOrWhiteSpace($ContextPack)) {
    Write-Error "context-pack 生成失败：输出为空。"
    exit 1
}

if ((-not $ContextPack.StartsWith("# Codex Context Pack")) -or ($ContextPack -like "*Error: Reached max turns*")) {
    Write-Error "context-pack 生成失败：输出必须以标题开头，或 Claude Code 达到 max turns。"
    exit 1
}

Write-Host "Generated $ContextPackPath"
