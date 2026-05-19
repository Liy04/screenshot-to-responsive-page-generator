# Week 11 Dev Smoke

## 文件目的

本文档归档 Week 11 的开发 smoke 口径、已完成验证结果和未执行项。可复现执行说明以 `docs/smoke/real-ai-smoke.md` 为准。

## Smoke 资产

- 样例说明：`samples/README.md`
- 样例图：
  - `samples/01-simple-card-page.png`
  - `samples/02-simple-form-page.png`
  - `samples/03-dashboard-cards-page.png`
- 真实 AI smoke 文档：`docs/smoke/real-ai-smoke.md`
- example 脚本：`scripts/smoke-real-ai.example.ps1`

## 推荐环境

- Python：`3.11.9`
- `OPENAI_BASE_URL`：`https://api.siliconflow.cn/v1`
- `OPENAI_MODEL`：`Qwen/Qwen3-VL-32B-Instruct`
- `IMAGEPAGE_WORKER_PYTHON_COMMAND`：`D:\environment\python11\python.exe`
- 后端 worker timeout：`120` 秒

`OPENAI_API_KEY` 必须通过环境变量设置，不写入仓库、脚本、文档、日志或 artifact。

## 结果判断口径

真实 AI 链路结果按三类归档：

- `REAL_AI`：真实 AI 生成成功，`fallbackUsed=false`，layout / preview / metadata artifact 可用。
- `FALLBACK`：真实 AI 调用、解析、校验或预览编译出现问题，但系统返回可展示 fallback 结果，并记录 `fallbackReason`。
- `FAILED`：上传、生成、Worker、artifact 或前端展示失败，且无可接受 fallback 结果。

## Artifact 检查口径

同一 `jobId` 成功生成后，本地 artifact 至少应包含：

- `layout.json`
- `preview.html`
- `metadata.json`

检查重点：

- `layout.json` 可解析，`version=0.1`，结构符合当前 layout 约定。
- `preview.html` 非空，且不包含脚本、事件属性、危险 iframe / object / embed 或 `javascript:`。
- `metadata.json` 包含 `promptVersion`、`sourceType` / `mode`、`fallbackUsed`、`fallbackReason`、warnings、errors、artifact 信息。
- 同一 `jobId` 第二次 generate 应命中 artifact 复用，并体现 `artifact.reused=true`。

## Week 11 测试记录

- Worker：`70 / 70` tests OK。
- Backend：`45 / 45` tests OK。
- Frontend：`10 / 10` tests OK。

## 真实联网 smoke 状态

Day 5 收口未执行真实联网 smoke。

原因：收口阶段不使用真实 key，不触发真实第三方 API 调用，避免将外部服务状态、真实 `OPENAI_API_KEY` 或本地私密环境混入归档。

当前状态：

- 文档已支持后续真实联网 smoke。
- example 脚本已支持后续按环境运行。
- 脚本默认不会直接执行真实联网 generate，需要显式 `-Run` 并二次确认。
- 后续真实联网 smoke 应在具备真实环境变量、本地后端和网络条件时单独执行并记录结果。

## 安全检查

- 未发现真实 key 泄漏。
- 文档和脚本只使用占位符或环境变量口径。
- `samples/` 无隐私、品牌、版权阻塞。
- `backend/storage/` 未进入可提交变更。
- `frontend/dist/` 未进入可提交变更。
- iframe sandbox 未放宽，仍不允许脚本执行。

## 遗留风险

- 真实 AI smoke 依赖外部模型服务、网络、额度、鉴权和模型输出稳定性。
- 同图多次真实 AI 生成仍可能存在轻微差异；同一 `jobId` artifact 复用用于降低重复查询漂移。
- 后续真实联网 smoke 的结果需要单独记录具体时间、环境变量是否存在、样例图、响应分类和 artifact 检查结果。
