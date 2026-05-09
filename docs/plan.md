# Plan

## Week 06 名称

Generated Page 回归稳定性与演示验收增强（已完成）。

## 本周目标

Week 06 的目标是围绕已完成的 generated-page 闭环，继续增强稳定性、测试覆盖和演示能力，让项目更好验收、更好复现、更好写进实践报告。

Week 06 已完成收口，不扩大到真实 AI、Figma 或数据库。

## 本周完成情况

| Day | 线程 | 目标 | 状态 |
|---|---|---|---|
| Day 1 | 文档线程 | 文档计划与任务边界 | 完成 |
| Day 2 | 前端线程 | 前端 preview 基础测试 | 完成 |
| Day 3 | Worker 线程 | Worker 小范围增强 | 完成 |
| Day 4 | Worker 测试线程 | Worker 回归测试 | 完成 |
| Day 5 | 后端测试线程 | 后端 artifact 边界测试 | 完成 |
| Day 6 | 文档线程 | smoke 文档与实践报告素材 | 完成 |
| Day 7 | 文档 / 总结线程 | 总体验收、归档、提交 | 完成 |

## Week 06 验收结果

- Worker unittest 通过，35 tests OK。
- 后端 `mvn test` 通过，10 tests OK。
- 前端 `npm run test` 通过，4 tests OK。
- 前端 `npm run build` 通过。
- Week 06 smoke 文档和实践报告素材已归档。
- 未接真实 AI、Figma、MySQL、Redis / RabbitMQ。

## 本周不做

- 不接真实 AI / OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器 / 在线编辑器。
- 不做真实截图解析。
- 不做登录注册 / 复杂权限。
- 不做 Playwright 视觉回归，除非用户明确批准。
- 不做复杂响应式布局算法。
- 不做 Tailwind 代码生成。
- 不做 Vue SFC 可运行化。

## Week 07 候选方向

1. 图片输入到 Layout JSON 的 mock / 半自动链路。
2. 继续增强前端演示体验和测试覆盖。
3. 继续增强 Worker 节点和安全 style subset。
4. 如用户明确批准，再规划 MySQL 持久化。
5. 整理实践报告中的系统实现和测试章节。

## 当前约定

- Worker 测试命令使用 `unittest`。
- Windows 上传命令优先使用 `curl.exe`。
- 前端日常 smoke 使用 `npm run dev`。
- 后端默认启动方式使用 `java -jar`。
- Week 06 原始长计划已归档到 `docs/archive/week/06-plan.md`。
- Week 06 smoke 文档已归档到 `docs/archive/week/06-dev-smoke.md`。
- Week 06 实践报告素材已归档到 `docs/archive/week/06-report-material.md`。
- 周任务执行完后，应将阶段计划、smoke 文档和总结移动到 `docs/archive/week/`，保持 `docs/` 根目录轻量。

当前唯一任务卡见 `docs/task.md`。
