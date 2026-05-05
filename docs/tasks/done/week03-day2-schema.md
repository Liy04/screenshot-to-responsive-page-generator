# Week 03 Day 2：JSON Schema

## 任务目标

只完成 `schema/layout.schema.json`，用 Schema 约束 Layout JSON v0.1 的基础结构。

## 必须完成

- 新增或完善 `schema/layout.schema.json`。
- 约束顶层字段：`version`、`page`、`source`、`tokens`、`layout`、`assets`、`responsive`、`assumptions`、`warnings`。
- 约束 `version` 为 `0.1`。
- 约束支持的 node type。
- 约束 `children` 必须是数组。

## 禁止事项

- 不写 examples。
- 不写 Worker 校验器。
- 不改后端、前端业务代码。
- 不接真实 AI、模型 API、Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL，不新增 Entity / Mapper。
- 不做 Vue 页面代码生成。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week03-day2-schema.md`
- `docs/layout-schema-design.md`
- `schema/layout.schema.json`，如已存在

## 建议修改文件

- `schema/layout.schema.json`
- `docs/week/03-status.md`，仅在状态需要同步时修改

## 验收标准

- `schema/layout.schema.json` 存在。
- 缺少关键顶层字段应无法通过。
- node type 不合法应无法通过。
- `children` 不是数组应无法通过。
- 不引入依赖，不改业务代码。

## Codex 执行要求

- 先输出计划，等待确认后再修改文件。
- 只做 Schema。
- 完成后说明 Schema 能覆盖和不能覆盖的规则。
