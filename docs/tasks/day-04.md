# Week 14 Day 04

## 负责角色

frontend-agent -> tester-agent -> reviewer-agent -> Lead

## 执行方式

- 是否需要 spawn subagent：是
- Lead 是否可直接执行：否，除非当前运行环境没有 subagent 工具且用户确认降级
- 必须 spawn 的 agent：frontend-agent、tester-agent、reviewer-agent
- 是否允许并行：否，默认顺序执行

## 任务目标

为 `/dev/image-to-layout` 增加最小下载能力，让用户能下载生成结果。

优先方案：

```text
下载单个完整 HTML 文件
```

可选补充：

```text
下载 index.html
下载 style.css
```

Week 14 不做复杂 ZIP 导出。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- `docs/tasks/day-04.md`
- `docs/agents/frontend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- 必要时 `docs/spec.md`
- 当前前端页面、复制逻辑和 preview 相关组件代码

说明：

- 不读取 `docs/archive/`。
- 不读取 backend / worker 全量代码。

## 允许修改

- `frontend/` 中与 `/dev/image-to-layout`、下载按钮、文件内容组合、前端测试相关的文件。

## 禁止修改

- `backend/`
- `worker/`
- `schema/`
- `docs/archive/`
- 复杂 ZIP 导出
- Vue SFC 可运行化
- 多文件项目模板导出
- 后端文件下载接口

## 实施步骤

1. 复用 Day 3 的 HTML / CSS / 完整 HTML 组合逻辑。
2. 增加下载完整 HTML 文件入口。
3. 如成本很低，可增加 `index.html` / `style.css` 分文件下载；否则只做单文件 HTML。
4. 文件名使用安全、简单、可预测的名称。
5. 没有可下载内容时展示禁用态或空状态。
6. 不生成 ZIP，不新增后端接口。
7. 补充前端测试或最低必要验证。
8. reviewer-agent 检查下载内容、安全边界和是否越界。
9. Lead 二次验收。

## 验收标准

- [ ] 用户可以下载至少一个完整 HTML 文件。
- [ ] 下载文件能在本地打开看到生成内容。
- [ ] 下载内容不包含真实 API key 或敏感信息。
- [ ] 没有实现复杂 ZIP。
- [ ] 没有修改后端或 Worker。
- [ ] iframe 安全策略没有被改动。
- [ ] 前端测试或 build 通过；无法运行时说明原因。

## Lead 二次验收

- 检查下载功能是否满足“用户可拿走结果”的 MVP 缺口。
- 检查是否没有扩大成导出系统。
- 检查 tester-agent 与 reviewer-agent 结论。
- 结论：通过 / 条件通过 / 不通过。

## 输出格式

```text
## 修改摘要
## 修改文件
## 页面影响
## 下载文件说明
## 测试结果
## Review 结果
## 风险提示
```
