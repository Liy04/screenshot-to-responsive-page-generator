# MVP Roadmap

## 文件目的

本文档是 MVP 长期路线锚点，用于防止按周开发逐渐偏离 PRD。

每次制定新一周计划前，应先阅读本文档，再判断下一周是否推动 MVP 主线。

`docs/archive/` 不参与默认阅读，除非需要历史追溯或验收证据。

## PRD 核心目标

项目目标是构建：

```text
截图 / Figma 设计信息 -> 响应式前端页面代码
```

当前主线优先聚焦截图输入：

```text
真实图片上传
-> 真实 AI 识别页面结构
-> Layout JSON v0.1
-> previewHtml 安全预览
-> 用户可拿走的页面代码 / 文件
```

## MVP 必须完成

MVP 不是只证明 AI 链路能跑通，而是要让用户完成一次最小产品闭环：

1. 用户上传一张页面截图。
2. 系统生成可解释的 Layout JSON。
3. 系统生成安全可预览的 HTML / CSS 页面。
4. 用户能在前端看到原图和生成结果对比。
5. 用户能复制或下载生成结果。
6. 生成结果有清晰状态：REAL_AI / FALLBACK / FAILED。
7. 失败时用户能看到原因，而不是只看到空白。
8. API key 不进入代码、文档、日志、artifact 或 Git。

## 当前已完成

- 真实图片上传。
- 后端保存原图并生成 jobId。
- 后端调用 Python Worker。
- Worker 调用真实多模态模型。
- 当前验证模型：`Qwen/Qwen3-VL-32B-Instruct`。
- AI 输出视觉清单。
- Worker 映射 Layout JSON v0.1。
- Worker 静态编译 `previewHtml`。
- 后端保存 artifact 并支持同 jobId 复用。
- 前端 `/dev/image-to-layout` 展示原图、Layout JSON、previewHtml 和 sandbox iframe。
- Week 13 三张 samples 顺序 smoke 通过，平均分 27.0 / 35。

## MVP 仍缺

当前最关键缺口不是继续无限提高模型质量，而是产品化交付：

1. 生成结果仍主要停留在 dev 页面。
2. 用户还不能方便复制 HTML / CSS。
3. 用户还不能下载生成文件。
4. 缺少面向 MVP 演示的结果页信息架构。
5. 缺少“生成成功后下一步做什么”的产品动作。
6. 缺少轻量的交付记录和验收说明。

## Week 14 主线

Week 14 进入：

```text
MVP 产品化交付闭环
```

目标不是继续做模型质量周，而是把 Week 09~13 已打通的能力包装成用户可理解、可操作、可演示的 MVP 闭环。

Week 14 优先级：

1. 结果页产品化：让 `/dev/image-to-layout` 更像 MVP 演示页，而不是调试页。
2. 代码交付：提供 HTML / CSS 复制入口。
3. 文件交付：提供最小下载能力，优先 HTML / CSS 单文件或分文件。
4. 状态说明：清楚展示 REAL_AI / FALLBACK / FAILED 以及原因。
5. 演示闭环：形成一条可复现的 MVP smoke。

## 暂缓事项

以下内容暂缓，除非用户明确重新立项：

- MySQL 持久化。
- Entity / Mapper / MyBatis-Plus 落库。
- Figma API / Figma MCP。
- 多页面生成。
- 拖拽编辑器。
- 在线编辑器。
- ZIP 复杂导出。
- 登录注册 / 权限。
- 复杂整站截图。
- Playwright 视觉回归系统。
- Layout JSON v0.2 大升级。

## 每周计划验收规则

每次验收新 Week 计划时必须回答：

1. 这周是否推动 MVP 主线？
2. 这周是功能推进周、产品化周、质量周、测试周，还是文档周？
3. 如果是质量周，是否已经连续超过 1 周？
4. 本周交付物是否能被用户感知？
5. 是否新增了偏离 MVP 的技术负担？
6. 是否应该暂停优化，转向产品化交付？

如果计划不能回答这些问题，应先退回修正。

## 当前推荐下一步

进入 Week 14：

```text
产品化生成结果页 + 代码复制 / 下载 + MVP smoke
```

不建议 Week 14 继续单纯优化模型输出质量。
