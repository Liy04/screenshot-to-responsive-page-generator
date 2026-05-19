# Week 11 Day 03

## 负责角色

docs-agent -> tester-agent

## 任务目标

整理真实 AI 链路 smoke 的可复现执行方式，让新人能按文档理解和复跑。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-03.md`
- `docs/agents/docs-agent.md`
- `docs/agents/tester-agent.md`
- 必要时 `docs/spec.md`
- 必要时 `samples/README.md`

不默认读取 `docs/archive/`。

## 允许修改

- `docs/smoke/real-ai-smoke.md`
- 可选：`scripts/smoke-real-ai.example.ps1`
- 必要时更新 `docs/tasks/day-03.md` 的执行记录

## 禁止修改

- `backend/`
- `frontend/`
- `worker/`
- `tests/`
- 真实 API key
- 自动提交脚本
- 默认真实联网执行脚本

## 实施步骤

1. docs-agent 编写真实 AI smoke 文档。
2. 可选创建 example PowerShell 脚本，只允许使用占位符。
3. tester-agent 验证命令口径、安全边界和可读性。
4. 明确 `REAL_AI` / `FALLBACK` / `FAILED` 的判断标准。
5. 明确 artifact 和 `jobId` 复用检查方式。

## 验收标准

- [x] 文档说明 Python 推荐版本 3.11.9。
- [x] 文档说明 `OPENAI_BASE_URL=https://api.siliconflow.cn/v1`。
- [x] 文档说明 `OPENAI_MODEL=Qwen/Qwen3-VL-32B-Instruct`。
- [x] 文档说明 `OPENAI_API_KEY` 必须通过环境变量设置。
- [x] 文档说明 `IMAGEPAGE_WORKER_PYTHON_COMMAND` 示例。
- [x] 文档说明后端 timeout 推荐 120 秒。
- [x] 文档说明 `REAL_AI` / `FALLBACK` / `FAILED` 判断口径。
- [x] 文档说明 artifact 文件检查和 `jobId` 复用检查。
- [x] 未写入真实 API key。

## 执行记录

- docs-agent 新增 `docs/smoke/real-ai-smoke.md`，整理真实 AI smoke 环境变量、推荐样例、执行流程、结果判断、artifact 检查、`jobId` 复用检查和失败排查分类。
- docs-agent 新增 `scripts/smoke-real-ai.example.ps1`，作为可选示例脚本；脚本默认 dry-run，需要 `-Run` 和用户确认后才会调用本地后端，不打印真实 key。
- 本任务未执行真实联网 smoke，未安装依赖，未修改 `backend/`、`frontend/`、`worker/`、`tests/`。

## 输出格式

```text
任务结果：
- 任务目标：
- 修改文件：
- 主要改动：
- 验证步骤：
- 验证结果：
- 风险 / 待确认事项：
```
