# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、`docs/task.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 05：Generated Page 独立预览与质量稳定化（已收口）。

## 阶段结论

Week 05 主链路已完成，Day 6 smoke 已通过，当前进入收口与归档状态，下一步准备进入 Week 06 规划。

## 本阶段已完成

1. Day 1：Docs Lite 文档定范围完成。
2. Day 2：前端任务详情页 generated-page UX 解耦完成。
3. Day 3：generated-page 独立 dev preview 页面完成。
4. Day 4：后端 generated-page artifact mock 接口测试完成，`mvn test` 通过。
5. Day 5：Worker 静态编译器 style subset 小幅增强完成，`python -m unittest worker.test_layout_static_generator` 通过。
6. Day 6：Week 05 dev smoke 文档完成，并补充 8080 占用时的备用端口流程、Vite proxy 口径和端到端 smoke 说明；端到端 smoke 已通过。
7. Day 7：总结归档完成，Week 05 总结文档已归档到 `docs/archive/week/05-summary.md`。

## 当前禁止

- 不接真实 AI。
- 不接 OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL 实际落库。
- 不创建数据库表。
- 不新增 Entity / Mapper。
- 不新增数据库配置。
- 不接 Redis / RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器或在线编辑器。
- 不做真实截图解析。
- 不做登录注册、历史记录持久化或复杂权限。
- 不要求 `vueCode` 真正可运行。
- 不做复杂响应式布局算法。
- 不做 Tailwind 代码生成。
- 不做 Vue SFC 可运行化。
- 不做 Playwright 视觉回归，除非用户明确批准。

## 当前允许

- 文档可以更新 Week 05 收口总结、Week 06 规划入口和归档索引。
- 如后续进入 Week 06，先以当前 Lite 文档为准，再按任务卡逐步展开。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前任务：`docs/task.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- context-scout 流程：`docs/playbooks/context-scout.md`
- Week 05 原始计划归档：`docs/archive/week/05-plan.md`
- Week 05 总结归档：`docs/archive/week/05-summary.md`
- 历史归档：`docs/archive/`
