# Frontend Pages

## 文件目的

本文档记录 Week 02 前端页面结构、路由规划、页面职责、页面跳转和 API 调用关系。

前端页面说明以本文档为准；接口契约以 `docs/api-contracts.md` 为准；周执行安排以 `docs/week/02-plan.md` 为准；实际进度以 `docs/week/02-status.md` 为准。

## Week 02 前端范围

第二周前端只做 3 个页面，不做完整历史记录、不做设置页、不做编辑器。

| 页面 | 路径 | 本周目标 |
|---|---|---|
| 工作台首页 | `/`，可选别名 `/dashboard` | 展示创建入口和最近一次任务入口 |
| 创建任务页 | `/generation/create` | 上传图片并创建任务 |
| 任务详情页 | `/generation/:jobId` | 展示状态、原图信息、mock 结果 |

## 路由规划

第二周明确引入 `vue-router`。

建议路由：

```text
/                         工作台首页
/dashboard                工作台首页，可选别名
/generation/create        创建任务页
/generation/:jobId        任务详情页
```

任务详情页路由参数统一命名为 `jobId`。

## 页面职责

### 工作台首页

目标：让用户知道当前项目能做什么，并能进入创建任务页。

页面内容：

- 项目标题：截图 / Figma 到响应式页面生成器。
- 当前阶段提示：MVP Mock 版本。
- 主按钮：上传截图开始生成。
- 简单说明：
  - 本阶段只支持截图上传。
  - 本阶段生成 mock 结果。
  - 暂不接入真实 AI 和 Figma。

操作：

```text
点击“上传截图开始生成”
↓
跳转 /generation/create
```

### 创建任务页

目标：完成图片选择、图片预览、上传截图、创建任务。

页面结构：

```text
顶部：页面标题
中间：图片上传区域
下方：图片预览
底部：开始生成按钮
错误提示区域
```

用户流程：

```text
选择图片
↓
本地预览
↓
点击“开始生成”
↓
调用上传接口
↓
调用创建任务接口
↓
跳转 /generation/:jobId
```

交互要求：

- 未选择图片时，按钮不可点击或点击后提示。
- 选择图片后显示本地预览。
- 上传过程中显示 loading。
- 上传失败时显示错误信息。
- 创建任务成功后跳转详情页。
- 不做复杂 UI，先保证流程稳定。

### 任务详情页

目标：展示任务状态和 mock 生成结果。

页面结构建议：

```text
顶部：任务 ID、状态标签
左侧：原始截图信息或图片预览
右侧：任务状态、生成进度
下方：layoutJson / Vue 代码 / CSS 代码
```

展示内容：

- `jobId`
- `status`
- `progress`
- `assetId`
- `layoutJson`
- `vueCode`
- `cssCode`

操作：

- 返回创建页。
- 复制 Vue 代码，可选。
- 复制 CSS 代码，可选。

复制代码按钮保持可选，不作为 Day 4 必过项。

## API 调用关系

建议新增：

```text
src/api/assetApi.js
src/api/generationApi.js
```

`assetApi.js`：

```javascript
uploadAsset(file)
```

`generationApi.js`：

```javascript
createGeneration(payload)
getGeneration(jobId)
getGenerationResult(jobId)
```

调用流程：

```text
GenerationCreate.vue
  -> uploadAsset(file)
  -> createGeneration({ assetId, mode, targetStack, responsive })
  -> router.push('/generation/' + jobId)

GenerationDetail.vue
  -> getGeneration(jobId)
  -> getGenerationResult(jobId)
```

## 组件拆分建议

建议组件：

```text
ImageUploader.vue
StatusTag.vue
CodeBlock.vue
```

`ImageUploader.vue` 职责：

- 选择图片。
- 本地预览。
- 文件类型初步校验。
- 将 file 传给父组件。

`StatusTag.vue` 职责：

- 根据 `pending` / `running` / `success` / `failed` 展示不同状态文案。

`CodeBlock.vue` 职责：

- 展示代码。
- 可选复制代码。

## mock 结果展示要求

任务详情页需要展示：

- mock `layoutJson`。
- mock `vueCode`。
- mock `cssCode`。

这些内容只用于验证前后端流程，不代表真实截图解析结果。

## 本周不做

前端本周明确不做：

- 不实现真实截图解析。
- 不实现真实代码生成。
- 不实现真实代码预览 iframe。
- 不实现拖拽编辑器。
- 不实现在线编辑器。
- 不实现导出 zip。
- 不做 Figma 页面。
- 不做复杂 UI 大改版。
