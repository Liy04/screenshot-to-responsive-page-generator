# Week 04 Day 6：集成 smoke

## 任务目标

线程：测试线程。

完成 Worker + 后端 + 前端集成 smoke，验证 Week 04 主链路是否跑通。

## 必须完成

- 执行 Worker validator 测试。
- 执行 Worker static generator 测试。
- 执行后端测试或 package。
- 执行前端 build。
- 使用 valid Layout JSON 生成 generated-page artifact。
- PUT 到后端 mock 接口。
- GET 查询 generated-page artifact。
- 打开前端 generated-page 页面。
- 验证 iframe sandbox 预览。
- 记录 mock-data 副产物不提交。

## 禁止事项

- 测试线程只报告问题，不直接修复业务代码。
- 不新增功能。
- 不接 AI / Figma。
- 不接 MySQL / Redis / RabbitMQ。
- 不做 Playwright 视觉回归。
- 不把集成 smoke 变成功能开发任务。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day6-integration-smoke.md`
- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`
- `tests/smoke/README.md`
- 当前任务相关 Worker / 后端 / 前端入口说明

## 建议修改文件

- 原则上不修改业务代码。
- 如需要记录 smoke 结果，可输出给文档线程，由 Day 7 更新文档。

## 验收标准

建议执行：

```bash
python -m unittest worker.test_layout_validator
python -m unittest worker.test_layout_static_generator
mvn test
npm run build
```

如 `mvn test` 暂时受环境影响，记录原因，并至少尝试：

```bash
mvn package
```

集成链路需验证：

- generated-page artifact 可生成。
- PUT / GET 可用。
- 前端代码展示可用。
- iframe sandbox 预览可用。
- 失败项均有记录和归属线程。

## Codex 执行要求

先输出计划，等待确认后再执行 smoke。发现问题只记录问题、命令、结果和建议归属线程，不直接扩展修复范围。
