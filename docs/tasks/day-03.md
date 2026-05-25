# Week 14 Day 03

## 负责角色

frontend-agent -> tester-agent -> reviewer-agent -> Lead

## 执行方式

- 是否需要 spawn subagent：是
- Lead 是否可直接执行：否，除非当前运行环境没有 subagent 工具且用户确认降级
- 必须 spawn 的 agent：frontend-agent、tester-agent、reviewer-agent
- 是否允许并行：否，默认顺序执行

## 任务目标

为 `/dev/image-to-layout` 增加最小代码复制能力，让用户能复制生成结果。

必须提供：

- 复制 HTML。
- 复制 CSS。
- 复制完整 HTML 文档。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/day-03.md`
- `docs/agents/frontend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- 必要时 `docs/spec.md`
- 当前前端页面、API 和 preview 相关组件代码

说明：

- 不读取 `docs/archive/`。
- 不读取 backend / worker 全量代码。

## 允许修改

- `frontend/` 中与 `/dev/image-to-layout`、生成结果展示、复制按钮、前端测试相关的文件。

## 禁止修改

- `backend/`
- `worker/`
- `schema/`
- `docs/archive/`
- 后端 API 契约
- 模型 prompt
- Worker 编译逻辑

## 实施步骤

1. 读取当前前端生成结果字段来源，确认可复制内容来自 Worker 静态编译结果。
2. 增加复制 HTML、复制 CSS、复制完整 HTML 文档入口。
3. 复制成功和失败都要有用户可读反馈。
4. 不复制模型原始输出。
5. 如果当前结果没有可复制内容，展示禁用态或清晰空状态。
6. 补充前端组件测试或最低必要测试。
7. reviewer-agent 检查复制内容来源、安全边界和未越界修改。
8. Lead 二次验收。

## 验收标准

- [ ] 用户可以复制 HTML。
- [ ] 用户可以复制 CSS。
- [ ] 用户可以复制完整 HTML 文档。
- [ ] 复制内容来自静态编译结果或前端安全组合结果。
- [ ] 复制失败有提示。
- [ ] 没有真实 API key、环境变量或敏感信息进入复制内容。
- [ ] 不修改 backend / worker。
- [ ] 前端测试或 build 通过；无法运行时说明原因。

## Lead 二次验收

- 检查复制功能是否满足 MVP 交付缺口。
- 检查是否没有扩大到下载、ZIP 或项目模板导出。
- 检查 tester-agent 与 reviewer-agent 结论。
- 结论：通过 / 条件通过 / 不通过。

## 输出格式

```text
## 修改摘要
## 修改文件
## 页面影响
## 复制内容说明
## 测试结果
## Review 结果
## 风险提示
```
