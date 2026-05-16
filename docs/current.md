# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、当天对应的 `docs/tasks/day-xx.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 10：真实 AI 链路稳定化与可复现验收。

## 阶段背景

Week 09 已完成真实 AI 最小闭环。Week 10 不追求大型功能扩展，而是把已有真实链路做稳、做清楚、做成可重复验收的状态。

Week 10 关注的主链路仍然是：

```text
真实图片上传
-> 后端保存临时文件
-> 后端调用 Python Worker
-> Worker 调真实 AI
-> Layout JSON v0.1
-> previewHtml
-> 前端展示原图、Layout JSON 和 iframe 预览
```

## 当前目标

1. 让真实 AI 输出更稳定。
2. 让失败原因更清楚。
3. 让同一 `jobId` 结果可复用。
4. 让前端状态更清晰。
5. 让测试和 smoke 可重复执行。

## 当前不做

- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不做多页面。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。
- 不做登录注册 / 权限系统。
- 不做高保真截图还原。
- 不提交真实 API key。
- 不提交私人截图、账号信息、公司资料、密钥或敏感页面。

## 当前允许

- 允许继续使用真实 AI 链路。
- 允许稳定化 `promptVersion`、JSON 清洗、repair、fallbackReason。
- 允许保存本地 artifact。
- 允许复用同一 `jobId` 的已生成结果。
- 允许前端补状态展示和 iframe 安全验收。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- 当前任务卡：`docs/tasks/day-xx.md`（由项目经理按当天指定）
- Week 10 原始计划归档：`docs/archive/week/10-acceptance-plan.md`
- 历史归档：`docs/archive/`

## 当前状态说明

Week 09 已完成真实 AI 最小闭环，Week 10 正式进入“稳定化与可复现验收”阶段。

本周默认不扩大功能面，不引入 MySQL、Figma、Redis、RabbitMQ 或编辑器能力；后续开发线程应优先围绕稳定性、可解释性、可复验和安全边界推进。
