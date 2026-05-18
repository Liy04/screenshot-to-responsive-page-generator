# Docs Index

## 文件目的

本文档是 Lite 文档结构入口，用于说明当前默认上下文和历史归档位置。

当前活跃文档压缩为：

```text
docs/
  current.md
  plan.md
  spec.md
  INDEX.md
  agents/
  tasks/
    _template.md
    day-xx.md  # only when an active task exists
  playbooks/
    context-scout.md
  archive/
```

## 默认阅读顺序

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/plan.md`
4. 当存在活跃日卡时，再读取当天对应的 `docs/tasks/day-xx.md`
5. 当前任务相关代码
6. 必要时读取 `docs/spec.md`

## 活跃文档

| 类型 | 路径 | 说明 |
|---|---|---|
| 当前阶段事实源 | `docs/current.md` | Week 10 已完成收口，可进入 Week 11 规划 |
| 当前计划摘要 | `docs/plan.md` | Week 10 完成摘要和后续建议 |
| 当前核心规格 | `docs/spec.md` | Week 09 真实链路契约 + Week 10 稳定化与验收补充契约 |
| Codex 角色边界 | `docs/agents/README.md` | Codex Lead + Lightweight Agents Workflow |
| 当前任务卡目录 | `docs/tasks/` | 当前不创建假 day 卡；模板见 `docs/tasks/_template.md` |
| context-scout 流程 | `docs/playbooks/context-scout.md` | 大任务上下文侦察流程 |
| 历史归档 | `docs/archive/` | 历史计划、总结、smoke、验收报告和参考文档 |

## Codex Lead + Lightweight Agents

`docs/agents/` 定义 Codex 执行任务时的角色阶段和边界规则。这不是 Claude Code Custom Subagents，不是 Claude Code `/agents`，也不是自动并发系统。

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
- 大任务 / 跨模块 / 边界不清时先进入 `explorer-agent` 阶段，可按需使用 context-scout。
- Agent 文档只定义长期角色边界，不记录临时 Week 任务。

## Day 卡建议模板

模板见 `docs/tasks/_template.md`。不要创建假的当前 `day-xx.md`；只有真实计划任务需要日卡时再创建。

## Week 10 归档入口

| 类型 | 路径 |
|---|---|
| Week 10 原始计划归档 | `docs/archive/week/10-acceptance-plan.md` |
| Week 10 Summary | `docs/archive/week/10-summary.md` |
| Week 10 Dev Smoke | `docs/archive/week/10-dev-smoke.md` |
| Week 10 Acceptance Report | `docs/archive/week/10-acceptance-report.md` |

## 归档说明

`docs/archive/` 只用于历史追溯，不参与默认上下文。

Week 10 已完成收口，当前不再有正在执行中的 `docs/tasks/day-xx.md`；下一周开始时再由 docs-agent 按真实计划重新生成。
