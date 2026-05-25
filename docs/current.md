# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、`docs/mvp-roadmap.md`、当前活跃任务卡和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 13 已完成并推送。

当前进入：

```text
Week 14：MVP 产品化交付闭环
```

Week 14 不再继续惯性做输出质量周，而是把 Week 09~13 已打通的真实 AI 能力包装成用户可理解、可操作、可演示的 MVP 闭环。

## 已完成主线

项目当前已经完成：

- Week 09：真实 AI 最小闭环。
- Week 10：真实 AI 链路稳定化、artifact 复用和可复现验收。
- Week 11：samples 建设、真实 AI smoke 文档化、metadata 增强和验收归档。
- Week 12：围绕三张简单 samples 提升真实 AI 输出质量和静态预览还原度。
- Week 13：继续提升三张 samples 的输出质量，完成顺序 smoke 和人工评分记录。

Week 13 结果：

- 三张 samples 顺序 smoke 全部通过。
- 三张 samples 均 `sourceType=REAL_AI`。
- 三张 samples 均 `fallbackUsed=false`。
- 三张 samples 均输出非空 `previewHtml`。
- 三张 samples 二次 generate 均 `artifact.reused=true`。
- 三张 samples 均通过 sandbox iframe 渲染检查。
- 平均分 27.0 / 35，最低分 26 / 35。
- 最新提交：`2cc56af Complete Week 13 output quality stabilization`。

## Week 14 目标

Week 14 的目标是 MVP 产品化交付：

```text
真实图片上传
-> 真实 AI 生成 Layout JSON
-> Worker 编译 previewHtml
-> 前端展示原图 / 生成结果
-> 用户复制或下载 HTML / CSS
-> 形成可演示 MVP 闭环
```

重点是让用户能拿到生成结果，而不是继续无限优化模型质量。

## Week 14 优先事项

1. 优化 `/dev/image-to-layout` 的结果展示，使其更像 MVP 演示页。
2. 增加 HTML / CSS 复制入口。
3. 增加最小文件下载能力。
4. 明确 REAL_AI / FALLBACK / FAILED 的用户可读状态。
5. 增加生成结果交付区，告诉用户下一步可以复制、下载或重新生成。
6. 补 Week 14 MVP smoke，确认上传、生成、预览、复制 / 下载链路可复现。

## 当前不做

- 不接 MySQL。
- 不设计数据库表。
- 不创建 Entity / Mapper。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不做多页面生成。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做复杂 ZIP 导出。
- 不做登录注册 / 权限系统。
- 不做复杂真实整站截图。
- 不追求 1:1 高保真。
- 不升级 Layout JSON schema v0.2，除非单独立项。
- 不把模型原始 HTML 直接作为最终页面代码。
- 不提交真实 API key、私人截图、账号信息、公司资料、密钥或敏感页面。

## 当前风险 / 遗留项

- 真实 AI smoke 依赖外部模型服务、网络、环境变量和较长 timeout。
- 真实模型并发请求不稳定，smoke 继续建议顺序执行。
- 复杂整页截图可能超时或质量较低，当前主要验证简单样例。
- 同图多次生成仍可能有轻微差异；`jobId` artifact 复用已缓解重复生成漂移。
- `IMAGEPAGE_WORKER_PYTHON_COMMAND` 建议显式设置为 `D:\environment\python11\python.exe`。
- 后端真实 AI smoke 推荐至少使用 `--imagepage.worker.timeout-seconds=180`。
- `backend/storage/`、`frontend/dist/` 及其他运行副产物不能提交。
- Week 14 需要避免继续变成质量优化周。

## 当前文档入口

- MVP 路线锚点：`docs/mvp-roadmap.md`
- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 输出质量标准：`docs/quality/week13-quality.md`
- Week 13 smoke 记录：`docs/smoke/week13-quality-smoke.md`
- Week 14 MVP smoke：`docs/smoke/week14-mvp-smoke.md`
- 文档索引：`docs/INDEX.md`
- Codex 角色边界：`docs/agents/README.md`
- 历史归档：`docs/archive/`

## 下一步状态

Week 14 day 卡已生成，当前按 `docs/tasks/day-xx.md` 执行 MVP 产品化交付任务。

执行时以当前 day 卡为准，并继续遵守 Codex Lead + Short-lived Subagents Workflow：中大型任务按需 spawn，代码实现后进行 tester / reviewer 验证与审查。
