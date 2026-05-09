# Week 06 Summary

## 一、阶段目标

Week 06 的目标是围绕 generated-page artifact 做回归稳定性与演示验收增强，让当前 generated-page MVP 闭环更稳定、更好测、更好演示，也更适合写入实践报告。

当前项目仍是学习型 MVP，不是真实 AI 生成器。

## 二、完成内容

1. 完成 Docs Lite 的 Week 06 文档拆分和根目录清理。
2. 为 generated-page 独立 preview 页面补充组件级基础测试。
3. 小幅增强 Worker 静态编译器，支持 `maxWidth` 和 `lineHeight`。
4. 补充 Worker 静态编译器和校验器回归测试。
5. 补充后端 generated-page artifact mock 接口边界测试。
6. 整理 Week 06 smoke 文档和实践报告素材。
7. 完成 Week 06 总体验收。

## 三、验证结果

### Worker

```text
python -m unittest worker.test_layout_validator worker.test_layout_static_generator
Ran 35 tests
OK
```

### Backend

```text
mvn test
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

### Frontend

```text
npm run test
Test Files 1 passed
Tests 4 passed
```

```text
npm run build
build success
```

## 四、前端完成情况

- 新增 generated-page preview 组件级基础测试。
- 覆盖 `SUCCESS` 状态展示 iframe。
- 覆盖 `FAILED` 状态不展示 iframe。
- 覆盖 iframe `sandbox=""`，且不包含 `allow-scripts`。
- 覆盖 validation、unsupportedNodes、代码展示、empty/error 状态。
- 使用 Vitest、Vue Test Utils 和 jsdom 做组件级测试。

## 五、Worker 完成情况

- 新增 `maxWidth` 到 `max-width` 的编译支持。
- 新增 `lineHeight` 到 `line-height` 的编译支持。
- 保持未知 style warning。
- 保持不安全 CSS 值 warning。
- 保持 HTML escape、script 禁止、inline event 禁止、javascript URL 禁止。
- 补充 `SUCCESS` / `FAILED`、layoutHash、unsupportedNodes、validator warning 等回归测试。

## 六、后端完成情况

- 补充 generated-page artifact controller 边界测试。
- 覆盖过长 jobId、空 body、array body、empty object、超过 2MB 等边界。
- 保持 PUT / GET 接口路径不变。
- 未修改生产代码。
- 未接 MySQL，未创建 Entity / Mapper。

## 七、文档完成情况

- 归档 Week 05 smoke 文档到 `docs/archive/week/05-dev-smoke.md`。
- 归档 Week 06 原始长计划到 `docs/archive/week/06-plan.md`。
- 归档 Week 06 smoke 文档到 `docs/archive/week/06-dev-smoke.md`。
- 归档 Week 06 实践报告素材到 `docs/archive/week/06-report-material.md`。
- 完成 Week 06 summary 归档。

## 八、安全验证

- iframe 预览继续要求 `sandbox=""`。
- iframe 不允许 `allow-scripts`。
- `status=SUCCESS` 才展示 iframe。
- `status=FAILED` 不展示 iframe。
- Worker 继续禁止 script、inline event 和 javascript URL。
- 不安全 image src 和不安全 CSS 值继续进入 warning。

## 九、未完成事项

- 未接真实 AI / OpenAI / Claude / Gemini SDK。
- 未接 Figma API / Figma MCP。
- 未接 MySQL。
- 未创建数据库表、Entity 或 Mapper。
- 未接 Redis / RabbitMQ。
- 未做 ZIP 导出。
- 未做拖拽编辑器或在线编辑器。
- 未做真实截图解析。
- 未做复杂响应式布局算法。
- 未做 Playwright 视觉回归。

## 十、已知风险

- 当前 generated-page 保存仍是本地 mock 文件，不是数据库持久化。
- 当前 Layout JSON 仍来自手写 / 示例，不是真实截图解析。
- 当前静态编译器仍是规则编译，不是真实 AI 生成。
- 后端当前尚未严格校验 generated-page 必填字段和 `status` 枚举，后续如需补强应另开后端开发任务。

## 十一、Week 07 候选方向

1. 图片输入到 Layout JSON 的 mock / 半自动链路，为图片到 HTML 预览做准备。
2. 继续增强前端演示体验和测试覆盖。
3. 继续增强 Worker 节点和安全 style subset。
4. 如用户明确批准，再规划 MySQL 持久化。
5. 整理实践报告中的系统实现和测试章节。
