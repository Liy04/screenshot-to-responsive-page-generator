# Current Phase

## 文件目的

本文档记录当前阶段的轻量上下文。Codex 执行日常任务时，默认读取 `AGENTS.md`、本文档、当前任务卡和相关代码即可。

完整 PRD、完整周计划、历史状态和全部 skills 只在任务卡明确要求，或任务确实必须参考时读取。

## 当前阶段

Week 03 Layout JSON v0.1 稳定落地。

## 当前目标

当前目标是跑通 Layout JSON v0.1 的 P0 验证链路：

```text
手写 Layout JSON -> Schema 校验 -> 业务规则校验 -> 示例验证
```

Week 02 已完成上传截图、创建任务、查询状态、查看 mock 结果。Worker 仅 smoke，不参与真实生成。

## 当前禁止

- 不接真实 AI。
- 不接 OpenAI / Claude / 其它模型 API。
- 不接 Figma API。
- 不接 Figma MCP。
- 不接 Redis。
- 不接 RabbitMQ。
- 不接 MySQL 实际落库。
- 不创建数据库表。
- 不新增 Entity / Mapper。
- 不新增数据库配置。
- 不做真实截图解析。
- 不做 Vue 页面代码生成。
- 不做导出 ZIP。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做登录注册。
- 不做历史记录持久化。
- 不做复杂权限系统。

## 当前推荐实现

- Layout JSON 使用手写示例。
- Schema 放在 `schema/layout.schema.json`。
- 示例放在 `examples/valid` 和 `examples/invalid`。
- Worker 只做本地 Layout JSON 校验器。
- 后端 / 前端 mock 保存与查看仅作为 P1。

## 当前执行方式

日常开发任务以 `docs/tasks/` 下的单任务卡为准。

任务卡会说明：

- 本次任务目标。
- 必须完成的内容。
- 禁止事项。
- 建议读取文件。
- 建议修改文件。
- 验收标准。
- Codex 执行要求。

除非任务卡明确要求，不要默认读取完整 PRD、完整周计划、全部历史状态和全部 skills。
