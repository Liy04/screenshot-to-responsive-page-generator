# Week 13 Day 02

## 负责角色

worker-agent -> tester-agent -> reviewer-agent -> lead

## 任务目标

让视觉清单提取更稳定，减少同图多次生成的结构漂移，并保持 `promptVersion` 和中间结构输出清晰可追踪。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-02.md`
- `docs/agents/worker-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/quality/week13-quality.md`
- 必要时 `docs/spec.md`
- `worker/` 当前相关代码

## 允许修改

- `worker/`
- worker 相关测试

## 禁止修改

- `backend/`
- `frontend/`
- `schema/`，除非 Lead 明确批准最小兼容变更
- 真实 API key
- 模型原始 HTML 直出路径

## 实施步骤

1. worker-agent 找到视觉清单输出和 prompt 构造位置。
2. 稳定 `texts / regions / components` 的输出结构，减少同图漂移和无关噪声。
3. 保持 JSON 清洗 / repair / fallback 机制，不因稳定性优化降低可控性。
4. tester-agent 运行 worker 相关测试。
5. reviewer-agent 审查是否泄漏 key、是否接受模型 HTML、是否破坏安全边界。

## 验收标准

- [ ] 视觉清单输出结构更稳定。
- [ ] `texts / regions / components` 仍是主要中间表达。
- [ ] prompt 输出仍可追踪、可复现。
- [ ] 模型输出 HTML / Markdown / 解释文字时，仍走 JSON 清洗 / repair / fallback。
- [ ] Worker 测试通过。
- [ ] 未执行真实联网测试，除非任务明确批准。
- [ ] 未修改 backend / frontend。

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
