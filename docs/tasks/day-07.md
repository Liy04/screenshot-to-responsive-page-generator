# Week 14 Day 07

## 负责角色

Lead -> docs-agent -> reviewer-agent -> Lead

## 任务目标

完成 Week 14 收口，判断 MVP 产品化交付闭环是否通过，并给出下一周建议。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/day-07.md`
- `docs/smoke/week14-mvp-smoke.md`
- `docs/agents/lead.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`
- 必要时 `docs/spec.md`

说明：

- 默认不读取 `docs/archive/`。
- 如确实需要归档 Week 14 总结，必须由 Lead 明确授权后再写入归档。

## 允许修改

- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/`
- `docs/smoke/week14-mvp-smoke.md`
- 必要时 Week 14 总结文档

## 禁止修改

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- 未授权修改 `docs/archive/`
- API key 或敏感信息

## 实施步骤

1. Lead 汇总 Day 2 到 Day 6 的实现、测试和 review 结果。
2. docs-agent 更新当前状态和必要收口文档。
3. reviewer-agent 审查 Week 14 是否满足 MVP 产品化目标。
4. Lead 判断 Week 14 是否通过：通过 / 条件通过 / 不通过。
5. 如果通过，给出 Git 收口建议。
6. 如果不通过，列出必须修复项并指派对应 Agent。
7. 给出 Week 15 建议方向，但不直接展开长计划。

## 验收标准

- [ ] Week 14 每天结果已汇总。
- [ ] MVP smoke 结论明确。
- [ ] 复制 / 下载 / 预览 / 状态说明是否通过有明确判断。
- [ ] 安全边界检查完成。
- [ ] 未提交真实 API key。
- [ ] 未提交运行副产物。
- [ ] 未新增 MySQL / Figma / 编辑器 / ZIP 复杂实现。
- [ ] Lead 给出是否可以进入 Week 15 的结论。

## Lead 二次验收

- 对照 `docs/mvp-roadmap.md` 检查 Week 14 是否推动 MVP 主线。
- 检查 Week 14 是否把“能生成”推进到“能交付”。
- 检查是否还存在阻塞用户演示的问题。
- 结论：通过 / 条件通过 / 不通过。

## 输出格式

```text
## Week 14 汇总
## 完成内容
## Smoke 结果
## Review 结果
## MVP 通过结论
## 风险
## Git 建议
## Week 15 建议
```
