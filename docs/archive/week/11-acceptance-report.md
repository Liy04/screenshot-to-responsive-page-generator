# Week 11 Acceptance Report

## 验收结论

Week 11 验收通过，可以收口归档。

本周按“真实 AI 链路可复现验收与样例资产建设”执行，没有扩展到 Week 11 禁止范围。最终产物覆盖 samples、安全 smoke 文档、example 脚本、轻量 metadata 增强、测试记录和安全边界归档。

## 验收清单

- [x] Week 11 Day 1 任务卡与边界确认已完成。
- [x] `samples/` 已建立。
- [x] `samples/` 图片公开安全、可提交。
- [x] `samples/README.md` 已说明每张图的验证目标和安全规则。
- [x] 真实 AI smoke 文档可复现。
- [x] `scripts/smoke-real-ai.example.ps1` 已提供后续本地执行参考。
- [x] `OPENAI_API_KEY` 只通过环境变量配置。
- [x] `REAL_AI` / `FALLBACK` / `FAILED` 判断标准清楚。
- [x] artifact 文件检查口径清楚。
- [x] `jobId` 复用检查口径清楚。
- [x] `durationMs`、`model`、`artifact.reused` 展示、保存和复用已完成。
- [x] Worker `70 / 70` tests OK。
- [x] Backend `45 / 45` tests OK。
- [x] Frontend `10 / 10` tests OK。
- [x] `backend/storage/` 未进入可提交变更。
- [x] `frontend/dist/` 未进入可提交变更。
- [x] 未发现真实 key 泄漏。
- [x] iframe sandbox 未放宽。
- [x] Week 11 summary 已归档。
- [x] Week 11 dev smoke 已归档。
- [x] Week 11 acceptance report 已归档。

## 事实记录

Week 11 完成内容：

1. 完成 Day 1 任务卡与边界确认。
2. 完成 `samples/` 安全样例集。
3. 完成真实 AI smoke 文档和 example 脚本。
4. 完成轻量 metadata 增强：`durationMs`、`model`、`artifact.reused` 展示、保存和复用。
5. 完成最终归档并同步 `docs/current.md`、`docs/plan.md`。

## 测试记录

- Worker：`70 / 70` tests OK。
- Backend：`45 / 45` tests OK。
- Frontend：`10 / 10` tests OK。

## 真实联网 smoke

Day 5 未执行真实联网 smoke。

原因：Day 5 收口不使用真实 key，不触发真实第三方 API 调用。当前文档和 example 脚本已支持后续在具备真实环境变量、网络和本地后端条件时运行。

## 安全验收

- 未发现真实 `OPENAI_API_KEY`、密钥、令牌或敏感材料泄漏。
- `samples/` 不包含真实手机号、账号、用户头像、公司内部页面、第三方品牌或版权不明素材。
- iframe sandbox 未放宽，仍保持无脚本执行能力。
- `backend/storage/` 未进入可提交变更。
- `frontend/dist/` 未进入可提交变更。
- 未提交真实隐私截图或运行副产物。

## 范围验收

Week 11 未进入以下范围：

- MySQL
- Figma / Figma MCP
- Redis
- RabbitMQ
- 多页面生成
- 拖拽编辑器 / 在线编辑器
- ZIP 导出
- 登录注册 / 权限系统
- Playwright 视觉回归

## 剩余风险

- 真实联网 smoke 仍依赖外部模型服务、网络、额度、鉴权和 timeout 配置。
- 后续执行真实联网 smoke 时，需要单独记录具体样例、时间、环境、结果分类和 artifact 检查结果。
- 后续如进入 MySQL / Figma / Redis / RabbitMQ / 多页面 / 编辑器 / Playwright 视觉回归，应重新开新阶段任务卡，不复用 Week 11 范围。
