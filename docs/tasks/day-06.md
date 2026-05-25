# Week 14 Day 06

## 负责角色

tester-agent -> reviewer-agent -> docs-agent -> Lead

## 任务目标

执行 Week 14 MVP smoke，确认上传、生成、预览、复制、下载和安全检查形成可复现闭环，并记录到 `docs/smoke/week14-mvp-smoke.md`。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/day-06.md`
- `docs/smoke/week14-mvp-smoke.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/agents/docs-agent.md`
- 必要时 `docs/spec.md`
- 当前任务相关前端页面和测试代码

说明：

- 不读取 `docs/archive/`。
- 不读取无关模块全量代码。

## 允许修改

- `docs/smoke/week14-mvp-smoke.md`
- 必要时仅更新 `docs/tasks/day-06.md` 的测试结果部分

## 禁止修改

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- `docs/archive/`
- `docs/current.md`
- `docs/plan.md`
- 业务代码
- 测试代码

## 实施步骤

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

## 验收标准

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

## Lead 二次验收

- 检查 smoke 是否覆盖 Week 14 MVP 交付闭环。
- 检查 tester-agent 是否只测试和记录，没有直接修业务代码。
- 检查 reviewer-agent 是否完成安全和边界审查。
- 结论：通过 / 条件通过 / 不通过。

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
