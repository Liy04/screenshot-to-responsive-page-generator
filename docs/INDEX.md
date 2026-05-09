# Docs Index

## 文件目的

本文档是 Lite 文档结构入口，用于说明当前默认上下文和历史归档位置。

当前活跃文档压缩为：

```text
docs/
  current.md
  plan.md
  task.md
  spec.md
  INDEX.md
  playbooks/
    context-scout.md
  archive/
```

## 默认阅读顺序

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/task.md`
4. 当前任务相关代码
5. 必要时读取 `docs/spec.md`

## 活跃文档

| 类型 | 路径 | 说明 |
|---|---|---|
| 当前阶段事实源 | `docs/current.md` | Week 06 收口状态、完成情况、允许项、禁止项 |
| 当前计划摘要 | `docs/plan.md` | Week 06 完成情况和 Week 07 候选方向 |
| 当前唯一任务卡 | `docs/task.md` | Week 06 已完成，等待用户确认 Week 07 方向 |
| 当前核心规格 | `docs/spec.md` | 当前 generated-page MVP 闭环仍有效的核心契约 |
| context-scout 流程 | `docs/playbooks/context-scout.md` | 大任务上下文侦察流程 |
| 历史归档 | `docs/archive/` | 历史计划、任务卡、规格、提示词和参考文档 |

## Week 06 归档

| 类型 | 路径 |
|---|---|
| Week 06 原始计划 | `docs/archive/week/06-plan.md` |
| Week 06 smoke 文档 | `docs/archive/week/06-dev-smoke.md` |
| Week 06 实践报告素材 | `docs/archive/week/06-report-material.md` |
| Week 06 总结 | `docs/archive/week/06-summary.md` |

## 归档说明

`docs/archive/` 只用于历史追溯，不参与默认上下文。

本次 Lite Refactor 后，旧的团队级目录结构已归档到：

- `docs/archive/lite-refactor/`
- `docs/archive/reference/`

早期周文档、旧任务卡、旧规格副本、旧提示词、Week 05 原始计划、Week 05 smoke、Week 05 总结归档、Week 06 原始计划、Week 06 smoke、Week 06 报告素材以及 Week 06 总结归档仍保留在已有归档目录中。

周计划、smoke 文档和总结在完成拆分或收口后应归档到 `docs/archive/week/`，不要长期留在 `docs/` 根目录。

## 路径优先级

新任务优先引用：

1. `docs/current.md`
2. `docs/plan.md`
3. `docs/task.md`
4. `docs/spec.md`
5. `docs/playbooks/context-scout.md`

历史归档中的旧路径允许保留，用于追溯当时上下文。
