# Week 03 Day 3：Layout JSON 示例

## 任务目标

只完成 `examples/valid` 和 `examples/invalid` 下的 Layout JSON 示例。

## 必须完成

- 至少 5 个合法示例：
  - `landing-page.layout.json`
  - `login-page.layout.json`
  - `dashboard-card.layout.json`
  - `mobile-list.layout.json`
  - `profile-page.layout.json`
- 至少 3 个非法示例：
  - `invalid-missing-version.layout.json`
  - `invalid-duplicate-node-id.layout.json`
  - `invalid-responsive-target.layout.json`
- 每个合法示例应能表达一个真实页面结构。

## 禁止事项

- 不写 Worker 校验器。
- 不改后端、前端业务代码。
- 不接真实 AI、模型 API、Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL，不新增 Entity / Mapper。
- 不做 Vue 页面代码生成。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week03-day3-examples.md`
- `docs/layout-schema-design.md`
- `schema/layout.schema.json`
- `examples/` 下已有示例，如存在

## 建议修改文件

- `examples/valid/*.layout.json`
- `examples/invalid/*.layout.json`
- `docs/week/03-status.md`，仅在状态需要同步时修改

## 验收标准

- 5 个合法示例存在。
- 3 个非法示例存在。
- 非法示例用途明确。
- 不修改业务代码。

## Codex 执行要求

- 先输出计划，等待确认后再修改文件。
- 只做示例文件。
- 完成后列出每个示例用途。
