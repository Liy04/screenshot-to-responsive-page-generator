# Week 08 Summary

## 本周阶段

Week 08：image-page mock 链路验证。

## 本周目标

把 Week 07 的 image-to-layout mock 链路推进到 image-page mock 链路，完成从本地图片场景 mock 输入到 generated-page mock 预览的闭环。

## 完成内容

- image-page mock API 已完成。
- image-page API 测试已完成。
- `/dev/image-to-layout` 页面已完成并能展示 generatedPageArtifact。
- 前端测试已完成。
- 联调 smoke 已完成。
- Week 08 的 smoke、summary、report material 已完成归档。

## 验收结果

- image-page mock API：通过。
- `landing-basic`：通过。
- `card-list`：通过。
- `invalid-layout`：通过。
- `unknown-template`：通过。
- 不存在 `jobId`：通过。
- `/dev/image-to-layout` 页面：通过。
- generated-page iframe 安全预览：通过。
- 前端测试：通过。
- 联调 smoke：通过。

## 安全边界

- 不接真实 AI。
- 不接 Figma。
- 不接 MySQL。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不上传真实图片到后端。
- 不让后端调用 Python Worker。
- iframe 使用 `sandbox=""`，不允许 `allow-scripts`。

## 未完成事项

- 未进入真实 AI 链路。
- 未进入真实图片上传和持久化链路。
- 未做 Playwright 视觉回归。

## 当前风险

- 仍是 mock 链路，不是真实数据链路。
- Java mock 与 Python fixture 的协议来源后续仍有统一空间。
- 还没有真实图片解析能力。
- 还没有数据库持久化能力。

## 后续建议

- Week 09 可以优先考虑统一 Java mock 与 Python fixture 的协议来源。
- 或者增强 Layout JSON 节点和样式表达能力。
- 暂不建议直接接真实 AI 或 MySQL。
