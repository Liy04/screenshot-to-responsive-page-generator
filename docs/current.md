# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、当天对应的 `docs/tasks/day-xx.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 10 已完成收口：真实 AI 链路稳定化与可复现验收。

## 阶段背景

Week 09 已完成真实 AI 最小闭环。Week 10 在不扩大功能面的前提下，完成了对真实链路稳定性、失败可解释性、artifact 保存与复用、前端状态展示和可重复 smoke 的收口。

## 当前完成内容

1. Worker：
   - `promptVersion` 已加入输出，当前值 `week10-v1`。
   - JSON 清洗支持纯 JSON、markdown code fence、前后带说明文字。
   - 非 JSON 输出不会崩溃，可进入 fallback。
   - 轻量 intermediate repair 已支持。
   - `fallbackReason` 已加入输出。
   - `REAL_AI` / `FALLBACK` / `FAILED` 路径已验证。
2. 后端：
   - 已保存 `layout.json`、`preview.html`、`metadata.json` artifact。
   - 同一 `jobId` 成功 artifact 可复用。
   - 第二次 generate 命中 `artifact.reused=true`，不重复调用 Worker。
   - 返回结构已包含 `promptVersion`、`fallbackReason`、`warnings`、`errors`、`artifact`。
   - 未接 MySQL，未创建 Entity / Mapper。
3. 前端：
   - 已展示 `REAL_AI` / `FALLBACK` / `FAILED` / `TIMEOUT`。
   - 已展示 `promptVersion`、`fallbackReason`、`warnings`、`errors`、artifact 信息。
   - iframe preview 保持稳定。
   - iframe 使用 `sandbox=""`，无 `allow-scripts`。
4. 测试与 smoke：
   - Worker：`67 / 67` 通过。
   - Backend：`45 / 45` 通过。
   - Frontend：`9 / 9` 通过。
   - 真实链路 smoke 通过。
   - `REAL_AI` / `FALLBACK` / `FAILED` 三种口径已验证。
   - artifact 文件检查通过。
   - `jobId` 复用检查通过。
   - API key 未泄漏。
   - `backend/storage/` 是运行副产物，已被 `backend/.gitignore` 忽略。

## 当前不做

- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不做多页面。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。
- 不做登录注册 / 权限系统。
- 不做高保真截图还原。
- 不提交真实 API key。
- 不提交私人截图、账号信息、公司资料、密钥或敏感页面。

## 当前风险 / 遗留项

- `samples/` 目录尚未正式落地；本轮使用临时公开安全样例图完成 smoke。
- `IMAGEPAGE_WORKER_PYTHON_COMMAND` 当前仍建议显式设置，虽然 PATH 上 Python 3.11.9 可用。
- 真实 AI 调用仍依赖外部模型服务和网络。
- 同图多次生成仍可能有轻微差异；`jobId` artifact 复用已缓解重复查询漂移。
- 当前仍未进入 MySQL / Figma / 编辑器 / 多页面阶段。
- `backend/storage/`、`frontend/dist/` 及其他运行副产物不能提交。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- Week 10 原始计划归档：`docs/archive/week/10-acceptance-plan.md`
- Week 10 总结归档：`docs/archive/week/10-summary.md`
- Week 10 smoke 归档：`docs/archive/week/10-dev-smoke.md`
- Week 10 验收报告：`docs/archive/week/10-acceptance-report.md`
- 历史归档：`docs/archive/`

## 当前状态说明

Week 10 已完成收口，当前项目已经进入“可提交 / 可归档 / 可进入 Week 11 规划”的状态。

本次不展开 Week 11 大计划，只保留进入下一周规划的准备状态。
