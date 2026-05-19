# Week 11 Summary

## 主题

真实 AI 链路可复现验收与样例资产建设。

## 完成结论

Week 11 已完成。项目没有进入 MySQL、Figma、Redis、RabbitMQ、多页面、编辑器、Playwright 视觉回归等新主线，而是围绕 Week 09 / Week 10 已跑通的真实 AI 链路完成资产化、文档化、轻量可解释性增强和最终验收归档。

## 已完成事项

1. Day 1 已完成 Week 11 任务卡与边界确认。
2. Day 2 已完成 `samples/` 安全样例集。
3. Day 3 已完成真实 AI smoke 文档和 example 脚本。
4. Day 4 已完成轻量 metadata 增强：`durationMs`、`model`、`artifact.reused` 展示、保存和复用。
5. Day 5 已完成 Week 11 summary、dev smoke、acceptance report 归档，并同步 `docs/current.md`、`docs/plan.md` 状态。

## 主要交付物

- `docs/tasks/day-01.md` 到 `docs/tasks/day-05.md`
- `samples/README.md`
- `samples/01-simple-card-page.png`
- `samples/02-simple-form-page.png`
- `samples/03-dashboard-cards-page.png`
- `docs/smoke/real-ai-smoke.md`
- `scripts/smoke-real-ai.example.ps1`
- `docs/archive/week/11-summary.md`
- `docs/archive/week/11-dev-smoke.md`
- `docs/archive/week/11-acceptance-report.md`

## 测试结果

- Worker：`70 / 70` tests OK。
- Backend：`45 / 45` tests OK。
- Frontend：`10 / 10` tests OK。

## Smoke 结论

Week 11 已完成真实 AI smoke 文档化和 example 脚本准备，但 Day 5 收口未执行真实联网 smoke。

原因：Day 5 收口不使用真实 `OPENAI_API_KEY`，避免在归档阶段引入真实 key、真实第三方调用或不可复现的外部服务状态。

后续如需执行真实联网 smoke，应按 `docs/smoke/real-ai-smoke.md` 和 `scripts/smoke-real-ai.example.ps1` 在本地环境设置真实环境变量后手动运行。

## 安全结论

- 未发现真实 key 泄漏。
- `OPENAI_API_KEY` 只允许通过环境变量配置。
- `samples/` 为公开安全 mock UI 样例，无隐私、品牌、版权阻塞。
- iframe sandbox 未放宽，仍保持 `sandbox=""`，未加入 `allow-scripts`。
- `backend/storage/` 未进入可提交变更。
- `frontend/dist/` 未进入可提交变更。
- 未提交真实隐私截图、真实账号信息、公司内部页面或运行副产物。

## 未进入范围

Week 11 明确未进入：

- MySQL
- Figma / Figma MCP
- Redis
- RabbitMQ
- 多页面生成
- 拖拽编辑器 / 在线编辑器
- Playwright 视觉回归

## 后续建议

下一阶段如继续推进，可以在不扩大 Week 11 归档事实的前提下，单独规划真实联网 smoke 执行记录、Playwright 视觉回归、Figma 输入或持久化能力。以上方向均应作为新阶段任务重新拆分和验收。
