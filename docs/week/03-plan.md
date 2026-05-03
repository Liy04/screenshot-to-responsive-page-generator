# Week 03 计划：Layout JSON v0.1 稳定落地

## 1. Week 03 主题

第三周主题：**稳定定义 Layout JSON v0.1，并用 Schema、示例和校验器证明它可用。**

Week 02 已完成上传截图、创建任务、查询状态、查看 mock 结果。Worker 仅 smoke，不参与真实生成。

## 2. 本周目标

本周只围绕 Layout JSON v0.1 稳定落地推进：

```text
手写 Layout JSON -> Schema 校验 -> 业务规则校验 -> 示例验证
```

P0 目标是把结构规则、示例和校验器做稳。后端 mock 保存、mock 查询和前端基础查看只作为 P1，在 P0 全部完成后再考虑。

## 3. 本周不做事项

- 不接真实 AI。
- 不接 OpenAI / Claude / Gemini 等模型 API。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL 实际落库。
- 不执行建表。
- 不新增 Entity / Mapper。
- 不新增数据库配置。
- 不做 JMeter 压测。
- 不做真实截图解析。
- 不做 Layout JSON 到 Vue 页面代码生成。
- 不做拖拽编辑器、在线编辑器或导出 ZIP。

## 4. 技术决策摘要

- Layout JSON 设计说明以 `docs/layout-schema-design.md` 为准。
- P1 mock 接口以 `docs/layout-api-contracts.md` 为准。
- 后续数据库草案以 `docs/database-artifact-draft.md` 为准，Week 03 不执行。
- 实际执行以 `docs/tasks/week03-*.md` 单任务卡为准。
- 实际进度以 `docs/week/03-status.md` 为准。

## 5. P0 / P1 / P2 范围

### P0：必须完成

- Layout JSON 设计文档。
- `schema/layout.schema.json`。
- `examples/valid/` 下 5 个合法示例。
- `examples/invalid/` 下 3 个非法示例。
- `worker/layout_validator.py`。
- `worker/test_layout_validator.py`。

### P1：P0 完成后可选

- 本地文件 mock 保存 Layout JSON。
- 本地文件 mock 查询 Layout JSON。
- 前端基础 Layout JSON 查看页。
- 展示校验状态和错误信息。

### P2：暂缓，需另行确认

- MySQL 实际落库。
- generation_artifact Entity / Mapper。
- Redis。
- RabbitMQ。
- JMeter。
- 真实 AI 生成 Layout JSON。
- Layout JSON 生成 Vue 页面。
- 拖拽编辑器、在线编辑器、导出 ZIP。

## 6. 每日任务表

| Day | 主题 | 范围 | 验收标准 |
|---|---|---|---|
| Day 1 | Layout JSON 设计文档 | 只做 `docs/layout-schema-design.md` | 说明中间层、字段、节点类型、限制和扩展方向 |
| Day 2 | JSON Schema | 只做 `schema/layout.schema.json` | 约束顶层字段、节点类型、children 数组 |
| Day 3 | 示例文件 | 只做 `examples/valid` 和 `examples/invalid` | 5 个合法示例、3 个非法示例 |
| Day 4 | Worker 校验器 | 只做 `worker/layout_validator.py` 和测试 | 支持 Schema 校验和基础业务规则校验 |
| Day 5 | 校验器修复与 smoke | 只做校验器测试、修复和 smoke | valid 通过，invalid 失败且错误清晰 |
| Day 6 | P1 mock / 查看 | P0 完成后才做 mock 保存 / 查询 / 前端基础查看 | 不接数据库，不新增 Entity / Mapper |
| Day 7 | 验收收口 | 只做验收、文档收口和总结 | `docs/week/03-summary.md` 填写准确 |

## 7. 交付物

```text
docs/
  context/current-phase.md
  layout-schema-design.md
  layout-api-contracts.md
  database-artifact-draft.md
  week/03-plan.md
  week/03-status.md
  week/03-summary.md
  tasks/week03-day1-layout-design.md
  tasks/week03-day2-schema.md
  tasks/week03-day3-examples.md
  tasks/week03-day4-validator.md
  tasks/week03-day5-validator-fix-and-smoke.md
  tasks/week03-day6-optional-mock-viewer.md
  tasks/week03-day7-smoke-and-summary.md

schema/
  layout.schema.json

examples/
  valid/
  invalid/
```

## 8. 验收标准

- `docs/layout-schema-design.md` 存在且结构清晰。
- `schema/layout.schema.json` 存在。
- 5 个合法示例和 3 个非法示例存在。
- Worker 校验器能检查 Schema 规则和业务规则。
- Day 5 smoke 能证明合法示例通过、非法示例失败。
- P1 如执行，只能使用本地文件 mock 或前端基础查看。
- 未接入真实 AI、Figma、Redis、RabbitMQ、MySQL。
- 未新增 Entity / Mapper / 数据库配置。
- 未实现 Vue 页面代码生成、拖拽编辑器、在线编辑器或导出 ZIP。

## 9. 风险摘要

| 风险 | 表现 | 控制方式 |
|---|---|---|
| 范围膨胀 | 顺手做数据库、AI、Vue 生成 | 每个任务只读 current-phase 和当天任务卡 |
| P1 抢主线 | mock 保存或前端查看提前占用时间 | P0 未完成前不做 P1 |
| 校验不足 | 只做 Schema，不做业务规则 | Day 4 / Day 5 明确业务规则和 smoke |
| 示例不足 | 无法证明校验器有效 | Day 3 必须同时写 valid 和 invalid |
| 文档混乱 | 继续使用长计划当执行入口 | 03-plan 只保留周计划，执行以任务卡为准 |

## 10. 相关文档入口

| 文档 | 职责 |
|---|---|
| `docs/context/current-phase.md` | 当前阶段轻量上下文 |
| `docs/layout-schema-design.md` | Layout JSON v0.1 设计说明 |
| `docs/layout-api-contracts.md` | P1 mock 保存 / 查询接口契约 |
| `docs/database-artifact-draft.md` | 后续数据库设计草案 |
| `docs/tasks/week03-*.md` | Week 03 单任务卡 |
| `docs/week/03-status.md` | Week 03 实际进展 |
| `docs/week/03-summary.md` | Week 03 Day 7 总结 |
| `docs/prompt-templates.md` | 可复制任务提示词 |
