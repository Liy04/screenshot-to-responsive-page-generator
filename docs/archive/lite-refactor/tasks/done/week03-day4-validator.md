# Week 03 Day 4：Worker Layout JSON 校验器

## 任务目标

只完成 `worker/layout_validator.py` 和 `worker/test_layout_validator.py`。

## 必须完成

- 支持 Schema 校验。
- 支持业务规则校验：
  - 节点 id 唯一。
  - layout 根节点 type 为 `page`。
  - `responsive.rules.target` 存在于 layout 节点中。
  - text 节点必须有 `content`。
  - button 节点必须有 `content`。
- 命令行支持校验单个 Layout JSON 文件。
- 输出清晰的通过 / 失败、errors、warnings。

## 禁止事项

- 不改后端、前端业务代码。
- 不接真实 AI、模型 API、Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL，不新增 Entity / Mapper。
- 不做真实截图解析。
- 不做 Vue 页面代码生成。
- 不安装依赖；如确需依赖，必须先说明原因并等待确认。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week03-day4-validator.md`
- `docs/layout-schema-design.md`
- `schema/layout.schema.json`
- `examples/valid/`
- `examples/invalid/`
- `worker/README.md`
- 当前任务相关 worker 代码

## 建议修改文件

- `worker/layout_validator.py`
- `worker/test_layout_validator.py`
- `docs/week/03-status.md`，仅在状态需要同步时修改

## 验收标准

- 合法示例校验通过。
- 缺少 version 校验失败。
- node type 不合法校验失败。
- 节点 id 重复校验失败。
- responsive target 不存在校验失败。
- text / button 节点缺 content 校验失败。

## Codex 执行要求

- 先输出计划，等待确认后再编码。
- 默认不新增依赖。
- 编码后执行最小测试。
- 不修改前端、后端业务代码。
