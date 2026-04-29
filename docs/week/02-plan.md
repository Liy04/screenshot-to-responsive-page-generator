# Week 02 计划：MVP 最小闭环开发周

## 1. 本周主题

第二周主题：**跑通最小业务闭环，不追求真实生成，只追求端到端可用。**

第一周是“骨架成立”，第二周是“业务闭环成立”。

本周只验证一件事：

```text
上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果
```

## 1.1 执行方式

从 Week 02 开始，日常开发任务不再要求 Codex 每次读取完整周计划和全部项目文档。

本周计划只作为阶段总纲，实际执行优先读取：

1. `AGENTS.md`
2. `docs/context/current-phase.md`
3. `docs/tasks/当前任务卡.md`
4. 当前任务相关模块代码

其它文档只在任务卡明确要求，或当前任务确实必须参考时读取。

## 2. 本周目标

第二周只围绕 `docs/mvp-scope.md` 定义的 MVP 第一版主流程开发。

本周目标不是做完整产品，而是让项目从“工程骨架”进入“可演示 MVP”：

- 前端可以选择图片并上传。
- 后端可以接收、校验并保存图片到本地目录。
- 后端可以返回 `assetId` 和 `/uploads/**` 静态资源路径。
- 前端可以基于 `assetId` 创建生成任务。
- 后端可以返回 `jobId` 和任务状态。
- 前端可以查看任务状态。
- 后端可以返回 mock 生成结果。
- 前端可以展示原图、任务状态、mock `layoutJson`、mock Vue 代码和 mock CSS 代码。

## 3. 本周不做事项

本周必须严格不做：

- 不接真实模型 API。
- 不接 OpenAI / Claude / Gemini 等模型 SDK。
- 不接 Figma API / Figma MCP。
- 不接 Redis。
- 不接 RabbitMQ。
- 不接 MySQL 实际落库。
- 不创建数据库表。
- 不创建 Mapper。
- 不创建 Entity 或数据库表映射。
- 不做真实截图解析。
- 不做真实页面代码生成。
- 不做导出 zip。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做登录注册。
- 不做历史记录持久化。
- 不做复杂权限。
- 不做复杂 UI 大改版。

## 4. 技术决策摘要

详细接口契约见 `docs/api-contracts.md`，前端页面说明见 `docs/frontend-pages.md`，实际进展见 `docs/week/02-status.md`。

### 4.1 前端路由

第二周明确引入 `vue-router`，作为前端多页面路由方案。

原因：

- 本周前端至少包含工作台首页、创建任务页、任务详情页 3 个页面。
- 任务详情页需要通过 `/generation/:jobId` 读取路由参数。
- 使用路由可以让页面职责更清晰，避免在单个 `App.vue` 中堆叠多个状态分支。
- `vue-router` 是 Vue 官方路由方案，属于轻量且符合技术栈的依赖。

### 4.2 后端存储

本周不引入 MySQL，不设计数据库表，不创建 Mapper。

本周采用：

```text
截图文件：保存到 backend/uploads/
任务数据：后端内存 Map 临时保存
mock 结果：后端固定返回模拟代码和模拟 layoutJson
```

限制说明：

- 内存 Map 数据在后端服务重启后会丢失。
- 第二周这是可接受限制，因为本周目标是验证最小闭环，不验证持久化。
- 本周可使用 DTO / VO，但不创建 Entity / Mapper / 数据库配置。

### 4.3 后端静态资源

后端需要明确 `/uploads/**` 静态资源映射：

```text
backend/uploads/              本地上传文件目录
/uploads/**                   浏览器可访问的静态资源路径
```

`backend/uploads/` 是本地运行产生的上传文件目录，必须加入 `.gitignore`，不提交用户上传图片或测试上传文件。

### 4.4 Worker

Worker 本周最多做 smoke 验证，不参与真实生成。

建议保留：

```bash
python main.py --smoke
```

可选增加：

```bash
python main.py --mock-job job_001
```

即使不增加 mock-job，也不影响第二周验收。

### 4.5 错误状态码

接口错误必须使用明确 HTTP 状态码：

- `400`：请求参数错误、文件类型不支持、文件为空、文件过大。
- `404`：资源不存在，例如查询不存在的 `assetId` / `jobId`。
- `500`：服务端未知异常，例如文件保存失败、未捕获异常。

响应体仍保持统一结构：

```json
{
  "code": 400,
  "message": "错误说明",
  "data": null
}
```

## 5. 每日任务表

| Day | 主题 | 主要任务 | 验收标准 |
|---|---|---|---|
| Day 1 | 后端上传接口日 | 实现 `POST /api/assets/upload`；保存文件到 `backend/uploads/`；配置 `/uploads/**` 静态资源映射；补充 Postman 或 curl 验证 | 上传 PNG 成功；上传 txt / 空文件失败；返回结构稳定；`mvn package -DskipTests` 通过 |
| Day 2 | 后端任务接口日 | 实现 `POST /api/generations`、`GET /api/generations/{jobId}`、`GET /api/generations/{jobId}/result`；使用内存 Map；返回 mock 结果 | 创建任务返回 `jobId`；查询状态返回 `success`；查询结果返回 `layoutJson`、`vueCode`、`cssCode`；不存在的 `jobId` 返回明确错误 |
| Day 3 | 前端创建任务页日 | 引入 `vue-router`；完成选择图片、本地预览、上传截图、创建任务、跳转 `/generation/:jobId` | 图片可预览；上传成功后能创建任务；创建后跳转详情页；非法文件有错误提示；`npm run build` 通过 |
| Day 4 | 前端任务详情与结果页日 | 根据 `jobId` 查询状态；展示进度、原图信息、mock `layoutJson`、mock Vue / CSS 代码；增加返回创建页按钮 | 直接访问 `/generation/:jobId` 能看到状态；`success` 时能看到 mock 结果；不存在的 `jobId` 有错误提示；复制代码按钮可选；`npm run build` 通过 |
| Day 5 | 端到端联调与收口日 | 从零跑完整流程；更新 `tests/smoke/README.md`；更新 `docs/week/02-status.md`；必要时更新 README | 前端 build 成功；后端 package 成功；Worker smoke 成功；完整流程可手动复现；smoke 文档可指导别人复现 |

## 6. 交付物

本周结束时，至少应新增或修改以下内容。

```text
backend/
  uploads/
  src/main/java/.../controller/AssetController.java
  src/main/java/.../controller/GenerationController.java
  src/main/java/.../service/AssetService.java
  src/main/java/.../service/GenerationService.java
  src/main/java/.../model/AssetInfo.java
  src/main/java/.../model/GenerationJob.java
  src/main/java/.../model/GenerationResult.java
  src/main/java/.../dto/...
  src/main/java/.../vo/...
  src/main/java/.../common/ApiResponse.java

frontend/
  src/router/...
  src/api/assetApi.js
  src/api/generationApi.js
  src/views/Dashboard.vue
  src/views/GenerationCreate.vue
  src/views/GenerationDetail.vue
  src/components/ImageUploader.vue
  src/components/CodeBlock.vue
  src/components/StatusTag.vue

docs/
  context/current-phase.md
  tasks/week02-day1-upload-api.md
  tasks/week02-day2-generation-api.md
  tasks/week02-day3-frontend-create-page.md
  tasks/week02-day4-generation-detail-page.md
  tasks/week02-day5-smoke-and-docs.md
  api-contracts.md
  frontend-pages.md
  week/02-plan.md
  week/02-status.md

tests/
  smoke/README.md
```

说明：文件名可以按当前项目实际结构调整，不必完全照抄。

## 7. 验收标准

Week 02 通过需要满足：

- 截图上传接口可用。
- 创建生成任务接口可用。
- 查询任务状态接口可用。
- 查询 mock 结果接口可用。
- 前端创建任务页面可用。
- 前端任务详情页面可用。
- 前后端完成最小闭环联调。
- smoke 文档完成更新。
- 未接入真实模型 API、Figma API / Figma MCP、Redis、RabbitMQ、MySQL 实际落库。
- 未创建数据库表、Mapper、Entity 或数据库表映射。
- 未实现真实截图解析、真实代码生成、导出 zip、拖拽编辑器。

端到端验收流程：

```text
启动后端
↓
启动前端
↓
打开创建任务页
↓
选择一张 PNG 截图
↓
点击开始生成
↓
上传成功
↓
创建任务成功
↓
跳转任务详情页
↓
查看状态 success
↓
查看 mock Vue / CSS / layoutJson
```

## 8. 风险摘要

| 风险 | 表现 | 控制方式 |
|---|---|---|
| 范围膨胀 | 想顺手接 MySQL / AI / Figma | 每个任务先读 `docs/context/current-phase.md` 和当前任务卡中的禁止事项 |
| 后端过度设计 | DTO、VO、Entity、Mapper 全套上来 | 本周可用 DTO / VO，但不创建 Entity / Mapper / 数据库配置 |
| 前端做太漂亮 | 花大量时间调 UI | 先完成流程，再做基础美化 |
| Worker 抢主线 | 想让 Python 真的处理图片 | 本周 Worker 只保留 smoke |
| 联调卡住 | 前后端接口字段不一致 | 以 `docs/api-contracts.md` 为接口契约 |
| 文档滞后 | 做完功能但别人跑不起来 | Day 5 专门做 smoke 收口 |
| 上传路径混乱 | 文件保存后前端无法访问 | 以 `/uploads/**` 静态资源映射为准 |
| 接口异常不清楚 | 前端不知道失败原因 | 后端统一返回 HTTP 状态码和 `code/message/data` |
| 内存数据丢失 | 后端重启后 `assetId` / `jobId` 查询不到 | 第二周可接受，文档明确这是内存 Map 限制 |

## 9. 相关文档入口

| 文档 | 职责 |
|---|---|
| `docs/context/current-phase.md` | Week 02 当前阶段目标、禁止项和推荐实现方式 |
| `docs/tasks/*.md` | Week 02 每日单任务卡，日常执行以任务卡为准 |
| `docs/mvp-scope.md` | 当前 MVP 范围锚点 |
| `docs/api-contracts.md` | Week 02 接口契约 |
| `docs/frontend-pages.md` | Week 02 前端页面、路由和交互说明 |
| `docs/week/02-plan.md` | Week 02 周执行安排 |
| `docs/week/02-status.md` | Week 02 实际进展和验收状态 |
| `docs/coding-rules.md` | 编码规范 |
| `docs/testing.md` | 测试策略 |
| `docs/prompt-templates.md` | 可复用任务提示词 |
| `tests/smoke/README.md` | smoke 验证步骤 |
