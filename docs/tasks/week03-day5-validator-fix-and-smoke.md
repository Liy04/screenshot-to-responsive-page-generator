# Week 03 Day 5：校验器修复与 Smoke

## 任务目标

只做校验器测试、修复和 smoke，确保 P0 校验链路可复现。

## 必须完成

- 运行合法示例校验。
- 运行非法示例校验。
- 修复 Day 4 校验器中发现的问题。
- 补充或修正 `worker/test_layout_validator.py`。
- 记录 smoke 命令和结果。

## 禁止事项

- 不新增 P1 mock 保存。
- 不做前端查看页。
- 不接真实 AI、模型 API、Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL，不新增 Entity / Mapper。
- 不做 Vue 页面代码生成。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week03-day5-validator-fix-and-smoke.md`
- `docs/layout-schema-design.md`
- `schema/layout.schema.json`
- `examples/valid/`
- `examples/invalid/`
- `worker/layout_validator.py`
- `worker/test_layout_validator.py`

## 建议修改文件

- `worker/layout_validator.py`
- `worker/test_layout_validator.py`
- `tests/smoke/README.md`，仅在需要补充 Week 03 smoke 说明时修改
- `docs/week/03-status.md`，仅在状态需要同步时修改

## 验收标准

- valid 示例通过。
- invalid 示例失败。
- 错误信息清晰。
- 校验器测试通过。
- 未修改前端、后端业务代码。

## Codex 执行要求

- 先输出 smoke 与修复计划，等待确认后再执行。
- 只修复校验器相关问题。
- 完成后汇报命令、结果和剩余风险。
