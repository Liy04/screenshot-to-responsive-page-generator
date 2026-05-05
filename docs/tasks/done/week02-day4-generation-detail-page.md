# Week 02 Day 4：前端任务详情与结果页

## 任务目标

实现任务详情页，根据 `jobId` 查询任务状态和 mock 生成结果，并展示给用户。

## 必须完成

- 提供任务详情路由 `/generation/:jobId`。
- 从路由参数读取 `jobId`。
- 调用 `GET /api/generations/{jobId}` 查询任务状态。
- 调用 `GET /api/generations/{jobId}/result` 查询 mock 结果。
- 展示任务状态、进度、`assetId` 和基础任务信息。
- 展示 mock `layoutJson`、`vueCode`、`cssCode`。
- 提供返回创建任务页的入口。
- 复制代码按钮保持可选，不作为 Day 4 必过项。

## 禁止事项

- 不使用旧版 `id` 参数命名，任务详情路由统一使用 `jobId`。
- 不实现真实代码预览 iframe。
- 不实现在线编辑器。
- 不实现拖拽编辑器。
- 不实现导出 ZIP。
- 不接真实模型 API。
- 不接 Figma API / Figma MCP。
- 不做真实截图解析或真实页面代码生成。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week02-day4-generation-detail-page.md`
- `docs/frontend-pages.md`
- `docs/api-contracts.md`
- `docs/coding-rules.md`
- `frontend/` 中与路由、任务详情页、API 调用相关的代码

## 建议修改文件

- `frontend/src/` 中任务详情页、路由、组件和 API 调用相关文件。
- `README.md` 或 `tests/smoke/README.md`，仅在验证说明确实变化时修改。

## 验收标准

- 直接访问 `/generation/:jobId` 可以触发状态查询。
- 任务成功时可以看到 mock `layoutJson`、`vueCode`、`cssCode`。
- 不存在的 `jobId` 有明确错误提示。
- 页面提供返回创建页入口。
- `npm run build` 通过。

## Codex 执行要求

- 先输出计划，等待确认后再编码。
- 启动 dev server 进行验证时，验证结束后必须停止进程。
- 不提交 `node_modules/`、`dist/`、临时日志文件或其它构建产物。
- 不修改 `backend/`、`worker/` 业务代码，除非用户另行确认。
