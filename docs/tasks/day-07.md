# Week 13 Day 07

## 负责角色

lead -> docs-agent -> reviewer-agent

## 任务目标

汇总 Week 13 的质量结果，判断下一步是继续质量增强，还是把关注点扩展到更广的样例覆盖或其他明确立项的方向。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-07.md`
- `docs/agents/lead.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/quality/week13-quality.md`
- `docs/smoke/week13-quality-smoke.md`
- 必要时 `docs/spec.md`

## 允许修改

- `docs/current.md`
- `docs/plan.md`
- `docs/INDEX.md`
- 必要时 `docs/tasks/day-07.md`

## 禁止修改

- 中大型业务代码。
- 真实 API key。
- `backend/storage/`
- `frontend/dist/`
- Week 13 禁止范围内的新功能。

## 实施步骤

1. docs-agent 汇总 Week 13 完成内容、测试结果和质量 smoke 评分。
2. reviewer-agent 检查安全、密钥、角色边界和未提交副产物。
3. Lead 按平均分和稳定性判断 Week 13 结论。
4. Lead 给出下一步建议，优先保持质量主线清晰。

## 验收标准

- [x] Week 13 smoke 已归档到当前文档层。
- [x] `docs/current.md` 更新到 Week 13 进行中或收口状态。
- [x] `docs/plan.md` 更新后续方向。
- [x] Week 13 判断基于平均分、最低分和顺序 smoke 稳定性。
- [x] 未提交真实 API key。
- [x] 未提交运行副产物。
- [x] 工作区可进入下一阶段文档收口。

## Lead 二次验收

- [x] 对照任务目标和验收标准检查。
- [x] 检查修改范围是否越界。
- [x] 检查测试 / smoke / review 是否完成或说明原因。
- [x] 检查安全边界和密钥风险。
- [x] 检查是否需要同步文档。
- [x] 结论：通过。

## 验收结果

Day 07 通过。

Week 13 收口结论：

- 三张 samples 顺序 smoke 全部通过。
- 平均分 27.0 / 35，最低分 26 / 35。
- 三张 samples 全部 `sourceType=REAL_AI`、`fallbackUsed=false`。
- 三张 samples 全部 `previewHtml` 非空，sandbox iframe 检查通过。
- 未发现真实 API key 泄漏。
- 未发现运行副产物进入可提交变更。
- 建议 Week 13 通过，下一步进入 Git diff 审查与合并收口。

## 输出格式

```text
任务结果：
- 任务目标：
- 改动文件：
- 主要改动：
- 验证步骤：
- 验证结果：
- 风险 / 待确认事项：
```
