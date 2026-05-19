# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、当前活跃任务卡和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 11：真实 AI 链路可复现验收与样例资产建设已完成并进入归档状态。

当前项目已经完成 Week 09 真实 AI 最小闭环、Week 10 稳定化收口，以及 Week 11 的 samples 建设、真实 AI smoke 文档化、轻量 metadata 增强和最终验收归档。下一阶段尚未开启新主线。

## Week 11 完成结果

1. 已完成 Day 1 任务卡与 Week 11 边界确认。
2. 已建立公开安全、可提交的 `samples/` 样例集。
3. 已固化真实 AI smoke 的输入、命令、环境变量和验收口径。
4. 已明确 `REAL_AI` / `FALLBACK` / `FAILED` 三种结果判断方式。
5. 已完成轻量 metadata 可解释性增强：`durationMs`、`model`、`artifact.reused` 展示、保存和复用。
6. 已完成 Week 11 summary、dev smoke 和 acceptance report 归档。

## 当前完成基础

- Worker 已支持真实 AI / fallback / failed 路径。
- `promptVersion` 当前为 `week10-v1`。
- JSON 清洗、轻量 repair、`fallbackReason` 已完成。
- 后端已保存 `layout.json`、`preview.html`、`metadata.json` artifact。
- 同一 `jobId` 成功 artifact 可复用。
- 前端已展示 `REAL_AI` / `FALLBACK` / `FAILED` / `TIMEOUT`、`promptVersion`、`fallbackReason`、warnings、errors、artifact 信息。
- 前端已展示 `durationMs`、`model`、`artifact.reused`。
- iframe 使用 `sandbox=""`，无 `allow-scripts`。
- Week 11 最终测试记录：Worker `70 / 70`、Backend `45 / 45`、Frontend `10 / 10` 通过。

## 当前不做

- 不接 MySQL。
- 不设计数据库表。
- 不创建 Entity / Mapper。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不做多页面生成。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。
- 不做登录注册 / 权限系统。
- 不做高保真截图还原。
- 不做 Playwright 视觉回归。
- 不提交真实 API key、私人截图、账号信息、公司资料、密钥或敏感页面。

## 当前风险 / 遗留项

- `samples/` 已正式落地，当前包含 3 张公开安全 mock UI 样例图和说明文档。
- 真实 AI smoke 依赖外部模型服务、网络、环境变量和较长 timeout。
- Week 11 Day 5 收口未执行真实联网 smoke，原因是收口阶段不使用真实 key；文档和 example 脚本已支持后续按环境运行。
- `IMAGEPAGE_WORKER_PYTHON_COMMAND` 建议显式设置为 `D:\environment\python11\python.exe`。
- 后端真实 AI smoke 推荐使用 `--imagepage.worker.timeout-seconds=120`。
- 同图多次生成仍可能有轻微差异；`jobId` artifact 复用已缓解重复查询漂移。
- `backend/storage/`、`frontend/dist/` 及其他运行副产物不能提交。
- 仍未进入 MySQL / Figma / Redis / RabbitMQ / 多页面 / 编辑器 / Playwright 视觉回归。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- Codex 角色边界：`docs/agents/README.md`
- 当前任务卡：`docs/tasks/day-01.md` 到 `docs/tasks/day-05.md`
- Week 11 原始计划归档：`docs/archive/week/11-plan.md`
- Week 11 总结归档：`docs/archive/week/11-summary.md`
- Week 11 smoke 归档：`docs/archive/week/11-dev-smoke.md`
- Week 11 验收归档：`docs/archive/week/11-acceptance-report.md`
- 历史归档：`docs/archive/`

## 当前状态说明

Week 11 已完成 Day 1 到 Day 5 的任务收口，`samples/` 已正式落地。Week 11 的执行结论、测试结果、安全结论和未进入范围已归档到 `docs/archive/week/`。

大任务、跨模块任务或边界不清任务先进入 `explorer-agent` 阶段；实现后进入 `tester-agent` 做最小验证，涉及代码变更时建议进入 `reviewer-agent` 做审查。
