# Week 02 Day 5：端到端验收与文档收口

## 任务目标

从零验收 Week 02 最小闭环，并同步 smoke 文档、状态看板和必要入口说明。

## 必须完成

- 验证后端打包或测试命令。
- 验证前端构建命令。
- 验证 Worker smoke。
- 手动验证完整流程：

```text
上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果
```

- 更新 `tests/smoke/README.md` 中 Week 02 验证步骤。
- 更新 `docs/week/02-status.md` 中线程状态、验收结果、风险和下一步。
- 必要时更新 `README.md` 中 Week 02 运行说明。

## 禁止事项

- 测试线程只报告问题，不直接修复业务代码。
- 不借验收机会接真实模型 API。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL 实际落库。
- 不创建数据库表、Mapper、Entity 或实体表映射。
- 不实现真实截图解析、真实页面代码生成、导出 ZIP、在线编辑器。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week02-day5-smoke-and-docs.md`
- `docs/week/02-status.md`
- `docs/api-contracts.md`
- `docs/frontend-pages.md`
- `docs/testing.md`
- `tests/smoke/README.md`
- 与启动和验证直接相关的前端、后端、worker 文件

## 建议修改文件

- `tests/smoke/README.md`
- `docs/week/02-status.md`
- `README.md`，仅在启动方式或入口说明需要同步时修改。

## 验收标准

- 前端构建通过。
- 后端打包或测试通过。
- Worker smoke 通过。
- 端到端流程可以按文档复现。
- smoke 文档命令与实际可执行命令一致。
- 状态看板准确记录验收结论、风险和下一步。

## Codex 执行要求

- 先输出验收计划，等待确认后再执行。
- 如启动 dev server 或后端服务，验证完成后必须停止进程。
- 如发现问题，记录复现步骤、实际结果、预期结果和影响范围。
- 不直接修复业务代码；如需修复，应另开 Bug 修复任务卡。
