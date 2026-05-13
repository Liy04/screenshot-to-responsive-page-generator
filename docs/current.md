# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、当天对应的 `docs/tasks/day-xx.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 09 已完成收口：真实 AI 最小接入，打通单张真实图片到 Layout JSON / generated-page 预览的最小闭环。

## 阶段背景

Week 08 已完成收口。Week 09 已完成真实主链路最小闭环，已经验证单张真实图片可以接入后端、Python Worker、真实多模态模型、Layout JSON validator、generated-page HTML compiler 和前端 iframe 预览。

Week 09 目标链路：

```text
单张真实图片
-> 后端保存临时文件
-> 后端创建 jobId
-> 后端调用 Python Worker
-> Worker 读取真实图片
-> Worker 调用真实多模态模型
-> 模型输出简化结构
-> Worker 映射到 Layout JSON v0.1
-> validator 校验
-> fallback rule resolver 保底
-> compiler 输出 generated.html
-> 后端返回 layoutJson + previewHtml
-> 前端展示原图、Layout JSON 和 iframe 预览
```

## 当前完成内容

1. Week 08 已完成收口。
2. Week 08 summary、smoke 和 report material 已归档。
3. Week 09 已完成真实 AI 最小闭环：
   `真实图片 -> 后端上传 -> 后端调用 Python Worker -> Worker 调 SiliconFlow Qwen3-VL -> REAL_AI 命中 -> Layout JSON v0.1 -> previewHtml -> 前端 iframe 预览`。
4. 最终关键通过结果已确认：
   `status=SUCCESS`、`mode=real-ai`、`fallbackUsed=false`、`sourceType=REAL_AI`、`layoutJson.version=0.1`、`validation.ok=true`、`previewHtml` 非空、iframe 渲染成功、`sandbox=""`、无 `allow-scripts`。
5. 已确认 REAL_AI 命中依赖运行配置：Python 3.11.9、`D:\environment\python11\python.exe`、`IMAGEPAGE_WORKER_PYTHON_COMMAND`、后端 `--imagepage.worker.timeout-seconds=120` 和 SiliconFlow `OPENAI_*` 环境变量。
6. Week 09 的 summary、dev smoke 和原始计划已进入 `docs/archive/week/` 归档。

## 当前不做

- 不接 Figma API / MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做 Playwright 视觉回归。
- 不做多页面。
- 不做批量任务。
- 不做登录注册。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。

## 当前允许

- 允许真实图片上传。
- 允许后端调用 Python Worker。
- 允许 Worker 读取真实图片。
- 允许 Worker 调用真实 AI。
- 允许 fallback rule resolver 保底。
- 允许前端展示原图、Layout JSON 和 iframe 预览。

## 当前待补

- Week 10 规划与任务拆分。
- 如继续推进真实链路质量，可补更稳定的页面级验收和生成结果一致性策略。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- context-scout 流程：`docs/playbooks/context-scout.md`
- Week 09 归档：`docs/archive/week/09-plan.md`、`docs/archive/week/09-summary.md`、`docs/archive/week/09-dev-smoke.md`
- 历史归档：`docs/archive/`

## 当前状态说明

Week 09 已完成收口，项目已经进入“可提交 / 可归档 / 可进入下一周规划”的状态。

真实 AI 后端链路已稳定命中过一次 `REAL_AI` 成功结果；当前最重要的运行前提是不要遗漏 Python 3.11、Worker 路径、120 秒 timeout 和 `OPENAI_*` 环境变量。

Week 09 的临时 `docs/tasks/day-*.md` 已按收口规则清理，`docs/tasks/` 目录保留为空目录，等待下一周重新生成任务卡。

下一步准备进入 Week 10 规划，但本文件不展开新的长计划。
