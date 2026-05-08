# Plan

## Week 05 名称

Generated Page 独立预览与质量稳定化（已完成）。

## 本周目标

围绕 generated-page artifact，完善独立预览体验、补齐基础自动化测试、整理端到端 smoke 流程，让项目从“能跑通”升级到“能稳定验收”。

Week 05 已完成收口，不再扩大范围，也不急着接真实 AI、数据库、Figma 或复杂编辑器。

## 本周完成情况

| Day | 线程 | 状态 | 结果 |
|---|---|---|---|
| Day 1 | 文档线程 | 完成 | Docs Lite 文档定范围完成。 |
| Day 2 | 前端线程 | 完成 | 任务详情页 generated-page UX 解耦完成。 |
| Day 3 | 前端线程 | 完成 | generated-page 独立 dev preview 页面完成。 |
| Day 4 | 后端测试线程 | 完成 | generated-page artifact mock 接口测试完成，`mvn test` 通过。 |
| Day 5 | Worker 线程 | 完成 | Worker 静态编译器 style subset 小幅增强完成，`python -m unittest worker.test_layout_static_generator` 通过。 |
| Day 6 | 文档 / 测试线程 | 完成 | `docs/dev-smoke-week05.md` 完成，端到端 smoke 已通过。 |
| Day 7 | 文档 / 总结线程 | 完成 | Week 05 总结归档完成。 |

## 本周核心目标

1. 修正前端任务详情页 UX，使 generated-page 展示不依赖旧 Week 02 generation job 查询结果。
2. 新增 generated-page 独立 dev preview 页面。
3. 为后端 generated-page artifact mock 接口补充自动化测试。
4. 小幅增强 Worker 静态编译器对常见安全 style subset 的支持。
5. 整理 Worker -> Backend -> Frontend 的 Week 05 dev smoke 文档。
6. 完成 Week 05 总结归档。

## P0：必须完成

- 修正现有任务详情页 generated-page UX。
- 新增 generated-page 独立 dev preview 页面。
- 补后端 generated-page artifact mock 接口测试。
- 整理 Week 05 dev smoke 文档。
- 完成 Week 05 总结归档。

## P1：应该完成

- 优化前端 generated-page 展示结构。
- Worker 静态编译器小幅增强安全 style subset。
- 补充 Worker unittest。

## P2：有余力再做

- 前端轻量自动化测试。
- 更完整的异常状态展示。
- 更细的实践报告素材整理。

## Week 05 结论

Week 05 主要任务已完成，当前处于收口归档状态，建议通过。

## Week 06 候选方向

1. 修正前端详情页 UX 的边角体验，让 generated-page dev preview 更独立。
2. 补后端 / 前端更稳定的自动化测试，减少回归风险。
3. 增强静态编译器对更多 Layout JSON 节点和 style subset 的支持。
4. 如用户确认，再规划 MySQL 持久化，但当前不要直接进入。

## 本周不做

- 不接真实 AI / OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL 实际落库。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器 / 在线编辑器。
- 不做真实截图解析。
- 不做登录注册 / 历史记录持久化 / 复杂权限。
- 不要求 `vueCode` 真正可运行。
- 不做复杂响应式布局算法。
- 不做 Tailwind 代码生成。
- 不做 Vue SFC 可运行化。
- 不做 Playwright 视觉回归，除非用户明确批准。

## 当前约定

- Worker 测试命令使用 `unittest`。
- Windows 上传命令优先使用 `curl.exe`。
- 前端日常 smoke 使用 `npm run dev`。
- 后端默认启动方式使用 `java -jar`。
- `docs/dev-smoke-week05.md` 作为 Week 05 smoke 的可重复说明。

当前唯一任务卡见 `docs/task.md`。
