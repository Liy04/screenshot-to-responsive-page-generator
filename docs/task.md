# Task

## 当前任务

Week 04 Day 7：Week 04 文档收口与最终验收。

线程：文档 / 总结线程。

## 任务目标

整理 Week 04 完成情况，更新当前文档，记录 smoke 结果、风险和下一步建议，为 Week 04 收口和后续 Week 05 计划做准备。

## Day 7 收口目标

- 记录 Week 04 主链路完成情况。
- 记录 Day 6 集成 smoke 结果。
- 明确 Week 04 建议通过。
- 保留当前阶段限制：确定性静态编译器，不是真实 AI 生成，不接数据库和队列。
- 给出 Week 05 候选方向，但不替用户做最终决策。

## 必须完成

- 更新 `docs/current.md` 中当前阶段状态。
- 更新 `docs/plan.md` 中 Week 04 完成情况。
- 更新 `docs/task.md` 为 Day 7 收口任务。
- 如需要，更新 `docs/INDEX.md` 的文档入口说明。
- 记录 Day 2 到 Day 6 完成内容。
- 记录 Day 6 集成 smoke 结果。
- 记录已知风险和待确认事项。
- 明确 Week 04 是否建议通过。
- 给出 Week 05 下一步建议。

## 禁止事项

- 不修改 frontend/。
- 不修改 backend/。
- 不修改 worker/。
- 不新增业务功能。
- 不新增依赖。
- 不接 AI / Figma / MySQL / Redis / RabbitMQ。
- 不创建 Entity / Mapper。
- 不做 ZIP / 编辑器 / Playwright 视觉回归。

## 建议读取文件

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/task.md`
- `docs/spec.md`
- 必要时查看 Git 改动清单

## 建议修改文件

- `docs/current.md`
- `docs/plan.md`
- `docs/task.md`
- 如确有必要：`docs/INDEX.md`

## 验收标准

- Week 04 完成内容记录清楚。
- Day 6 smoke 结果记录清楚。
- 风险和待确认事项记录清楚。
- 下一步建议清楚。
- Week 04 完成判断明确。
- 未把 Playwright 视觉回归写成已完成。
- 未把本地 mock 写成数据库持久化。
- 未把规则编译写成真实 AI 生成。
- 未修改 frontend/、backend/、worker/。

## 输出要求

完成后按以下结构汇报：

```text
# Week 04 Day 7 文档收口结果

## 修改文件
## 主要更新
## Day 6 smoke 记录
## Week 04 完成判断
## 风险 / 待确认事项
## Week 05 建议
## 是否修改业务代码
```

## Day 6 smoke 记录

- Worker smoke 通过。
- 后端 PUT / GET / 404 / 400 通过。
- 前端 build 通过。
- 前端页面联调通过。
- iframe 使用 `sandbox=""`，且无 `allow-scripts`。
- 未做 Playwright 视觉回归，符合当前限制。
- 无残留后台服务。

## 风险 / 待确认事项

- 详情页旧 Week 02 generation 查询失败时，会显示“加载失败 / 任务不存在”，但 Week 04 generated-page 区域仍可正常展示；这是 UX / 联调口径待确认项。
- `backend/target`、`frontend/dist` 是构建副产物，按忽略规则处理。
- `backend/mock-data` 是本地 mock 副产物，按忽略规则处理。
- 当前 generated-page 保存仍是本地 mock 文件，不是数据库持久化。
- 当前 Layout JSON 仍来自手写 / 示例，不是真实截图解析。
- 当前静态编译器是规则编译，不是真实 AI 生成。

## 下一步建议

- 方向 A：修正前端详情页 UX，让 generated-page dev 预览不依赖 Week 02 generation job。
- 方向 B：补后端 / 前端更稳定的自动化测试。
- 方向 C：增强静态编译器支持更多 Layout JSON 节点和 style subset。
- 方向 D：如用户确认，再规划 MySQL 持久化；当前不直接进入。

## Codex 执行要求

先输出文档收口计划，等待确认后再修改文档。完成后输出修改文件、主要内容、风险和是否建议 Week 04 通过。
