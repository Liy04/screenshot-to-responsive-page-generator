# Spec

## 文件目的

本文档记录当前 generated-page MVP 闭环仍有效的核心契约，并补充 Week 07 / Week 08 mock 协议与 Week 09 真实 AI 最小接入契约，供 Worker、后端 mock / 真实链路和前端预览共用。

当前 Week 09 已允许真实 AI 生成布局中间结果；但对外仍以 Layout JSON v0.1 为契约，`previewHtml` 仍由 Worker 的确定性静态编译器生成，不直接把模型原始输出当页面代码使用。

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

## Week 06 相关补充

Week 06 在不改变现有接口契约的前提下，只做稳定性和验收增强。

### generated-page preview 安全规则

- `iframe` 必须使用 `sandbox=""`。
- `iframe` 不允许 `allow-scripts`。
- `status=SUCCESS` 时展示 `iframe`。
- `status=FAILED` 时不展示 `iframe`，只展示失败原因和 validation 信息。

### Worker 小范围增强边界

- 只允许小范围增强少量安全节点或安全 style subset。
- 不扩成复杂布局引擎。
- 不做复杂响应式布局算法。
- 不做 Tailwind 代码生成。
- 不做 Vue SFC 可运行化。

### 前端测试关注点

- `SUCCESS` / `FAILED` 状态展示是否清晰。
- `validation.errors` / `validation.warnings` 是否可展示。
- `unsupportedNodes` 是否可展示。
- `htmlCode` / `cssCode` / `vueCode` 是否可查看。
- `iframe` 的安全属性是否符合约定。

### 后端边界测试要求

- 边界测试不应改变接口契约。
- 仍保持 generated-page artifact 的 PUT / GET 路径不变。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。

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

## Week 07：image-to-layout mock 协议

Week 07 目标是把“本地图片选择 -> templateKey -> mock Layout JSON”这条链路定义清楚，但仍不接真实 AI、不接真实图片上传、不让后端调用 Python Worker。

### 协议目标

- 前端只负责本地选择图片并显示浏览器本地预览。
- 后端只接收 `imageName` 和 `templateKey`。
- Worker 的 `image_layout_resolver.py` 只作为离线 / 本地 mock resolver。
- 后端 Week 07 不调用 Python Worker，使用 Java 侧 mock 模板或固定 mock 数据返回。

### 支持的 templateKey

Week 07 至少建议支持以下模板键：

- `landing-basic`
- `card-list`
- `invalid-layout`

可选再补：

- `dashboard-simple`

### 请求接口

```text
POST /api/dev/image-layout-jobs
GET  /api/dev/image-layout-jobs/{jobId}
```

### 成功响应包装

后端响应必须使用现有 `ApiResponse` 包装。成功示例：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "img-layout-001",
    "status": "SUCCESS",
    "sourceType": "IMAGE_TEMPLATE_MOCK",
    "imageName": "demo-home.png",
    "templateKey": "landing-basic",
    "layoutArtifact": {
      "status": "SUCCESS",
      "layoutJson": {
        "version": "0.1",
        "page": {},
        "source": {},
        "tokens": {},
        "layout": {},
        "assets": [],
        "responsive": {},
        "assumptions": [],
        "warnings": []
      }
    },
    "errors": [],
    "warnings": []
  }
}
```

### 错误响应包装

请求参数错误时返回 400，示例：

```json
{
  "code": 400,
  "message": "Unknown templateKey: unknown-template",
  "data": null
}
```

### Layout JSON 结构要求

- Week 07 返回的 `layoutJson` 必须继续使用当前 v0.1 结构。
- 根节点字段必须是 `layout`，不能改成 `root`。
- 至少应包含当前 v0.1 必需顶层字段：`version`、`page`、`source`、`tokens`、`layout`、`assets`、`responsive`、`assumptions`、`warnings`。

### templateKey 口径

- `unknown templateKey` 属于请求参数错误，后端返回 400。
- `invalid-layout` 是已知测试模板，用于返回失败状态或错误展示。
- `invalid-layout` 不等同于 `unknown templateKey`，不要把它写成 400 和 FAILED 两种互相冲突的口径。
- 不要在同一计划里同时写 `unknown templateKey` 既可 FAILED 又可 400。
- `invalid-layout` 的返回仍然可以包在 `ApiResponse` 的 200 响应里，`data.status` 为 `FAILED`，`layoutArtifact.status` 也为 `FAILED`。

### Worker / Backend 职责边界

- `worker/image_layout_resolver.py` 只做 templateKey 到 Layout JSON fixture 的离线解析。
- 后端 Week 07 不调用 Python Worker。
- 后端 dev mock API 使用 Java 侧 mock 模板或固定 mock 数据返回。
- 两边通过相同 templateKey 和文档协议保持一致。

### 兼容性要求

- 不接真实 AI。
- 不接 Figma。
- 不接 MySQL。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不做真实图片上传到后端。
- 不做 ZIP 导出。
- 不做拖拽编辑器。
- 不做真实截图解析。

## Week 08：image-page mock 协议

Week 08 目标是把 Week 07 的 image-to-layout mock 链路推进到 image-page mock 链路，但仍只做 mock / 本地验证，不接真实 AI、不接 Figma、不接 MySQL。

### 协议目标

- 前端只负责本地选择图片、浏览器本地预览和选择 `templateKey`。
- 后端只接收 `imageName` 和 `templateKey`，不接真实图片文件。
- 后端使用 Java 侧 mock，不调用 Python Worker。
- `layoutArtifact` 和 `generatedPageArtifact` 一起返回，供前端展示和预览。
- 后端响应继续使用现有 `ApiResponse` 包装，`unknown templateKey` 返回 `code=400`，不存在 `jobId` 返回 `code=404`。

### 请求接口

```text
POST /api/dev/image-page-jobs
GET  /api/dev/image-page-jobs/{jobId}
```

### 请求体

```json
{
  "imageName": "string",
  "templateKey": "string"
}
```

### 成功响应字段

| 字段 | 说明 |
|---|---|
| `jobId` | mock job id |
| `status` | `SUCCESS` 或 `FAILED` |
| `sourceType` | 固定 `IMAGE_TEMPLATE_MOCK` |
| `imageName` | 请求中的图片名 |
| `templateKey` | 请求中的模板键 |
| `layoutArtifact` | Layout JSON mock 结果 |
| `generatedPageArtifact` | generated-page mock 结果 |
| `errors` | 错误列表 |
| `warnings` | 警告列表 |

### layoutArtifact 口径

- `layoutArtifact.status=SUCCESS` 时应包含可用 `layoutJson`。
- `layoutArtifact.status=FAILED` 时应包含失败原因或错误信息。
- `layoutJson` 继续使用当前 v0.1 结构，根节点字段必须是 `layout`。

### generatedPageArtifact 口径

- `generatedPageArtifact` 至少应包含 `status`、`htmlCode`、`cssCode`、`vueCode`。
- `SUCCESS` 时 `generatedPageArtifact` 不为空，并应展示给前端。
- `FAILED` 时 `generatedPageArtifact` 为空、`null` 或不返回。
- `generatedPageArtifact` 仍然必须遵守当前 HTML 安全规则。

### 状态与错误口径

- `landing-basic` 和 `card-list` 返回 `200 + SUCCESS`。
- `invalid-layout` 返回 `200 + FAILED`。
- `unknown templateKey` 返回 HTTP 400，并且 `ApiResponse.code=400`。
- 不存在 `jobId` 返回 HTTP 404，并且 `ApiResponse.code=404`。

### 安全规则

- `generatedPageArtifact` 不包含 `script`。
- 不包含 `onclick`、`onerror`、`onload`、`javascript:`。
- 前端 iframe 必须使用 `sandbox=""`。
- iframe 不允许 `allow-scripts`。

### 职责边界

- Backend 使用 Java 侧 mock，不调用 Python Worker。
- Worker 仍保留现有 resolver / validator / static generator。
- Frontend 只上传 `imageName` + `templateKey`，不上传真实图片文件。

## Week 09：真实 AI 最小接入契约

Week 09 在不推翻现有 generated-page / Week 07 / Week 08 契约的前提下，增加真实单图链路的最小协议。

### 真实链路接口

```text
POST /api/image-page/upload
GET /api/image-page/jobs/{jobId}/source
POST /api/image-page/jobs/{jobId}/generate
```

### 迁移口径

- Week 09 新真实链路接口是新增实现。
- Week 08 `/api/dev/image-page-jobs*` 先保留，用于回退和对照。
- 不要求 Day 2 / Day 6 直接删除旧 dev mock 接口。

### 输入边界

- 只支持单张图片。
- 只支持 `png` / `jpg` / `jpeg` / `webp`。
- 文件最大 5MB。
- 不支持多文件、`zip`、`pdf`、`gif`、`svg`。

### Worker 主链路

```text
单张真实图片
-> 后端保存临时文件
-> 后端生成 jobId
-> 后端调用 Python Worker
-> Worker 读取真实图片
-> Worker 调真实 AI
-> AI 输出先映射为当前 Layout JSON v0.1
-> validator 校验
-> 校验失败轻量修正或 fallback
-> compiler 输出 generated.html
-> 后端返回 layoutJson + previewHtml
-> 前端展示原图、Layout JSON 和 iframe 预览
```

### Layout JSON 口径

- Week 09 继续沿用当前 Layout JSON v0.1 主结构。
- AI 如果存在简化输出，只能作为 Worker 内部中间态。
- 对外契约仍然是当前 v0.1，根节点字段仍是 `layout`。

### 安全规则

- 模型原始输出不能直接给前端。
- 不能让模型直接输出 HTML 给前端使用。
- generated.html 禁止 `script`、`onload`、`onerror`、`onclick`、`iframe`、`object`、`embed`。
- 所有文本要 HTML escape。
- iframe 必须 `sandbox=""`。
- 不允许 `allow-scripts`。
- 不返回后端本地 `imagePath` 给前端。
- `jobId` 必须防路径穿越。

### fallback 规则

- AI 失败可 fallback。
- validator 失败可 fallback。
- fallback 仍必须产出当前 v0.1 合法 Layout JSON。

### generated-page 输出

- Week 09 后端最终返回的结果以 `layoutJson + previewHtml` 为主。
- `previewHtml` 仍只用于 iframe 静态预览，不要求可编辑。

### 运行配置要求

- `OPENAI_BASE_URL` 必须通过环境变量提供；当前已验证可用供应商入口是 `https://api.siliconflow.cn/v1`。
- `OPENAI_MODEL` 必须通过环境变量提供；当前已验证命中模型是 `Qwen/Qwen3-VL-32B-Instruct`。
- `OPENAI_API_KEY` 只允许通过环境变量提供，不写入仓库、不写入文档真实值。
- `IMAGEPAGE_WORKER_PYTHON_COMMAND` 必须指向可用的 Python 3.11+ 解释器；当前已验证路径是 `D:\\environment\\python11\\python.exe`。
- Python 3.11+ 推荐；当前已验证版本是 `Python 3.11.9`。
- `imagepage.worker.timeout-seconds` 建议使用 `120`；默认 30 秒不适合真实多模态调用。

### 最终 smoke 可复现条件

- Week 09 最终通过的 REAL_AI 闭环依赖以下条件同时满足：
  - `OPENAI_BASE_URL=https://api.siliconflow.cn/v1`
  - `OPENAI_MODEL=Qwen/Qwen3-VL-32B-Instruct`
  - `OPENAI_API_KEY` 已通过环境变量设置，但不得写入仓库或文档真实值
  - `IMAGEPAGE_WORKER_PYTHON_COMMAND=D:\\environment\\python11\\python.exe`
  - Python 版本为 `3.11.9`
  - backend 启动参数带 `--imagepage.worker.timeout-seconds=120`
- 默认 30 秒超时不适合 Week 09 真实多模态调用。
- 如果缺少 `OPENAI_*` 环境变量、Python 版本不符、Worker 路径错误或 timeout 不足，结果可能 fallback 或直接失败。
- 最终通过口径是：
  - `status=SUCCESS`
  - `mode=real-ai`
  - `fallbackUsed=false`
  - `sourceType=REAL_AI`
  - `layoutJson.version=0.1`
  - `validation.ok=true`
  - `previewHtml` 非空
  - 前端 iframe 正常渲染，且 `sandbox=""`、无 `allow-scripts`

PowerShell 示例：

```powershell
$env:OPENAI_BASE_URL="https://api.siliconflow.cn/v1"
$env:OPENAI_MODEL="Qwen/Qwen3-VL-32B-Instruct"
$env:OPENAI_API_KEY="<your-api-key>"
$env:IMAGEPAGE_WORKER_PYTHON_COMMAND="D:\environment\python11\python.exe"

cd backend
java -jar target/backend-0.0.1-SNAPSHOT.jar --imagepage.worker.timeout-seconds=120
```

## Week 10：稳定化与可复现验收补充契约

Week 10 不改 Week 09 主链路，只补稳定性、可解释性和可复验相关契约。

### promptVersion

- Worker 返回的 metadata 应包含 `promptVersion`。
- `promptVersion` 用于标识当前真实 AI 提示词版本，便于回看和比对。
- 当前已收口值为 `week10-v1`。

### fallbackReason

- fallback 时必须返回 `fallbackReason`。
- 建议至少支持以下值：
  - `MODEL_UNAVAILABLE`
  - `MODEL_NON_JSON_OUTPUT`
  - `JSON_PARSE_FAILED`
  - `SCHEMA_VALIDATION_FAILED`
  - `IMAGE_READ_FAILED`
  - `WORKER_TIMEOUT`
  - `PREVIEW_COMPILE_FAILED`

### warnings / errors

- `warnings` 和 `errors` 必须作为数组返回。
- `warnings` 用于提示可继续展示但质量受影响的情况。
- `errors` 用于提示本次失败或 fallback 的直接原因。

### artifact 文件约定

Week 10 约定同一 `jobId` 对应的本地 artifact 至少包含：

- `layout.json`
- `preview.html`
- `metadata.json`

如实现线程需要，也可补：

- `warnings.json`
- `errors.json`
- `input.png`

### jobId 复用规则

- 同一 `jobId` 已存在成功 artifact 时，不应重复调用真实 AI。
- 查询已有结果时应优先返回本地 artifact。
- 复用结果时返回内容应与原始生成结果保持一致或在 metadata 中说明差异来源。
- 当前收口口径：第二次 generate 命中 `artifact.reused=true`，不重复调用 Worker。

### API key 安全规则

- `OPENAI_API_KEY` 只允许通过环境变量提供。
- 不允许写入代码、仓库、文档、日志或 artifact 文件。
- 检查环境变量时，只允许确认是否存在，不允许打印真实值。

### 样例图规则

- `samples/` 目录只允许放公开、无隐私、可提交的测试图片。
- 不允许提交私人截图、账号信息、公司资料、密钥或敏感页面。

### Worker smoke 样例路径

- Worker smoke 示例应使用明确存在的样例路径，例如：
  - `samples/01-simple-card-page.png`
- 不要依赖不存在的路径，如 `storage/temp/job_demo/input.png`。

### 运行副产物规则

- `backend/storage/` 属于运行副产物目录，不应提交到仓库。
- `frontend/dist/` 和其他本地产物同样不应提交。
- 本轮 smoke 使用临时公开安全样例图，不要求把私人本地图片路径固化进文档或仓库。
