# Week 05 总结归档

## 阶段目标

Week 05 的目标是围绕 generated-page artifact 做独立预览与质量稳定化，让 Week 04 跑通的闭环进一步稳定、清晰、可复现、可验收，并能写入实践报告。

## 完成内容

- 修正前端任务详情页 generated-page UX，让展示不再依赖旧 Week 02 generation job 查询结果。
- 新增 generated-page 独立 dev preview 页面。
- 补充后端 generated-page artifact mock 接口自动化测试。
- 小幅增强 Worker 静态编译器的常见安全 style subset。
- 整理 Worker -> Backend -> Frontend 的 Week 05 dev smoke 文档。
- 完成 Week 05 收口与归档。

## Day 1 到 Day 6 完成情况

### Day 1

Docs Lite 文档定范围完成，Week 05 原始计划进入 Lite 入口和归档入口。

### Day 2

前端任务详情页 generated-page UX 解耦完成，generated-page 展示不再依赖旧 Week 02 generation job 查询结果。

### Day 3

generated-page 独立 dev preview 页面完成，形成更清晰的独立预览入口。

### Day 4

后端 generated-page artifact mock 接口测试完成，`mvn test` 通过。

### Day 5

Worker 静态编译器 style subset 小幅增强完成，`python -m unittest worker.test_layout_static_generator` 通过。

### Day 6

Week 05 dev smoke 文档完成，补充了 8080 占用时的备用端口流程、`VITE_API_PROXY_TARGET` 代理口径和端到端 smoke 说明；端到端 smoke 已通过。

## 前端完成情况

- 前端任务详情页的 generated-page 区域已经解耦，失败状态不会拖垮整个详情页。
- 新增了 generated-page 独立 dev preview 页面。
- iframe 预览使用 `sandbox=""`，不允许 `allow-scripts`。
- 前端侧已支持使用代理环境变量切换后端端口的 smoke 口径。

## 后端测试完成情况

- generated-page artifact mock 接口已补充自动化测试。
- 接口覆盖了保存、查询、404、400 等关键路径。
- 后端仍保持本地 mock 文件方案，不接 MySQL。

## Worker 完成情况

- Worker 静态编译器已完成小幅安全 style subset 增强。
- Worker 仍然是确定性规则编译，不是真实 AI 生成。
- Worker 测试使用 `unittest` 口径。

## dev smoke 完成情况

- `docs/dev-smoke-week05.md` 已完成。
- Worker 编译命令使用项目根目录 `examples`。
- 后端默认启动方式使用 `java -jar`。
- 前端日常 smoke 使用 `npm run dev`。
- Windows 上传 generated-page artifact 时优先使用 `curl.exe`。
- 已补充 8080 占用时切换到 18080 的备用端口流程。

## 安全验证结果

- `iframe` 使用 `sandbox=""`。
- `iframe` 不允许 `allow-scripts`。
- `status=SUCCESS` 时展示 iframe。
- `status=FAILED` 时不展示 iframe，只展示失败原因和 validation 信息。
- `script`、inline event 和 `javascript:` URL 等安全规则保持不变。

## 未完成事项

- 没有接真实 AI / OpenAI / Claude / Gemini SDK。
- 没有接 Figma API / Figma MCP。
- 没有接 MySQL、Redis、RabbitMQ。
- 没有创建数据库表、Entity 或 Mapper。
- 没有做 ZIP 导出、拖拽编辑器、在线编辑器或真实截图解析。

## 已知风险

- 详情页旧 Week 02 generation 查询失败时，会显示旧任务信息不可用的降级提示，但不影响 Week 05 generated-page 区域展示；后续可继续优化提示文案。
- `backend/target`、`frontend/dist` 是构建副产物，按忽略规则处理。
- `backend/mock-data` 是本地 mock 副产物，按忽略规则处理。
- 当前 generated-page 保存仍是本地 mock 文件，不是数据库持久化。
- 当前 Layout JSON 仍来自手写 / 示例，不是真实截图解析。
- 当前静态编译器是规则编译，不是真实 AI 生成。

## Week 06 建议方向

1. 修正前端详情页 UX 的边角体验，让 generated-page dev preview 更独立。
2. 补后端 / 前端更稳定的自动化测试，减少回归风险。
3. 增强静态编译器对更多 Layout JSON 节点和 style subset 的支持。
4. 如用户确认，再规划 MySQL 持久化，但当前不要直接进入。
