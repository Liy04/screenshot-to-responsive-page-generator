# Week 04 Day 4A：后端 generated-page artifact API

## 任务目标

线程：后端线程。

新增 generated-page artifact PUT / GET mock 接口，复用本地 mock 文件方案。

## 必须完成

- 新增 `PUT /api/dev/generation-jobs/{jobId}/artifacts/generated-page`。
- 新增 `GET /api/dev/generation-jobs/{jobId}/artifacts/generated-page`。
- PUT 请求体提交完整 `generated-page` artifact。
- 保存到 `backend/mock-data/generated-page-artifacts/{jobId}.generated-page.json`。
- `jobId` 使用白名单校验：`^[A-Za-z0-9_-]{1,64}$`。
- generated-page artifact JSON 文件大小限制建议为 2MB。
- 校验 `artifactType=generated-page`。
- 校验 `htmlCode`、`cssCode` 在 `status=SUCCESS` 时不能为空。
- 允许保存 `status=FAILED` artifact，但前端不用于预览。

## 禁止事项

- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity。
- 不创建 Mapper。
- 不新增数据库配置。
- 不接 Redis / RabbitMQ。
- 不调用 Python Worker。
- 不修改前端或 worker 代码。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day4-backend-generated-artifact-api.md`
- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`
- 后端 Week 03 mock artifact 相关代码

## 建议修改文件

- `backend/src/main/java/com/screenshot/generator/backend/generated/*`
- 必要的后端 mock 存储复用文件

## 验收标准

- PUT 保存成功。
- GET 查询成功。
- 查询不存在 `jobId` 返回 404。
- 非法 `jobId` 返回 400。
- 空请求体或非法 artifact 返回 400。
- 不创建 Entity / Mapper / 数据库配置。

## Codex 执行要求

先输出计划，等待确认后再编码。计划中必须说明 Controller、Service、DTO / VO；未确认数据库前不得新增 Mapper、Entity 或数据库配置。
