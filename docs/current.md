# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、`docs/task.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 06：Generated Page 回归稳定性与演示验收增强（已收口）。

## 阶段结论

Week 06 已完成 generated-page MVP 闭环的回归稳定性、测试覆盖、smoke 文档和实践报告素材整理，下一步准备进入 Week 07 规划。

## 本阶段已完成

1. Day 1：文档计划与任务边界完成。
2. Day 2：前端 preview 基础测试完成。
3. Day 3：Worker 小范围增强完成。
4. Day 4：Worker 回归测试完成。
5. Day 5：后端 artifact 边界测试完成。
6. Day 6：smoke 文档与实践报告素材完成。
7. Day 7：总体验收、归档完成。

## 当前禁止

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
- 不做登录注册 / 复杂权限。
- 不做 Playwright 视觉回归，除非用户明确批准。
- 不做复杂响应式布局算法。
- 不做 Tailwind 代码生成。
- 不做 Vue SFC 可运行化。

## 当前允许

- 文档可以更新 Week 06 收口总结、Week 07 规划入口和归档索引。
- 如后续进入 Week 07，先以当前 Lite 文档为准，再按任务卡逐步展开。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前任务：`docs/task.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- context-scout 流程：`docs/playbooks/context-scout.md`
- Week 06 原始计划归档：`docs/archive/week/06-plan.md`
- Week 06 smoke 归档：`docs/archive/week/06-dev-smoke.md`
- Week 06 实践报告素材归档：`docs/archive/week/06-report-material.md`
- Week 06 总结归档：`docs/archive/week/06-summary.md`
- 历史归档：`docs/archive/`

## 当前状态说明

Week 06 已完成收口并归档，后续进入 Week 07 前应先确认方向，再更新 `docs/current.md`、`docs/plan.md` 和 `docs/task.md`。

周计划、smoke 文档和总结在完成拆分或收口后应移动到 `docs/archive/week/`，不要长期留在 `docs/` 根目录。
