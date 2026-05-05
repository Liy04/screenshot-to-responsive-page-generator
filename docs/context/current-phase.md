# Current Phase

## 文件目的

本文档记录当前阶段的轻量上下文。Codex 执行日常任务时，默认读取 `AGENTS.md`、本文档、`docs/tasks/active/` 下的当前任务卡和相关代码即可。

完整 PRD、完整周计划、历史状态和全部 skills 只在任务卡明确要求，或任务确实必须参考时读取。

## 当前阶段

Week 04 Layout JSON 静态编译器 v0.1 与安全预览闭环。

## 当前目标

当前目标是跑通 Layout JSON v0.1 到静态预览产物的确定性规则编译链路：

```text
Layout JSON v0.1
-> Worker 校验
-> Worker 静态编译 htmlCode / cssCode
-> generated-page artifact
-> 后端 mock 保存 / 查询
-> 前端 iframe sandbox 安全预览
```

这里的“生成”不是 AI 生成，而是基于 Layout JSON 的规则编译。

## 当前禁止

- 不接真实 AI。
- 不接 OpenAI / Claude / Gemini SDK。
- 不接 Figma API。
- 不接 Figma MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不新增 Entity / Mapper。
- 不新增数据库配置。
- 不接 Redis。
- 不接 RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做真实截图解析。
- 不做登录注册。
- 不做历史记录持久化。
- 不做复杂权限系统。
- 不要求 `vueCode` 真正可运行。
- 不做 Playwright 视觉回归。

## 当前推荐实现

- Worker 使用 Python 标准库实现静态编译器。
- Worker 必须复用 `worker/layout_validator.py`，不另写一套校验逻辑。
- Worker 输入已通过 Layout JSON v0.1 校验约束。
- Worker 输出 `generated-page` artifact，核心字段为 `htmlCode`、`cssCode`、`vueCode`、`validation`、`warnings`、`unsupportedNodes`。
- 后端继续使用 `backend/mock-data/` 本地 mock 文件保存 / 查询。
- 后端不连接 MySQL，不创建 Entity / Mapper。
- 前端使用 `iframe sandbox=""` 预览 `htmlCode + cssCode`。
- `vueCode` 只作为文本展示，不要求可运行，不要求构建。

## 当前执行方式

日常开发任务以 `docs/tasks/active/` 下的单任务卡为准。

任务卡会说明：

- 本次任务目标。
- 必须完成的内容。
- 禁止事项。
- 建议读取文件。
- 建议修改文件。
- 验收标准。
- Codex 执行要求。

除非任务卡明确要求，不要默认读取完整 PRD、完整周计划、全部历史状态和全部 skills。

## 当前活跃文档入口

- 文档总索引：`docs/INDEX.md`
- 当前周计划：`docs/plans/week-04.md`
- 当前任务卡：`docs/tasks/active/week04-*.md`
- generated-page artifact 契约：`docs/specs/generated-page-artifact-v0.1.md`
- Layout JSON 到 HTML / CSS 映射：`docs/specs/layout-to-html-v0.1.md`
- Layout JSON v0.1 设计：`docs/specs/layout-json-v0.1.md`
- Layout API 契约：`docs/specs/layout-api-contracts.md`
- context-scout 流程：`docs/playbooks/context-scout.md`
- 当前提示词模板：`docs/prompts/current.md`
- 架构决策记录：`docs/decisions/ADR-*.md`
