# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、当天对应的 `docs/tasks/day-xx.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 08：image-page mock 链路已完成收口，进入下一周规划准备。

## 阶段背景

Week 08 已完成 image-page mock API、API 测试、`/dev/image-to-layout` 页面增强、前端测试和联调 smoke。当前重点不再是继续补 Week 08 功能，而是保留收口事实、归档 smoke / summary / report material，并准备下一周计划。

Week 08 目标链路：

```text
本地选择图片
-> 选择 templateKey
-> POST /api/dev/image-page-jobs
-> 返回 layoutArtifact
-> 返回 generatedPageArtifact
-> 前端展示 Layout JSON
-> 前端展示 generated-page artifact
-> iframe sandbox="" 安全预览
```

## 当前完成内容

1. image-page mock API 已完成。
2. image-page API 测试已完成。
3. `/dev/image-to-layout` 页面已能展示 generatedPageArtifact。
4. 前端测试已完成。
5. 联调 smoke 已完成。
6. Week 08 summary、smoke 和 report material 已归档。

## 当前不做

- 不接真实 AI。
- 不接 OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器 / 在线编辑器。
- 不做真实截图解析。
- 不上传真实图片到后端。
- 不让后端调用 Python Worker。
- 不做 Playwright 视觉回归，除非用户明确批准。

## 当前允许

- 文档可以回看 Week 08 结果、总结和归档说明。
- Worker / 后端 / 前端的既有 mock 能力可以被总结、归档和回看。
- 当前仍保留 Week 07 的 mock 协议与安全预览边界，供回溯使用。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- context-scout 流程：`docs/playbooks/context-scout.md`
- Week 08 原始计划归档：`docs/archive/week/08-plan.md`
- Week 08 summary：`docs/archive/week/08-summary.md`
- Week 08 smoke：`docs/archive/week/08-dev-smoke.md`
- Week 08 report material：`docs/archive/week/08-report-material.md`
- Week 07 原始计划归档：`docs/archive/week/07-plan.md`
- 历史归档：`docs/archive/`

## 当前状态说明

Week 08 已完成收口，当前可以进入下一周计划准备，不再继续扩展 Week 08 功能。

`docs/tasks/day-*.md` 已在收口后清理，`docs/tasks/` 仅保留空目录，等待后续新周再生成新的日任务卡。

周计划和总结在完成拆分或收口后应归档到 `docs/archive/week/`，不要长期留在 `docs/` 根目录。
