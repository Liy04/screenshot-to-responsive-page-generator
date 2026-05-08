# Week 05 开发计划：Generated Page 独立预览与质量稳定化

项目名称：`screenshot-to-responsive-page-generator`

GitHub 仓库：

```text
https://github.com/Liy04/screenshot-to-responsive-page-generator
```

当前最新提交：

```text
86581f3 Complete Week 04 static generated page flow
```

当前阶段：

```text
Week 05：Generated Page 独立预览与质量稳定化
```

---

## 1. 本周阶段定位

Week 04 已完成：

```text
Layout JSON
↓
Worker 静态编译器
↓
generated-page artifact
↓
后端 mock 保存 / 查询
↓
前端 sandbox iframe 安全预览
```

Week 05 不继续扩大范围，不急着接真实 AI、数据库、Figma 或复杂编辑器。

本周的核心方向是：

```text
稳住 Week 04 已经跑通的 generated-page 闭环。
```

也就是说，本周重点不是“加大功能”，而是：

```text
1. 修正现有 UX 问题。
2. 补齐基础自动化测试。
3. 增强 generated-page 独立预览能力。
4. 整理可复现的 smoke 流程。
5. 小幅增强 Worker 静态编译器。
6. 沉淀可写入实践报告的阶段成果。
```

---

## 2. 本周总目标

Week 05 的总目标是：

> 围绕 generated-page artifact，完善独立预览体验、补齐基础自动化测试、整理端到端 smoke 流程，让项目从“能跑通”升级到“能稳定验收”。

本周需要完成：

```text
1. 修正前端任务详情页 UX，使 generated-page 展示不依赖旧 Week 02 generation job 查询结果。
2. 新增 generated-page 独立 dev preview 页面。
3. 为后端 generated-page artifact mock 接口补充自动化测试。
4. 小幅增强 Worker 静态编译器对常见安全 style subset 的支持。
5. 整理 Worker -> Backend -> Frontend 的 Week 05 dev smoke 文档。
6. 完成 Week 05 总结归档。
```

---

## 3. 本周禁止事项

Week 05 必须继续控制范围，以下内容本周不做：

```text
1. 不接真实 AI / OpenAI / Claude / Gemini SDK
2. 不接 Figma API / Figma MCP
3. 不接 MySQL 实际落库
4. 不创建数据库表
5. 不创建 Entity / Mapper
6. 不接 Redis / RabbitMQ
7. 不做 ZIP 导出
8. 不做拖拽编辑器 / 在线编辑器
9. 不做真实截图解析
10. 不做登录注册 / 历史记录持久化 / 复杂权限
11. 不要求 vueCode 真正可运行
12. 不做 Playwright 视觉回归，除非用户明确批准
13. 不做复杂响应式布局算法
14. 不做 Tailwind 代码生成
15. 不做 Vue SFC 可运行化
```

本周重点是：

```text
修正现有 UX
补测试
增强稳定性
整理 smoke 流程
沉淀文档
```

不是：

```text
接入真实 AI
接入数据库
做复杂编辑器
做真实截图识别
做完整生产级系统
```

---

## 4. Week 05 总体路线

推荐本周按以下顺序推进：

```text
Day 1：文档定范围
Day 2：修正前端详情页 UX
Day 3：新增 generated-page 独立 dev preview 页面
Day 4：补后端 generated-page mock 接口自动化测试
Day 5：Worker 静态编译器小幅增强
Day 6：整理 Worker -> Backend -> Frontend dev smoke 文档
Day 7：总结归档，形成 Week 05 commit
```

本周最终希望形成的闭环是：

```text
Layout JSON 示例
↓
Worker 静态编译 generated-page artifact
↓
后端 mock 接口保存 artifact
↓
后端 mock 接口查询 artifact
↓
前端任务详情页可展示 artifact
↓
前端独立 dev preview 页面可展示 artifact
↓
sandbox iframe 安全预览
↓
测试和 smoke 文档可复现
```

---

## 5. 优先级划分

---

## 5.1 P0：必须完成

### P0-1：修正前端详情页 UX

当前问题：

```text
详情页旧 Week 02 generation 查询失败时，会显示“加载失败 / 任务不存在”，但 Week 04 generated-page 区域仍可正常展示。
```

这会导致页面体验混乱。

用户可能会疑惑：

```text
为什么页面说任务不存在，但是 generated-page 又能展示？
这个任务到底是成功了还是失败了？
```

因此，Week 05 必须修正该问题。

目标：

```text
generated-page artifact 的展示不应该依赖旧 Week 02 generation job 查询结果。
```

完成后效果：

```text
1. generation job 查询失败时，不应该导致整个详情页失败。
2. generated-page artifact 应该有独立的 loading / success / failed / empty / error 状态。
3. 如果 generated-page 存在，就正常展示。
4. 如果 generated-page 不存在，就展示清晰空状态。
5. 如果 status=FAILED，只展示失败原因，不展示 iframe 预览。
6. 如果 status=SUCCESS，展示 htmlCode + cssCode 的安全预览。
7. iframe 必须继续使用 sandbox=""。
8. iframe 不允许出现 allow-scripts。
```

### Day 2 与 Day 3 的边界说明

Day 2 只做：

```text
修正现有任务详情页 generated-page UX。
```

Day 2 不做：

```text
1. 不新增独立 dev preview 页面。
2. 不新增新路由。
3. 不大改页面结构。
4. 不顺手完成 Day 3 任务。
```

如果需要抽取可复用组件，可以只做最小必要抽取，例如：

```text
GeneratedPageMeta
GeneratedPagePreview
GeneratedPageValidationPanel
```

但组件抽取必须服务于 Day 2 当前任务，不能扩大成完整新页面开发。

---

### P0-2：新增 generated-page 独立 dev preview 页面

建议新增路由：

```text
/dev/generated-page-preview/:jobId
```

这个页面只负责：

```text
根据 jobId 查询 generated-page artifact，然后展示生成结果。
```

它不依赖：

```text
Week 02 generation job 详情接口
旧 mock generation 查询
任务历史记录
数据库
登录状态
```

页面应该展示：

```text
1. jobId
2. status
3. htmlCode
4. cssCode
5. vueCode
6. validation.errors
7. validation.warnings
8. unsupportedNodes
9. source.layoutHash
10. generator 信息
11. sandbox iframe 安全预览
```

status=SUCCESS 时：

```text
展示 iframe 预览
展示代码
展示校验信息
```

status=FAILED 时：

```text
不展示 iframe
只展示失败原因
展示 validation.errors
展示 validation.warnings
展示 unsupportedNodes
```

### Day 3 与 Day 2 的边界说明

Day 3 只做：

```text
新增 generated-page 独立 dev preview 页面。
```

Day 3 可以复用 Day 2 中已有的 generated-page 展示组件。

Day 3 不做：

```text
1. 不继续重构任务详情页。
2. 不修改旧 generation job 逻辑。
3. 不修改后端接口。
4. 不做编辑器。
5. 不做复杂页面设计。
```

---

### P0-3：补后端 generated-page mock 接口测试

Week 04 后端已经有以下接口：

```text
PUT /api/dev/generation-jobs/{jobId}/artifacts/generated-page
GET /api/dev/generation-jobs/{jobId}/artifacts/generated-page
```

Week 05 要补自动化测试。

测试覆盖：

```text
1. PUT 成功保存 generated-page artifact。
2. GET 成功读取 generated-page artifact。
3. artifact 不存在时返回 404。
4. 非法 jobId 返回 400。
5. 超过 2MB 返回 400。
6. status=FAILED artifact 可以保存和读取。
7. 测试数据隔离，不污染 backend/mock-data。
8. 不接 MySQL。
9. 不创建 Entity / Mapper。
```

后端测试要求：

```text
优先使用项目已有 Spring Boot Test / MockMvc 能力。
如缺少测试依赖，先报告，不擅自新增。
```

---

## 5.2 P1：应该完成

### P1-1：优化前端 generated-page 展示结构

当前前端已经可以展示 generated-page 信息，但结构可以更清楚。

建议页面结构：

```text
Generated Page 状态区
↓
安全预览区
↓
代码查看区
  - HTML
  - CSS
  - Vue 文本
↓
校验结果区
  - errors
  - warnings
  - unsupportedNodes
↓
来源信息区
  - layoutHash
  - generator name
  - generator version
```

页面重点不是做得花哨，而是让人一眼能看懂：

```text
1. 这个页面是怎么来的。
2. 有没有生成成功。
3. 有没有校验错误。
4. 有没有安全风险。
5. 能不能预览。
6. 代码在哪里。
7. 来源 layoutHash 是什么。
8. generator 信息是什么。
```

---

### P1-2：Worker 静态编译器小幅增强

当前 Worker 规则编译器支持的节点和样式仍有限。

Week 05 可以小幅增强，但必须严格控制范围。

只允许增强以下安全 style subset：

```text
width
height
padding
margin
borderRadius
backgroundColor
color
fontSize
fontWeight
textAlign
display
flexDirection
gap
objectFit
```

必须保持：

```text
1. 未知 style 进入 warnings。
2. HTML escape 不退化。
3. script 禁止。
4. inline event 禁止。
5. javascript URL 禁止。
6. 不安全 image src warning。
7. layoutHash 稳定性不破坏。
```

明确不做：

```text
1. 不做布局推断。
2. 不做响应式算法。
3. 不做复杂 grid 推断。
4. 不做真实截图解析。
5. 不做 Tailwind 代码生成。
6. 不做动态交互生成。
7. 不做可运行 Vue SFC 生成。
8. 不做 AI 生成代码。
```

这一天的目标不是让生成页面变得非常智能，而是：

```text
让规则编译器多支持一些常见安全样式，同时保持简单、可测、可控。
```

---

### P1-3：整理半自动 dev smoke 流程

目标是形成一条可复现流程：

```text
Layout JSON 示例
↓
Worker 编译 generated-page
↓
后端保存 artifact
↓
前端独立预览页展示
```

建议新增文档：

```text
docs/dev-smoke-week05.md
```

文档需要覆盖：

```text
1. 如何首次准备依赖。
2. 如何启动后端。
3. 如何启动前端。
4. 如何运行 Worker 编译器。
5. 如何上传 generated-page artifact。
6. 如何打开独立预览页。
7. 如何验证 SUCCESS 状态。
8. 如何验证 FAILED 状态。
9. 如何验证 iframe sandbox=""。
10. 如何确认无 allow-scripts。
11. 常见失败排查。
```

---

## 5.3 P2：有余力再做

### P2-1：前端轻量自动化测试

如果时间充足，可以补前端测试。

优先测试：

```text
1. generated-page API 封装函数。
2. artifact 为空时页面展示。
3. status=FAILED 时不渲染 iframe。
4. status=SUCCESS 时才渲染 iframe。
5. iframe sandbox 属性不包含 allow-scripts。
```

如果测试成本过高，可以先用手动 smoke 文档替代。

Week 05 不强制 Playwright 视觉回归。

---

# 6. 每日任务计划

---

## Day 1：文档定范围

### 目标

更新 Docs Lite 文档，明确 Week 05 的目标、范围、禁止事项和验收标准，防止 Codex 乱扩展。

### 涉及文件

```text
docs/current.md
docs/plan.md
docs/spec.md
docs/task.md
```

### 任务内容

```text
1. 更新 docs/current.md，写入当前阶段。
2. 更新 docs/plan.md，写入 Week 05 总计划。
3. 更新 docs/spec.md，补充 generated-page 独立预览页规格。
4. 更新 docs/task.md，只保留 Day 1 当前任务。
5. 明确 Week 05 不接数据库、不接真实 AI、不接 Figma、不做 ZIP、不做编辑器。
6. 明确 Day 2 / Day 3 前端任务边界。
7. 明确每天任务必须拆分，不能混合多个线程。
```

### Day 1 验收标准

```text
1. docs/current.md 已更新。
2. docs/plan.md 已更新。
3. docs/spec.md 已更新。
4. docs/task.md 只保留 Day 1 当前任务。
5. Week 05 禁止事项明确。
6. Day 2 / Day 3 边界明确。
7. 没有产生大规模代码修改。
```

### Day 1 给 Codex 的提示词

```text
任务：进入 Week 05 文档定范围阶段。

项目：screenshot-to-responsive-page-generator

当前阶段：
Week 05 - Generated Page 独立预览与质量稳定化。

请先阅读：
- AGENTS.md
- docs/current.md
- docs/plan.md
- docs/task.md
- docs/spec.md

然后只更新文档，不改业务代码。

要求：
1. 在 docs/current.md 中写明 Week 05 当前阶段。
2. 在 docs/plan.md 中写明 Week 05 总目标、每日计划、验收标准。
3. 在 docs/spec.md 中补充 generated-page 独立 dev preview 页面规格。
4. docs/task.md 只保留 Day 1 当前任务。
5. 明确 Week 05 禁止事项：
   - 不接真实 AI
   - 不接 Figma API / Figma MCP
   - 不接 MySQL
   - 不创建数据库表
   - 不创建 Entity / Mapper
   - 不接 Redis / RabbitMQ
   - 不做 ZIP 导出
   - 不做拖拽编辑器
   - 不做真实截图解析
   - 不做登录注册
   - 不要求 vueCode 真正可运行
   - 不做 Playwright 视觉回归
6. 明确 Day 2 和 Day 3 的边界：
   - Day 2 只修正现有详情页 UX
   - Day 3 只新增独立 dev preview 页面
   - 可以复用组件，但不要在 Day 2 顺手完成 Day 3
7. 完成后输出：
   - 修改文件
   - Week 05 范围摘要
   - 风险
   - 下一步建议
```

---

## Day 2：修正前端详情页 UX

### 目标

让 generated-page artifact 展示逻辑不再依赖旧 Week 02 generation job 查询结果。

### 当前问题

```text
旧 generation job 查询失败时，详情页会显示“加载失败 / 任务不存在”，但 generated-page 区域仍可正常展示。
```

### 修改目标

```text
1. generation job 查询失败，不应该让整个详情页失败。
2. generated-page artifact 区域应该有独立状态。
3. generated-page artifact 成功时正常展示。
4. generated-page artifact 不存在时展示空状态。
5. generated-page artifact 失败时展示失败原因。
6. status=FAILED 时不展示 iframe。
7. status=SUCCESS 时展示 sandbox iframe。
```

### 本日范围

Day 2 只做：

```text
修正现有详情页 generated-page UX。
```

Day 2 不做：

```text
1. 不新增 /dev/generated-page-preview/:jobId 路由。
2. 不新增独立 dev preview 页面。
3. 不修改后端接口。
4. 不大改整体页面结构。
5. 不顺手完成 Day 3 任务。
```

### 前端状态建议

generated-page 区域建议独立维护以下状态：

```text
loading
success
empty
failed
error
```

含义：

```text
loading：正在请求 generated-page artifact
success：artifact 存在且 status=SUCCESS
empty：artifact 不存在，例如后端返回 404
failed：artifact 存在但 status=FAILED
error：请求异常或非预期错误
```

### Day 2 验收标准

```text
1. 前端 npm run build 通过。
2. 旧 generation job 查询失败时，generated-page 区域仍可正常展示。
3. status=SUCCESS 时展示 iframe 预览。
4. status=FAILED 时不展示 iframe。
5. artifact 不存在时展示清晰空状态。
6. iframe 使用 sandbox=""。
7. iframe 不包含 allow-scripts。
8. 不引入新的 UI 框架。
9. 不修改后端接口。
10. 没有新增独立 dev preview 页面。
```

### Day 2 给 Codex 的提示词

```text
任务：修正前端任务详情页 generated-page 展示逻辑，使其不依赖旧 Week 02 generation job 查询结果。

本日范围：
只修正现有任务详情页 UX。
不要新增独立 dev preview 页面。
不要新增 /dev/generated-page-preview/:jobId 路由。
不要顺手完成 Day 3 任务。

要求：
1. 先阅读当前任务详情页、generated-page artifact API、LayoutJsonViewer 或相关展示组件代码。
2. 不修改后端接口。
3. 不新增复杂状态管理库。
4. generation job 查询失败时，页面不能整体失败。
5. generated-page artifact 区域应独立显示 loading / success / failed / empty / error 状态。
6. status=FAILED 时不展示 iframe 预览。
7. status=SUCCESS 时展示 iframe 预览。
8. iframe 必须使用 sandbox=""。
9. iframe 不得加入 allow-scripts。
10. 如需要抽取组件，只做服务于当前详情页 UX 修正的最小抽取。
11. 完成后运行 npm run build。
12. 输出修改文件、验收结果、风险和未完成项。
```

---

## Day 3：新增 generated-page 独立 dev preview 页面

### 目标

新增一个独立页面，只负责 generated-page artifact 的查询与展示。

### 推荐路由

```text
/dev/generated-page-preview/:jobId
```

### 页面职责

这个页面只负责：

```text
1. 从路由参数中获取 jobId。
2. 调用 generated-page artifact GET 接口。
3. 展示 artifact 状态。
4. 展示 htmlCode / cssCode / vueCode。
5. 展示 validation 信息。
6. 展示 unsupportedNodes。
7. 展示 source.layoutHash。
8. 展示 generator 信息。
9. 在 SUCCESS 状态下使用 sandbox iframe 预览。
```

这个页面不负责：

```text
1. 查询旧 generation job。
2. 创建任务。
3. 上传截图。
4. 修改 artifact。
5. 接数据库。
6. 接真实 AI。
7. 编辑生成代码。
8. 继续重构任务详情页。
```

### 本日范围

Day 3 只做：

```text
新增 generated-page 独立 dev preview 页面。
```

Day 3 可以复用 Day 2 已有组件，例如：

```text
GeneratedPageMeta
GeneratedPagePreview
GeneratedPageValidationPanel
GeneratedPageCodeBlock
```

Day 3 不做：

```text
1. 不继续修改任务详情页 UX。
2. 不修改旧 generation job 详情逻辑。
3. 不修改后端接口。
4. 不做复杂页面设计。
5. 不引入新 UI 框架。
```

### 页面结构建议

```text
页面标题：Generated Page Dev Preview

区域一：Artifact 状态
- jobId
- status
- generator.name
- generator.version
- source.layoutHash

区域二：安全预览
- 仅 status=SUCCESS 时展示
- iframe sandbox=""
- 不包含 allow-scripts

区域三：代码展示
- htmlCode
- cssCode
- vueCode

区域四：校验信息
- validation.errors
- validation.warnings
- unsupportedNodes

区域五：异常状态
- 404 artifact 不存在
- 请求失败
- status=FAILED
```

### Day 3 验收标准

```text
1. 新路由可以访问。
2. 输入已有 jobId 可以看到 generated-page。
3. 输入不存在 jobId 可以看到清晰 404 / empty 状态。
4. status=SUCCESS 时展示 iframe。
5. status=FAILED 时不展示 iframe。
6. htmlCode / cssCode / vueCode 可以展示。
7. validation.errors / validation.warnings / unsupportedNodes 可以展示。
8. source.layoutHash 和 generator 信息可以展示。
9. npm run build 通过。
10. 不引入新 UI 框架。
11. 不继续重构任务详情页。
```

### Day 3 给 Codex 的提示词

```text
任务：新增 generated-page 独立 dev preview 页面。

推荐路由：
/dev/generated-page-preview/:jobId

本日范围：
只新增独立 dev preview 页面。
可以复用 Day 2 已有组件。
不要继续重构任务详情页。
不要修改后端接口。

要求：
1. 先阅读前端路由结构、generated-page artifact API 和现有 generated-page 展示逻辑。
2. 页面只调用 generated-page artifact GET 接口。
3. 不依赖 generation job 详情接口。
4. status=SUCCESS 时展示 sandbox iframe 预览。
5. status=FAILED 时只展示失败原因和校验信息。
6. 展示 htmlCode / cssCode / vueCode。
7. 展示 validation.errors / validation.warnings / unsupportedNodes。
8. 展示 source.layoutHash 和 generator 信息。
9. 保持页面简洁，不引入新的 UI 框架。
10. iframe 必须使用 sandbox=""，不得包含 allow-scripts。
11. 完成后运行 npm run build。
12. 输出修改文件、访问路径、验收结果、风险和未完成项。
```

---

## Day 4：补后端 generated-page mock 接口测试

### 目标

为 generated-page artifact mock 接口补充自动化测试。

### 后端接口

```text
PUT /api/dev/generation-jobs/{jobId}/artifacts/generated-page
GET /api/dev/generation-jobs/{jobId}/artifacts/generated-page
```

### 测试覆盖范围

```text
1. PUT 成功保存 artifact。
2. GET 成功读取 artifact。
3. artifact 不存在返回 404。
4. 非法 jobId 返回 400。
5. 超过 2MB 返回 400。
6. status=FAILED artifact 可以保存和读取。
7. 测试数据隔离。
8. 测试结束后清理临时 mock 数据。
```

### 测试依赖要求

```text
优先使用项目已有 Spring Boot Test / MockMvc 能力。
如缺少测试依赖，先报告，不擅自新增。
```

### 明确禁止

```text
1. 不接 MySQL。
2. 不创建数据库表。
3. 不创建 Entity。
4. 不创建 Mapper。
5. 不改接口路径。
6. 不擅自引入新的复杂测试框架。
```

### Day 4 验收标准

```text
1. 后端测试通过。
2. 关键边界场景都有覆盖。
3. 测试不污染 backend/mock-data。
4. 接口路径不变。
5. 没有新增数据库相关代码。
6. 没有新增 Entity / Mapper。
7. 如缺少测试依赖，已明确报告，而不是擅自新增。
```

### Day 4 给 Codex 的提示词

```text
任务：为 generated-page artifact mock 接口补充后端自动化测试。

要求：
1. 先阅读当前 generated-page artifact controller / service / mock storage 代码。
2. 优先使用项目已有 Spring Boot Test / MockMvc 能力。
3. 如缺少测试依赖，先报告，不擅自新增。
4. 不接 MySQL。
5. 不创建 Entity / Mapper。
6. 不改变现有接口路径。
7. 覆盖 PUT 成功、GET 成功、404、非法 jobId 400、超过 2MB 400。
8. 覆盖 status=FAILED artifact 保存和读取。
9. 测试数据应隔离，不污染真实 backend/mock-data。
10. 完成后运行 mvn test 或项目当前后端测试命令。
11. 输出修改文件、测试覆盖点、测试结果、风险和未完成项。
```

---

## Day 5：Worker 静态编译器小幅增强

### 目标

在不扩大范围的前提下，让 Worker 静态生成页面更像真实页面。

### 本日范围

只增强以下字段：

```text
width
height
padding
margin
borderRadius
backgroundColor
color
fontSize
fontWeight
textAlign
display
flexDirection
gap
objectFit
```

### 必须保持的安全规则

```text
1. HTML escape 必须保持。
2. 禁止 script。
3. 禁止 inline event。
4. 禁止 javascript URL。
5. 不安全 image src 继续 warning。
6. 未知 style 继续 warning。
7. invalid 示例继续 FAILED。
8. layoutHash 稳定性不能破坏。
```

### 明确不做

```text
1. 不做真实截图解析。
2. 不做 AI 生成代码。
3. 不做复杂 grid 推断。
4. 不做响应式算法。
5. 不做拖拽编辑器。
6. 不做 Vue SFC 可运行化。
7. 不做 Tailwind 生成。
8. 不扩大 style subset 到列表之外。
```

### Day 5 验收标准

```text
1. Worker 测试通过。
2. valid 示例输出 SUCCESS。
3. invalid 示例输出 FAILED。
4. layoutHash 稳定性测试通过。
5. HTML escape 测试通过。
6. script / inline event / javascript URL 禁止测试通过。
7. 未知 style warning 测试通过。
8. 不安全 image src warning 测试通过。
9. 新增 style subset 有对应测试。
10. 没有新增响应式算法。
11. 没有新增 Tailwind 生成。
12. 没有新增 Vue SFC 可运行化逻辑。
```

### Day 5 给 Codex 的提示词

```text
任务：小幅增强 Worker Layout JSON 静态编译器的 style subset 支持。

本日范围：
只支持以下字段：
- width
- height
- padding
- margin
- borderRadius
- backgroundColor
- color
- fontSize
- fontWeight
- textAlign
- display
- flexDirection
- gap
- objectFit

明确不做：
- 不做布局推断
- 不做响应式算法
- 不做真实截图解析
- 不做 Tailwind 生成
- 不做 Vue SFC 可运行化
- 不做 AI 生成代码
- 不扩大字段范围

要求：
1. 先阅读 worker/layout_static_generator.py、worker/layout_validator.py 和现有测试。
2. 未知样式继续进入 warnings，不要静默忽略。
3. 保持 HTML escape。
4. 保持禁止 script、inline event、javascript URL。
5. 保持不安全 image src warning。
6. 保持 layoutHash 稳定性。
7. 补充对应测试。
8. 运行 Worker 测试。
9. 输出修改文件、测试结果、风险和未完成项。
```

---

## Day 6：整理端到端 dev smoke 流程

### 目标

形成一条可以重复演示的 Week 05 smoke 流程。

### 推荐新增文档

```text
docs/dev-smoke-week05.md
```

### smoke 流程

```text
Layout JSON 示例
↓
Worker 编译 generated-page artifact
↓
后端 PUT 保存 artifact
↓
后端 GET 查询 artifact
↓
前端独立预览页展示
↓
确认 iframe sandbox 安全策略
```

### 重要修正

当前 examples 在项目根目录下，不在 `worker/examples/` 下。

因此 Worker 编译命令应使用：

```bash
python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
```

不要写成：

```bash
cd worker
python layout_static_generator.py examples/valid-layout.json > ../generated-page-valid.json
```

### 后端启动方式修正

由于之前记录过 Windows 中文路径下：

```bash
mvn spring-boot:run
```

存在风险，因此 Week 05 smoke 文档中后端启动优先写：

```bash
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

可以把以下方式写为可选方式：

```bash
cd backend
mvn spring-boot:run
```

### 前端启动方式修正

不要把 `npm install` 写成每次 smoke 的必需步骤。

首次安装依赖时：

```bash
cd frontend
npm install
```

日常 smoke 时：

```bash
cd frontend
npm run dev
```

---

### docs/dev-smoke-week05.md 建议内容

```markdown
# Week 05 Dev Smoke

## 1. 目标

验证 Worker -> Backend -> Frontend 的 generated-page artifact 预览闭环。

本 smoke 流程用于确认：

1. Worker 可以从 Layout JSON 示例生成 generated-page artifact。
2. 后端可以保存 generated-page artifact。
3. 后端可以查询 generated-page artifact。
4. 前端独立 dev preview 页面可以展示 generated-page artifact。
5. SUCCESS 状态可以安全预览。
6. FAILED 状态不会展示 iframe。
7. iframe 使用 sandbox=""，且不包含 allow-scripts。

---

## 2. 前置条件

- 当前在项目根目录。
- 已安装 Java 17。
- 已安装 Maven。
- 已安装 Node.js。
- 已安装 Python，推荐 Python 3.11。
- 当前不接 MySQL。
- 当前不接真实 AI。
- 当前使用本地 mock artifact。
- 后端 mock-data 按忽略规则处理，不提交构建副产物。

---

## 3. 首次安装前端依赖

首次运行前端前执行：

```bash
cd frontend
npm install
```

之后日常 smoke 不需要每次执行 `npm install`。

回到项目根目录：

```bash
cd ..
```

---

## 4. 启动后端

推荐方式：

```bash
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

说明：

```text
该方式优先用于 Week 05 smoke。
原因是之前记录过 Windows 中文路径下 mvn spring-boot:run 存在风险。
```

可选方式：

```bash
cd backend
mvn spring-boot:run
```

回到项目根目录：

```bash
cd ..
```

---

## 5. 启动前端

```bash
cd frontend
npm run dev
```

默认访问地址通常为：

```text
http://localhost:5173
```

回到项目根目录：

```bash
cd ..
```

---

## 6. 运行 Worker 编译器

注意：

```text
当前 examples 在项目根目录下，不在 worker/examples/ 下。
```

在项目根目录执行：

```bash
python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
```

预期结果：

```text
项目根目录生成 generated-page-valid.json。
该文件内容应包含 generated-page artifact。
status 应为 SUCCESS。
htmlCode / cssCode 应有内容。
vueCode 仅作为文本展示，不要求可运行。
```

---

## 7. 上传 generated-page artifact

在项目根目录执行：

```bash
curl -X PUT ^
  http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page ^
  -H "Content-Type: application/json" ^
  --data-binary @generated-page-valid.json
```

如果使用 Git Bash / macOS / Linux，可使用：

```bash
curl -X PUT \
  http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page \
  -H "Content-Type: application/json" \
  --data-binary @generated-page-valid.json
```

预期结果：

```text
后端返回保存成功。
```

---

## 8. 查询 generated-page artifact

```bash
curl http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page
```

预期结果：

```text
能查询到刚才上传的 generated-page artifact。
status=SUCCESS。
htmlCode / cssCode / vueCode 字段存在。
validation / source / generator 信息存在。
```

---

## 9. 打开独立 dev preview 页面

访问：

```text
http://localhost:5173/dev/generated-page-preview/demo-job-001
```

预期结果：

```text
页面可以展示 generated-page artifact。
```

---

## 10. SUCCESS 状态验收点

需要确认：

```text
1. status=SUCCESS。
2. htmlCode 正常展示。
3. cssCode 正常展示。
4. vueCode 作为文本展示。
5. validation.errors 为空或符合预期。
6. validation.warnings 正常展示。
7. unsupportedNodes 正常展示。
8. source.layoutHash 正常展示。
9. generator 信息正常展示。
10. iframe 预览正常展示。
11. iframe sandbox=""。
12. iframe 不包含 allow-scripts。
```

---

## 11. FAILED 状态验收点

使用 invalid 示例生成失败 artifact 后，需要确认：

```text
1. status=FAILED。
2. 不展示 iframe 预览。
3. 展示 validation.errors。
4. 展示 validation.warnings。
5. htmlCode / cssCode / vueCode 为空或符合失败状态约定。
```

---

## 12. 常见问题排查

### 12.1 后端 404

检查：

```text
1. jobId 是否正确。
2. artifact 是否已经 PUT 保存。
3. 后端是否正常启动。
```

### 12.2 后端 400

检查：

```text
1. jobId 是否非法。
2. 请求体是否超过 2MB。
3. JSON 是否有效。
```

### 12.3 前端无法访问

检查：

```text
1. 前端 dev server 是否启动。
2. 端口是否为 5173。
3. 路由是否为 /dev/generated-page-preview/:jobId。
```

### 12.4 Worker 找不到示例文件

确认当前在项目根目录，并使用：

```bash
python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
```

不要使用：

```bash
cd worker
python layout_static_generator.py examples/valid-layout.json > ../generated-page-valid.json
```

### 12.5 iframe 未展示

检查：

```text
1. artifact status 是否为 SUCCESS。
2. 如果 status=FAILED，前端不应该展示 iframe。
```

### 12.6 安全策略异常

检查：

```text
1. iframe 是否仍为 sandbox=""。
2. iframe 是否不包含 allow-scripts。
3. Worker 是否继续禁止 script / inline event / javascript URL。
```
```

### Day 6 验收标准

```text
1. docs/dev-smoke-week05.md 已新增。
2. Worker 命令路径正确：
   python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
3. 后端默认启动方式使用 jar：
   cd backend
   mvn package -DskipTests
   java -jar target/backend-0.0.1-SNAPSHOT.jar
4. mvn spring-boot:run 仅作为可选方式。
5. 前端日常 smoke 使用 npm run dev。
6. npm install 只写在首次安装依赖部分。
7. 按文档可以完整跑通一次。
8. Worker smoke 通过。
9. 后端 PUT / GET 通过。
10. 前端 build 通过。
11. 独立预览页可访问。
12. SUCCESS artifact 可预览。
13. FAILED artifact 不展示 iframe。
14. iframe sandbox=""。
15. iframe 无 allow-scripts。
```

### Day 6 给 Codex 的提示词

```text
任务：整理 Week 05 端到端 dev smoke 流程文档。

要求：
1. 不新增复杂自动化平台。
2. 不接队列。
3. 不接 Redis / RabbitMQ。
4. 不接 MySQL。
5. 文档应覆盖 Worker -> Backend -> Frontend 的完整手动或半自动流程。
6. 文档放在 docs/dev-smoke-week05.md。
7. Worker 命令必须使用项目根目录 examples：
   python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
8. 不要写成 worker/examples 路径。
9. 后端启动方式优先使用：
   cd backend
   mvn package -DskipTests
   java -jar target/backend-0.0.1-SNAPSHOT.jar
10. mvn spring-boot:run 可以写为可选方式，但不能作为默认推荐方式。
11. 前端日常 smoke 写：
   cd frontend
   npm run dev
12. npm install 只放在首次安装依赖部分，不作为每次 smoke 必需步骤。
13. 验收点必须包含 iframe sandbox="" 且无 allow-scripts。
14. 完成后输出修改文件、smoke 步骤、风险和未完成项。
```

---

## Day 7：总结归档与 Week 05 commit

### 目标

沉淀 Week 05 成果，方便写实践报告和后续答辩。

### 涉及文件

```text
docs/current.md
docs/plan.md
docs/spec.md
docs/archive/week05-summary.md
```

### 建议新增归档

```text
docs/archive/week05-summary.md
```

### week05-summary.md 建议内容

```markdown
# Week 05 Summary

## 一、本周阶段

Week 05：Generated Page 独立预览与质量稳定化。

## 二、本周目标

本周目标是围绕 generated-page artifact 完善预览体验、补齐测试、整理 smoke 流程，使 Week 04 已完成的静态生成闭环从“能跑通”升级为“能稳定验收”。

## 三、完成内容

1. 修正任务详情页 generated-page 展示依赖旧 generation job 的 UX 问题。
2. 新增 generated-page 独立 dev preview 页面。
3. 补充后端 generated-page artifact mock 接口测试。
4. 小幅增强 Worker 静态编译器 style subset。
5. 整理 Worker -> Backend -> Frontend dev smoke 流程。

## 四、验收结果

### Worker

- valid 示例：通过
- invalid 示例：通过
- layoutHash 稳定性：通过
- HTML escape：通过
- script / inline event / javascript URL 禁止：通过
- unknown style warning：通过
- unsafe image src warning：通过

### Backend

- PUT generated-page artifact：通过
- GET generated-page artifact：通过
- 404 artifact 不存在：通过
- 400 非法 jobId：通过
- 400 超过 2MB：通过
- status=FAILED artifact 保存读取：通过

### Frontend

- npm run build：通过
- 任务详情页 UX 解耦：通过
- generated-page 独立 preview 页面：通过
- status=SUCCESS 展示 iframe：通过
- status=FAILED 不展示 iframe：通过
- iframe sandbox=""：通过
- 无 allow-scripts：通过

### Dev Smoke

- Worker -> Backend -> Frontend 流程：通过
- Worker 命令路径已修正：通过
- 后端 jar 启动方式已记录：通过
- 前端 smoke 命令已修正：通过
- 文档复现流程：通过

## 五、安全验证

1. iframe 使用 sandbox=""。
2. iframe 不包含 allow-scripts。
3. Worker 禁止 script。
4. Worker 禁止 inline event。
5. Worker 禁止 javascript URL。
6. HTML escape 保持有效。
7. 不安全 image src 进入 warning。

## 六、未完成事项

1. 未接真实 AI。
2. 未接 Figma API / Figma MCP。
3. 未接 MySQL。
4. 未做 ZIP 导出。
5. 未做拖拽编辑器。
6. 未做真实截图解析。
7. 未做 Playwright 视觉回归。
8. vueCode 仍仅作为文本展示，不要求可运行。

## 七、后续建议

Week 06 可以在以下方向中选择：

1. 增强 Layout JSON 节点和样式表达能力。
2. 进一步补充前端自动化测试。
3. 开始规划 MySQL 持久化，但需用户明确批准。
4. 设计 Worker -> Backend 的更正式 artifact 流程，但不接队列。
5. 继续完善实践报告中的系统实现与测试章节。
```

### 推荐 Week 05 commit message

```text
Complete Week 05 generated page preview stabilization
```

### Day 7 验收标准

```text
1. docs/archive/week05-summary.md 已新增。
2. docs/current.md 已更新到 Week 05 完成状态。
3. docs/plan.md 已更新后续方向。
4. docs/task.md 清理完成。
5. 本地 main 干净。
6. 本地 main 与 origin/main 对齐。
7. 形成 Week 05 commit。
```

---

# 7. 多线程任务拆分

Week 05 建议拆成 4 条线程：

```text
Frontend Preview Thread
Backend Artifact Test Thread
Worker Static Generator Thread
Docs & Smoke Thread
```

---

## 7.1 Frontend Preview Thread

负责内容：

```text
1. 任务详情页 UX 解耦。
2. generated-page 独立 dev preview 页面。
3. iframe 安全展示。
4. 前端 build。
5. 前端 smoke。
```

边界要求：

```text
1. Day 2 只修任务详情页 UX。
2. Day 3 只新增独立 dev preview 页面。
3. 两天可以复用组件。
4. 不允许 Day 2 顺手把 Day 3 做完。
5. 不允许 Day 3 继续大改详情页。
```

禁止内容：

```text
1. 不改后端接口。
2. 不接真实 AI。
3. 不接 Figma。
4. 不做编辑器。
5. 不做复杂状态管理。
```

验收命令：

```bash
npm run build
```

核心验收点：

```text
1. SUCCESS 展示预览。
2. FAILED 不展示预览。
3. iframe sandbox=""。
4. 无 allow-scripts。
5. 旧 generation job 查询失败不影响 generated-page 展示。
6. 独立预览页可访问。
```

---

## 7.2 Backend Artifact Test Thread

负责内容：

```text
1. generated-page artifact mock 接口测试。
2. 400 / 404 / 2MB 限制。
3. mock 文件隔离。
4. status=FAILED 保存读取测试。
```

测试依赖要求：

```text
优先使用项目已有 Spring Boot Test / MockMvc 能力。
如缺少测试依赖，先报告，不擅自新增。
```

禁止内容：

```text
1. 不接 MySQL。
2. 不创建数据库表。
3. 不创建 Entity。
4. 不创建 Mapper。
5. 不改接口路径。
6. 不擅自新增复杂测试框架。
```

验收命令：

```bash
mvn test
```

如果项目当前后端测试命令不同，以项目实际命令为准。

核心验收点：

```text
1. PUT 成功。
2. GET 成功。
3. 不存在返回 404。
4. 非法 jobId 返回 400。
5. 超过 2MB 返回 400。
6. 测试不污染真实 mock-data。
```

---

## 7.3 Worker Static Generator Thread

负责内容：

```text
1. 小幅增强 style subset。
2. 保持安全过滤。
3. 补 Worker 测试。
4. 保持 layoutHash 稳定。
```

只允许增强字段：

```text
width
height
padding
margin
borderRadius
backgroundColor
color
fontSize
fontWeight
textAlign
display
flexDirection
gap
objectFit
```

禁止内容：

```text
1. 不做真实截图解析。
2. 不做 AI 生成代码。
3. 不做复杂 grid 推断。
4. 不做响应式算法。
5. 不做 Vue SFC 可运行化。
6. 不做 Tailwind 生成。
7. 不扩大字段范围。
```

验收命令：

```bash
python -m pytest worker
```

如果项目当前 Worker 测试命令不同，以项目实际命令为准。

核心验收点：

```text
1. valid 示例 SUCCESS。
2. invalid 示例 FAILED。
3. HTML escape 通过。
4. script 禁止。
5. inline event 禁止。
6. javascript URL 禁止。
7. 未知 style warning。
8. 不安全 image src warning。
9. layoutHash 稳定。
```

---

## 7.4 Docs & Smoke Thread

负责内容：

```text
1. docs/current.md
2. docs/plan.md
3. docs/task.md
4. docs/spec.md
5. docs/dev-smoke-week05.md
6. docs/archive/week05-summary.md
```

必须修正：

```text
1. Day 6 Worker 命令路径。
2. Day 6 后端启动方式。
3. Day 6 前端 smoke 命令。
4. Day 2 / Day 3 前端任务边界。
5. Day 4 测试依赖要求。
6. Day 5 Worker 增强范围。
```

验收点：

```text
1. 文档能指导别人复现流程。
2. 命令可执行。
3. 验收标准清晰。
4. 禁止事项明确。
5. 和 Week 05 实际成果一致。
```

---

# 8. Week 05 最终交付物清单

Week 05 结束时，建议交付以下内容：

```text
1. 前端任务详情页 generated-page UX 修正
2. generated-page 独立 dev preview 页面
3. 后端 generated-page artifact mock 接口测试
4. Worker 静态编译器 style subset 小幅增强
5. Worker 测试补充
6. docs/dev-smoke-week05.md
7. docs/archive/week05-summary.md
8. 一次完整联调记录
9. 一个清晰的 Git commit
```

推荐最终提交信息：

```text
Complete Week 05 generated page preview stabilization
```

---

# 9. 给 Codex 的 Week 05 总提示词

```text
项目：screenshot-to-responsive-page-generator

当前阶段：
Week 05 - Generated Page 独立预览与质量稳定化。

背景：
Week 04 已完成 Layout JSON 静态编译器 v0.1 与 generated-page artifact 安全预览闭环。当前 generated-page 可以通过后端 mock artifact 接口保存和查询，前端可以展示 htmlCode/cssCode/vueCode、validation 信息和 sandbox iframe 预览。

Week 05 目标：
1. 修正前端任务详情页 UX，使 generated-page 展示不依赖旧 Week 02 generation job 查询结果。
2. 新增 generated-page 独立 dev preview 页面。
3. 为后端 generated-page artifact mock 接口补充自动化测试。
4. 小幅增强 Worker 静态编译器对常见安全 style subset 的支持。
5. 整理 Worker -> Backend -> Frontend 的 Week 05 dev smoke 文档。
6. 完成 Week 05 总结归档。

关键修正要求：
1. Day 6 Worker 命令必须使用：
   python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json

2. 后端 smoke 默认启动方式必须使用：
   cd backend
   mvn package -DskipTests
   java -jar target/backend-0.0.1-SNAPSHOT.jar

3. mvn spring-boot:run 只作为可选方式，不作为默认 smoke 方式。

4. 前端日常 smoke 使用：
   cd frontend
   npm run dev

5. npm install 只放在首次安装依赖部分，不作为每次 smoke 必需步骤。

6. Day 2 和 Day 3 边界必须明确：
   - Day 2 只修正现有详情页 UX
   - Day 3 只新增独立 dev preview 页面
   - 可以复用组件，但不要在 Day 2 顺手完成 Day 3

7. Day 4 后端测试优先使用项目已有 Spring Boot Test / MockMvc 能力。
   如缺少测试依赖，先报告，不擅自新增。

8. Day 5 Worker 只小幅增强列出的 style subset。
   不做布局推断、不做响应式算法、不做 Tailwind、不做 Vue SFC。

严格禁止：
- 不接真实 AI / OpenAI / Claude / Gemini SDK
- 不接 Figma API / Figma MCP
- 不接 MySQL
- 不创建数据库表
- 不创建 Entity / Mapper
- 不接 Redis / RabbitMQ
- 不做 ZIP 导出
- 不做拖拽编辑器 / 在线编辑器
- 不做真实截图解析
- 不做登录注册
- 不要求 vueCode 真正可运行
- 不做 Playwright 视觉回归，除非用户明确批准

协作要求：
- 继续保持 Docs Lite 模式。
- 每天 docs/task.md 只保留当前任务。
- 前端、后端、Worker、文档任务要拆分，不要混在一个大任务里。
- 每个任务开始前先阅读相关文件，再给出计划，再执行。
- 每个任务结束必须给出验收命令、验收结果、风险和未完成项。
```

---

# 10. Week 05 结束后的状态预期

Week 05 完成后，项目状态应该从：

```text
我已经能把 Layout JSON 编译成静态页面并预览。
```

升级为：

```text
我有一个稳定的 generated-page 预览闭环，有后端测试、有 Worker 测试、有前端安全预览、有独立 dev preview 页面、有可复现 smoke 文档。
```

这个阶段完成后，项目更适合继续进入 Week 06。

Week 06 可以考虑的方向包括：

```text
1. 继续增强 Layout JSON 节点和样式表达能力。
2. 补前端自动化测试。
3. 经用户明确批准后，开始规划 MySQL 持久化。
4. 继续完善 Worker -> Backend 的半自动 artifact 流程。
5. 整理实践报告中的系统实现与测试章节。
```

但在 Week 05 内，核心原则仍然是：

```text
先稳住闭环，再考虑扩展。
```

当前项目最需要的是：

```text
稳定、可验收、可复现、可写进实践报告。
```

不是：

```text
功能膨胀。
```