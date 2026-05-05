# Week 02 Day 3：前端创建任务页

## 任务目标

实现前端工作台与创建任务页，让用户可以选择图片、预览图片、上传截图、创建生成任务，并跳转到任务详情页。

## 必须完成

- 引入并配置 `vue-router`。
- 提供工作台首页 `/`，可选别名 `/dashboard`。
- 提供创建任务页 `/generation/create`。
- 支持选择图片和本地预览。
- 调用上传接口 `POST /api/assets/upload`。
- 调用创建任务接口 `POST /api/generations`。
- 创建成功后跳转 `/generation/:jobId`。
- 处理 loading、错误提示和非法文件提示。

## 禁止事项

- 不实现真实截图解析。
- 不实现真实代码生成。
- 不接真实模型 API。
- 不接 Figma API / Figma MCP。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做导出 ZIP。
- 不做复杂 UI 大改版。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week02-day3-frontend-create-page.md`
- `docs/frontend-pages.md`
- `docs/api-contracts.md`
- `docs/coding-rules.md`
- `frontend/` 中与入口、路由、页面、接口调用相关的代码

## 建议修改文件

- `frontend/src/` 中路由、页面、组件和 API 调用相关文件。
- `README.md` 或 `tests/smoke/README.md`，仅在启动或验证说明确实变化时修改。

## 验收标准

- `/` 或 `/dashboard` 可以进入创建任务页。
- `/generation/create` 可以选择图片并展示本地预览。
- 上传成功后可以创建任务。
- 创建成功后跳转 `/generation/:jobId`。
- 非法文件或接口失败时有错误提示。
- `npm run build` 通过。

## Codex 执行要求

- 先输出计划，等待确认后再编码。
- 启动 dev server 进行验证时，验证结束后必须停止进程。
- 不提交 `node_modules/`、`dist/`、临时日志文件或其它构建产物。
- 不修改 `backend/`、`worker/` 业务代码，除非用户另行确认。
