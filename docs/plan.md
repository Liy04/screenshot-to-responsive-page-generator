# Plan

## Week 08 名称

图片输入场景与 image-page mock 链路验证。

## 本周目标

Week 08 的目标是把 Week 07 的 image-to-layout mock 链路推进到 image-page mock 链路，形成“本地图片选择 -> imageName + templateKey -> POST /api/dev/image-page-jobs -> layoutArtifact -> generatedPageArtifact -> iframe sandbox="" 安全预览”的最小闭环。

Week 08 已完成收口，当前计划页仅保留结果摘要和下一周建议，不再作为正在执行中的开发计划。

## 本周不做

- 不接真实 AI / OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器 / 在线编辑器。
- 不做真实截图解析。
- 不上传真实图片到后端。
- 不让后端调用 Python Worker。
- 不做 Playwright 视觉回归，除非用户明确批准。

## 每日完成情况

| Day | 线程 | 结果 |
|---|---|---|
| Day 1 | 文档线程 | 已完成：定义 image-page mock API 契约、归档长计划、生成 day-01 到 day-07 任务卡 |
| Day 2 | 后端开发线程 | 已完成：实现 `POST /api/dev/image-page-jobs` 和 `GET /api/dev/image-page-jobs/{jobId}` |
| Day 3 | 后端测试线程 | 已完成：补 image-page API 自动化测试 |
| Day 4 | 前端开发线程 | 已完成：增强 `/dev/image-to-layout` 页面，展示 layoutArtifact 和 generatedPageArtifact |
| Day 5 | 前端测试线程 | 已完成：补页面、API 和 iframe 安全测试 |
| Day 6 | 测试线程 | 已完成：执行 Worker + Backend + Frontend 联调 smoke |
| Day 7 | 文档线程 | 已完成：归档 Week 08 summary / smoke / report material，清理 day 卡 |

## Week 08 完成摘要

### 完成内容

- image-page mock API 已落地。
- image-page API 测试已完成。
- `/dev/image-to-layout` 页面已能展示 generatedPageArtifact。
- 前端测试已完成。
- 联调 smoke 已完成。
- Week 08 summary、smoke、report material 已归档。

### 收口口径

- `docs/tasks/day-*.md` 已清理。
- `docs/tasks/` 仅保留空目录。
- `docs/archive/week/08-plan.md` 保留为完整原始计划。

## 当前约定

- Worker 测试命令使用 `unittest`。
- 后端测试命令使用 `mvn test`。
- 前端测试命令使用 `npm run test`。
- 前端构建命令使用 `npm run build`。
- 后端默认启动优先使用 jar。
- Windows 上传 artifact 优先使用 `curl.exe`。
- `docs/archive/week/08-plan.md` 已保存 Week 08 原始计划，日常不作为默认上下文。

## 后续建议

- Week 09 可以优先考虑统一 Java mock 与 Python fixture 的协议来源。
- 如果要继续扩展能力，建议先补清更清晰的场景边界，再决定是否进入真实数据链路。
- 真实 AI、Figma、MySQL、Redis / RabbitMQ 仍建议单独拆任务，不要和当前 mock 链路混做。
