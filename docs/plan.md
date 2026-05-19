# Plan

## Week 11 名称

真实 AI 链路可复现验收与样例资产建设。

## 本周总目标

Week 11 不开启 MySQL、Figma、编辑器、多页面等新主线，而是把 Week 09 / Week 10 已经跑通的真实 AI 能力沉淀为可复现、可验收、可展示、可回归的项目资产。

当前状态：Week 11 已完成并归档。

核心链路：

```text
公开安全 samples
-> 真实 AI smoke
-> Worker / Backend / Frontend 验收
-> artifact 检查
-> 安全与密钥检查
-> Week 11 总结归档
```

## 本周不做

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

## Day 计划

| Day | 主题 | 负责角色 | 交付物 |
|---|---|---|---|
| Day 1 | Week 11 任务卡与边界确认 | lead + docs-agent | `docs/tasks/day-01.md` 到 `day-05.md`、归档长计划 |
| Day 2 | samples/ 安全样例集 | explorer-agent -> docs-agent -> tester-agent -> reviewer-agent | `samples/`、样例说明、安全检查 |
| Day 3 | 真实 AI smoke 文档与示例脚本 | docs-agent -> tester-agent | `docs/smoke/real-ai-smoke.md`、可选 example 脚本 |
| Day 4 | metadata 可解释性小增强 | explorer-agent -> worker/backend/frontend -> tester-agent -> reviewer-agent | `durationMs`、`model`、`artifact.reused` 最小增强 |
| Day 5 | Week 11 验收、总结与 Git 收口 | lead + tester-agent + reviewer-agent + docs-agent | Week 11 summary / smoke / acceptance report |

执行结果：

- Day 1 已完成任务卡与边界确认。
- Day 2 已完成 `samples/` 安全样例集。
- Day 3 已完成真实 AI smoke 文档和 example 脚本。
- Day 4 已完成轻量 metadata 增强：`durationMs`、`model`、`artifact.reused` 展示、保存和复用。
- Day 5 已完成 Week 11 最终归档与 current / plan 状态同步。

## Day 4 范围控制

Day 4 是可选任务。只有 Day 2 / Day 3 完成后才执行。

Day 4 只允许做轻量 metadata polish，优先字段：

- `durationMs`
- `model`
- `artifact.reused`

默认不做 `sourceImageName` 和 `baseUrlHost`。如后续确实需要，必须单独验收隐私和配置泄漏风险。

## 验收重点

- `samples/` 图片公开安全、可提交。
- 真实 AI smoke 文档可复现。
- `OPENAI_API_KEY` 只通过环境变量配置。
- `REAL_AI` / `FALLBACK` / `FAILED` 判断标准清楚。
- artifact 文件检查和 `jobId` 复用检查清楚。
- 前端能展示 `durationMs` / `model` / `artifact.reused`。
- Worker `70 / 70`、Backend `45 / 45`、Frontend `10 / 10` 测试通过。
- Week 11 Day 5 未执行真实联网 smoke，原因是收口阶段不使用真实 key；文档和 example 脚本支持后续按环境运行。
- 未发现真实 key 泄漏；samples 无隐私 / 品牌 / 版权阻塞；iframe sandbox 未放宽。
- `backend/storage/`、`frontend/dist/`、真实隐私截图和运行副产物未进入可提交变更。

## 当前执行入口

Week 11 已执行完成。执行记录入口：

- `docs/tasks/day-01.md`
- `docs/tasks/day-02.md`
- `docs/tasks/day-03.md`
- `docs/tasks/day-04.md`
- `docs/tasks/day-05.md`

原始长计划已归档到 `docs/archive/week/11-plan.md`，不作为日常默认上下文。

最终归档入口：

- `docs/archive/week/11-summary.md`
- `docs/archive/week/11-dev-smoke.md`
- `docs/archive/week/11-acceptance-report.md`
