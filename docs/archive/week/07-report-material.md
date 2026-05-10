# Week 07 Report Material

## 可写入实践报告的内容

Week 07 完成了图片输入场景下的 image-to-layout mock 链路验证，目标不是接入真实 AI 或真实图片处理，而是把“本地图片选择 -> templateKey -> mock Layout JSON -> 前端展示”的最小闭环跑通，并保证整条链路可以复现、可以演示、可以验收。

## 本周新增模块

- Worker image template layout resolver
- Worker resolver 回归测试
- 后端 image-layout dev mock API
- 后端 image-layout API 自动化测试
- 前端 `/dev/image-to-layout` 页面
- Dev smoke 文档

## 技术实现说明

- Worker 只负责本地离线 mock resolver，不调用后端，也不接真实 AI。
- 后端只做 Java 侧 mock 模板和固定数据返回，使用现有 `ApiResponse` 包装。
- 前端页面只接 `imageName` 和 `templateKey` 的 mock job 流程，不上传真实图片到后端。
- iframe 采用 `sandbox=""`，并且不允许 `allow-scripts`，保证预览安全边界清晰。
- `invalid-layout` 与 `unknown-template` 分开处理：前者是已知失败模板，后者是请求参数错误。

## 测试与验证说明

- Worker 相关测试已通过。
- 后端 API 测试已通过。
- 前端构建与页面测试已通过。
- Day 7A smoke 验证已通过。
- 8080 占用时的备用端口 18080 和 `VITE_API_PROXY_TARGET` 说明已写入 smoke 文档。

## 当前局限

- 仍是 mock 链路，不是真实 AI 生成。
- 不接 Figma。
- 不接 MySQL 持久化。
- 不上传真实图片到后端。
- 不调用 Python Worker 作为后端依赖。
- 不做 Playwright 视觉回归。

## 下一步可选方向

- 继续增强页面体验和验收稳定性。
- 扩大 mock 模板覆盖范围，但仍保持离线 / 本地 mock。
- 如果未来要进入真实链路，再单独拆分真实图片输入、数据库持久化和 AI 接入任务。

