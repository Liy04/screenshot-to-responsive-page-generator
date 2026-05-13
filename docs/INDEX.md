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
| 当前阶段事实源 | `docs/current.md` | Week 09 已完成收口，准备进入下一周规划 |
| 当前计划摘要 | `docs/plan.md` | Week 09 完成摘要和后续建议 |
| 当前核心规格 | `docs/spec.md` | 当前 generated-page MVP 闭环、Week 09 真实链路契约与运行配置要求 |
| 当前任务卡目录 | `docs/tasks/` | Week 09 日卡已清理，等待下一周重新生成 `day-xx.md` |
| context-scout 流程 | `docs/playbooks/context-scout.md` | 大任务上下文侦察流程 |
| 历史归档 | `docs/archive/` | 历史计划、任务卡、规格、提示词和参考文档 |

## Week 09 入口

| 类型 | 路径 |
|---|---|
| Week 09 原始长计划归档 | `docs/archive/week/09-plan.md` |
| Week 09 总结归档 | `docs/archive/week/09-summary.md` |
| Week 09 smoke 归档 | `docs/archive/week/09-dev-smoke.md` |
| Week 09 运行配置说明 | `docs/spec.md` |

## 归档说明

`docs/archive/` 只用于历史追溯，不参与默认上下文。

Week 09 的原始长计划、summary 和 dev smoke 已归档到 `docs/archive/week/`。

Week 09 已完成 backend `REAL_AI` 命中验证和前端 iframe 预览验证；后续运行配置以 `docs/spec.md` 为准。

当前没有正在执行中的 `docs/tasks/day-xx.md`；下一周开始时再由文档线程重新生成。

## 路径优先级

新任务优先引用：

1. `docs/current.md`
2. `docs/plan.md`
3. `docs/spec.md`
4. 当存在活跃日卡时，再读取当天对应的 `docs/tasks/day-xx.md`
5. `docs/playbooks/context-scout.md`
6. `docs/archive/week/` 中的归档文档（回看或验收时使用）

历史归档中的旧路径允许保留，用于追溯当时上下文。
