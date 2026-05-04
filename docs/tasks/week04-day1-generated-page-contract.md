# Week 04 Day 1：generated-page 契约与映射规则

## 任务目标

线程：文档线程。

完成 Week 04 generated-page artifact 契约、Layout JSON 到 HTML/CSS 映射、安全规则和 P0 / P1 / P2 边界定稿。

## 必须完成

- 更新 `docs/generated-page-artifact-design.md`。
- 更新 `docs/layout-to-html-mapping.md`。
- 必要时同步 `docs/week/04-plan.md`。
- 明确 validator 失败处理口径。
- 明确后端 PUT 请求体提交完整 `generated-page` artifact。
- 明确 iframe 使用 `sandbox=""`，不加 `allow-scripts`。
- 明确 `jobId` 白名单：只允许字母、数字、下划线、短横线。
- 明确 generated-page artifact JSON 文件大小限制建议为 2MB。

## 禁止事项

- 不写业务代码。
- 不改 `worker/`。
- 不改 `backend/`。
- 不改 `frontend/`。
- 不创建数据库内容。
- 不接 AI / Figma / MySQL / Redis / RabbitMQ。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day1-generated-page-contract.md`
- `docs/week/04-plan.md`
- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`

## 建议修改文件

- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`
- `docs/week/04-plan.md`

## 验收标准

- artifact 字段完整且口径统一。
- validator 失败时只保留一种处理方式。
- 后端请求体结构清楚。
- HTML / CSS 安全规则清楚。
- P0 / P1 / P2 边界清楚。

## Codex 执行要求

先输出计划，等待确认后再修改文档。完成后汇报改动文件、主要改动、验证步骤、验证结果和风险。
