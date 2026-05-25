# Week 13 Day 06

## 负责角色

tester-agent -> reviewer-agent -> docs-agent -> lead

## 任务目标

按顺序执行三张 samples 的质量 smoke 和人工评分记录，确认 Week 13 的清单稳定性、映射质量和 preview 表达是否真的提升。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-06.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/agents/docs-agent.md`
- `docs/quality/week13-quality.md`
- `docs/smoke/week13-quality-smoke.md`
- 必要时 `docs/spec.md`
- 当前任务相关代码

## 允许修改

- `docs/smoke/week13-quality-smoke.md`
- 必要时补充测试记录文档

## 禁止修改

- 业务代码，除非 Lead 明确授权修复极小测试脚本问题。
- 真实 API key。
- `backend/storage/`
- `frontend/dist/`
- 私人截图或敏感图片。

## 实施步骤

1. tester-agent 按固定顺序执行三张 samples 的顺序 smoke。
2. 记录 status、运行顺序、sourceType、fallbackUsed、promptVersion、artifact.reused、previewHtml、iframe。
3. 按 `docs/quality/week13-quality.md` 人工评分。
4. reviewer-agent 审查安全、密钥、iframe、运行副产物。
5. docs-agent 将结果写入 `docs/smoke/week13-quality-smoke.md`。
6. Lead 判断 Week 13 是否达到轻量验收口径。

## 验收标准

- [x] 三张 samples 都有记录。
- [x] 每张 sample 记录评分人。
- [x] 每张 sample 记录评分日期。
- [x] 每张 sample 记录运行顺序。
- [x] 每张 sample 记录模型。
- [x] 每张 sample 记录 promptVersion。
- [x] 每张 sample 记录 artifact.reused。
- [x] 每张 sample 记录 fallbackUsed。
- [x] 每张 sample 记录总分和主要缺陷。
- [x] 记录平均分和最低分。
- [x] 无真实 key 泄漏。
- [x] `backend/storage/`、`frontend/dist/` 未进入可提交变更。

## Lead 二次验收

- [x] 对照任务目标和验收标准检查。
- [x] 检查修改范围是否越界。
- [x] 检查测试 / smoke / review 是否完成或说明原因。
- [x] 检查安全边界和密钥风险。
- [x] 检查是否需要同步文档。
- [x] 结论：通过。

## 验收结果

Day 06 通过。

验证摘要：

- 三张 samples 均按固定顺序完成真实 AI generate。
- 三张 samples 均 `status=SUCCESS`、`sourceType=REAL_AI`、`fallbackUsed=false`。
- 三张 samples 首次 generate 后二次 generate 均命中 `artifact.reused=true`。
- 三张 samples 的 `previewHtml` 均非空。
- iframe 安全检查通过：`sandbox=""`，无 `allow-scripts`。
- 未发现真实 API key 泄漏。
- 平均分 27.0 / 35，最低分 26 / 35，达到 Week 13 稳定通过线。

详细记录见：

```text
docs/smoke/week13-quality-smoke.md
```

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
