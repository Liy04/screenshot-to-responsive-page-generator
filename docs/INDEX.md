# Docs Index

## 文件目的

本文档是 Lite 文档结构入口，用于说明当前默认上下文和历史归档位置。

当前活跃文档压缩为：

```text
docs/
  current.md
  mvp-roadmap.md
  plan.md
  spec.md
  INDEX.md
  agents/
  quality/
    week13-quality.md
  smoke/
    week14-mvp-smoke.md
    week13-quality-smoke.md
    real-ai-smoke.md
  tasks/
    _template.md
    day-xx.md
  playbooks/
    context-scout.md
  archive/
```

## 默认阅读顺序

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/mvp-roadmap.md`
4. `docs/plan.md`
5. 当存在活跃日卡时，再读取当天对应的 `docs/tasks/day-xx.md`
6. 中大型任务执行前读取 `docs/agents/README.md` 的 spawn 规则
7. 当前任务相关代码
8. 必要时读取 `docs/spec.md`

## 活跃文档

| 类型 | 路径 | 说明 |
|---|---|---|
| 当前阶段事实源 | `docs/current.md` | Week 14：MVP 产品化交付闭环 |
| MVP 路线锚点 | `docs/mvp-roadmap.md` | PRD / MVP 对齐、当前缺口、暂缓事项和周计划验收规则 |
| 当前计划摘要 | `docs/plan.md` | Week 14 产品化目标、Day 计划和安全边界 |
| 当前核心规格 | `docs/spec.md` | 当前有效口径、真实 AI 链路、artifact、前端预览等核心规格 |
| 输出质量标准 | `docs/quality/week13-quality.md` | Week 13 质量标准、评分表和通过线 |
| Week 14 MVP smoke | `docs/smoke/week14-mvp-smoke.md` | Week 14 MVP 上传、生成、预览、复制 / 下载链路 smoke |
| 质量 smoke 记录 | `docs/smoke/week13-quality-smoke.md` | 三张 samples 的顺序 smoke 记录 |
| Codex 角色边界 | `docs/agents/README.md` | Codex Lead + Short-lived Subagents Workflow |
| 当前任务卡目录 | `docs/tasks/` | Week 14 day 卡生成后放在此处 |
| context-scout playbook | `docs/playbooks/context-scout.md` | explorer-agent 可选使用的只读上下文压缩方法 |
| 历史归档 | `docs/archive/` | 历史计划、总结、smoke、验收报告和参考文档 |

## Codex Lead + Short-lived Subagents

`docs/agents/` 定义 Codex Lead + Short-lived Subagents Workflow。Subagent 指 Codex 当前运行环境支持 subagent 工具时，由 Lead 显式创建的短生命周期子智能体。

这不是 Claude Code Custom Subagents，不是 `.claude/agents/`，不是 `CLAUDE.md`，不是 Claude Code `/agents`，不是 Claude Code Agent Teams，不是自动并发系统，也不是长期常驻代理。

- `docs/agents/README.md`：工作流总说明
- `docs/agents/lead.md`：Lead 角色
- `docs/agents/explorer-agent.md`：上下文侦察角色
- `docs/agents/docs-agent.md`：文档角色
- `docs/agents/backend-agent.md`：后端角色
- `docs/agents/frontend-agent.md`：Vue3 + Vite + JavaScript 前端角色
- `docs/agents/worker-agent.md`：Worker 角色
- `docs/agents/tester-agent.md`：测试 / smoke / 复现角色
- `docs/agents/reviewer-agent.md`：代码质量 / 安全 / 潜在 bug / 边界审查角色

说明：

- 默认新任务仍优先读取 Docs Lite 文件。
- `docs/archive/` 不是默认读取内容。
- 小任务 Lead 可直接做；用户显式要求 spawn 时必须 spawn；中大型开发任务必须 spawn 对应实现 agent。
- 大任务 / 跨模块 / 边界不清时先 spawn `explorer-agent`，再由 explorer-agent 按需使用 context-scout。
- 代码实现后 spawn `tester-agent`；有代码变更后 spawn `reviewer-agent`。
- 如果当前运行环境没有 subagent 工具，Lead 必须明确说明降级原因并请求确认，不能静默主线程自演。
- Agent 文档只定义长期角色边界，不记录临时 Week 任务。

## Day 卡

当前任务卡：

- Week 14 day 卡已生成，执行时以当前 day 卡为准。
- 旧任务卡应在周收口后归档或清理，避免污染当前上下文。

模板见 `docs/tasks/_template.md`。

## 旧周归档入口

| 类型 | 路径 |
|---|---|
| Week 12 原始严格验收报告 | `docs/archive/week/12-plan-strict-acceptance.md` |
| Week 11 原始计划归档 | `docs/archive/week/11-plan.md` |
| Week 11 Summary | `docs/archive/week/11-summary.md` |
| Week 11 Dev Smoke | `docs/archive/week/11-dev-smoke.md` |
| Week 11 Acceptance Report | `docs/archive/week/11-acceptance-report.md` |

## 归档说明

`docs/archive/` 只用于历史追溯，不参与默认上下文。
