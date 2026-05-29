# Week 14 Day 07

## Source Bet

- Current single bet from `docs/plan.md`: 完成 Week 14 收口，判断 MVP 产品化交付闭环是否通过，并形成当前 handoff。
- 本 day 卡只执行 `docs/plan.md` 的当前 single bet，不重新定义产品方向、不扩展 roadmap、不生成 Week 15 / Cycle 15 计划、不把 Should / Could 自动升级为 Must。

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: 将 Week 14 的交付闭环结果沉淀为是否可演示、可进入下一 handoff 的明确判断。

## Task Goal

完成 Week 14 收口，判断 MVP 产品化交付闭环是否通过，并给出下一周建议。

说明：下一周建议只允许作为下一 handoff 风险和方向提示，不展开 Week 15 / Cycle 15 计划。

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-07.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/smoke/week14-mvp-smoke.md`
- 必要时 `docs/spec.md`
- do not read `docs/archive/` by default

说明：

- 默认不读取 `docs/archive/`。
- 如确实需要归档 Week 14 总结，必须由 Lead 明确授权后再写入归档。

## Write Scope

- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/`
- `docs/smoke/week14-mvp-smoke.md`
- 必要时 Week 14 总结文档

禁止修改：

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- 未授权修改 `docs/archive/`
- API key 或敏感信息

## Spawn Decision

- Lead 判断本任务需要 spawn subagent。
- Lead 仅可做范围判断和最终验收，docs / review 工作需 spawn。
- 必须按顺序执行，不允许并行。
- 多个 agent 不允许同时修改同一目录。
- Day 卡只执行当前 plan，不重新定义产品方向。
- Day 卡不扩展 roadmap。
- Day 卡不生成 Week 15 / Cycle 15 计划。
- Day 卡不把 Should / Could 自动升级为 Must。

## Required Agents

- Lead: 汇总范围、分派、判断 Week 14 是否通过、最终验收。
- Explorer: 默认不需要；仅在 Week 14 状态缺口不清时由 Lead 决定是否 spawn。
- Implementation: 不需要；本卡是 docs-only 收口和 review。
- Tester: 默认不需要；如发现 smoke 证据缺口，只报告缺口，不修业务代码。
- Reviewer: `reviewer-agent` 审查 Week 14 是否满足 MVP 产品化目标，只报告问题，不修业务代码。
- Docs: `docs-agent` 更新当前状态和必要收口文档。

## Acceptance

- [x] Week 14 每天结果已汇总。
- [x] MVP smoke 结论明确。
- [x] 复制 / 下载 / 预览 / 状态说明是否通过有明确判断。
- [x] 安全边界检查完成。
- [x] 未提交真实 API key。
- [x] 未提交运行副产物。
- [x] 未新增 MySQL / Figma / 编辑器 / ZIP 复杂实现。
- [x] Lead 给出是否可以进入 Week 15 的结论，但不生成 Week 15 / Cycle 15 计划。
- [x] reviewer-agent 只审查和报告，不修业务代码。
- [x] docs-agent 修改保持在 Write Scope 内。

## Day 07 Closeout Result

- Week 14 MVP 产品化交付闭环结论：通过。
- 依据：`docs/smoke/week14-mvp-smoke.md` 已记录 Day 06 smoke 通过，覆盖上传、REAL_AI 生成、预览、复制、下载、安全检查和服务清理。
- 当前交付状态：`docs/plan.md` 的 Must、Acceptance Criteria、Smoke Plan 和 Exit Criteria 已标记为满足 / 通过。
- 下一 handoff：进入 Lead / Git 收口，先确认当前 docs diff，再按仓库流程 stage / commit；不在本卡生成 Week 15 / Cycle 15 计划。
- 范围确认：未读取或修改 `docs/archive/`，未修改 backend / frontend / worker / schema，未新增 Claude Code 配置。

## Test / Smoke

1. Lead 汇总 Day 2 到 Day 6 的实现、测试和 review 结果。
2. docs-agent 更新当前状态和必要收口文档。
3. reviewer-agent 审查 Week 14 是否满足 MVP 产品化目标。
4. Lead 判断 Week 14 是否通过：通过 / 条件通过 / 不通过。
5. 如果通过，给出 Git 收口建议。
6. 如果不通过，列出必须修复项并指派对应 Agent。
7. 给出下一 handoff 建议方向，但不直接展开 Week 15 / Cycle 15 计划。

## Stop Conditions

- Requested work no longer maps to the Source Bet.
- Required read / write scope would touch unauthorized files.
- Multiple agents would modify the same directory at the same time.
- The task requires reading `docs/archive/` without explicit approval.
- The task requires secrets, real API keys, or sensitive materials.
- The task would add Claude Code config, `CLAUDE.md`, or `.claude/agents`.
- The task would redefine product direction or expand the roadmap.
- The task would generate Week 15 / Cycle 15 plans.
- The task would auto-upgrade Should / Could items into Must work.
- tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Week 14 汇总
- 完成内容
- Smoke 结果
- Review 结果
- MVP 通过结论
- Lead 二次验收：对照 `docs/mvp-roadmap.md` 检查 Week 14 是否推动 MVP 主线；检查 Week 14 是否把“能生成”推进到“能交付”；检查是否还存在阻塞用户演示的问题；结论为通过 / 条件通过 / 不通过。
- 风险
- Git 建议
- 下一 handoff 建议，不展开 Week 15 / Cycle 15 计划

## 输出格式

```text
## Week 14 汇总
## 完成内容
## Smoke 结果
## Review 结果
## MVP 通过结论
## 风险
## Git 建议
## 下一 handoff 建议
```
