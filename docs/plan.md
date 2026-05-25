# Plan

## 当前阶段

Week 14：MVP 产品化交付闭环。

Week 09~13 已证明：

```text
真实图片
-> 真实 AI 识别视觉清单
-> Worker 映射 Layout JSON v0.1
-> static generator 编译 previewHtml
-> 前端 sandbox iframe 预览
```

Week 14 不继续做单纯输出质量增强，而是让这条链路更像一个用户可操作、可演示、可交付的 MVP。

## Week 14 类型

```text
产品化周 / MVP 交付周
```

不是：

```text
质量增强周
数据库周
Figma 周
编辑器周
复杂导出周
```

## Week 14 总目标

把当前 dev 链路升级为最小产品交付闭环：

1. 用户上传截图。
2. 用户触发生成。
3. 用户看到生成状态。
4. 用户看到原图 / 生成结果对比。
5. 用户看到 Layout JSON 和 previewHtml。
6. 用户可以复制 HTML / CSS。
7. 用户可以下载最小生成文件。
8. 用户能理解 REAL_AI / FALLBACK / FAILED。
9. 项目有一条可复现的 MVP smoke。

## Week 14 P0

### P0-1：产品化生成结果区

将 `/dev/image-to-layout` 的生成结果区域从“调试信息堆叠”调整为更清晰的 MVP 展示结构：

```text
生成状态
-> 原图 / 生成预览
-> 交付操作
-> Layout JSON / previewHtml 调试信息
```

要求：

- 保留现有真实 AI 信息。
- 保留 fallback / failed 可读说明。
- 保留 iframe `sandbox=""`。
- 不加入 `allow-scripts`。

### P0-2：HTML / CSS 复制

提供最小复制入口：

- 复制 HTML。
- 复制 CSS。
- 复制完整 HTML 文档。

说明：

- 复制内容来自 Worker 静态编译结果。
- 不复制模型原始输出。
- 复制失败要有用户可读提示。

### P0-3：最小下载能力

提供最小下载能力：

- 下载 `index.html`。
- 可选下载 `style.css`。
- 或优先下载单个完整 HTML 文件。

说明：

- Week 14 不做复杂 ZIP。
- 不做项目模板导出。
- 不做 Vue SFC 可运行化。

### P0-4：MVP smoke

形成一条 Week 14 MVP smoke：

```text
上传 sample
-> generate
-> REAL_AI 或 FALLBACK 状态可读
-> iframe 可预览
-> 复制 HTML / CSS
-> 下载文件
-> 检查 sandbox
-> 检查无真实 key 泄漏
```

## Week 14 P1

### P1-1：结果页文案收口

让页面说明更适合演示：

- 当前生成是否来自 REAL_AI。
- 是否使用 fallback。
- 生成结果能做什么。
- 用户下一步可以复制或下载。

### P1-2：交付 artifact 口径整理

必要时在 `docs/spec.md` 补充 Week 14 交付口径：

- previewHtml。
- htmlCode / cssCode 当前如何获得。
- download artifact 当前是否只在前端组合。
- 哪些字段是调试字段。

## Week 14 暂不做

- 不接 MySQL。
- 不创建 Entity / Mapper。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做复杂 ZIP 导出。
- 不做 Vue SFC 可运行化。
- 不做多页面生成。
- 不做登录注册 / 权限。
- 不做 Playwright 视觉回归系统。
- 不升级 Layout JSON v0.2。

## Week 14 Day 建议

| Day | 角色 | 目标 |
|---|---|---|
| Day 1 | docs-agent -> reviewer-agent -> lead | 生成 Week 14 day 卡，明确 MVP 产品化范围和验收标准 |
| Day 2 | frontend-agent -> tester-agent -> reviewer-agent -> lead | 重组 `/dev/image-to-layout` 结果区，使演示路径更清晰 |
| Day 3 | frontend-agent -> tester-agent -> reviewer-agent -> lead | 增加 HTML / CSS / 完整 HTML 复制入口 |
| Day 4 | frontend-agent -> tester-agent -> reviewer-agent -> lead | 增加最小下载能力，优先单文件 HTML |
| Day 5 | frontend-agent -> tester-agent -> reviewer-agent -> lead | 优化 REAL_AI / FALLBACK / FAILED 用户可读状态和交付提示 |
| Day 6 | tester-agent -> reviewer-agent -> docs-agent -> lead | 执行 Week 14 MVP smoke，记录复制、下载、iframe、安全检查 |
| Day 7 | lead -> docs-agent -> reviewer-agent | Week 14 收口，判断 MVP 产品化闭环是否通过 |

## Week 14 验收标准

- 用户能完成上传和生成。
- 用户能看到原图 / iframe 对比。
- 用户能复制 HTML。
- 用户能复制 CSS 或完整 HTML。
- 用户能下载最小生成文件。
- REAL_AI / FALLBACK / FAILED 状态清楚。
- iframe 仍为 `sandbox=""`。
- 不出现 `allow-scripts`。
- 不提交真实 API key。
- 不提交 `backend/storage/`、`frontend/dist/` 或下载副产物。
- 不新增 MySQL / Figma / 编辑器 / ZIP 复杂实现。

## PRD 对齐检查

Week 14 推动 MVP 主线。

原因：

- 过去几周已经证明真实 AI 和质量增强可行。
- 当前 MVP 缺口是用户交付动作，而不是继续模型细节优化。
- 复制 / 下载 / 演示页能让项目从“能生成”变成“能交付”。

## 下一步

由 docs-agent 生成 Week 14 Day 1~Day 7 任务卡。

Day 卡生成后，由 Lead 验收任务拆分，再进入 Day 2 前端产品化实现。
