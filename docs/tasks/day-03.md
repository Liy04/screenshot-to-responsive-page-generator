# Week 13 Day 03

## 负责角色

worker-agent -> tester-agent -> reviewer-agent -> lead

## 任务目标

提升 Layout JSON v0.1 的映射质量和 deterministic repair，让页面、section、card、form、button、input、text 的语义更准确。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-03.md`
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
- `schema/` 大升级
- Layout JSON v0.2
- 真实 API key
- 不可信 style 直通 CSS

## 实施步骤

1. worker-agent 梳理当前 intermediate -> Layout JSON 映射和 repair 流程。
2. 在 v0.1 兼容范围内补齐 page / section / card / button / input / form / text 的基础默认值。
3. 让 repair 仅基于 node role / type / safety 规则补默认值，不调用模型自由发挥。
4. tester-agent 运行 worker 测试。
5. reviewer-agent 审查 sanitizer、validator、fallback 边界。

## 验收标准

- [ ] 不升级 Layout JSON schema v0.2。
- [ ] repair 是 deterministic rule，不再调用模型自由发挥。
- [ ] repair 只能基于 node role / type 补默认值。
- [ ] repair 不保留危险 style value。
- [ ] repair 不绕过 validator。
- [ ] 未知 style key 进入 warnings 或被拒绝，不静默编译。
- [ ] Worker 测试通过。
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
