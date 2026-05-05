# Layout JSON v0.1 设计文档

## 文件目的

本文档是 Week 03 Layout JSON v0.1 的设计依据。

它用于指导后续 Schema、示例文件和 Worker 校验器实现，不用于定义真实 AI、Figma 接入、数据库落库或 Vue 页面代码生成。

Week 03 P0 只验证：

```text
手写 Layout JSON -> Schema 校验 -> 业务规则校验 -> 示例验证
```

## 1. Layout JSON 是什么

Layout JSON 是页面结构说明书。

它用 JSON 描述一个页面的结构、节点语义、设计变量引用、位置参考、响应式规则、资源引用、假设和风险。

它的目标不是直接渲染页面，而是让系统先拥有一个稳定、可校验、可追踪的页面结构中间层。

可以把它理解为：

```text
输入截图 / Figma 信息 / 手写样本
  -> Layout JSON
  -> 后续校验、保存、查看、代码生成
```

Week 03 只做其中的 Layout JSON 结构稳定和校验准备。

## 2. 为什么需要中间层

如果直接从截图进入 Vue 代码生成，会出现这些问题：

- 结构不稳定：同一张图可能生成不同的代码结构。
- 难以校验：代码层面很难判断页面结构是否完整。
- 难以追踪：后端难以记录“识别出了哪些节点”。
- 难以调试：生成失败时，不容易区分是结构问题、样式问题还是代码问题。
- 难以复用：响应式、tokens、节点语义很难在不同生成任务间复用。
- 难以扩展：后续局部重生成、节点查看、人工修正都需要稳定节点 id。

Layout JSON 把流程拆成两步：

```text
截图 / Figma / 手写样本 -> Layout JSON -> Vue 页面代码
```

这样 Week 03 可以先把“页面结构说明书”做稳，Week 04 或后续阶段再考虑代码生成。

## 3. 为什么 Layout JSON 不是 HTML / Vue

HTML / Vue 是最终实现代码，关注的是页面如何被浏览器渲染。

Layout JSON 关注的是页面应该如何被理解：

- 页面有哪些区域。
- 区域之间是什么层级关系。
- 节点有什么语义。
- 节点引用哪些设计变量。
- 节点在原图中大致位于哪里。
- 响应式时应该如何变化。
- 哪些信息是明确的，哪些只是暂时假设。

Layout JSON 不应该直接塞入大量 CSS 细节，也不应该提前绑定 Vue 组件结构。

推荐表达设计意图：

```json
{
  "style": {
    "typography": "headingLg",
    "color": "textPrimary",
    "spacing": "lg"
  }
}
```

不推荐过早写成 CSS 像素堆叠：

```json
{
  "style": {
    "marginTop": "17px",
    "fontSize": "23px",
    "color": "#111827"
  }
}
```

## 4. v0.1 顶层字段

Layout JSON v0.1 顶层字段固定为以下 9 个：

| 字段 | 类型建议 | 说明 | P0 要求 |
|---|---|---|---|
| `version` | string | Layout JSON 版本，v0.1 固定为 `0.1` | 必填 |
| `page` | object | 页面基础信息，如名称、类型、视口尺寸 | 必填 |
| `source` | object | 来源信息，如 manual / screenshot / figma | 必填 |
| `tokens` | object | 设计变量，如颜色、字体、间距、圆角 | 必填 |
| `layout` | object | 页面结构树根节点 | 必填 |
| `assets` | array | 图片等资源引用 | 必填 |
| `responsive` | object | 断点和响应式规则 | 必填 |
| `assumptions` | array | 当前无法确认但暂时采用的假设 | 必填 |
| `warnings` | array | 可能影响后续生成质量的风险提示 | 必填 |

### 4.1 version

`version` 用于标识 Layout JSON 结构版本。

Week 03 固定为：

```json
"version": "0.1"
```

### 4.2 page

`page` 描述页面基础信息。

建议字段：

```json
{
  "name": "Landing Page",
  "type": "marketing",
  "viewport": {
    "width": 1440,
    "height": 900
  }
}
```

### 4.3 source

`source` 描述 Layout JSON 的来源。

Week 03 主要使用 `manual`，为后续截图和 Figma 来源保留字段。

```json
{
  "type": "manual",
  "fileUrl": null,
  "figmaFileKey": null,
  "figmaNodeId": null
}
```

说明：保留 Figma 字段不代表 Week 03 接入 Figma API / Figma MCP。

### 4.4 tokens

`tokens` 记录设计变量。

建议包含：

- `colors`
- `typography`
- `spacing`
- `radius`

Week 03 不要求 tokens 完整覆盖真实设计系统，只要求示例可表达基础引用。

### 4.5 layout

`layout` 是页面结构树，是 Layout JSON 的核心。

根节点必须是 `page` 类型，并通过 `children` 组织子节点。

### 4.6 assets

`assets` 记录图片等资源引用。

Week 03 示例中可以使用占位资源或空数组。

### 4.7 responsive

`responsive` 记录断点和响应式规则。

Week 03 至少保留断点结构和 `rules` 数组。

### 4.8 assumptions

`assumptions` 记录无法从当前输入确认、但为了继续流程暂时采用的假设。

### 4.9 warnings

`warnings` 记录会影响后续生成或还原质量的风险。

## 5. Layout Node 字段

每个 layout node 建议包含以下字段：

| 字段 | 说明 | P0 要求 |
|---|---|---|
| `id` | 节点唯一标识 | 必填 |
| `type` | 节点类型 | 必填 |
| `role` | 节点语义角色 | 建议必填 |
| `content` | 文本内容，适用于 text / button | 按类型需要 |
| `bounds` | 原图或设计稿中的位置参考 | 建议必填 |
| `style` | 设计变量引用或语义化样式 | 必填 |
| `constraints` | 响应式约束 | 必填 |
| `interactions` | 交互意图占位 | 必填，可为空数组 |
| `dataBinding` | 数据绑定占位 | 可选 |
| `children` | 子节点数组 | 必填 |

节点 `id` 必须唯一，因为后续校验、响应式规则、错误定位、节点查看和代码生成映射都会依赖它。

## 6. v0.1 支持的节点类型

Week 03 v0.1 只支持基础节点类型：

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

节点类型说明：

| 类型 | 用途 |
|---|---|
| `page` | 页面根节点 |
| `section` | 页面大区块 |
| `container` | 通用容器 |
| `text` | 文本 |
| `button` | 按钮 |
| `image` | 图片 |
| `card` | 卡片 |
| `list` | 列表 |
| `listItem` | 列表项 |
| `form` | 表单 |
| `input` | 输入框 |

## 7. v0.1 暂不支持的节点类型

Week 03 暂不支持：

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

这些节点涉及更复杂的数据结构、交互状态或渲染逻辑，后续在 v0.2 或更晚阶段扩展。

## 8. bounds

`bounds` 表示节点在原始截图或设计稿中的参考位置。

```json
{
  "x": 120,
  "y": 80,
  "width": 520,
  "height": 160
}
```

作用：

- 记录视觉位置参考。
- 方便后续对比截图和结构。
- 帮助校验器或查看器定位问题节点。
- 为后续代码生成提供布局参考。

注意：`bounds` 不代表后续必须使用绝对定位。

## 9. constraints

`constraints` 表示节点在响应式布局中的约束。

```json
{
  "horizontal": "fill",
  "vertical": "hug"
}
```

常见取值：

| 值 | 含义 |
|---|---|
| `fixed` | 固定尺寸 |
| `fill` | 填满父容器 |
| `hug` | 根据内容撑开 |
| `center` | 居中 |
| `stretch` | 拉伸 |

Week 03 不要求实现真实响应式布局，只要求结构中能表达这些约束。

## 10. responsive

`responsive` 用于集中描述页面断点和节点响应式规则。

建议基础结构：

```json
{
  "breakpoints": {
    "mobile": 390,
    "tablet": 768,
    "desktop": 1440
  },
  "rules": []
}
```

如果存在 `responsive.rules`，其中的 `target` 必须指向一个存在的 layout node id。

这条规则属于 Day 4 / Day 5 校验器需要覆盖的业务规则。

## 11. assumptions

`assumptions` 用于记录暂时假设。

适合记录：

- 按钮点击行为未知。
- 图片真实来源未知。
- 表单提交接口未知。
- 列表数据来源未知。

示例：

```json
{
  "target": "hero-button",
  "message": "按钮点击行为未知，暂时按主操作按钮处理"
}
```

## 12. warnings

`warnings` 用于记录风险提示。

适合记录：

- 截图中某个区域遮挡严重。
- 图片资源缺失。
- 文本可能识别不完整。
- 响应式规则需要人工确认。

示例：

```json
{
  "target": "hero-image",
  "message": "图片资源未知，后续需要替换真实资源"
}
```

## 13. 当前限制

Week 03 v0.1 明确限制：

- 只支持基础页面结构。
- 只使用手写 Layout JSON 示例。
- 只做 Schema 和校验器验证。
- 不做真实截图解析。
- 不接真实 AI / 模型 API。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不接 MySQL 实际落库。
- 不新增 Entity / Mapper。
- 不做 Vue 页面代码生成。
- 不做拖拽编辑器、在线编辑器或导出 ZIP。
- P1 mock 保存和前端基础查看不属于 P0。

## 14. 后续扩展方向

后续可以在 v0.1 稳定后逐步扩展：

- 增加 `table`、`chart`、`modal` 等复杂节点。
- 增强 tokens 引用校验。
- 增强 responsive rules 表达能力。
- 增加 Layout JSON 可视化查看。
- 增加本地文件 mock 保存和查询。
- 在确认后引入数据库持久化。
- 实现 Layout JSON 到 Vue3 页面初稿生成。
- 在 Schema 稳定后再评估真实 AI / Figma 接入。

以上内容均不是 Week 03 Day 1 的交付范围。
