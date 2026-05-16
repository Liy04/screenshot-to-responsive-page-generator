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
  tasks/
    day-xx.md
  playbooks/
    context-scout.md
  archive/
```

## 默认阅读顺序

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/plan.md`
4. 当天对应的 `docs/tasks/day-xx.md`
5. 当前任务相关代码
6. 必要时读取 `docs/spec.md`

## 活跃文档

| 类型 | 路径 | 说明 |
|---|---|---|
| 当前阶段事实源 | `docs/current.md` | Week 10：真实 AI 链路稳定化与可复现验收 |
| 当前计划摘要 | `docs/plan.md` | Week 10 简版开发计划、P0/P1/P2 和 7 天计划 |
| 当前核心规格 | `docs/spec.md` | Week 09 真实链路契约 + Week 10 稳定化补充契约 |
| 当前任务卡 | `docs/tasks/day-xx.md` | 由项目经理按当天指定的 Week 10 任务卡 |
| context-scout 流程 | `docs/playbooks/context-scout.md` | 大任务上下文侦察流程 |
| 历史归档 | `docs/archive/` | 历史计划、总结、smoke、提示词和参考文档 |

## Week 10 入口

| 类型 | 路径 |
|---|---|
| Week 10 原始计划归档 | `docs/archive/week/10-acceptance-plan.md` |
| Week 10 Day 01 | `docs/tasks/day-01.md` |
| Week 10 Day 02 | `docs/tasks/day-02.md` |
| Week 10 Day 03 | `docs/tasks/day-03.md` |
| Week 10 Day 04 | `docs/tasks/day-04.md` |
| Week 10 Day 05 | `docs/tasks/day-05.md` |
| Week 10 Day 06 | `docs/tasks/day-06.md` |
| Week 10 Day 07 | `docs/tasks/day-07.md` |

## 归档说明

`docs/archive/` 只用于历史追溯，不参与默认上下文。

`docs/archive/week/10-acceptance-plan.md` 是 Week 10 原始验收计划来源，不作为日常默认上下文。

## 路径优先级

新任务优先引用：

1. `docs/current.md`
2. `docs/plan.md`
3. `docs/spec.md`
4. 当天对应的 `docs/tasks/day-xx.md`
5. `docs/playbooks/context-scout.md`
6. `docs/archive/week/` 中的归档文档（回看或验收时使用）
