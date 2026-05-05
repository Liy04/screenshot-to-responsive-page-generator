# Week 03 Day 6：P1 可选 Mock 保存与基础查看

## 任务目标

只在 P0 全部完成后，执行 P1 mock 保存 / 查询和前端基础查看。

## 必须完成

- 如执行后端 mock：使用 `mock-data/layout-artifacts/{jobId}.layout.json`。
- 如执行后端 mock：实现 PUT / GET mock 接口。
- 如执行前端查看：只做格式化 JSON、状态和错误信息展示。
- 明确本任务是 P1，不影响 Week 03 P0 验收。

## 禁止事项

- 不连接 MySQL。
- 不新增 Entity / Mapper。
- 不写 MyBatis-Plus 持久层代码。
- 不接 Redis / RabbitMQ。
- 不接真实 AI、模型 API、Figma API / Figma MCP。
- 不做 Vue 页面代码生成。
- 不做 JSON 在线编辑器。
- 不做拖拽编辑器或导出 ZIP。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week03-day6-optional-mock-viewer.md`
- `docs/layout-api-contracts.md`
- 当前任务相关前端或后端代码

## 建议修改文件

- 后端 mock Controller / DTO / MockStorageService，若执行后端 mock。
- 前端基础查看页和 API 调用文件，若执行前端查看。
- `tests/smoke/README.md`，仅在验证说明需要同步时修改。
- `docs/week/03-status.md`，仅在状态需要同步时修改。

## 验收标准

- P0 已确认完成。
- mock 保存 / 查询不依赖数据库。
- 前端查看不包含编辑器能力。
- 构建或后端最小验证通过。

## Codex 执行要求

- 先输出计划，等待确认后再执行。
- 计划中必须确认 P0 已完成。
- 启动 dev server 或后端服务后，验证完成必须停止进程。
- 不提交构建产物、上传文件或 mock 运行副产物。
