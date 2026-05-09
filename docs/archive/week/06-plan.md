# Week 06 开发计划验收与最终执行版

项目名称：screenshot-to-responsive-page-generator

当前阶段：Week 01 ~ Week 05 已完成，准备进入 Week 06。

当前最新提交：

```text
d6727bd Complete Week 05 generated page preview stabilization
```

当前项目定位：

本项目是一个“截图 / Figma 到响应式页面生成器”的学习型 MVP 项目。

当前阶段还不是完整 AI 生成器，而是先通过 mock、Layout JSON、静态编译器和安全预览，逐步搭建一个最小可验证闭环。

当前已经完成的核心链路是：

```text
Layout JSON
-> Worker validator 校验
-> Worker static generator 静态编译
-> generated-page artifact
-> 后端 mock 保存 / 查询
-> 前端 sandbox iframe 安全预览
```

Week 06 的核心目标不是继续追求“炫酷功能”，而是让当前已经跑通的 generated-page 预览链路变得更稳定、更好测试、更好演示、更适合写入实践报告。

---

# 一、对原 Week 06 计划的验收结论

## 1. 总体结论

原计划整体合理，可以作为 Week 06 的基础执行方案。

它符合当前项目阶段：

- 没有默认接真实 AI。
- 没有默认接 Figma API / Figma MCP。
- 没有默认接 MySQL。
- 没有默认接 Redis / RabbitMQ。
- 没有默认做 ZIP 导出。
- 没有默认做拖拽编辑器。
- 没有默认做真实截图解析。
- 没有默认做复杂响应式布局算法。
- 优先关注稳定性、测试覆盖、可演示性、实践报告素材。

因此，Week 06 继续围绕 generated-page artifact 进行稳定化，是正确方向。

---

## 2. 原计划合理的地方

### 2.1 主题选择合理

原计划将 Week 06 定位为：

```text
Generated Page 回归稳定性与演示验收增强
```

这个主题是合理的。

原因是 Week 04 已经跑通了 generated-page 静态预览闭环，Week 05 已经完成了独立预览页、后端 mock 接口测试、Worker 安全规则增强和 dev smoke 文档。

所以 Week 06 不应该突然扩展到 AI、Figma、数据库，而应该先把当前闭环打磨稳定。

---

### 2.2 优先级合理

原计划将 Week 06 的重点放在：

```text
1. 前端 generated-page preview 自动化测试
2. Worker 静态编译器小范围增强
3. Worker 编译器回归测试
4. 后端 generated-page artifact 边界测试
5. smoke 文档与实践报告素材整理
6. 总体验收归档
```

这个优先级是合理的。

因为当前项目最需要证明的是：

```text
这个 MVP 虽然还不是完整 AI 生成器，但已经具备稳定的中间层、静态编译、安全预览和测试验证链路。
```

这对于学习、答辩、简历项目展示都很有价值。

---

### 2.3 范围控制基本合理

原计划明确了 Week 06 不做：

```text
不接真实 AI
不接 OpenAI / Claude / Gemini SDK
不接 Figma API / Figma MCP
不接 MySQL
不创建 Entity / Mapper
不接 Redis / RabbitMQ
不做 ZIP 导出
不做拖拽编辑器 / 在线编辑器
不做真实截图解析
不做复杂响应式布局算法
不做 Tailwind 代码生成
不做 Vue SFC 可运行化
```

这个边界非常重要，必须保留。

如果 Week 06 失控去接 MySQL、Figma 或真实 AI，这个项目会从“稳定化阶段”突然变成“架构大改阶段”，风险会明显上升。

---

# 二、原计划需要修正的地方

原计划虽然总体合理，但有几处需要收口，否则 Codex 执行时容易扩范围。

---

## 修正点 1：Day 3 Worker 增强不能同时扩太多节点和样式

原计划中 Day 3 提到可以增强：

```text
section
container
heading
paragraph
button
image
card
list
```

同时又提到可以新增：

```text
justifyContent
alignItems
border
borderColor
borderWidth
lineHeight
maxWidth
minHeight
```

这里有一点风险。

如果一天里同时扩节点类型和样式字段，Codex 很容易把 Worker 改成“小型布局引擎”，导致：

- schema 变复杂；
- 测试变多；
- 文档跟不上；
- 前端展示字段可能不一致；
- Worker 规则变得不好验收。

因此修正为：

```text
Day 3 只允许做“小范围增强”：
- 最多新增 1 到 2 类节点；
- 最多新增 3 到 5 个安全 style 字段；
- 必须同步补测试；
- 不允许引入复杂布局推导。
```

推荐本周只增强这些：

```text
节点能力：
1. card
2. list

样式字段：
1. justifyContent
2. alignItems
3. maxWidth
4. lineHeight
```

如果当前已有 card / list，则不要重复扩展，只补齐测试和文档。

---

## 修正点 2：Day 2 前端测试不要强行引入复杂测试框架

原计划建议补前端 generated-page preview 自动化测试，这是对的。

但需要加一个前提：

```text
先检查 frontend/package.json 中是否已有测试框架。
```

如果已经有 Vitest / Vue Test Utils，就沿用现有方案。

如果没有测试框架，Week 06 可以选择两种方式之一：

```text
方案 A：引入最小 Vitest + Vue Test Utils
方案 B：先写轻量级 smoke 验证脚本，不引入复杂 E2E
```

不要一上来接 Playwright 视觉回归。

Week 06 的前端测试重点不是“截图对比”，而是：

```text
SUCCESS 展示 iframe
FAILED 不展示 iframe
iframe sandbox="" 且无 allow-scripts
validation 信息可展示
代码区域可展示
接口错误状态可展示
```

---

## 修正点 3：Day 5 后端测试不要为了测试而强行改接口契约

原计划提到补这些后端边界测试：

```text
空 body 返回 400
缺少 status 返回 400
status 非法返回 400
htmlCode 超长返回 400
cssCode 超长返回 400
vueCode 超长返回 400
```

方向没问题，但要注意：

如果当前 Controller 并没有定义这些严格校验规则，不能为了测试强行大改接口。

正确做法是：

```text
先阅读当前 generated-page artifact 接口实现；
只测试已经明确存在的接口契约；
如果发现契约不清晰，先补文档，再做最小校验；
不要引入数据库；
不要重构 Controller；
不要改变已有 Week 04 / Week 05 smoke 行为。
```

后端测试的目标是“稳定接口契约”，不是“创造一堆新规则”。

---

## 修正点 4：Day 6 不要提前写归档总结

原计划 Day 6 提到可以整理：

```text
docs/archive/week/06-summary.md
```

这里需要修正。

因为 Week 06 还没结束，Day 6 不应该提前归档总结。

正确做法是：

```text
Day 6：
整理 docs/dev-smoke-week06.md
整理 docs/report-material-week06.md

Day 7：
最终验收后再新增 docs/archive/week/06-summary.md
```

这样更符合 Docs Lite 模式。

---

## 修正点 5：每天任务必须严格单线程

原计划已经说“不要把前端、后端、Worker、测试、文档混成一个任务”，这个是对的。

但执行时还要更严格：

```text
每天 docs/task.md 只写当天一个任务。
当天任务完成后再进入下一个任务。
不要让 Codex 一次性执行 Week 06 全部任务。
```

这点非常关键。

因为你现在是在学习 Codex 的 vibe coding 开发方式，重点不是让 Codex 一口气干完，而是训练自己掌控节奏：

```text
先计划
再编码
再测试
再总结
再提交
```

---

# 三、Week 06 最终推荐结论

最终建议：

```text
Week 06 可行。
Week 06 应该执行。
Week 06 不应该扩展到真实 AI / Figma / MySQL。
Week 06 应该优先做稳定性、测试覆盖、可演示性、实践报告素材。
```

最终主题建议定为：

```text
Week 06：Generated Page 回归稳定性与演示验收增强
```

更通俗一点也可以叫：

```text
Week 06：让生成页预览更稳定、更好测、更好展示
```

---

# 四、Week 06 最终执行版计划

## 1. Week 06 总目标

Week 06 的目标是围绕 generated-page artifact，继续增强当前 MVP 的稳定性、测试覆盖和演示能力。

本周不追求新大功能，而是让当前已有闭环更可靠：

```text
Layout JSON
-> Worker validator
-> Worker static generator
-> generated-page artifact
-> 后端 mock 保存 / 查询
-> 前端 sandbox iframe 预览
```

最终要达到：

```text
1. 前端 generated-page preview 有基础自动化测试。
2. Worker 静态编译器有更完整的回归测试。
3. Worker 可小范围增强 1 到 2 类基础节点或少量安全样式。
4. 后端 generated-page artifact 接口边界测试更完整。
5. Week 06 smoke 流程清晰可复现。
6. 能整理出可写入实践报告的素材。
```

---

## 2. Week 06 不做事项

Week 06 严格禁止默认做以下内容：

```text
不接真实 AI
不接 OpenAI / Claude / Gemini SDK
不接 Figma API
不接 Figma MCP
不接 MySQL
不创建数据库表
不创建 Entity
不创建 Mapper
不接 Redis
不接 RabbitMQ
不做 ZIP 导出
不做拖拽编辑器
不做在线编辑器
不做真实截图解析
不做登录注册
不做复杂权限
不做 Playwright 视觉回归
不做复杂响应式布局算法
不做 Tailwind 代码生成
不做 Vue SFC 可运行化
```

如果要进入 MySQL、真实 AI、Figma 或 ZIP 导出，必须单独开 Week 07 或后续专题，并由用户明确批准。

---

# 五、Week 06 每日计划

---

## Day 1：整理 Week 06 文档与任务边界

### 目标

只整理文档，不改代码。

目的是让项目上下文清楚 Week 06 做什么、不做什么，避免后续执行时扩范围。

### 修改范围

只允许修改：

```text
AGENTS.md
docs/current.md
docs/plan.md
docs/task.md
docs/spec.md
可选新增：docs/week-06.md
```

不允许修改：

```text
frontend/
backend/
worker/
```

### 任务内容

1. 更新当前阶段为 Week 06。
2. 明确 Week 06 主题：generated-page 回归稳定性与演示验收增强。
3. 明确 Week 06 不接真实 AI、不接 Figma、不接 MySQL、不接 Redis / RabbitMQ。
4. 在 docs/task.md 中只保留当前一个任务。
5. 如新增 docs/week-06.md，则作为 Week 06 原始计划源文件。
6. docs/archive/ 只做历史归档，不作为默认上下文。

### 验收标准

完成后应满足：

```text
1. docs/current.md 能说明当前项目状态。
2. docs/plan.md 能看到 Week 06 目标。
3. docs/task.md 只保留 Day 1 当前任务。
4. 文档明确禁止本周扩展到 AI / Figma / MySQL / Redis / RabbitMQ。
5. 未修改任何业务代码。
```

---

## Day 2：补前端 generated-page preview 基础测试

### 目标

为前端 generated-page 独立预览页补基础测试，重点验证页面状态和安全 iframe 行为。

当前已有独立预览路由：

```text
/dev/generated-page-preview/:jobId
```

Week 05 已经实现页面，但还缺系统性的前端自动化测试。

### 修改范围

只允许修改：

```text
frontend/
```

可根据项目情况新增：

```text
frontend/src/views/__tests__/GeneratedPagePreviewDev.test.js
```

或当前测试规范对应的目录。

不允许修改：

```text
backend/
worker/
docs/archive/
```

### 执行前检查

先检查：

```text
frontend/package.json
```

确认是否已有测试框架。

如果已有 Vitest / Vue Test Utils：

```text
沿用现有测试框架。
```

如果没有测试框架：

```text
优先考虑最小引入 Vitest + Vue Test Utils。
不要引入 Playwright 视觉回归。
不要引入复杂 E2E。
```

### 测试重点

至少覆盖：

```text
1. SUCCESS 状态展示 iframe。
2. FAILED 状态不展示 iframe。
3. iframe 使用 sandbox=""。
4. iframe 不包含 allow-scripts。
5. validation.errors 可以展示。
6. validation.warnings 可以展示。
7. unsupportedNodes 可以展示。
8. htmlCode 可以展示。
9. cssCode 可以展示。
10. vueCode 可以展示。
11. 接口 404 或错误时页面显示 error/empty 状态。
```

### 验收标准

完成后应满足：

```text
1. 前端测试可以运行。
2. npm run build 通过。
3. SUCCESS / FAILED 两条主路径有测试覆盖。
4. iframe 安全属性有测试覆盖。
5. 不修改后端。
6. 不修改 Worker。
7. 不做 Playwright 视觉回归。
```

---

## Day 3：Worker 静态编译器小范围增强

### 目标

在不扩大成复杂布局引擎的前提下，小幅增强 Worker 静态编译器。

本日只允许做“小改动”，不允许大范围扩展 Layout JSON。

### 修改范围

只允许修改：

```text
worker/layout_static_generator.py
worker/test_layout_static_generator.py
必要时可修改 worker 相关示例文件
```

不允许修改：

```text
frontend/
backend/
docs/archive/
```

### 推荐增强内容

本周只建议从下面内容中选择很少一部分。

推荐新增或完善节点：

```text
1. card
2. list
```

推荐新增安全 style 字段：

```text
1. justifyContent
2. alignItems
3. maxWidth
4. lineHeight
```

注意：

```text
最多新增 1 到 2 类节点。
最多新增 3 到 5 个安全 style 字段。
```

如果当前已经支持 card / list，则不要重复扩展，只补齐行为一致性和测试。

### 不允许做

```text
不做复杂响应式布局算法
不做 grid 自动推导
不做自动断点推导
不做拖拽布局
不做动态交互
不做表单提交
不做脚本执行
不做 Tailwind 生成
不做 Vue SFC 可运行化
不扩大成复杂组件系统
```

### 安全规则必须保持

必须继续保持：

```text
HTML escape
禁止 script
禁止 inline event
禁止 javascript URL
不安全 image src warning
未知 style warning
layoutHash 稳定性
```

### 验收标准

完成后应满足：

```text
1. Worker unittest 通过。
2. 原有 valid 示例仍然 SUCCESS。
3. 原有 invalid 示例仍然 FAILED。
4. 新增节点或样式有测试覆盖。
5. 不安全内容仍然会被拦截或产生 warning。
6. layoutHash 稳定性不破坏。
7. 未修改前端。
8. 未修改后端。
```

---

## Day 4：补 Worker 编译器回归测试

### 目标

Day 4 只补测试，不继续扩功能。

如果 Day 3 已经做了 Worker 小范围增强，那么 Day 4 用来把测试补完整，避免 Worker 后续改动时回归。

### 修改范围

只允许修改：

```text
worker/test_layout_static_generator.py
worker/test_layout_validator.py
必要时可新增 worker 测试样例
```

不允许修改：

```text
frontend/
backend/
```

除非测试无法通过，且是 Day 3 引入的小问题，才允许做最小修复。

### 测试重点

建议覆盖：

```text
1. 新增 style 字段允许通过。
2. 未知 style 字段产生 warning。
3. script 标签被 escape 或禁止。
4. inline event 被禁止。
5. javascript URL 被禁止。
6. image src 不安全时产生 warning。
7. unsupportedNodes 正确记录。
8. valid layout 输出 SUCCESS。
9. invalid layout 输出 FAILED。
10. layoutHash 对同一输入保持稳定。
11. FAILED 状态下 htmlCode / cssCode / vueCode 行为符合当前规则。
12. SUCCESS 状态下 generated-page artifact 字段完整。
```

### 验收标准

完成后应满足：

```text
1. Worker 测试数量增加。
2. 所有 Worker 测试通过。
3. 每个测试只验证一个核心行为。
4. 测试名称清晰可读。
5. 测试结果可以写进实践报告。
6. 不修改前端。
7. 不修改后端。
```

---

## Day 5：补后端 generated-page artifact 边界测试

### 目标

增强后端 generated-page artifact mock 接口的边界测试覆盖。

注意：本日不接 MySQL，不创建 Entity / Mapper，不做真实持久化。

### 修改范围

只允许修改：

```text
backend/src/test/java/com/screenshot/generator/backend/layout/GeneratedPageArtifactControllerTest.java
必要时可做极小 Controller 校验修复
```

不允许修改：

```text
frontend/
worker/
数据库相关代码
Entity
Mapper
MyBatis-Plus 配置
```

### 执行前检查

先阅读当前接口实现和已有测试，确认当前接口契约。

不要为了测试强行创造新规则。

如果某些字段当前没有明确校验规则，处理方式应是：

```text
优先补文档说明；
必要时做最小校验；
不能破坏 Week 04 / Week 05 已有 smoke 行为。
```

### 建议测试内容

优先测试已经明确的行为：

```text
1. PUT 成功保存。
2. GET 成功读取。
3. artifact 不存在返回 404。
4. 非法 jobId 返回 400。
5. 超过 2MB 返回 400。
6. status=FAILED artifact 可以保存和读取。
7. unsupportedNodes 为空数组时行为正确。
8. validation.errors / validation.warnings 为空数组时行为正确。
9. 缺少明显必填字段时返回合理错误。
10. 非法 status 返回合理错误。
```

### 验收标准

完成后应满足：

```text
1. mvn test 通过。
2. generated-page artifact controller 测试覆盖更完整。
3. 没有引入 Entity。
4. 没有引入 Mapper。
5. 没有接 MySQL。
6. 没有接 Redis / RabbitMQ。
7. 没有修改前端。
8. 没有修改 Worker。
9. 没有破坏已有 PUT / GET 接口路径。
```

---

## Day 6：整理 Week 06 smoke 流程与实践报告素材

### 目标

Day 6 只整理文档，不写功能代码。

本日重点是把 Week 06 的演示流程和实践报告素材沉淀下来。

### 修改范围

只允许修改或新增：

```text
docs/dev-smoke-week06.md
docs/report-material-week06.md
docs/current.md
docs/plan.md
docs/task.md
```

不建议 Day 6 提前新增：

```text
docs/archive/week/06-summary.md
```

因为 Week 06 还没有最终验收，归档总结应放到 Day 7。

### smoke 文档应覆盖

```text
1. Worker valid -> SUCCESS。
2. Worker invalid -> FAILED。
3. 后端 PUT 保存 generated-page artifact。
4. 后端 GET 读取 generated-page artifact。
5. 前端任务详情页展示 generated-page。
6. 前端独立 preview 页面展示 generated-page。
7. SUCCESS 展示 iframe。
8. FAILED 不展示 iframe。
9. iframe sandbox=""，无 allow-scripts。
10. 前端 build 通过。
11. 后端 mvn test 通过。
12. Worker unittest 通过。
13. 8080 被占用时使用 18080 备用端口。
14. Vite 使用 VITE_API_PROXY_TARGET 切换后端代理。
```

### 实践报告素材应覆盖

```text
1. generated-page artifact 数据结构说明。
2. Worker 静态编译器设计。
3. Layout JSON 校验设计。
4. 安全预览 iframe sandbox 设计。
5. 后端 mock artifact 接口设计。
6. 前端独立预览页设计。
7. SUCCESS / FAILED 状态处理设计。
8. 测试用例设计。
9. 当前系统限制。
10. 后续扩展方向。
```

### 验收标准

完成后应满足：

```text
1. docs/dev-smoke-week06.md 可按步骤复现。
2. docs/report-material-week06.md 可直接用于实践报告素材。
3. 文档明确说明当前仍是学习型 MVP。
4. 文档明确说明尚未接真实 AI / Figma / MySQL。
5. 未修改前端、后端、Worker 业务代码。
6. 未提前归档 Week 06 summary。
```

---

## Day 7：Week 06 总体验收、归档与提交

### 目标

Day 7 只做收尾验收和归档，不开发新功能。

### 修改范围

允许修改：

```text
docs/current.md
docs/plan.md
docs/task.md
docs/archive/week/06-summary.md
```

必要时允许做极小修复，但不能开新功能。

### 最终验收命令

至少运行：

```bash
# Worker
python -m unittest worker.test_layout_validator worker.test_layout_static_generator

# 后端
mvn test

# 前端
npm run build
```

如果 Day 2 引入了前端测试命令，还要运行：

```bash
npm run test
```

或项目实际配置的测试命令。

### 最终 smoke 验收

按 `docs/dev-smoke-week06.md` 检查：

```text
1. Worker valid -> SUCCESS。
2. Worker invalid -> FAILED。
3. 后端 generated-page PUT 成功。
4. 后端 generated-page GET 成功。
5. 前端独立 preview 页面可访问。
6. SUCCESS 展示 iframe。
7. FAILED 不展示 iframe。
8. iframe sandbox=""。
9. iframe 无 allow-scripts。
10. 前端 build 通过。
11. 后端测试通过。
12. Worker 测试通过。
```

### 归档内容

新增：

```text
docs/archive/week/06-summary.md
```

归档内容包括：

```text
1. Week 06 阶段目标。
2. 完成内容。
3. 测试命令与结果。
4. smoke 验收结果。
5. 当前仍未做的事项。
6. 已知风险。
7. Week 07 可选方向。
```

### docs/task.md 处理

Week 06 完成后，`docs/task.md` 应更新为：

```text
当前任务：Week 06 已完成，等待用户确认 Week 07 方向。
```

或只保留下一个明确任务。

不要在 docs/task.md 中堆多个未来任务。

### 推荐提交信息

```text
Complete Week 06 generated page regression stabilization
```

或者：

```text
Complete Week 06 generated-page stability and test coverage
```

---

# 六、Week 06 最终交付物清单

Week 06 结束时，建议至少具备这些交付物：

```text
docs/week-06.md
docs/dev-smoke-week06.md
docs/report-material-week06.md
docs/archive/week/06-summary.md
前端 generated-page preview 基础测试
Worker 静态编译器回归测试
后端 generated-page artifact 边界测试
更新后的 docs/current.md
更新后的 docs/plan.md
更新后的 docs/task.md
```

如果 Day 3 做了 Worker 小范围增强，还应有：

```text
新增或完善的 card / list 节点处理
新增或完善的安全 style subset
对应 Worker unittest
```

---

# 七、Week 06 最终验收标准

Week 06 不能只看“代码写完了没有”，而要看下面这些是否都满足。

## 1. 文档验收

```text
1. docs/current.md 已更新到 Week 06 状态。
2. docs/plan.md 已记录 Week 06 计划。
3. docs/task.md 始终只保留当前一个任务。
4. docs/dev-smoke-week06.md 可复现演示流程。
5. docs/report-material-week06.md 可用于实践报告。
6. docs/archive/week/06-summary.md 只在最终验收后新增。
```

## 2. 前端验收

```text
1. /dev/generated-page-preview/:jobId 页面仍可访问。
2. SUCCESS 状态展示 iframe。
3. FAILED 状态不展示 iframe。
4. iframe sandbox=""。
5. iframe 无 allow-scripts。
6. validation.errors / warnings 可展示。
7. unsupportedNodes 可展示。
8. htmlCode / cssCode / vueCode 可展示。
9. npm run build 通过。
10. 前端测试通过，如已配置。
```

## 3. Worker 验收

```text
1. valid layout 输出 SUCCESS。
2. invalid layout 输出 FAILED。
3. HTML escape 保持有效。
4. script 被禁止或安全处理。
5. inline event 被禁止。
6. javascript URL 被禁止。
7. 不安全 image src 有 warning。
8. 未知 style 有 warning。
9. unsupportedNodes 正确记录。
10. layoutHash 保持稳定。
11. Worker unittest 通过。
```

## 4. 后端验收

```text
1. generated-page artifact PUT 成功。
2. generated-page artifact GET 成功。
3. artifact 不存在返回 404。
4. 非法 jobId 返回 400。
5. 超过大小限制返回 400。
6. FAILED artifact 可以保存和读取。
7. mvn test 通过。
8. 未接 MySQL。
9. 未创建 Entity / Mapper。
10. 未接 Redis / RabbitMQ。
```

## 5. 范围验收

Week 06 必须确认没有做以下事情：

```text
没有接真实 AI。
没有接 Figma API / MCP。
没有接 MySQL。
没有创建数据库表。
没有创建 Entity。
没有创建 Mapper。
没有接 Redis。
没有接 RabbitMQ。
没有做 ZIP 导出。
没有做拖拽编辑器。
没有做真实截图解析。
没有做复杂响应式布局算法。
没有做 Tailwind 代码生成。
没有做 Vue SFC 可运行化。
```

---

# 八、Week 06 风险与控制方式

## 风险 1：Worker 增强范围扩大

### 表现

可能会尝试一次性支持很多节点和样式，导致 Worker 变复杂。

### 控制方式

```text
最多新增 1 到 2 类节点。
最多新增 3 到 5 个安全 style 字段。
当天必须补测试。
不做复杂布局推导。
```

---

## 风险 2：前端测试引入过重工具

### 表现

为了测 preview 页面，引入 Playwright、视觉回归、大量 E2E 配置。

### 控制方式

```text
Week 06 不做 Playwright 视觉回归。
优先 Vitest / Vue Test Utils。
测试重点是状态展示和 iframe 安全属性。
```

---

## 风险 3：后端测试导致接口大改

### 表现

为了让测试更完整，强行修改 Controller、DTO、接口行为。

### 控制方式

```text
先确认已有接口契约。
只做最小边界测试。
不破坏 Week 04 / Week 05 smoke。
不引入数据库。
```

---

## 风险 4：文档和代码不同步

### 表现

代码增强了，但 docs/spec.md、docs/current.md、docs/dev-smoke-week06.md 没更新。

### 控制方式

```text
每个任务完成后更新当前文档。
Day 6 专门整理 smoke 和报告素材。
Day 7 统一归档。
```

---

## 风险 5：Week 06 被扩展成数据库改造周

### 表现

突然开始建表、写 Entity、Mapper、Service，导致主线偏移。

### 控制方式

```text
Week 06 不接 MySQL。
MySQL 只能作为 Week 07 可选方向。
必须用户单独批准后再进入。
```

---

# 九、为什么 Week 06 不建议接 MySQL

你当前会 Java、Spring Boot、MyBatis-Plus、MySQL，所以接 MySQL 从能力上不是问题。

但是 Week 06 不建议接 MySQL，原因是当前阶段重点不是持久化，而是稳定当前 generated-page 闭环。

当前最需要解决的问题是：

```text
1. generated-page 预览是否稳定。
2. Worker 编译规则是否可靠。
3. 前端状态展示是否清晰。
4. 后端接口契约是否稳。
5. smoke 流程是否可复现。
6. 实践报告素材是否完整。
```

MySQL 解决的是：

```text
artifact 如何长期保存
generation job 如何持久化
后续如何查询历史记录
```

这些当然重要，但不是 Week 06 的最高优先级。

如果现在接 MySQL，会额外引入：

```text
数据库表设计
Entity
Mapper
Service
Controller 改造
mock 数据迁移
测试数据清理
事务处理
本地环境配置
文档更新
```

这会把 Week 06 从“稳定性增强周”变成“数据库改造周”。

因此建议：

```text
Week 06：稳定性、测试覆盖、演示验收、报告素材
Week 07：如用户批准，再考虑 MySQL 持久化
```

---

# 十、Week 07 可选方向

Week 06 完成后，Week 07 可以从以下方向中选择一个。

注意：一次只选一个方向，不要混着做。

---

## 方向 A：MySQL 持久化

适合目标：

```text
强化 Java 后端能力
强化 MyBatis-Plus 能力
让项目更像完整后端项目
```

可能内容：

```text
generation_job 表
generation_artifact 表
design_source 表
MyBatis-Plus Entity
Mapper
Service
Controller mock 存储迁移
后端接口测试改造
```

前提：

```text
必须用户明确批准。
```

---

## 方向 B：前端演示体验增强

适合目标：

```text
让项目更适合作品集展示
让页面更好看
让演示更顺畅
```

可能内容：

```text
更好的任务列表页
更好的 artifact 详情页
代码复制按钮
预览区域布局优化
SUCCESS / FAILED 状态展示优化
演示样例入口
```

---

## 方向 C：实践报告优先

适合目标：

```text
把项目沉淀为求职 / 实习 / 答辩材料
```

可能内容：

```text
系统架构说明
模块设计说明
接口设计说明
测试报告
阶段性迭代记录
项目难点与解决方案
项目截图整理
```

---

## 方向 D：真实 AI / Figma 预研

适合目标：

```text
为后续真正进入 AI 生成器做准备
```

可能内容：

```text
OpenAI / Claude API 调研
Figma API 调研
Figma MCP 可行性验证
截图到 Layout JSON 的 prompt 设计
少量离线样例验证
```

注意：

```text
这只是预研，不应直接接入主链路。
```

---

# 十一、最终推荐执行路线

最终建议按下面顺序执行 Week 06：

```text
Day 1：文档计划与任务边界
Day 2：前端 preview 基础测试
Day 3：Worker 小范围增强
Day 4：Worker 回归测试
Day 5：后端 artifact 边界测试
Day 6：smoke 文档与实践报告素材
Day 7：总体验收、归档、提交
```

这个顺序最稳。

原因是：

```text
1. 先定边界，避免任务乱扩展。
2. 先补前端测试，稳定演示入口。
3. 再小幅增强 Worker，提升 generated-page 表达力。
4. 然后补 Worker 回归测试，防止后续破坏规则。
5. 再补后端边界测试，稳定 artifact 接口契约。
6. 最后整理 smoke 和报告素材，让项目可演示、可总结。
7. 最终验收归档，准备 Week 07。
```

---

# 十二、执行建议

使用 Codex 时，不要一次性把整份 Week 06 计划丢进去让它全部做。

正确方式是：

```text
每天只给一个 Day 任务。
每次只开一个线程。
每次先读 AGENTS.md、docs/current.md、docs/plan.md、docs/task.md。
每次先复述当前任务边界。
再改代码。
最后必须跑测试。
测试通过后再提交。
```

推荐日常节奏：

```text
1. 先读当前文档。
2. 输出执行计划。
3. 确认计划没有越界。
4. 修改代码或文档。
5. 运行测试。
6. 总结改动。
7. 检查 git diff。
8. 通过后提交。
```

这个节奏比“一口气写完所有东西”更适合学习 vibe coding。

---

# 十三、最终结论

Week 06 计划经过验收后，结论如下：

```text
可行。
合理。
建议执行。
但必须严格控制范围。
```

最终执行原则：

```text
不要追新功能。
不要接真实 AI。
不要接 Figma。
不要接 MySQL。
不要做 ZIP。
不要做拖拽编辑器。
不要做复杂响应式算法。
```

Week 06 真正要完成的是：

```text
让当前 generated-page MVP 闭环更稳定。
让前端 preview 更好测。
让 Worker 编译器更可靠。
让后端 artifact 接口契约更清楚。
让 smoke 流程可复现。
让实践报告有素材可写。
```

这才是当前最适合本项目的路线。