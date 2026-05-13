# Plan

## Week 09 名称

真实 AI 最小接入，打通单张真实图片到 Layout JSON / generated-page 预览。

## 本周核心目标

Week 09 的目标是打通单张真实图片的最小闭环：

```text
真实图片上传 -> 后端保存临时文件 -> 后端调用 Python Worker -> Worker 调真实 AI
-> Layout JSON v0.1 校验 -> fallback rule resolver 保底 -> generated.html 编译
-> 后端返回 layoutJson + previewHtml -> 前端展示原图、Layout JSON 和 iframe 预览
```

本周只追求最小闭环，不追求高保真还原。

## 本周禁止事项

- 不接 Figma API / MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做 Playwright 视觉回归。
- 不做多页面。
- 不做批量任务。
- 不做登录注册。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。

## 每日计划

| Day | 线程 | 完成情况 |
|---|---|---|
| Day 1 | 文档线程 | 已完成 Week 09 范围、协议和入口切换 |
| Day 2 | 后端开发线程 | 已完成单张图片上传与 source 接口 |
| Day 3 | 后端开发线程（Worker 调用链路） | 已完成后端调用 Python Worker |
| Day 4 | Worker 开发线程 | 已完成真实图片读取、AI、fallback、validator |
| Day 5 | Worker 开发线程（HTML compiler 子任务） | 已完成 Layout JSON 到 previewHtml 编译 |
| Day 6 | 前端开发线程 | 已完成真实主链路接入和 iframe 预览 |
| Day 7 | 测试线程 | 已完成全链路 smoke 验收与问题收敛 |

## Day 边界

- Day 2 保持在上传与原图访问边界内完成。
- Day 3 只承担后端调用 Python Worker 的调用链路。
- Day 4 以 Worker 真实 AI、fallback 和 validator 为主。
- Day 5 只完成 HTML compiler 子任务，不新增 Vue、ZIP 或编辑器。
- Day 6 只接前端真实链路和 iframe 预览。
- Day 7 只负责 smoke、记录问题和给出通过 / 不通过结论，不混入修复线程职责。

## 完成摘要

Week 09 已完成真实 AI 最小闭环，项目当前已经具备：

- 单张真实图片上传。
- 后端保存临时文件并生成 jobId。
- 后端真实调用 Python Worker。
- Worker 读取真实图片并调用 SiliconFlow OpenAI-compatible 模型。
- AI 输出映射到 Layout JSON v0.1。
- validator、fallback 和 previewHtml 编译链路。
- 前端展示原图、Layout JSON、previewHtml 和 iframe 预览。

## 当前状态

- Week 09 已完成收口。
- Day 7 阻断最终收敛为运行配置问题，而不是协议设计问题。
- backend generate 已在 `--imagepage.worker.timeout-seconds=120` 条件下命中 `REAL_AI`。
- 最终成功链路已确认：`HTTP 200`、`status=SUCCESS`、`mode=real-ai`、`fallbackUsed=false`、`sourceType=REAL_AI`、`layoutJson.version=0.1`、`validation.ok=true`、`previewHtml` 非空、前端 iframe 渲染成功、`sandbox=""`、无 `allow-scripts`。
- `docs/tasks/day-01.md` 到 `docs/tasks/day-07.md` 已按收口规则清理，`docs/tasks/` 保留为空目录。

## 后续建议

- Week 10 可优先考虑提升真实 AI 输出质量和稳定性。
- 可以考虑固定生成参数或缓存结果，降低同图重复生成的轻微差异。
- 可以继续增强 Layout JSON 映射质量、测试覆盖和报告材料。
- 暂不急于接 MySQL、Figma 或编辑器类能力。
