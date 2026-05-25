# Week 11 Day 05

## 负责角色

lead + tester-agent + reviewer-agent + docs-agent

## 任务目标

完成 Week 11 验收、总结归档与 Git 收口准备。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-05.md`
- `docs/agents/lead.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/agents/docs-agent.md`
- 本周变更文件

需要核对 Week 11 原始计划时，可以读取 `docs/archive/week/11-plan.md`。

## 允许修改

- `docs/current.md`
- `docs/plan.md`
- `docs/archive/week/11-summary.md`
- `docs/archive/week/11-dev-smoke.md`
- `docs/archive/week/11-acceptance-report.md`
- 必要时 `docs/tasks/day-05.md`

## 禁止修改

- 中大型业务代码。
- 真实 API key。
- `backend/storage/`
- `frontend/dist/`
- 真实隐私截图。
- Week 11 禁止范围内的新功能。

## 实施步骤

1. tester-agent 汇总本周测试和 smoke 结果。
2. reviewer-agent 检查密钥、运行副产物、边界和安全风险。
3. docs-agent 归档 Week 11 summary / dev smoke / acceptance report。
4. Lead 验收是否可收口。
5. Lead 给出 Git commit 建议。

## 验收标准

- [x] `samples/` 已建立且安全可提交。
- [x] 真实 AI smoke 文档可复现。
- [x] `OPENAI_API_KEY` 只通过环境变量配置。
- [x] `REAL_AI` / `FALLBACK` / `FAILED` 判断标准清楚。
- [x] artifact 文件检查清楚。
- [x] `jobId` 复用检查清楚。
- [x] 如执行 Day 4，metadata 展示清楚且测试通过。
- [x] Worker / Backend / Frontend 测试结果已记录。
- [x] `backend/storage/` 未提交。
- [x] `frontend/dist/` 未提交。
- [x] Week 11 summary 和 acceptance report 已归档。

## 输出格式

```text
任务结果：
- 任务目标：
- 修改文件：
- 主要改动：
- 验证步骤：
- 验证结果：
- 风险 / 待确认事项：
```
