# Plan

## Week 10 名称

真实 AI 链路稳定化与可复现验收。

## 本周总目标

Week 10 的目标不是扩功能，而是让 Week 09 已跑通的真实 AI 主链路更稳定、更可解释、更可复验：

```text
真实图片
-> 后端上传
-> Python Worker
-> 真实 AI / fallback
-> Layout JSON v0.1
-> previewHtml
-> 前端状态展示与 iframe 预览
-> artifact 保存与复用
```

## P0 / P1 / P2

### P0

- `promptVersion` 口径固定。
- JSON 清洗可处理 markdown code fence 和前后废话。
- `fallbackReason`、`warnings`、`errors` 可返回。
- `layout.json`、`preview.html`、`metadata.json` artifact 约定清楚。
- 同一 `jobId` 可复用，不重复调用 AI。
- 前端可区分 `REAL_AI` / `FALLBACK` / `FAILED` / `TIMEOUT`。
- smoke 文档与可公开样例图口径清楚。

### P1

- repair 轻修复规则更稳。
- Worker / 后端 / 前端测试覆盖更完整。
- 结果说明、错误提示、调试字段更清楚。

### P2

- `durationMs`、`repairUsed`、debug metadata 展示增强。
- 结果缓存和一致性策略进一步细化。

## 本周禁止事项

- 不接 MySQL。
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
- 不提交私人截图或敏感图片。

## 7 天计划

| Day | 线程 | 目标 |
|---|---|---|
| Day 01 | 文档线程 | 切换 Week 10 Lite 文档、补契约、生成 day 卡、归档原始长计划 |
| Day 02 | Worker 线程 | 增加 `promptVersion` 与 JSON 清洗 |
| Day 03 | Worker 线程 | 增加 repair、`fallbackReason` 与相关测试口径 |
| Day 04 | 后端线程 | 保存 artifact、支持 `jobId` 复用、补返回字段 |
| Day 05 | 前端线程 | 清晰展示 REAL_AI / FALLBACK / FAILED / TIMEOUT 与 iframe 安全 |
| Day 06 | 测试线程 | 固化 Worker / 后端 / 前端测试与真实链路 smoke |
| Day 07 | 文档线程 | 收口 summary / dev smoke / 验收结果，并清理 day 卡 |

## Day 2 到 Day 6 边界摘要

- Day 02 只动 Worker 的 `promptVersion` 和 JSON 清洗，不改前后端。
- Day 03 只动 Worker 的 repair、fallbackReason 和相关测试口径，不扩大成复杂修复系统。
- Day 04 只动后端 artifact 保存、读取和 `jobId` 复用，不接数据库。
- Day 05 只动前端状态展示和 iframe 安全，不做编辑器或大 UI 迁移。
- Day 06 只做测试和 smoke，不修改业务代码。

## 最终交付物

- Week 10 活跃文档与 day 卡。
- 可公开样例图约定。
- Worker / 后端 / 前端测试与 smoke 文档口径。
- Week 10 summary、dev smoke、验收报告归档。

## 原始计划来源

`docs/archive/week/10-acceptance-plan.md` 是 Week 10 原始验收计划来源，不作为日常默认上下文。
