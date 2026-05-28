# Week 14 Day 06

## Source Bet

- Current single bet from `docs/plan.md`: 执行 Week 14 MVP 产品化交付闭环 smoke，确认上传、生成、预览、复制、下载和安全检查可复现。
- 本 day 卡只执行 `docs/plan.md` 的当前 single bet，不重新定义产品方向、不扩展 roadmap、不把 Should / Could 自动升级为 Must。

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: 将“能生成”推进到“能交付”的 MVP 闭环证据。

## Task Goal

执行 Week 14 MVP smoke，确认上传、生成、预览、复制、下载和安全检查形成可复现闭环，并记录到 `docs/smoke/week14-mvp-smoke.md`。

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-06.md`
- `docs/agents/README.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/agents/docs-agent.md`
- `docs/smoke/week14-mvp-smoke.md`
- 必要时 `docs/spec.md`
- 当前任务相关前端页面和测试代码
- do not read `docs/archive/` by default

说明：

- 不读取 `docs/archive/`。
- 不读取无关模块全量代码。

## Write Scope

- `docs/smoke/week14-mvp-smoke.md`
- 必要时仅更新 `docs/tasks/day-06.md` 的测试结果部分

禁止修改：

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- `docs/archive/`
- `docs/current.md`
- `docs/plan.md`
- 业务代码
- 测试代码

## Spawn Decision

- Lead 判断本任务需要 spawn subagent。
- Lead 不直接执行测试、审查和记录，除非当前运行环境没有 subagent 工具且用户确认降级。
- 必须按顺序执行，不允许并行。
- 多个 agent 不允许同时修改同一目录。
- Day 卡只执行当前 plan，不重新定义产品方向。
- Day 卡不扩展 roadmap。
- Day 卡不把 Should / Could 自动升级为 Must。

## Required Agents

- Lead: 判断范围、分派、二次验收。
- Explorer: 默认不需要；仅在 smoke 范围不清或上下文不足时由 Lead 决定是否 spawn。
- Implementation: 不需要；本卡禁止修改业务代码和测试代码。
- Tester: `tester-agent` 执行 MVP smoke，只测试和记录，不修业务代码。
- Reviewer: `reviewer-agent` 审查 smoke 结果、安全风险和边界，只报告问题，不修业务代码。
- Docs: `docs-agent` 将结果记录到 `docs/smoke/week14-mvp-smoke.md`。

## Acceptance

- [ ] 上传成功。
- [ ] 生成成功或失败状态可解释。
- [ ] 原图展示正常。
- [ ] iframe 预览正常或失败时有清晰说明。
- [ ] HTML 复制可用。
- [ ] CSS 或完整 HTML 复制可用。
- [ ] 下载文件可用。
- [ ] iframe 为 `sandbox=""`。
- [ ] 无 `allow-scripts`。
- [ ] 未发现真实 API key 泄漏。
- [ ] 本轮服务已清理，无残留监听。
- [ ] smoke 结果已记录到 `docs/smoke/week14-mvp-smoke.md`。
- [ ] Lead 二次验收通过、条件通过或不通过结论明确。

## Test / Smoke

1. tester-agent 读取 smoke 模板和当前页面验收标准。
2. 启动后端和前端，使用真实或公开安全样例图执行 MVP smoke。
3. 验证上传和生成。
4. 验证原图 / iframe 对比。
5. 验证 HTML / CSS / 完整 HTML 复制。
6. 验证最小下载文件。
7. 验证 REAL_AI / FALLBACK / FAILED 状态展示。
8. 验证 iframe `sandbox=""` 且无 `allow-scripts`。
9. 验证不泄漏真实 API key。
10. reviewer-agent 审查 smoke 结果和安全风险。
11. docs-agent 将结果记录到 smoke 文档。
12. Lead 二次验收。

## Stop Conditions

- Requested work no longer maps to the Source Bet.
- Required read / write scope would touch unauthorized files.
- Multiple agents would modify the same directory at the same time.
- The task requires reading `docs/archive/` without explicit approval.
- The task requires secrets, real API keys, or sensitive materials.
- The task would add Claude Code config, `CLAUDE.md`, or `.claude/agents`.
- The task would redefine product direction or expand the roadmap.
- The task would auto-upgrade Should / Could items into Must work.
- tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- 测试范围
- 执行命令
- 测试结果
- Smoke 记录
- Review 结果
- Lead 二次验收：检查 smoke 是否覆盖 Week 14 MVP 交付闭环；检查 tester-agent 是否只测试和记录，没有直接修业务代码；检查 reviewer-agent 是否完成安全和边界审查；结论为通过 / 条件通过 / 不通过。
- 风险提示
- 是否通过验收

## 输出格式

```text
## 测试范围
## 执行命令
## 测试结果
## Smoke 记录
## Review 结果
## 风险提示
## 是否通过验收
```
