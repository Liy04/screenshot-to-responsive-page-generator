# Week 08 Report Material

## 本周成果

Week 08 完成了 image-page mock 与 generated-page mock 预览链路打通，实现从图片场景 mock 输入到页面产物 mock 预览的完整闭环。

## 核心能力

- 支持 `imageName + templateKey` 创建 image-page dev mock job。
- 支持 `landing-basic` / `card-list` 成功生成 `layoutArtifact` 与 `generatedPageArtifact`。
- 支持 `invalid-layout` 失败链路验证。
- 支持 `unknown-template` 400 与不存在 `jobId` 404。
- 前端支持 generated-page iframe 安全预览。

## 技术亮点

- 使用 dev mock API 验证生成链路，避免过早接入真实 AI。
- 使用 `ApiResponse` 统一接口响应。
- 使用 iframe `sandbox=""` 控制预览安全。
- 保持真实图片不上传，仅在浏览器本地预览。
- 保持后端不调用 Python Worker，降低 Week 08 集成复杂度。

## 测试结果

- Backend `mvn test`: PASS。
- Worker unittest: PASS。
- Frontend `npm run test`: PASS。
- Frontend `npm run build`: PASS。

## 当前边界

- 未接真实 AI。
- 未接 Figma。
- 未接数据库。
- 未接 Redis / RabbitMQ。
- 未上传真实图片。
- 未调用 Python Worker。
- 未做 ZIP 导出。

## 下一步方向

- Week 09 建议优先处理协议统一或 Layout JSON 表达能力增强。
- 暂不建议直接接真实 AI。
- 暂不建议直接接 MySQL。
