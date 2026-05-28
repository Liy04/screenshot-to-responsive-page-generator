# Docs Index

## 文件目的

本文档是 Docs Lite 入口，用于说明默认阅读顺序和活跃文档职责。

## 默认阅读顺序

1. `AGENTS.md`
2. `docs/INDEX.md`
3. `docs/current.md`
4. `docs/mvp-roadmap.md`
5. `docs/plan.md`
6. `docs/tasks/day-xx.md`
7. `docs/agents/README.md`
8. `docs/agents/<role>.md`
9. 代码实现任务读取 `docs/engineering-baseline.md`
10. reviewer-agent 必须读取 `docs/engineering-baseline.md`
11. Lead acceptance 回查 `docs/engineering-baseline.md`
12. 必要时 `docs/spec.md`

`docs/archive/` 默认不读；只有明确要求历史追溯、审计、验收证据或归档整理时才读取。

## 文档职责

| 路径 | 职责 |
|---|---|
| `AGENTS.md` | 长期入口规则、默认工作方式和协作边界 |
| `docs/INDEX.md` | Docs Lite 阅读顺序和文档职责索引 |
| `docs/current.md` | One-screen live state，只记录当前事实状态、active gate、当前任务、阻塞、已验证事实和下一交接 |
| `docs/mvp-roadmap.md` | 长期 MVP 路线锚点，保存 Product Goal、MVP Scope、Gap Pool、Now / Next / Later、Candidate Bets、Cycle Plan Gate 和 Drift Guard |
| `docs/plan.md` | 当前 Cycle / Week single bet，保存本周期规划检查、Must / Should / Could / Won’t、验收、smoke、退出和下一周期规则 |
| `docs/tasks/day-xx.md` | 执行层 day 卡，只执行当前 plan 的 single bet |
| `docs/tasks/_template.md` | Day 卡模板和执行边界 |
| `docs/engineering-baseline.md` | 工程质量底线，约束新代码和被触碰代码，不替代 roadmap / plan / spec |
| `docs/spec.md` | 当前有效产品规格、接口契约和验收口径 |
| `docs/agents/` | Codex Lead + Short-lived Subagents 角色边界 |
| `docs/smoke/` | 当前有效 smoke 说明或记录 |
| `docs/quality/` | 当前有效质量标准 |
| `docs/playbooks/` | 可选 playbook |
| `docs/archive/` | 历史归档，默认不参与上下文 |

## Cycle 边界

- `docs/mvp-roadmap.md` 是长期路线锚点，不写每日执行细节或当前周流水账。
- `docs/plan.md` 是当前 Cycle / Week single bet，不承载长期路线和候选 backlog。
- `docs/current.md` 是当前事实状态，不承载 roadmap、候选池或下一周期规划。
- Day 卡是执行层，不重新定义产品方向、不扩展 roadmap、不把 Should / Could 自动升级为 Must。
- 未完成 Should / Could 默认回候选池，不自动滚入下一周期。
- 生成新周期计划前，必须重新执行 `docs/mvp-roadmap.md` 的 Cycle Plan Gate。

## Subagents

`docs/agents/` 定义 Codex Lead + Short-lived Subagents Workflow。

Subagent 指 Codex 当前运行环境支持 subagent 工具时，由 Lead 显式创建的短生命周期子智能体；不是 Claude Code Custom Subagents，不是 `.claude/agents/`，不是 `CLAUDE.md`，不是 Claude Code `/agents`，也不是自动并发系统。
