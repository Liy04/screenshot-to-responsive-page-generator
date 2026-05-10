# Week 07 开发计划：图片输入场景与 Layout JSON Mock 链路验证

## 一、Week 07 主题

Week 07 的主题是：

**图片输入场景与 Layout JSON Mock 链路验证**

本周不接真实 AI，不接 Figma，不接 MySQL，不接 Redis，不接 RabbitMQ，不做 ZIP 导出，不做拖拽编辑器，不做复杂响应式算法，不做后端调用 Python Worker。

本周目标是为后续“图片 -> Layout JSON -> HTML 静态预览”做准备，而不是直接实现完整 AI 页面生成器。

---

## 二、当前项目阶段判断

当前项目已经完成 Week 01 ~ Week 06。

目前已有能力：

1. 已经有 Layout JSON v0.1。
2. 已经有 Worker validator 校验器。
3. 已经有 Worker static generator 静态编译器。
4. 已经能从 Layout JSON 生成 generated-page artifact。
5. 已经能得到 htmlCode / cssCode / vueCode。
6. 已经有后端 generated-page artifact mock 保存和查询接口。
7. 已经有前端 generated-page preview 页面。
8. 已经能通过 sandbox iframe 安全预览生成页面。
9. 已经有 Worker、后端、前端的基础自动化测试。
10. 已经有 Docs Lite 文档协作模式。

当前还没有完成：

1. 没有从真实图片解析出 Layout JSON。
2. 没有从真实 Figma 文件生成 Layout JSON。
3. 没有接真实 AI / 视觉模型。
4. 没有接 MySQL。
5. 没有历史任务列表 / 任务持久化。
6. 没有 ZIP 导出。
7. 没有拖拽编辑器 / 在线编辑器。
8. vueCode 仍然只作为文本展示，不要求可运行。

因此 Week 07 最合理的目标不是接 MySQL，也不是接真实 AI，而是先补齐“图片输入如何进入 Layout JSON 链路”这一段。

---

## 三、Week 07 核心目标

本周核心目标：

**建立一个“图片输入场景 -> templateKey 半自动选择 -> mock Layout JSON -> 前端展示”的最小闭环。**

本周目标链路：

```text
本地选择图片
-> 浏览器本地预览图片
-> 选择 templateKey
-> 创建 image-layout mock job
-> 后端根据 templateKey 返回 mock Layout JSON
-> 前端展示 Layout JSON / errors / warnings
-> 为后续 generated-page 预览做准备
```

注意：

- Week 07 不做真实图片解析。
- Week 07 不上传真实图片到后端。
- Week 07 不让后端调用 Python Worker。
- Week 07 不接 MySQL。
- Week 07 不接真实 AI。
- Week 07 不接 Figma。

---

## 四、Week 07 关键设计原则

### 1. 图片只做“输入场景演示”

前端可以让用户选择本地图片，并在浏览器中预览。

但是后端请求中不上传真实图片文件，只提交：

```json
{
  "imageName": "demo-home.png",
  "templateKey": "landing-basic"
}
```

这样做的原因：

1. 避免引入 multipart 文件上传。
2. 避免处理文件大小限制、文件类型校验、文件存储路径。
3. 避免安全风险。
4. 避免 Week 07 变成“文件上传系统开发”。
5. 保持本周重点在“图片输入场景如何进入 Layout JSON 链路”。

---

### 2. templateKey 是半自动 mock 参数

`templateKey` 用于模拟“图片经过识别后选择页面结构”的结果。

当前不是 AI 识图，而是用户手动选择模板类型。

例如：

```text
landing-basic      基础落地页
card-list          卡片列表页
dashboard-simple   简单后台面板
invalid-layout     故意失败的测试模板
```

页面和文档中必须明确写明：

```text
当前为 Week 07 mock / 半自动链路。
图片仅用于输入场景演示。
系统暂未接入真实 AI 视觉解析。
Layout JSON 由 templateKey 对应的 mock 模板生成。
```

---

### 3. 后端不调用 Python Worker

当前项目还没有 Spring Boot 后端调用 Python Worker 的机制。

因此 Week 07 不做：

```text
前端上传图片
-> 后端调用 Python Worker
-> Worker 编译 generated-page
-> 后端保存 artifact
```

这条链路需要额外架构设计，不适合塞进 Week 07。

Week 07 后端只做：

```text
imageName + templateKey
-> 创建 image-layout mock job
-> 返回 mock Layout JSON
```

---

### 4. Worker 只做 templateKey 到 Layout JSON fixture 的解析

Worker 可以新增 `image_layout_resolver.py`。

但它只负责：

```text
templateKey -> Layout JSON fixture
```

不负责：

1. 读取真实图片。
2. OCR。
3. 视觉识别。
4. AI 调用。
5. HTTP 服务。
6. 后端通信。
7. 数据库存储。

---

### 5. generated-page 自动预览不作为 Week 07 必须项

Week 07 的必须成果是：

```text
图片输入场景
-> mock Layout JSON
-> 前端展示 Layout JSON
```

如果时间足够，可以做一个“mock 预览”按钮，但必须明确它是 mock generated-page preview，不是实时 AI 生成。

不强制做：

```text
图片
-> Layout JSON
-> Worker 自动编译
-> 后端自动保存
-> 前端自动预览
```

因为这需要后端和 Python Worker 打通，不属于 Week 07 范围。

---

## 五、Week 07 必做范围

### Docs

1. 更新 `docs/current.md`。
2. 更新 `docs/spec.md`。
3. 更新 `docs/task.md`。
4. 新增或归档 `docs/archive/week/07-plan.md`。
5. 完成后新增 `docs/archive/week/07-dev-smoke.md`。
6. 完成后新增 `docs/archive/week/07-summary.md`。
7. 完成后新增 `docs/archive/week/07-report-material.md`。

---

### Worker

新增：

```text
worker/image_layout_resolver.py
worker/fixtures/image_templates/landing-basic.layout.json
worker/fixtures/image_templates/card-list.layout.json
worker/fixtures/image_templates/invalid-layout.layout.json
worker/test_image_layout_resolver.py
```

Worker 职责：

```text
templateKey -> Layout JSON fixture
```

---

### Backend

新增 dev mock API：

```text
POST /api/dev/image-layout-jobs
GET  /api/dev/image-layout-jobs/{jobId}
```

后端职责：

```text
接收 imageName + templateKey
创建 image-layout mock job
返回 mock Layout JSON
保存 mock job 状态
支持按 jobId 查询
```

---

### Frontend

新增页面：

```text
/dev/image-to-layout
```

页面职责：

```text
选择本地图片
浏览器本地预览图片
选择 templateKey
创建 image-layout mock job
展示 jobId
展示 status
展示 templateKey
展示 Layout JSON
展示 errors / warnings
明确提示当前未接真实 AI
```

---

## 六、Week 07 不做范围

本周明确不做以下内容：

1. 不接真实 AI。
2. 不接 OpenAI / Claude / Gemini SDK。
3. 不接 Figma API。
4. 不接 Figma MCP。
5. 不接 MySQL。
6. 不创建数据库表。
7. 不创建 Entity。
8. 不创建 Mapper。
9. 不接 Redis。
10. 不接 RabbitMQ。
11. 不做真实图片上传到后端。
12. 不做图片文件持久化。
13. 不做后端调用 Python Worker。
14. 不做 Worker HTTP 服务。
15. 不做 ZIP 导出。
16. 不做拖拽编辑器。
17. 不做在线编辑器。
18. 不做复杂响应式算法。
19. 不做 Tailwind 代码生成。
20. 不做 Vue SFC 可运行化。
21. 不做历史任务列表。
22. 不做用户系统。

---

## 七、Week 07 数据协议设计

### 1. 创建 image-layout mock job 请求

接口：

```text
POST /api/dev/image-layout-jobs
```

请求体：

```json
{
  "imageName": "demo-home.png",
  "templateKey": "landing-basic"
}
```

字段说明：

```text
imageName:
本地选择图片的文件名。
当前只作为 mock 元信息，不上传真实图片。

templateKey:
半自动 mock 模板标识。
用于选择对应的 Layout JSON fixture。
```

---

### 2. 创建成功响应

```json
{
  "jobId": "img-layout-001",
  "status": "SUCCESS",
  "sourceType": "IMAGE_TEMPLATE_MOCK",
  "imageName": "demo-home.png",
  "templateKey": "landing-basic",
  "layoutArtifact": {
    "status": "SUCCESS",
    "layoutJson": {
      "version": "0.1",
      "root": {
        "id": "root",
        "type": "container",
        "children": []
      }
    }
  },
  "errors": [],
  "warnings": []
}
```

---

### 3. 创建失败响应

未知 templateKey 示例：

```json
{
  "jobId": "img-layout-002",
  "status": "FAILED",
  "sourceType": "IMAGE_TEMPLATE_MOCK",
  "imageName": "demo-home.png",
  "templateKey": "unknown-template",
  "layoutArtifact": null,
  "errors": [
    {
      "code": "IMAGE_TEMPLATE_NOT_FOUND",
      "message": "Unknown templateKey: unknown-template"
    }
  ],
  "warnings": []
}
```

---

### 4. 查询 image-layout mock job

接口：

```text
GET /api/dev/image-layout-jobs/{jobId}
```

成功响应：

```json
{
  "jobId": "img-layout-001",
  "status": "SUCCESS",
  "sourceType": "IMAGE_TEMPLATE_MOCK",
  "imageName": "demo-home.png",
  "templateKey": "landing-basic",
  "layoutArtifact": {
    "status": "SUCCESS",
    "layoutJson": {}
  },
  "errors": [],
  "warnings": []
}
```

不存在响应：

```json
{
  "status": 404,
  "message": "Image layout job not found"
}
```

---

## 八、templateKey 设计

Week 07 至少支持三个 templateKey：

### 1. landing-basic

用途：

基础落地页，用于模拟普通官网首页 / 产品页 / 活动页。

建议包含节点：

```text
root container
hero section
title text
subtitle text
primary button
image placeholder
feature section
feature card
```

---

### 2. card-list

用途：

卡片列表页，用于模拟内容列表、商品列表、文章列表。

建议包含节点：

```text
root container
header
title
grid container
card item 1
card item 2
card item 3
card title
card description
card image
```

---

### 3. invalid-layout

用途：

故意失败的测试模板，用于验证 validator 和错误展示。

可以包含：

```text
缺少 root
非法 node type
非法 style 字段
空 children 结构异常
```

注意：

`invalid-layout` 用于测试失败状态，不用于正常演示。

---

### 4. dashboard-simple，可选

如果时间足够，再加 `dashboard-simple`。

用途：

简单后台面板，用于模拟仪表盘页面。

建议包含节点：

```text
sidebar
topbar
stat cards
chart placeholder
table placeholder
```

如果 Week 07 时间紧张，可以不做 `dashboard-simple`。

---

## 九、每日开发计划

## Day 1：Docs 线程

### 任务名称

```text
Define Week 07 image-to-layout mock protocol
```

### 任务目标

只做文档规划，不修改前端、后端、Worker 代码。

### 需要修改

```text
docs/current.md
docs/spec.md
docs/task.md
docs/archive/week/07-plan.md
```

### 需要写清楚

1. Week 07 主题是“图片输入场景与 Layout JSON Mock 链路验证”。
2. 本周不接 MySQL。
3. 本周不接真实 AI。
4. 本周不接 Figma。
5. 本周不上传真实图片到后端。
6. 前端只做本地图片选择和本地预览。
7. 后端请求只提交 imageName + templateKey。
8. templateKey 是半自动 mock 参数。
9. image-layout mock job 的请求和响应协议。
10. Week 07 每日单线程任务安排。

### 完成标准

1. `docs/task.md` 只保留当前一个任务。
2. `docs/current.md` 明确 Week 07 当前目标。
3. `docs/spec.md` 记录 image-to-layout mock 协议。
4. `docs/archive/week/07-plan.md` 形成完整周计划。
5. 没有修改任何代码。

---

## Day 2：Worker 实现线程

### 任务名称

```text
Implement image template layout resolver
```

### 任务目标

新增 Worker image layout resolver，实现 templateKey 到 Layout JSON fixture 的解析。

### 需要新增

```text
worker/image_layout_resolver.py
worker/fixtures/image_templates/landing-basic.layout.json
worker/fixtures/image_templates/card-list.layout.json
worker/fixtures/image_templates/invalid-layout.layout.json
```

### resolver 职责

输入：

```json
{
  "templateKey": "landing-basic",
  "imageName": "demo-home.png"
}
```

输出：

```json
{
  "status": "SUCCESS",
  "layoutJson": {},
  "source": {
    "type": "IMAGE_TEMPLATE_MOCK",
    "templateKey": "landing-basic",
    "imageName": "demo-home.png"
  },
  "errors": [],
  "warnings": []
}
```

未知 templateKey 输出：

```json
{
  "status": "FAILED",
  "layoutJson": null,
  "source": {
    "type": "IMAGE_TEMPLATE_MOCK",
    "templateKey": "unknown-template"
  },
  "errors": [
    {
      "code": "IMAGE_TEMPLATE_NOT_FOUND",
      "message": "Unknown templateKey: unknown-template"
    }
  ],
  "warnings": []
}
```

### 不允许做

1. 不读取图片像素。
2. 不做 OCR。
3. 不接 AI。
4. 不接 HTTP 服务。
5. 不调用后端。
6. 不新增第三方依赖。
7. 不改前端。
8. 不改后端。

### 完成标准

1. 可以根据 templateKey 读取对应 fixture。
2. 可以返回统一结构。
3. 未知 templateKey 有明确错误。
4. 不影响原有 Worker validator 和 static generator。
5. 不新增复杂依赖。

---

## Day 3：Worker 测试线程

### 任务名称

```text
Add image template resolver regression tests
```

### 任务目标

为 `image_layout_resolver.py` 增加回归测试。

### 需要新增

```text
worker/test_image_layout_resolver.py
```

### 测试覆盖

1. `landing-basic` 返回 SUCCESS。
2. `card-list` 返回 SUCCESS。
3. `unknown templateKey` 返回 FAILED。
4. `unknown templateKey` 包含 `IMAGE_TEMPLATE_NOT_FOUND` 错误码。
5. `landing-basic` 返回的 layoutJson 可以通过 validator。
6. `card-list` 返回的 layoutJson 可以通过 validator。
7. `invalid-layout` 返回的 layoutJson 可以触发 validator 失败。
8. 返回 `source.type = IMAGE_TEMPLATE_MOCK`。
9. 返回 `source.templateKey` 与输入一致。
10. 多次解析同一个 templateKey，输出结构稳定。

### 验证命令

```bash
python -m unittest worker.test_image_layout_resolver
python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver
```

### 完成标准

1. 新增测试通过。
2. 原有 Worker 35 个测试不回退。
3. 不修改前端。
4. 不修改后端。

---

## Day 4：Backend 实现线程

### 任务名称

```text
Implement image-layout dev mock job API
```

### 任务目标

新增后端 image-layout dev mock job API。

### 建议新增接口

```text
POST /api/dev/image-layout-jobs
GET  /api/dev/image-layout-jobs/{jobId}
```

### POST 请求

```json
{
  "imageName": "demo-home.png",
  "templateKey": "landing-basic"
}
```

### POST 成功响应

```json
{
  "jobId": "img-layout-001",
  "status": "SUCCESS",
  "sourceType": "IMAGE_TEMPLATE_MOCK",
  "imageName": "demo-home.png",
  "templateKey": "landing-basic",
  "layoutArtifact": {
    "status": "SUCCESS",
    "layoutJson": {}
  },
  "errors": [],
  "warnings": []
}
```

### POST 失败响应

```json
{
  "jobId": "img-layout-002",
  "status": "FAILED",
  "sourceType": "IMAGE_TEMPLATE_MOCK",
  "imageName": "demo-home.png",
  "templateKey": "unknown-template",
  "layoutArtifact": null,
  "errors": [
    {
      "code": "IMAGE_TEMPLATE_NOT_FOUND",
      "message": "Unknown templateKey: unknown-template"
    }
  ],
  "warnings": []
}
```

### GET 成功响应

```json
{
  "jobId": "img-layout-001",
  "status": "SUCCESS",
  "sourceType": "IMAGE_TEMPLATE_MOCK",
  "imageName": "demo-home.png",
  "templateKey": "landing-basic",
  "layoutArtifact": {
    "status": "SUCCESS",
    "layoutJson": {}
  },
  "errors": [],
  "warnings": []
}
```

### GET 不存在响应

```json
{
  "status": 404,
  "message": "Image layout job not found"
}
```

### 实现要求

1. 使用 dev mock 方式保存 job。
2. 可以使用内存 Map 或当前项目已有 mock 保存方式。
3. 不接 MySQL。
4. 不创建 Entity。
5. 不创建 Mapper。
6. 不上传文件。
7. 不调用 Python Worker。
8. 不影响已有 generated-page artifact 接口。

### 参数校验建议

需要校验：

```text
imageName 不能为空
imageName 不能过长
templateKey 不能为空
templateKey 必须是已支持的模板
body 不能为空
body 不能是 array
```

### 完成标准

1. POST 可以创建 image-layout mock job。
2. GET 可以查询已创建 job。
3. 未知 templateKey 有明确失败状态。
4. 不存在 job 返回 404。
5. 不影响原有 generated-page artifact 接口。
6. 没有新增数据库相关代码。

---

## Day 5：Backend 测试线程

### 任务名称

```text
Add image-layout dev mock API tests
```

### 任务目标

为后端 image-layout dev mock API 增加测试。

### 建议新增测试类

```text
ImageLayoutJobDevControllerTest
```

### 测试覆盖

1. POST `landing-basic` 成功。
2. POST `card-list` 成功。
3. POST `unknown templateKey` 返回 FAILED 或 400。
4. POST 空 body 返回 400。
5. POST array body 返回 400。
6. POST 空 imageName 返回 400。
7. POST 空 templateKey 返回 400。
8. POST 过长 imageName 返回 400。
9. GET 已存在 job 成功。
10. GET 不存在 job 返回 404。
11. SUCCESS 响应包含 layoutArtifact。
12. FAILED 响应 layoutArtifact 为 null 或空。
13. errors 字段结构稳定。
14. warnings 字段结构稳定。

### 验证命令

```bash
mvn test
```

### 完成标准

1. 新增测试通过。
2. 原 generated-page artifact 相关测试不回退。
3. 不修改前端。
4. 不修改 Worker。
5. 不接 MySQL。

---

## Day 6：Frontend 页面线程

### 任务名称

```text
Implement image-to-layout dev page
```

### 任务目标

新增前端 image-to-layout dev 页面。

### 新增路由

```text
/dev/image-to-layout
```

### 页面模块

#### 1. 页面标题区

标题：

```text
Image to Layout Mock Preview
```

副标题：

```text
Week 07 图片输入场景与 Layout JSON Mock 链路验证
```

必须显示说明：

```text
当前为 Week 07 mock / 半自动链路。
图片仅用于输入场景演示，暂未接入真实 AI 视觉解析。
Layout JSON 由 templateKey 对应的 mock 模板生成。
```

---

#### 2. 图片选择区

功能：

1. 选择本地图片。
2. 显示图片名称。
3. 显示浏览器本地预览。
4. 不上传图片文件到后端。

注意：

图片只用于本地展示。
后端请求只提交 imageName 和 templateKey。

---

#### 3. templateKey 选择区

下拉选项：

```text
landing-basic
card-list
invalid-layout
```

可选：

```text
dashboard-simple
```

每个选项需要有中文说明：

```text
landing-basic：基础落地页
card-list：卡片列表页
invalid-layout：失败状态测试模板
dashboard-simple：简单后台面板，可选
```

---

#### 4. 创建任务区

按钮：

```text
创建 image-layout mock job
```

点击后调用：

```text
POST /api/dev/image-layout-jobs
```

请求体：

```json
{
  "imageName": "demo-home.png",
  "templateKey": "landing-basic"
}
```

---

#### 5. 结果展示区

展示：

```text
jobId
status
sourceType
imageName
templateKey
layoutArtifact.status
layoutJson
errors
warnings
```

SUCCESS 状态：

显示 Layout JSON。

FAILED 状态：

显示错误码和错误信息。

ERROR 状态：

显示请求失败提示。

EMPTY 状态：

提示尚未创建任务。

LOADING 状态：

提示正在创建 mock job。

---

### 页面不做

1. 不做真实图片上传。
2. 不做拖拽编辑。
3. 不做 AI 解析 loading。
4. 不做历史任务列表。
5. 不做 ZIP 导出。
6. 不做复杂预览编辑器。
7. 不宣称“AI 已解析图片”。

### 完成标准

1. `/dev/image-to-layout` 可以访问。
2. 可以选择本地图片并预览。
3. 可以选择 templateKey。
4. 可以创建 image-layout mock job。
5. 可以展示返回的 Layout JSON。
6. 可以展示 errors / warnings。
7. 页面明确提示当前未接真实 AI。
8. `npm run build` 通过。

---

## Day 7：Frontend 测试与 Week 07 文档归档

Day 7 建议拆成两个单线程任务执行。

---

### Day 7 任务 A：Frontend 测试线程

#### 任务名称

```text
Add image-to-layout dev page tests
```

#### 新增测试文件

```text
frontend/src/views/__tests__/ImageToLayoutDev.test.js
```

#### 测试覆盖

1. 页面标题显示。
2. mock / 半自动说明文案显示。
3. “暂未接入真实 AI 视觉解析”文案显示。
4. templateKey 下拉框显示。
5. `landing-basic` 选项显示。
6. `card-list` 选项显示。
7. `invalid-layout` 选项显示。
8. 创建任务 loading 状态显示。
9. SUCCESS 状态展示 Layout JSON。
10. FAILED 状态展示 errors。
11. 请求失败展示 error 状态。
12. 未创建任务时展示 empty 状态。
13. 页面不出现“真实 AI 已解析”这类误导文案。

#### 验证命令

```bash
npm run test
npm run build
```

#### 完成标准

1. 新增前端测试通过。
2. 原 generated-page preview 测试不回退。
3. 前端 build 通过。

---

### Day 7 任务 B：Smoke 与总结文档线程

#### 任务名称

```text
Archive Week 07 smoke and summary docs
```

#### 新增文档

```text
docs/archive/week/07-dev-smoke.md
docs/archive/week/07-summary.md
docs/archive/week/07-report-material.md
```

#### 更新文档

```text
docs/current.md
docs/task.md
```

#### 07-dev-smoke.md 建议内容

```md
# Week 07 Dev Smoke

## 1. Worker Smoke

Command:

python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver

Expected:

OK

## 2. Backend Smoke

Command:

mvn test

Expected:

OK

## 3. Frontend Smoke

Command:

npm run test
npm run build

Expected:

OK

## 4. Manual Smoke

Steps:

1. 打开 /dev/image-to-layout。
2. 选择本地图片。
3. 确认图片只在浏览器本地预览。
4. 选择 landing-basic。
5. 点击创建 image-layout mock job。
6. 确认页面展示 jobId。
7. 确认页面展示 status = SUCCESS。
8. 确认页面展示 templateKey = landing-basic。
9. 确认页面展示 Layout JSON。
10. 选择 invalid-layout。
11. 确认页面可以展示失败状态或校验错误。
12. 确认页面明确提示：暂未接入真实 AI 视觉解析。
13. 确认没有真实图片上传逻辑。
14. 确认没有 MySQL 相关代码。
```

#### 07-summary.md 建议内容

```md
# Week 07 Summary

## Theme

图片输入场景与 Layout JSON Mock 链路验证。

## Completed

1. 定义 image-to-layout mock 协议。
2. 新增 templateKey 到 Layout JSON fixture 的 Worker resolver。
3. 新增 Worker resolver 测试。
4. 新增后端 image-layout dev mock job API。
5. 新增后端 API 测试。
6. 新增前端 /dev/image-to-layout 页面。
7. 支持本地图片选择和浏览器本地预览。
8. 支持 templateKey 选择。
9. 支持创建 image-layout mock job。
10. 支持展示 Layout JSON、errors、warnings。
11. 明确标注当前未接真实 AI。
12. 完成 Week 07 smoke 文档和实践报告素材。

## Not Included

1. 未接真实 AI。
2. 未接 Figma。
3. 未接 MySQL。
4. 未上传真实图片到后端。
5. 未让后端调用 Python Worker。
6. 未做 ZIP 导出。
7. 未做拖拽编辑器。
8. 未做复杂响应式算法。

## Next Direction

Week 08 可以考虑：

1. 将 image-layout mock job 与 generated-page preview 更自然地串联。
2. 设计后端调用 Worker 的最小方案。
3. 或者继续增强图片 mock 模板质量。
4. MySQL 持久化建议放到 Week 09 作为单独专题。
```

#### 07-report-material.md 建议内容

```md
# Week 07 Report Material

## 本周实践主题

本周围绕“图片输入场景与 Layout JSON Mock 链路验证”展开，目标是在不接入真实 AI 的前提下，先验证截图 / 图片输入如何进入页面生成链路。

## 实现思路

系统通过 templateKey 模拟图片识别后的页面结构选择结果。用户在前端选择本地图片后，图片仅用于浏览器本地预览，不上传到后端。前端将 imageName 和 templateKey 提交给后端，后端创建 image-layout mock job，并返回对应的 mock Layout JSON。前端展示 Layout JSON、任务状态、错误信息和警告信息。

## 技术价值

1. 补齐了图片输入到 Layout JSON 链路的入口。
2. 为后续真实 AI 视觉解析预留了接口结构。
3. 避免过早接入 AI、Figma、MySQL 导致项目范围失控。
4. 保持了项目当前的可测试性和可演示性。
5. 延续了 Worker、后端、前端分层验证的开发方式。

## 当前限制

当前系统暂未接入真实 AI 视觉模型，因此不会真实解析图片内容。Layout JSON 由 templateKey 对应的 mock 模板生成。该设计用于验证产品流程和系统接口，为后续真实图片解析能力做准备。
```

---

## 十、Week 07 最终验收标准

### Worker 验收

命令：

```bash
python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver
```

必须通过。

---

### Backend 验收

命令：

```bash
mvn test
```

必须通过。

---

### Frontend 验收

命令：

```bash
npm run test
npm run build
```

必须通过。

---

### Manual Smoke 验收

手动验证：

1. 打开 `/dev/image-to-layout`。
2. 选择一张本地图片。
3. 确认图片能在浏览器本地预览。
4. 选择 `landing-basic`。
5. 点击创建 image-layout mock job。
6. 确认返回 jobId。
7. 确认 `status = SUCCESS`。
8. 确认 `sourceType = IMAGE_TEMPLATE_MOCK`。
9. 确认 `templateKey = landing-basic`。
10. 确认页面展示 Layout JSON。
11. 选择 `card-list`。
12. 确认可以创建另一个 mock job。
13. 选择 `invalid-layout`。
14. 确认可以展示失败状态或校验错误。
15. 确认页面明确提示“暂未接入真实 AI 视觉解析”。
16. 确认没有真实图片上传到后端。
17. 确认没有 MySQL 相关代码。
18. 确认没有 Redis / RabbitMQ 相关代码。
19. 确认没有 Figma API 相关代码。
20. 确认没有 AI SDK 相关代码。

---

## 十一、Week 07 成功后的项目状态

Week 07 完成后，项目状态应该变成：

已完成：

1. 图片输入场景入口。
2. 本地图片预览。
3. templateKey 半自动模板选择。
4. image-layout mock job 创建。
5. mock Layout JSON 返回。
6. 前端 Layout JSON 展示。
7. Worker template resolver。
8. Worker resolver 回归测试。
9. 后端 image-layout mock API。
10. 后端 API 测试。
11. 前端 image-to-layout 页面。
12. 前端页面测试。
13. Week 07 smoke 和总结文档。

仍未完成：

1. 真实图片解析。
2. 真实 AI 视觉模型。
3. Figma 文件解析。
4. MySQL 持久化。
5. 后端调用 Python Worker。
6. generated-page 自动编译预览链路。
7. 历史任务列表。
8. ZIP 导出。
9. 拖拽编辑器。

---

## 十二、Week 08 建议方向

Week 07 完成后，Week 08 可以在以下两个方向中选择一个，不能同时做。

### 方向 A：继续图片链路

主题：

```text
图片 mock 链路接 generated-page 自动预览
```

目标：

```text
image-layout mock job
-> Layout JSON
-> generated-page artifact
-> preview 页面
```

需要解决：

1. 是否由后端调用 Worker。
2. 是否先做 mock generated-page。
3. 是否设计一个 dev compile endpoint。
4. 是否继续保持不接真实 AI。

适合情况：

如果想继续强化“截图 / 图片到页面生成器”的核心能力，优先选这个。

---

### 方向 B：MySQL 持久化专题

主题：

```text
MySQL 持久化最小闭环
```

目标：

```text
generation_job
layout_artifact
generated_page_artifact
```

需要做：

1. 数据库表设计。
2. MyBatis-Plus Entity / Mapper。
3. 后端 mock 保存替换为数据库保存。
4. 后端测试。
5. generated-page preview 查询兼容。

适合情况：

如果想强化简历里的 Java / Spring Boot / MyBatis-Plus / MySQL 全栈能力，可以选这个。

建议：

MySQL 更适合放到 Week 09。
Week 08 更建议继续收口图片链路。

---

## 十三、给 Codex 的执行提示词

下面这段可以直接放进 `docs/task.md` 或发给 Codex：

```md
# Week 07 Task

## Goal

Week 07 只实现“图片输入场景与 Layout JSON Mock 链路验证”，为后续“图片 -> Layout JSON -> HTML 静态预览”做准备。

本周不接真实 AI，不接 Figma，不接 MySQL，不接 Redis / RabbitMQ，不做 ZIP 导出，不做拖拽编辑器，不做复杂响应式算法，不做后端调用 Python Worker。

## Scope Correction

本周不做真实图片上传到后端。

前端可以选择本地图片，并在浏览器本地预览，但后端请求只提交 imageName 和 templateKey。

templateKey 是半自动 mock 参数，用于模拟“图片识别后选择页面结构”的结果。

当前不会真实解析图片内容。

## Target Chain

Local image selection
-> local browser preview
-> imageName + templateKey
-> backend image-layout mock job
-> mock Layout JSON
-> frontend Layout JSON display
-> prepare for later generated-page preview

## Day 1 Docs

只更新 docs/current.md、docs/spec.md、docs/task.md、docs/archive/week/07-plan.md。

定义 image-to-layout mock 协议。

不要修改前端、后端、Worker 代码。

## Day 2 Worker

新增 image_layout_resolver.py 和 image template fixtures。

resolver 只做 templateKey -> Layout JSON fixture。

不要读取图片。
不要接 AI。
不要接 HTTP。
不要调用后端。
不要新增第三方依赖。

## Day 3 Worker Tests

新增 test_image_layout_resolver.py。

覆盖 success、unknown templateKey、invalid layout、source.type、结构稳定性。

验证：

python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver

## Day 4 Backend

新增 dev mock API：

POST /api/dev/image-layout-jobs
GET /api/dev/image-layout-jobs/{jobId}

不接 MySQL。
不创建 Entity / Mapper。
不上传文件。
不调用 Python Worker。

## Day 5 Backend Tests

覆盖：

创建 landing-basic 成功
创建 card-list 成功
unknown templateKey 失败
空 body 失败
array body 失败
空 imageName 失败
空 templateKey 失败
过长 imageName 失败
GET 已存在 job 成功
GET 不存在 job 404

验证：

mvn test

## Day 6 Frontend

新增 /dev/image-to-layout 页面。

支持：

本地图片选择
本地图片预览
templateKey 选择
创建 image-layout mock job
展示 jobId / status / sourceType / imageName / templateKey
展示 Layout JSON
展示 errors / warnings

页面必须明确提示：

当前为 Week 07 mock / 半自动链路。
图片仅用于输入场景演示，暂未接入真实 AI 视觉解析。
Layout JSON 由 templateKey 对应的 mock 模板生成。

## Day 7 Frontend Tests and Smoke Docs

拆成两个单线程任务：

1. 前端测试
2. Week 07 smoke 和 summary 文档归档

前端测试覆盖：

页面标题显示
mock 说明文案显示
templateKey 下拉显示
创建任务成功展示 Layout JSON
创建任务失败展示错误
请求失败展示 error 状态
不出现“真实 AI 已解析”误导文案

文档归档：

docs/archive/week/07-dev-smoke.md
docs/archive/week/07-summary.md
docs/archive/week/07-report-material.md

## Acceptance

Worker:

python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver

Backend:

mvn test

Frontend:

npm run test
npm run build

Manual smoke:

打开 /dev/image-to-layout
选择本地图片
确认本地图片预览
选择 landing-basic
创建 image-layout mock job
查看 Layout JSON
确认页面明确提示未接真实 AI
确认没有真实图片上传到后端
确认没有 MySQL 相关代码
```

---

## 十四、最终结论

Week 07 最终采用：

```text
图片输入场景与 Layout JSON Mock 链路验证
```

不采用：

```text
MySQL 持久化专题
```

原因：

1. 当前项目核心卖点是“截图 / 图片到响应式页面生成器”。
2. Week 07 应该优先补齐图片输入到 Layout JSON 的入口。
3. MySQL 是工程完整性增强，但不是当前最关键的生成器能力。
4. 图片链路和 MySQL 同周做会导致范围扩大。
5. MySQL 更适合作为 Week 09 独立专题处理。

推荐后续节奏：

```text
Week 07：图片输入场景与 Layout JSON Mock 链路验证
Week 08：图片 mock 链路接 generated-page 自动预览
Week 09：MySQL 持久化最小闭环
Week 10：历史任务列表 / 任务详情增强
```
