# Week 03 Day 1：Layout JSON 设计文档

## 任务目标

只完成 `docs/layout-schema-design.md`，明确 Layout JSON v0.1 的定位、字段、节点类型和边界。

## 必须完成

- 说明 Layout JSON 是什么。
- 说明为什么需要中间层。
- 说明为什么不是 HTML / Vue。
- 说明 v0.1 支持字段。
- 说明支持节点类型。
- 说明 `bounds`、`constraints`、`responsive`、`assumptions`、`warnings`。
- 说明当前限制和后续扩展方向。

## 禁止事项

- 不写 Schema。
- 不写 examples。
- 不改 Worker、后端、前端业务代码。
- 不接真实 AI、模型 API、Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL，不新增 Entity / Mapper。
- 不做 Vue 页面代码生成。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week03-day1-layout-design.md`
- `docs/week/03-plan.md`
- `docs/layout-schema-design.md`，如已存在

## 建议修改文件

- `docs/layout-schema-design.md`
- `docs/week/03-status.md`，仅在状态需要同步时修改

## 验收标准

- 文档能说明中间层价值。
- 文档包含 v0.1 字段、节点类型和关键字段说明。
- 文档不包含大段执行计划或提示词。
- 文档不把 P1 / P2 内容写成 P0。

## Codex 执行要求

- 先输出计划，等待确认后再修改文档。
- 只做设计文档。
- 完成后检查是否违反当前阶段禁止项。
