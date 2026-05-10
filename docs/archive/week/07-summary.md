# Week 07 Summary

## 本周阶段

Week 07：图片输入场景与 Layout JSON Mock 链路验证。

## 本周目标

把“本地图片选择 -> templateKey -> mock Layout JSON -> 前端展示”的最小闭环补齐，并保持整个链路只做 mock / 本地验证，不接真实 AI、Figma 或数据库。

## 完成内容

- Day 1：文档拆分与 image-to-layout mock 协议完成。
- Day 2：Worker image template layout resolver 完成。
- Day 3：Worker resolver 回归测试完成。
- Day 4：后端 image-layout dev mock API 完成。
- Day 5：后端 image-layout API 自动化测试完成。
- Day 6：前端 `/dev/image-to-layout` 页面完成。
- Day 7A：测试 / 联调 smoke 验收通过。

## 验收结果

- Worker 全量相关测试通过：45 tests OK。
- 后端测试通过：20 tests, 0 failures。
- 前端构建通过：`npm run build`。
- 前端测试通过：4 tests passed。
- 后端 jar 启动成功，8080 可用。
- 前端 dev server 启动成功，5174 可访问。
- `/dev/image-to-layout` 页面入口返回 200。
- Vite proxy 调 `/api/dev/image-layout-jobs` 成功。
- `landing-basic` 返回 SUCCESS。
- `card-list` 返回 SUCCESS。
- `invalid-layout` 返回 200 且 FAILED。
- `unknown-template` 返回 400。
- 不存在 `jobId` 返回 404。
- iframe 使用 `sandbox=""`，未发现 `allow-scripts`。
- 未做 Playwright 视觉回归，符合边界。

## 安全边界

- 不接真实 AI。
- 不接 Figma。
- 不接 MySQL。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不上传真实图片到后端。
- 不让后端调用 Python Worker。
- iframe 只做前端基于 Layout JSON 的 mock 安全预览。

## 未完成事项

- 本周未进入真实 AI / Figma / MySQL 的下一阶段。
- 未做 Playwright 视觉回归。
- 未把 mock 链路升级为真实持久化。

## 后续建议

- Week 08 可以优先考虑更稳定的页面验收方式、mock 数据边界或更清晰的用户路径收敛。
- 若后续要进入真实数据链路，再单独拆分数据库或真实图片输入相关任务。

