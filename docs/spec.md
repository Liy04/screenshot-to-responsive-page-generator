# Spec

## 文件目的

本文档是 Week 04 当前执行所需核心契约，供 Worker 静态编译器、后端 mock 保存和前端安全预览共用。

Week 04 的“生成”是确定性静态编译，不是真实 AI 生成。

## Layout JSON v0.1 核心结构摘要

Layout JSON 是页面结构中间层，不是 HTML / Vue。

顶层字段：

| 字段 | 说明 |
|---|---|
| `version` | Layout JSON 版本，Week 04 使用 `0.1` |
| `page` | 页面基础信息 |
| `source` | 来源信息，当前主要是 `manual` |
| `tokens` | 设计变量，如颜色、字体、间距、圆角 |
| `layout` | 页面结构树根节点 |
| `assets` | 图片等资源引用 |
| `responsive` | 断点和响应式规则 |
| `assumptions` | 当前无法确认但暂时采用的假设 |
| `warnings` | 可能影响生成质量的风险提示 |

支持节点类型：

```text
page
section
container
text
button
image
card
list
listItem
form
input
```

暂不支持：

```text
table
chart
modal
drawer
carousel
video
map
animation
complex-form
```

## generated-page artifact 字段

`generated-page` artifact 示例字段：

| 字段 | 必填 | 说明 |
|---|---|---|
| `version` | 是 | artifact 契约版本，Week 04 使用 `0.1` |
| `artifactType` | 是 | 固定为 `generated-page` |
| `jobId` | 是 | 任务 id，建议只允许字母、数字、下划线、短横线 |
| `generator.name` | 是 | 固定为 `layout-static-generator` |
| `generator.version` | 是 | 静态编译器版本，Week 04 使用 `0.1` |
| `source.layoutVersion` | 是 | 来自 Layout JSON 的 `version` |
| `source.layoutHash` | 是 | Layout JSON 稳定 hash |
| `source.layoutSourceType` | 是 | Week 04 默认 `manual` |
| `validation.passed` | 是 | validator 是否通过 |
| `validation.errors` | 是 | validator errors，失败时非空 |
| `validation.warnings` | 是 | validator warning 与 generator warning 合并结果 |
| `status` | 是 | `SUCCESS` 或 `FAILED` |
| `htmlCode` | 是 | 可预览 HTML 片段 |
| `cssCode` | 是 | 可预览 CSS 文本 |
| `vueCode` | 是 | Vue 文本展示字段，不要求可运行 |
| `unsupportedNodes` | 是 | 静态编译器未支持节点列表 |
| `createdAt` | 是 | artifact 创建时间 |

## htmlCode / cssCode / vueCode 口径

- `htmlCode`：由 Layout JSON 节点确定性编译得到的 HTML 片段。
- `cssCode`：由支持的 style subset 确定性编译得到的 CSS 文本。
- `vueCode`：只作为展示文本，不要求可运行，不要求构建，不作为 Week 04 验收的可运行产物。

## status 规则

### SUCCESS

满足以下条件时，`status=SUCCESS`：

- Layout JSON validator 通过。
- 静态编译器能输出非空 `htmlCode`。
- 静态编译器能输出非空 `cssCode`。
- `validation.errors` 为空。

### FAILED

validator 失败时，Week 04 统一采用以下口径：

- CLI 仍输出一份 `status=FAILED` 的 `generated-page` artifact。
- `validation.passed=false`。
- `validation.errors` 非空。
- `validation.warnings` 可以保留已有 warning。
- `htmlCode` 为空字符串。
- `cssCode` 为空字符串。
- `vueCode` 为空字符串。
- 命令退出码为 1。
- FAILED artifact 只用于调试和记录失败原因，不用于前端可视化预览。

不要同时写“失败时输出 FAILED artifact”和“失败时不写 artifact”两种口径。

## validation 规则

- `validation.errors` 来自 `worker/layout_validator.py`。
- `validation.errors` 非空时，`status` 必须为 `FAILED`。
- `validation.warnings` 可以合并 validator warning 和 generator warning。
- generator warning 包括未知 style 字段、缺少 image src、暂不支持节点类型、不安全 CSS 值等。

建议 warning 结构：

```json
{
  "code": "UNKNOWN_STYLE_FIELD",
  "message": "style 字段暂不支持",
  "path": "layout.children[0].style.unknown"
}
```

## unsupportedNodes 规则

- 编译器遇到暂不支持节点类型时，不直接渲染为原始 HTML。
- 将节点信息记录到 `unsupportedNodes`。
- 同时可追加 warning。
- 未知节点不能导致注入 HTML、script 或任意属性。

## layoutHash 稳定生成规则

- `source.layoutHash` 用于判断 Layout JSON 是否变更。
- 建议对规范化后的 Layout JSON 生成 SHA-256。
- 规范化建议：按 key 排序、使用稳定 JSON 序列化、去掉运行时无关字段。
- 同一份 Layout JSON 在不同机器上应得到相同 hash。

## Layout JSON 到 HTML/CSS 映射摘要

| Layout JSON 节点 | HTML 输出 | class |
|---|---|---|
| `page` | `div` | `lg-page` |
| `section` | `section` | `lg-section` |
| `container` | `div` | `lg-container` |
| `text` | `h1` / `h2` / `p` / `span` | `lg-text` |
| `button` | `button` | `lg-button` |
| `image` | `img` | `lg-image` |
| `card` | `div` | `lg-card` |
| `list` | `ul` | `lg-list` |
| `listItem` | `li` | `lg-list-item` |
| `form` | `form` | `lg-form` |
| `input` | `input` | `lg-input` |

`text` 节点可按 `role` 和 `level` 选择 `h1`、`h2`、`p` 或 `span`。

## style subset

Week 04 只支持以下 style 字段：

- `backgroundColor`
- `color`
- `fontSize`
- `fontWeight`
- `borderRadius`
- `padding`
- `margin`
- `display`
- `flexDirection`
- `gap`
- `justifyContent`
- `alignItems`

处理规则：

- 已支持字段映射为 CSS。
- 缺失字段跳过。
- 未知 style 字段不报错，但必须写入 warnings。
- CSS 值必须做最小白名单或安全过滤。

## HTML 安全规则

- `text` / `button` content 必须 HTML escape。
- `input` 的 `placeholder` / `value` 必须 HTML escape。
- 禁止输出 `script` 标签。
- 禁止输出 `onclick`、`onload` 等内联事件。
- 禁止输出 `javascript:` URL。
- 禁止把未知字段直接拼进 HTML 属性。
- 未知节点类型不直接渲染为原始 HTML。
- iframe 预览必须使用 `sandbox=""`，不加 `allow-scripts`。

## image 规则

`image.src` 只允许：

- `http://` 或 `https://` URL。
- `/uploads/...` 本地上传资源路径。
- 不含 `../`、`<`、`>` 的安全相对路径。

禁止：

- `javascript:` URL。
- `data:` URL。
- 包含 `<` 或 `>` 的 URL。
- 伪造内联事件的 URL 或属性片段。

如果 image 缺少安全 `src`，可以跳过 `src`，并写入 warning。

## CSS 值安全过滤

建议使用保守规则：

- 颜色只允许 hex、rgb、rgba、常见安全颜色名。
- 长度只允许数字加 `px`、`rem`、`em`、`%`。
- `fontWeight` 只允许 `normal`、`bold`、`100` 到 `900`。
- `display` 只允许 `block`、`inline-block`、`flex`、`grid`、`none`。
- `flexDirection` 只允许 `row`、`row-reverse`、`column`、`column-reverse`。
- `justifyContent` 和 `alignItems` 只允许常见 flex 对齐值。
- CSS 值中禁止 `url(`、`expression(`、`javascript:`、`<`、`>`。
- 不安全值跳过，并写入 warnings。

## 后端 mock 保存摘要

Week 04 后端 mock 接口：

```text
PUT /api/dev/generation-jobs/{jobId}/artifacts/generated-page
GET /api/dev/generation-jobs/{jobId}/artifacts/generated-page
```

- PUT 请求体提交完整 `generated-page` artifact。
- jobId 使用白名单：`^[A-Za-z0-9_-]{1,64}$`。
- artifact JSON 文件大小限制建议为 2MB。
- Week 04 不连接 MySQL，不创建数据库表，不创建 Entity / Mapper。

## 当前边界

- 当前是确定性静态编译器，不是真实 AI 生成。
- 不做真实截图解析。
- 不接真实模型 API。
- 不接 Figma API / Figma MCP。
- 不做 Vue 页面代码生成。
- 不要求 `vueCode` 可运行。
- 不做拖拽编辑器、在线编辑器或 ZIP 导出。
- 不做 Playwright 视觉回归。

## Week 05：generated-page 独立 dev preview 页面规格

Week 05 新增 generated-page 独立 dev preview 页面，用于稳定验证 generated-page artifact 展示链路。

推荐路由：

```text
/dev/generated-page-preview/:jobId
```

页面职责：

- 从路由参数读取 `jobId`。
- 只调用 generated-page artifact GET 接口。
- 展示 generated-page artifact 状态。
- 展示 `htmlCode` / `cssCode` / `vueCode`。
- 展示 `validation.errors` / `validation.warnings`。
- 展示 `unsupportedNodes`。
- 展示 `source.layoutHash`。
- 展示 `generator.name` 和 `generator.version`。
- `status=SUCCESS` 时展示 sandbox iframe 预览。
- `status=FAILED` 时不展示 iframe，只展示失败原因和 validation 信息。

页面不依赖：

- Week 02 generation job 详情接口。
- 旧 mock generation 查询。
- 任务历史记录。
- 数据库。
- 登录状态。

## Week 05：前端预览安全规则

- iframe 必须使用 `sandbox=""`。
- iframe 不允许 `allow-scripts`。
- `status=SUCCESS` 才展示 iframe。
- `status=FAILED` 不展示 iframe。
- `htmlCode` / `cssCode` / `vueCode` 必须作为代码文本可查看。
- `vueCode` 仍只作为文本展示，不要求可运行，不要求构建。
- 页面不得提供拖拽编辑器、在线编辑器或 ZIP 导出。

## Week 05：generated-page 展示状态

generated-page 展示建议区分以下状态：

| 状态 | 含义 |
|---|---|
| `loading` | 正在请求 generated-page artifact |
| `success` | artifact 存在且 `status=SUCCESS` |
| `empty` | artifact 不存在，例如后端返回 404 |
| `failed` | artifact 存在但 `status=FAILED` |
| `error` | 请求异常或非预期错误 |

## Week 05：Worker style subset 增强范围

Week 05 只允许小幅增强以下安全 style subset：

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

增强时必须保持：

- 未知 style 进入 warnings。
- HTML escape 不退化。
- 禁止 script。
- 禁止 inline event。
- 禁止 javascript URL。
- 不安全 image src 进入 warning。
- layoutHash 稳定性不破坏。

明确不做：

- 不做布局推断。
- 不做复杂响应式算法。
- 不做复杂 grid 推断。
- 不做 Tailwind 代码生成。
- 不做动态交互生成。
- 不做可运行 Vue SFC 生成。
- 不做 AI 生成代码。

## Week 05：后端 generated-page mock 接口测试范围

后端测试覆盖：

- PUT 成功保存 generated-page artifact。
- GET 成功读取 generated-page artifact。
- artifact 不存在时返回 404。
- 非法 `jobId` 返回 400。
- 超过 2MB 返回 400。
- `status=FAILED` artifact 可以保存和读取。
- 测试数据隔离，不污染真实 `backend/mock-data`。

实现边界：

- 优先使用项目已有 Spring Boot Test / MockMvc 能力。
- 如缺少测试依赖，先报告，不擅自新增。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
