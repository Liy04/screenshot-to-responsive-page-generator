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
4. 当存在活跃日卡时，再读取当天对应的 `docs/tasks/day-xx.md`
5. 当前任务相关代码
6. 必要时读取 `docs/spec.md`

## 活跃文档

| 类型 | 路径 | 说明 |
|---|---|---|
| 当前阶段事实源 | `docs/current.md` | Week 10 已完成收口，可进入 Week 11 规划 |
| 当前计划摘要 | `docs/plan.md` | Week 10 完成摘要和后续建议 |
| 当前核心规格 | `docs/spec.md` | Week 09 真实链路契约 + Week 10 稳定化与验收补充契约 |
| 当前任务卡目录 | `docs/tasks/` | Week 10 日卡清理后保留空目录，等待下一周重新生成 |
| context-scout 流程 | `docs/playbooks/context-scout.md` | 大任务上下文侦察流程 |
| 历史归档 | `docs/archive/` | 历史计划、总结、smoke、验收报告和参考文档 |

## Week 10 归档入口

| 类型 | 路径 |
|---|---|
| Week 10 原始计划归档 | `docs/archive/week/10-acceptance-plan.md` |
| Week 10 Summary | `docs/archive/week/10-summary.md` |
| Week 10 Dev Smoke | `docs/archive/week/10-dev-smoke.md` |
| Week 10 Acceptance Report | `docs/archive/week/10-acceptance-report.md` |

## 归档说明

`docs/archive/` 只用于历史追溯，不参与默认上下文。

Week 10 已完成收口，当前不再有正在执行中的 `docs/tasks/day-xx.md`；下一周开始时再由文档线程重新生成。
