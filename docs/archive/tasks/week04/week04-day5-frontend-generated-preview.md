# Week 04 Day 5：前端 generated-page 安全预览

## 任务目标

线程：前端线程。

新增 GeneratedPageViewer、CodeTabs、PagePreviewFrame，实现 generated-page artifact 的代码展示和 iframe sandbox 安全预览。

## 必须完成

- 新增 generated-page artifact 查询 API。
- 新增 `GeneratedPageViewer` 页面。
- 新增 `CodeTabs` 组件，展示 HTML / CSS / Vue 文本。
- 新增 `PagePreviewFrame` 组件，使用 iframe 预览 `htmlCode + cssCode`。
- iframe 必须使用 `sandbox=""`。
- 不添加 `allow-scripts`。
- 展示 `status`、`errorMessage`、`warnings`、`unsupportedNodes`。
- `status=FAILED` 时不做可视化预览，只展示失败信息。
- `vueCode` 只展示文本，不要求可运行。

## 禁止事项

- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。
- 不接 AI。
- 不接 Figma。
- 不修改后端或 worker 代码。
- 不引入大型依赖。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day5-frontend-generated-preview.md`
- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`
- Week 03 前端 Layout JSON 查看页相关代码

## 建议修改文件

- `frontend/src/api/devGeneratedPageArtifact.js`
- `frontend/src/views/GeneratedPageViewer.vue`
- `frontend/src/components/generated/CodeTabs.vue`
- `frontend/src/components/generated/PagePreviewFrame.vue`
- 必要的路由文件
- 必要的样式文件

## 验收标准

- `npm run build` 通过。
- `/generation/{jobId}/generated-page` 可访问。
- 可以请求后端 generated-page artifact。
- HTML / CSS / Vue 文本可展示。
- iframe sandbox 预览正常。
- 404、FAILED、warnings、unsupportedNodes 有明确展示。

## Codex 执行要求

先输出计划，等待确认后再编码。验证完成后如启动 dev server，需要停止进程，不留下后台服务。
