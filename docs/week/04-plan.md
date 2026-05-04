# Week 04 计划：Layout JSON 静态编译器 v0.1 与安全预览闭环

## Week 04 总目标

Week 04 的目标是把一份已通过校验的 Layout JSON v0.1，通过确定性规则编译生成 `htmlCode + cssCode`，保存为 `generated-page` artifact，并在前端 `iframe sandbox` 中安全预览。

这里的“生成”不是 AI 生成，而是规则编译。

## Week 04 主链路

```text
Layout JSON v0.1
-> Worker layout_validator.py 校验
-> Worker layout_static_generator.py 静态编译
-> generated-page artifact
-> 后端 mock 文件保存 / 查询
-> 前端展示 HTML / CSS / Vue 文本
-> 前端 iframe sandbox 安全预览
-> 集成 smoke
-> Week 04 总结
```

## P0 / P1 / P2 边界

### P0：必须完成

- `generated-page` artifact 契约。
- Layout JSON 到 HTML / CSS 的基础映射规则。
- Worker 静态编译器 v0.1。
- Worker 静态编译器测试。
- 后端 `generated-page` artifact PUT / GET mock 接口。
- 后端 generated-page 最小测试。
- 前端 GeneratedPageViewer 基础页面。
- `iframe sandbox=""` 安全预览。
- Week 04 集成 smoke。
- Week 04 收口总结。

### P1：尽量完成

- `vueCode` 文本展示。
- HTML / CSS / Vue 三个 tab 展示。
- `warnings` 展示。
- `unsupportedNodes` 展示。
- `layoutHash` / `source` 信息展示。

### P2：本周不做或需另行确认

- `vueCode` 真正可运行。
- Playwright 视觉回归。
- ZIP 导出。
- 自动调用 Worker。
- MySQL 持久化。
- Figma 导入。
- AI 生成。
- Redis / RabbitMQ 异步链路。
- 拖拽编辑器或在线编辑器。

## Week 04 禁止事项

- 不接真实 AI。
- 不接 OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis。
- 不接 RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做真实截图解析。
- 不做登录注册。
- 不做复杂权限。
- 不要求 `vueCode` 真正可运行。
- 不做 Playwright 视觉回归。

## 每日安排概要

| Day | 线程 | 任务卡 | 目标 |
|---|---|---|---|
| Day 1 | 文档线程 | `docs/tasks/week04-day1-generated-page-contract.md` | 定稿 generated-page 契约、映射规则和安全规则 |
| Day 2 | Worker 线程 | `docs/tasks/week04-day2-worker-static-generator.md` | 实现 Worker 静态编译器 |
| Day 3 | Worker 测试线程 | `docs/tasks/week04-day3-worker-generator-tests.md` | 补 Worker 编译器测试 |
| Day 4A | 后端线程 | `docs/tasks/week04-day4-backend-generated-artifact-api.md` | 实现 generated-page mock 保存 / 查询接口 |
| Day 4B | 后端测试线程 | `docs/tasks/week04-day4-backend-generated-artifact-test.md` | 补后端 generated-page 接口测试 |
| Day 5 | 前端线程 | `docs/tasks/week04-day5-frontend-generated-preview.md` | 实现 generated-page 代码展示和 iframe 预览 |
| Day 6 | 测试线程 | `docs/tasks/week04-day6-integration-smoke.md` | 执行 Worker + 后端 + 前端集成 smoke |
| Day 7 | 文档 / 总结线程 | `docs/tasks/week04-day7-summary.md` | 更新状态、总结和 smoke 文档 |

## 线程拆分原则

- 文档线程只改文档，不改业务代码。
- Worker 线程只改 `worker/` 静态编译器相关文件。
- Worker 测试线程只改 Worker 测试。
- 后端线程只改 generated-page artifact API。
- 后端测试线程只改后端测试。
- 前端线程只改 generated-page 预览页面、组件和 API 调用。
- 测试线程只执行验证、记录问题，不直接修复。
- 总结线程只记录已给出的结果，不编造测试结论。

## 验收总标准

- Worker 复用 `worker/layout_validator.py`，不重写校验逻辑。
- validator 失败时，CLI 输出 `status=FAILED` 的 artifact，`htmlCode/cssCode` 为空字符串，退出码为 1。
- `generated-page` artifact 字段清晰，`artifactType` 固定为 `generated-page`。
- 后端 PUT 请求提交完整 `generated-page` artifact。
- 后端 jobId 使用白名单校验：只允许字母、数字、下划线、短横线。
- 后端 generated-page artifact JSON 文件大小限制建议为 2MB。
- 前端 iframe 必须使用 `sandbox=""`，不加 `allow-scripts`。
- 产物不允许 `script` 标签、内联事件或 `javascript:` URL。
- `vueCode` 只展示文本，不要求可运行。
- Day 6 集成 smoke 只验收和记录问题，不变成功能开发任务。

## 相关文档入口

- 当前阶段上下文：`docs/context/current-phase.md`
- generated-page artifact 契约：`docs/generated-page-artifact-design.md`
- Layout JSON 到 HTML / CSS 映射：`docs/layout-to-html-mapping.md`
- Week 04 单任务卡：`docs/tasks/week04-*.md`
- Week 04 状态看板：`docs/week/04-status.md`（Day 7 创建或更新）
- Week 04 总结：`docs/week/04-summary.md`（Day 7 创建或更新）
