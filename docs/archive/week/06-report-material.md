# Week 06 Report Material

## 1. Week 06 主题

Week 06 的重点是围绕 generated-page artifact 做回归稳定性与演示验收增强，让当前 generated-page MVP 闭环更稳定、更好测、更好演示，也更适合写入实践报告。

当前项目仍然是学习型 MVP，不是完整 AI 生成器。

## 2. generated-page artifact 数据结构说明

generated-page artifact 是 Week 06 的核心产物，围绕 Layout JSON v0.1 的静态编译结果保存：

- `version`
- `artifactType`
- `jobId`
- `generator.name`
- `generator.version`
- `source.layoutVersion`
- `source.layoutHash`
- `source.layoutSourceType`
- `validation.passed`
- `validation.errors`
- `validation.warnings`
- `status`
- `htmlCode`
- `cssCode`
- `vueCode`
- `unsupportedNodes`
- `createdAt`

它的定位是：

```text
Layout JSON -> Worker 静态编译 -> generated-page artifact -> 后端 mock 保存 / 查询 -> 前端安全预览
```

## 3. Worker 静态编译器设计

Worker 负责把 Layout JSON 确定性地编译成可预览的 generated-page artifact。

设计要点：

1. 先做 validator 校验。
2. 校验通过后再进入静态编译。
3. `htmlCode` 和 `cssCode` 由规则编译生成。
4. `vueCode` 只作为文本展示，不要求可运行。
5. 未支持节点进入 `unsupportedNodes`。
6. 未知 style / 不安全值进入 `warnings`。
7. `layoutHash` 保持稳定。

Worker 仍然不是 AI 生成器，而是确定性规则编译器。

## 4. Layout JSON 校验设计

Layout JSON 是页面结构中间层，不是 HTML / Vue。

Week 06 仍沿用以下结构要点：

- `version`
- `page`
- `source`
- `tokens`
- `layout`
- `assets`
- `responsive`
- `assumptions`
- `warnings`

校验目标是保证输入稳定、结构明确、风险可控。

常见校验关注点：

- 结构字段是否完整。
- 节点类型是否支持。
- style 字段是否属于安全 subset。
- image src 是否安全。
- 是否存在需要写入 warning 的未知项。

## 5. 安全预览 iframe sandbox 设计

generated-page 预览必须安全，核心要求是：

- iframe 使用 `sandbox=""`。
- iframe 不允许 `allow-scripts`。
- `status=SUCCESS` 才展示 iframe。
- `status=FAILED` 不展示 iframe，只展示失败原因和 validation 信息。

这部分是 Week 06 演示验收的重要保障，也是实践报告里最值得说明的安全设计点。

## 6. 后端 mock artifact 接口设计

Week 06 继续沿用 mock 文件方案，不接 MySQL。

接口口径：

```text
PUT /api/dev/generation-jobs/{jobId}/artifacts/generated-page
GET /api/dev/generation-jobs/{jobId}/artifacts/generated-page
```

后端设计重点：

1. 保存完整 generated-page artifact。
2. 按 jobId 查询 artifact。
3. 非法 jobId 返回 400。
4. artifact 不存在返回 404。
5. 文件大小有上限，建议 2MB。
6. 不创建 Entity / Mapper。
7. 不改变接口契约。

## 7. 前端独立预览页设计

Week 06 的独立预览页推荐路由：

```text
/dev/generated-page-preview/:jobId
```

页面职责：

- 只调用 generated-page artifact GET 接口。
- 展示状态、代码、validation、unsupportedNodes、source.layoutHash、generator 信息。
- `status=SUCCESS` 时展示 iframe。
- `status=FAILED` 时不展示 iframe。

页面不依赖：

- Week 02 generation job 详情接口。
- 数据库。
- 登录状态。

## 8. SUCCESS / FAILED 状态处理设计

### SUCCESS

- `status=SUCCESS`
- `htmlCode` / `cssCode` 可展示
- `vueCode` 可展示
- iframe 可预览

### FAILED

- `status=FAILED`
- 不展示 iframe
- 展示 validation.errors
- 展示 validation.warnings
- 代码区仍可作为失败产物文本展示或置空展示，取决于当前实现口径

这个状态设计方便用户理解“验证通过”和“验证失败”两条主路径。

## 9. 测试用例设计

Week 06 的测试重点围绕“闭环稳定”而不是“继续扩大能力”。

建议覆盖：

1. Worker valid -> `SUCCESS`。
2. Worker invalid -> `FAILED`。
3. 后端 PUT 成功。
4. 后端 GET 成功。
5. 后端 404。
6. 后端 400。
7. 前端 preview 页面成功展示。
8. iframe 安全属性正确。
9. 前端 build 通过。
10. 前端测试通过。
11. Worker unittest 通过。

## 10. 当前系统限制

Week 06 仍然不是完整产品，当前限制包括：

- 不接真实 AI。
- 不接 Figma。
- 不接 MySQL 持久化。
- 不创建数据库表、Entity、Mapper。
- 不接 Redis / RabbitMQ。
- 不做 ZIP。
- 不做编辑器。
- 不做真实截图解析。
- 不做复杂响应式布局算法。
- 不做 Tailwind 代码生成。
- 不做 Vue SFC 可运行化。

## 11. 后续扩展方向

Week 06 之后可以考虑的方向包括：

1. 更稳的前端 preview 体验。
2. 更完整的自动化测试。
3. 更丰富的 Worker 节点和安全 style subset。
4. 如果用户确认，再规划 MySQL 持久化。
5. 如果用户确认，再考虑真实 AI / Figma 预研。

这些都应在当前 MVP 闭环继续稳定后再推进。
