# Week 14 Day 01

## 负责角色

docs-agent -> reviewer-agent -> Lead

## 执行方式

- 是否需要 spawn subagent：是
- Lead 是否可直接执行：否，除非当前运行环境没有 subagent 工具且用户确认降级
- 必须 spawn 的 agent：docs-agent、reviewer-agent
- 是否允许并行：否，默认顺序执行

## 任务目标

把 Week 14 MVP 产品化交付计划拆成可执行 day 卡，并建立 Week 14 MVP smoke 记录模板。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/_template.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`

说明：

- 不读取 `docs/archive/`。
- 不读取 backend / frontend / worker 业务代码。

## 允许修改

- `docs/tasks/day-01.md`
- `docs/tasks/day-02.md`
- `docs/tasks/day-03.md`
- `docs/tasks/day-04.md`
- `docs/tasks/day-05.md`
- `docs/tasks/day-06.md`
- `docs/tasks/day-07.md`
- `docs/smoke/week14-mvp-smoke.md`

## 禁止修改

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- `docs/archive/`
- `docs/spec.md`
- `docs/current.md`
- `docs/plan.md`
- `README.md`
- `AGENTS.md`

## 实施步骤

1. 根据 `docs/plan.md` 生成 Week 14 Day 1 到 Day 7 任务卡。
2. 每张任务卡明确负责角色、允许修改范围、禁止修改范围和验收标准。
3. 新增 `docs/smoke/week14-mvp-smoke.md`，用于 Day 6 记录 MVP smoke。
4. reviewer-agent 检查任务是否推动 MVP 主线，是否违反 Docs Lite 和 Agent 边界。
5. Lead 做二次验收，确认 Week 14 可以逐日执行。

## 验收标准

- [ ] 7 张 day 卡全部存在。
- [ ] `docs/smoke/week14-mvp-smoke.md` 已新增。
- [ ] Day 2 到 Day 5 明确由 frontend-agent 执行。
- [ ] Day 6 明确由 tester-agent 执行。
- [ ] Day 7 明确由 docs-agent / reviewer-agent / Lead 收口。
- [ ] 每张 day 卡都写明不读取或修改 `docs/archive/`。
- [ ] 未修改业务代码。
- [ ] 未新增 MySQL / Figma / 编辑器 / ZIP 复杂实现。

## Lead 二次验收

- 对照 Week 14 MVP 目标检查 day 卡是否可执行。
- 检查修改范围是否只限任务授权文档。
- 检查是否把 Week 14 推向产品化交付，而不是继续质量优化。
- 检查 smoke 模板是否覆盖上传、生成、预览、复制、下载和安全检查。
- 结论：通过 / 条件通过 / 不通过。

## 输出格式

```text
## 修改摘要
## 新增文件
## 修改文件
## Review 结果
## Lead 验收结论
## 风险提示
```
