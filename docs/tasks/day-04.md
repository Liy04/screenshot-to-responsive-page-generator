# Week 13 Day 04

## 负责角色

worker-agent -> tester-agent -> reviewer-agent -> lead

## 任务目标

增强 preview 的静态样式表达，让 card / button / input / text 更像实际 UI，同时保持严格安全边界。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-04.md`
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
- 模型原始 HTML 直出
- CSS `url(`、`expression(`、`@import`
- inline event
- `javascript:` URL

## 实施步骤

1. worker-agent 找到 Layout JSON -> HTML/CSS 静态编译器。
2. 增加或校准 style key 白名单映射。
3. 增加 style value sanitizer。
4. 优先提升 card / button / input / text 的视觉表达，不扩展复杂页面能力。
5. tester-agent 覆盖 HTML escape、安全 CSS、危险 style 丢弃或 warning、valid / invalid 行为。
6. reviewer-agent 审查 CSS 注入、HTML 注入和安全边界。

## 验收标准

- [x] card 样式更清晰。
- [x] button 样式更清晰。
- [x] input 样式更清晰。
- [x] text 样式更清晰。
- [x] style key 必须白名单。
- [x] style value 必须 sanitizer。
- [x] CSS 禁止 `url(`。
- [x] CSS 禁止 `expression(`。
- [x] CSS 禁止 `@import`。
- [x] HTML attribute 禁止 `on*`。
- [x] href / src 禁止 `javascript:`。
- [x] 所有 text content 必须 escape。
- [x] Worker 测试通过。
- [x] 未修改 backend / frontend。

## Lead 二次验收

- [x] 对照任务目标和验收标准检查。
- [x] 检查修改范围是否越界。
- [x] 检查测试 / smoke / review 是否完成或说明原因。
- [x] 检查安全边界和密钥风险。
- [x] 检查是否需要同步文档。
- [x] 结论：通过。

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
