# Week 13 Day 01

## 负责角色

docs-agent -> reviewer-agent -> lead

## 任务目标

建立 Week 13 输出质量标准、评分表和顺序 smoke 模板，明确本周继续做输出质量增强，但不进入 MySQL、Figma、复杂编辑器或持久化主线。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-01.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/quality/week13-quality.md`
- `docs/smoke/week13-quality-smoke.md`
- 必要时 `docs/spec.md`

## 允许修改

- `docs/quality/week13-quality.md`
- `docs/smoke/week13-quality-smoke.md`
- 必要时 `docs/current.md`
- 必要时 `docs/plan.md`
- 必要时 `docs/INDEX.md`

## 禁止修改

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- 真实 API key
- `docs/archive/` 历史内容，除非只做路径核对

## 实施步骤

1. docs-agent 核对 Week 13 质量目标、评分表和顺序 smoke 口径是否完整。
2. reviewer-agent 检查质量标准是否过宽，是否遗漏安全边界和顺序 smoke 要求。
3. Lead 验收 Day 1 是否可以作为后续 Day 2 到 Day 6 的统一验收依据。

## 验收标准

- [ ] `docs/quality/week13-quality.md` 包含 35 分评分表。
- [ ] 包含视觉清单稳定性、Layout JSON 映射质量、preview 样式表达、顺序 smoke 可复现性和安全边界。
- [ ] 包含三张 samples 的适用范围。
- [ ] 包含顺序 smoke 记录模板。
- [ ] 包含通过线和 Week 13 判断标准。
- [ ] 明确不进入 MySQL、Figma、复杂编辑器和持久化主线。
- [ ] 没有修改业务代码。

## Lead 二次验收

- [ ] 对照任务目标和验收标准检查。
- [ ] 检查修改范围是否越界。
- [ ] 检查测试 / smoke / review 是否完成或说明原因。
- [ ] 检查安全边界和密钥风险。
- [ ] 检查是否需要同步文档。
- [ ] 结论：通过 / 条件通过 / 不通过。
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
