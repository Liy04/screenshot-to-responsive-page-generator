# Week 14 Day 05

## 负责角色

frontend-agent -> tester-agent -> reviewer-agent -> Lead

## 任务目标

优化 REAL_AI / FALLBACK / FAILED 的用户可读状态和交付提示，让用户知道当前生成结果意味着什么、下一步可以做什么。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/day-05.md`
- `docs/agents/frontend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- 必要时 `docs/spec.md`
- 当前前端页面、状态展示和错误展示相关代码

说明：

- 不读取 `docs/archive/`。
- 不读取 backend / worker 全量代码。

## 允许修改

- `frontend/` 中与 `/dev/image-to-layout` 状态展示、提示文案、错误说明和测试相关的文件。

## 禁止修改

- `backend/`
- `worker/`
- `schema/`
- `docs/archive/`
- 后端响应字段
- Worker 状态枚举
- 模型 prompt

## 实施步骤

1. 梳理当前页面展示的 `status`、`sourceType`、`fallbackUsed`、`fallbackReason`、`errors`、`warnings`。
2. 将 REAL_AI、FALLBACK、FAILED、TIMEOUT 等状态转成用户可读说明。
3. 在成功状态下提示用户可复制或下载。
4. 在 fallback 状态下说明结果可用但来自保底规则。
5. 在 failed / timeout 状态下说明失败原因和建议重试动作。
6. 保留调试信息，但不要让它成为页面第一信息。
7. 补充前端测试或最低必要验证。
8. reviewer-agent 检查文案准确性、安全边界和接口契约是否被擅自改变。
9. Lead 二次验收。

## 验收标准

- [ ] REAL_AI 状态说明清楚。
- [ ] FALLBACK 状态说明清楚。
- [ ] FAILED / TIMEOUT 状态说明清楚。
- [ ] 用户能看到下一步动作：复制、下载、重新生成或检查输入。
- [ ] 调试字段仍可查看，但不压过主流程。
- [ ] 没有修改 backend / worker。
- [ ] 前端测试或 build 通过；无法运行时说明原因。

## Lead 二次验收

- 检查文案是否服务 MVP 演示。
- 检查是否没有修改接口和 Worker 行为。
- 检查 tester-agent 与 reviewer-agent 结论。
- 结论：通过 / 条件通过 / 不通过。

## 输出格式

```text
## 修改摘要
## 修改文件
## 页面影响
## 状态说明
## 测试结果
## Review 结果
## 风险提示
```
