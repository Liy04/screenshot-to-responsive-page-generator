# Week 03 状态看板

## 文件目的

本文件用于记录 Week 03 Layout JSON v0.1 稳定落地的实际进展、线程状态、验收结果、风险和下一步计划。

周计划以 `docs/week/03-plan.md` 为准，实际执行以 `docs/tasks/week03-*.md` 单任务卡为准。

## 当前日期 / Day

- 当前日期：2026-05-01
- 当前 Day：Week 03 最终验收通过
- 当前阶段：Layout JSON v0.1 稳定落地已完成

## 今日目标

根据当前可见验收记录完成 Week 03 文档收口：

- 更新 Week 03 状态看板。
- 填写 Week 03 总结。
- 补充 Week 03 smoke 说明。
- 记录 Week 04 输入。

说明：当前文档上下文中未提供独立的测试线程 Day 7A 输出原文；本看板以已有状态记录和 smoke 文档中可确认的验收项为依据。

## 线程分工

| 线程 | 职责 |
|---|---|
| 项目经理线程 | 控制 Week 03 P0 / P1 / P2 范围并确认最终收口 |
| 文档线程 | 维护周计划、专项文档、任务卡、状态看板和总结 |
| Worker / 校验器线程 | 实现 Layout JSON 校验器和测试 |
| 测试线程 | 执行校验器 smoke、mock 接口 smoke、前端查看页 smoke |
| 后端开发线程 | P1 本地文件 mock 保存 / 查询 |
| 前端开发线程 | P1 基础 Layout JSON 查看页 |

## 线程状态

状态枚举：待执行 / 执行中 / 待验收 / 通过 / 阻塞

| 线程 | 当前状态 | 说明 |
|---|---|---|
| 项目经理线程 | 通过 | 已完成 Week 03 最终验收，确认本周可收口 |
| 文档线程 | 通过 | Day 7B 文档收口已完成并通过确认 |
| Worker / 校验器线程 | 通过 | valid / invalid smoke 和单元测试通过 |
| 测试线程 | 通过 | Week 03 最终 smoke 已由项目经理复验通过 |
| 后端开发线程 | 通过 | P1 后端 Layout JSON 本地文件 mock 保存 / 查询已通过 |
| 前端开发线程 | 通过 | P1 前端 Layout JSON 基础查看页已通过项目经理复验 |

## 验收结果

### 文档拆分验收

- [x] `docs/week/03-plan.md` 已收敛为周计划。
- [x] `docs/context/current-phase.md` 已更新为 Week 03。
- [x] `docs/layout-schema-design.md` 已存在。
- [x] `docs/layout-api-contracts.md` 已存在。
- [x] `docs/database-artifact-draft.md` 已存在，并明确只是后续草案。
- [x] `docs/week/03-status.md` 已存在。
- [x] `docs/week/03-summary.md` 已存在。
- [x] `docs/tasks/` 下 7 张 Week 03 任务卡已存在。
- [x] `docs/prompt-templates.md` 已补充 Week 03 轻量任务模板。

### Day 1 文档验收

- [x] `docs/layout-schema-design.md` 已说明 Layout JSON 是什么。
- [x] 已说明为什么需要中间层。
- [x] 已说明为什么 Layout JSON 不是 HTML / Vue。
- [x] 已明确 v0.1 顶层字段。
- [x] 已明确支持和暂不支持的节点类型。
- [x] 已说明 `bounds`、`constraints`、`responsive`、`assumptions`、`warnings`。
- [x] 已说明当前限制和后续扩展方向。
- [x] 未将 P1 / P2 内容写成 P0。

### Day 5 校验器 smoke 验收

- [x] `examples/valid/landing-page.layout.json` 输出 `校验通过`。
- [x] `examples/valid/login-page.layout.json` 输出 `校验通过`。
- [x] `examples/valid/dashboard-card.layout.json` 输出 `校验通过`。
- [x] `examples/valid/mobile-list.layout.json` 输出 `校验通过`。
- [x] `examples/valid/profile-page.layout.json` 输出 `校验通过`。
- [x] `examples/invalid/invalid-missing-version.layout.json` 失败并包含 `SCHEMA_VALIDATION_ERROR`。
- [x] `examples/invalid/invalid-duplicate-node-id.layout.json` 失败并包含 `DUPLICATE_NODE_ID`。
- [x] `examples/invalid/invalid-responsive-target.layout.json` 失败并包含 `RESPONSIVE_TARGET_NOT_FOUND`。
- [x] `python -m unittest worker.test_layout_validator` 通过。
- [x] 未接 MySQL / Entity / Mapper / Redis / RabbitMQ / AI / Figma。
- [x] 未修改 `schema/layout.schema.json`。
- [x] 未修改示例文件。
- [x] 未修改前端或后端业务代码。

### Day 6A 后端 mock 保存 / 查询验收

- [x] 已确认 P0 完成后再执行 P1。
- [x] `mvn package -DskipTests` 通过。
- [x] `PUT /api/dev/generation-jobs/{jobId}/artifacts/layout-json` 保存成功。
- [x] `GET /api/dev/generation-jobs/{jobId}/artifacts/layout-json` 查询成功。
- [x] 查询不存在的 `jobId` 返回 404。
- [x] 保存空 `layoutJson` 返回 400。
- [x] 使用本地文件 `mock-data/layout-artifacts/{jobId}.layout.json` 保存 mock 数据。
- [x] `mock-data/` 已加入 `backend/.gitignore`。
- [x] 未接 MySQL / Entity / Mapper / Redis / RabbitMQ / AI / Figma。

### Day 6B 前端查看验收

- [x] `npm run build` 通过。
- [x] `/layout-json-viewer` 返回 200。
- [x] `/generation/{jobId}/layout-json` 返回 200。
- [x] 前端通过 Vite proxy 查询 Layout JSON 成功。
- [x] 查询不存在的 `jobId` 返回 404，并由页面错误态承接。
- [x] 未实现 JSON 在线编辑器、拖拽编辑器、导出 ZIP 或 Vue 页面生成能力。

### Week 03 最终验收

- [x] Week 03 P0 验收通过。
- [x] P1 后端 mock 保存 / 查询通过。
- [x] P1 前端 Layout JSON 查看页通过。

Week 03 收口结论：通过，可收口。

## 风险

- P1 mock 保存和前端查看不能被误认为 Week 03 P0。
- 数据库草案不能被误当成 Week 03 默认任务。
- Week 03 不做真实 AI 或 Vue 页面生成，避免把 Week 04 内容提前。
- Day 5 曾发现 Windows / PowerShell 捕获环境下校验器中文 CLI 输出可能乱码，记录显示已通过显式设置 stdout / stderr 为 UTF-8 修复。
- 后端 mock 使用本地文件 `mock-data/layout-artifacts/{jobId}.layout.json`，该目录为本地副产物，不应提交。

## 下一步

- Week 03 已通过最终验收并可收口。
- Week 04 可进入 Layout JSON -> Vue3 静态页面初稿生成任务，但仍需另开任务确认范围。
