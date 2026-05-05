# Week 04 Day 2：Worker 静态编译器

## 任务目标

线程：Worker 线程。

实现 `worker/layout_static_generator.py`，将已通过校验的 Layout JSON v0.1 编译为 `generated-page` artifact。

## 必须完成

- 实现 `worker/layout_static_generator.py`。
- 必须复用 `worker/layout_validator.py`。
- 不允许重写一套校验逻辑。
- 输出 `htmlCode` 和 `cssCode`。
- `vueCode` 只作为文本输出，不要求可运行。
- 输出 `artifactType=generated-page`。
- 输出 `generator.name=layout-static-generator`。
- 生成稳定 `source.layoutHash`。
- validator 失败时输出 `status=FAILED` artifact，`htmlCode/cssCode` 为空字符串，退出码为 1。
- 使用 Python 标准库，不新增依赖。

## 禁止事项

- 不新增第三方依赖。
- 不调用后端接口。
- 不接模型 API。
- 不接 Figma API / Figma MCP。
- 不接数据库。
- 不处理真实截图。
- 不修改前端或后端代码。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day2-worker-static-generator.md`
- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`
- `worker/layout_validator.py`
- `schema/layout.schema.json`
- `examples/valid/*.layout.json`
- `examples/invalid/*.layout.json`

## 建议修改文件

- `worker/layout_static_generator.py`

## 验收标准

- valid Layout JSON 可以生成 `status=SUCCESS` artifact。
- invalid Layout JSON 生成 `status=FAILED` artifact，退出码为 1。
- 生成结果不包含 `script` 标签、内联事件或 `javascript:` URL。
- 未知 style 字段进入 warnings。
- image 缺少安全 src 时进入 warnings。

## Codex 执行要求

先输出计划，等待确认后再编码。修改完成后执行最小验证；如验证无法执行，说明原因。
