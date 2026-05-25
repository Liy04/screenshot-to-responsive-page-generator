# Week 14 Day 02

## 负责角色

frontend-agent -> tester-agent -> reviewer-agent -> Lead

## 任务目标

重组 `/dev/image-to-layout` 的生成结果区，使页面从调试信息堆叠变成更清晰的 MVP 演示路径。

目标结构：

```text
生成状态
-> 原图 / 生成预览
-> 交付操作入口
-> Layout JSON / previewHtml 调试信息
```

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/day-02.md`
- `docs/agents/frontend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- 必要时 `docs/spec.md`
- 当前前端页面和组件代码

说明：

- 不读取 `docs/archive/`。
- 不读取 backend / worker 全量代码。

## 允许修改

- `frontend/` 中与 `/dev/image-to-layout` 页面相关的文件。
- 当前任务必要的前端测试文件。

## 禁止修改

- `backend/`
- `worker/`
- `schema/`
- `docs/archive/`
- `docs/plan.md`
- `docs/current.md`
- `docs/spec.md`
- API 契约

## 实施步骤

1. 只读探索当前 `/dev/image-to-layout` 页面结构和已有 preview 组件。
2. 将结果区整理为用户可理解的展示顺序。
3. 保留原图展示、生成结果、Layout JSON、previewHtml 和 iframe 预览。
4. 预留 Day 3 / Day 4 的复制和下载操作区，但不实现复制 / 下载。
5. 保持 iframe `sandbox=""`，不得加入 `allow-scripts`。
6. 运行前端最低必要测试或 build。
7. reviewer-agent 检查页面安全、Agent 边界和是否提前做 Day 3 / Day 4。
8. Lead 二次验收。

## 验收标准

- [ ] 页面结果区展示顺序更清晰。
- [ ] 原图和 iframe 预览都保留。
- [ ] REAL_AI / FALLBACK / FAILED 基础信息仍可见。
- [ ] Layout JSON 和 previewHtml 调试信息仍可展开或查看。
- [ ] 未实现 Day 3 复制功能。
- [ ] 未实现 Day 4 下载功能。
- [ ] iframe 仍为 `sandbox=""`。
- [ ] 无 `allow-scripts`。
- [ ] 前端测试或 build 通过；无法运行时说明原因。

## Lead 二次验收

- 检查是否只修改 frontend 范围。
- 检查是否服务 Week 14 MVP 产品化，而不是继续模型质量优化。
- 检查 tester-agent 与 reviewer-agent 结论。
- 结论：通过 / 条件通过 / 不通过。

## 输出格式

```text
## 修改摘要
## 修改文件
## 页面影响
## 测试结果
## Review 结果
## 风险提示
```
