# Week 02 Day 2：后端生成任务接口

## 任务目标

实现生成任务创建、任务状态查询和 mock 结果查询接口，跑通后端任务侧最小闭环。

## 必须完成

- 实现 `POST /api/generations`。
- 实现 `GET /api/generations/{jobId}`。
- 实现 `GET /api/generations/{jobId}/result`。
- 使用后端内存 Map 暂存任务数据。
- 创建任务后可以直接返回 `success` 状态。
- 返回 mock `layoutJson`、`vueCode`、`cssCode`。
- 不存在的 `assetId` 或 `jobId` 返回明确错误。

## 禁止事项

- 不接 MySQL。
- 不创建数据库表。
- 不创建 Mapper。
- 不创建 Entity 或实体表映射。
- 不新增数据库配置。
- 不接 Redis / RabbitMQ。
- 不调用 Python Worker 执行真实任务。
- 不接真实模型 API。
- 不接 Figma API / Figma MCP。
- 不做真实截图解析或真实页面代码生成。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week02-day2-generation-api.md`
- `docs/api-contracts.md`
- `docs/coding-rules.md`
- `backend/` 中与任务接口、统一响应、上传资源记录相关的代码

## 建议修改文件

- `backend/` 中生成任务相关 Controller / Service / DTO / VO / 内存模型。
- `tests/smoke/README.md`，仅在需要补充接口验证说明时修改。

## 验收标准

- 创建任务接口返回 `jobId` 和 `status`。
- 查询任务状态接口返回 `jobId`、`assetId`、`status`、`progress`。
- 查询结果接口返回 mock `layoutJson`、`vueCode`、`cssCode`。
- 不存在的 `jobId` 返回 HTTP `404` 和统一错误结构。
- `mvn package -DskipTests` 通过。

## Codex 执行要求

- 先输出计划，等待确认后再编码。
- 计划中必须说明涉及的 Controller、Service、Mapper、DTO、VO；本任务默认不涉及 Mapper。
- mock 阶段优先使用固定数据或简单内存数据。
- 编码后执行最小验证。
- 不修改 `frontend/`、`worker/` 业务代码。
