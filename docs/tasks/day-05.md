# Week 13 Day 05

## 负责角色

frontend-agent -> tester-agent -> reviewer-agent -> lead

## 任务目标

让 `/dev/image-to-layout` 和相关对照区域更适合顺序 smoke 与人工检查，但不做拖拽编辑器或复杂工作台。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-05.md`
- `docs/agents/frontend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/quality/week13-quality.md`
- 必要时 `docs/spec.md`
- `frontend/` 当前相关代码

## 允许修改

- `frontend/`
- frontend 相关测试

## 禁止修改

- `backend/`
- `worker/`
- iframe sandbox 放宽
- `allow-scripts`
- 拖拽编辑器
- 在线编辑器
- 复杂状态管理

## 实施步骤

1. frontend-agent 梳理当前 `/dev/image-to-layout` 页面。
2. 增加更清晰的原图、生成预览、metadata 与 warning 对照布局。
3. 保持 iframe `sandbox=""`，不得加入 `allow-scripts`。
4. tester-agent 运行前端测试和最小页面检查。
5. reviewer-agent 审查安全和边界。

## 验收标准

- [x] 原图和生成 iframe 更容易对比。
- [x] Layout JSON 仍可查看。
- [x] warnings / errors 仍可查看。
- [x] metadata 仍可查看。
- [x] iframe sandbox 不放宽。
- [x] 不加入 `allow-scripts`。
- [x] 不做拖拽 / 编辑器 / 复杂工作台。
- [x] Frontend 测试通过。
- [x] 未修改 backend / worker。

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
