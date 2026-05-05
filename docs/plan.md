# Plan

## Week 04 名称

Layout JSON 静态编译器 v0.1 与安全预览闭环。

## 本周目标

把一份已通过校验的 Layout JSON v0.1，通过确定性规则编译生成 `htmlCode + cssCode`，保存为 `generated-page` artifact，并在前端 `iframe sandbox` 中安全预览。

这里的“生成”不是 AI 生成，而是规则编译。

## 主链路

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

## P0：必须完成

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

## P1：尽量完成

- `vueCode` 文本展示。
- HTML / CSS / Vue 三个 tab 展示。
- `warnings` 展示。
- `unsupportedNodes` 展示。
- `layoutHash` / `source` 信息展示。

## P2：本周不做或需另行确认

- `vueCode` 真正可运行。
- Playwright 视觉回归。
- ZIP 导出。
- 自动调用 Worker。
- MySQL 持久化。
- Figma 导入。
- AI 生成。
- Redis / RabbitMQ 异步链路。
- 拖拽编辑器或在线编辑器。

## 当前推进顺序

| Day | 线程 | 目标 |
|---|---|---|
| Day 1 | 文档线程 | 定稿 generated-page 契约、映射规则和安全规则 |
| Day 2 | Worker 线程 | 实现 Worker 静态编译器 |
| Day 3 | Worker 测试线程 | 补 Worker 编译器测试 |
| Day 4A | 后端线程 | 实现 generated-page mock 保存 / 查询接口 |
| Day 4B | 后端测试线程 | 补后端 generated-page 接口测试 |
| Day 5 | 前端线程 | 实现 generated-page 代码展示和 iframe 预览 |
| Day 6 | 测试线程 | 执行 Worker + 后端 + 前端集成 smoke |
| Day 7 | 文档 / 总结线程 | 更新状态、总结和 smoke 文档 |

当前唯一任务卡见 `docs/task.md`。

## 验收总标准

- Worker 复用 `worker/layout_validator.py`，不重写校验逻辑。
- validator 失败时，CLI 输出 `status=FAILED` artifact，`htmlCode/cssCode/vueCode` 为空字符串，退出码为 1。
- `generated-page` artifact 字段清晰，`artifactType` 固定为 `generated-page`。
- 后端 PUT 请求提交完整 `generated-page` artifact。
- 后端 jobId 使用白名单校验：只允许字母、数字、下划线、短横线。
- 前端 iframe 必须使用 `sandbox=""`，不加 `allow-scripts`。
- 产物不允许 `script` 标签、内联事件或 `javascript:` URL。
- `vueCode` 只展示文本，不要求可运行。
- Day 6 集成 smoke 只验收和记录问题，不变成功能开发任务。
