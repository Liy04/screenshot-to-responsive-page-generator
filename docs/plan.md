# Plan

## Week 10 名称

真实 AI 链路稳定化与可复现验收。

## 本周总目标

Week 10 的目标是在 Week 09 已跑通真实 AI 最小闭环的基础上，把链路做得更稳定、更可解释、更可复验：

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

## P0 完成情况

- `promptVersion` 已固定并返回，当前值 `week10-v1`。
- JSON 清洗已支持纯 JSON、markdown code fence 和前后说明文字。
- `fallbackReason`、`warnings`、`errors` 已可返回。
- `layout.json`、`preview.html`、`metadata.json` artifact 约定已落实。
- 同一 `jobId` 可复用，不重复调用 AI。
- 前端已可区分 `REAL_AI` / `FALLBACK` / `FAILED` / `TIMEOUT`。
- smoke 文档和临时公开安全样例图口径已明确。

## P1 / P2 收口情况

- P1：repair、Worker / 后端 / 前端测试、结果说明与错误提示已进入收口通过状态。
- P2：`durationMs`、debug metadata 和进一步一致性增强仍可继续优化，但不构成 Week 10 收口阻塞。

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

## Day 02 到 Day 07 完成情况

| Day | 线程 | 完成情况 |
|---|---|---|
| Day 02 | Worker 线程 | 已完成 `promptVersion` 与 JSON 清洗 |
| Day 03 | Worker 线程 | 已完成 repair、`fallbackReason` 与相关输出口径 |
| Day 04 | 后端线程 | 已完成 artifact 保存、`jobId` 复用与返回结构补强 |
| Day 05 | 前端线程 | 已完成状态展示与 iframe 安全展示 |
| Day 06 | 测试线程 | 已完成 Worker / 后端 / 前端测试与真实链路 smoke |
| Day 07 | 文档线程 | 收口 summary / dev smoke / acceptance report，并清理 day 卡 |

## 最终 smoke 结论

- Worker：`67 / 67` 通过。
- Backend：`45 / 45` 通过。
- Frontend：`9 / 9` 通过。
- 真实链路 smoke 通过。
- `REAL_AI` / `FALLBACK` / `FAILED` 三种口径已验证。
- artifact 文件检查通过。
- `jobId` 复用检查通过。
- API key 未泄漏。
- iframe 使用 `sandbox=""`，且无 `allow-scripts`。

## 后续建议

- Week 11 可以优先考虑继续提升真实 AI 输出质量和稳定性。
- 可以继续完善结果一致性策略、缓存策略和测试 / 报告材料。
- 暂不急于进入 MySQL、Figma、编辑器或多页面方向。
