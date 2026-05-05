# Week 02 / Week 03 Prompt Archive

本文件归档 Week 02 / Week 03 阶段性长提示词。

这些内容保留历史原貌，用于追溯，不作为当前任务默认上下文。

## 模板九：Week 02 总任务

```text
你现在是本项目的项目经理 + 工程师。

当前阶段：Week 02 MVP 最小闭环开发。

请先阅读：
- AGENTS.md
- README.md
- docs/mvp-scope.md
- docs/prd.md
- docs/week/01-status.md
- docs/week/02-plan.md
- docs/week/02-status.md
- docs/api-contracts.md
- docs/frontend-pages.md
- docs/coding-rules.md
- tests/smoke/README.md

本周目标只做：
上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果。

严格不做：
- 不接真实模型 API
- 不接 Figma API / Figma MCP
- 不接 Redis
- 不接 RabbitMQ
- 不接 MySQL 实际落库
- 不创建数据库表
- 不新增 Mapper
- 可使用 DTO / VO，但不新增 Entity / Mapper / 数据库配置
- 不做真实截图解析
- 不做真实页面代码生成
- 不做导出 zip
- 不做拖拽编辑器

请先输出开发计划，不要直接改代码。

计划必须包含：
1. 准备修改哪些文件
2. 后端接口如何设计
3. 前端页面如何设计
4. 如何验证
5. 有哪些风险
6. 如何确保不越界
```

## 模板十：Week 02 Day 1 后端上传接口

```text
你现在执行 Week 02 Day 1：后端上传接口日。

目标：
完成截图上传接口 POST /api/assets/upload。

请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- docs/tasks/week02-day1-upload-api.md
- docs/api-contracts.md
- docs/coding-rules.md
- 后端上传接口相关代码

本任务只做：
1. 实现截图上传接口。
2. 保存图片到 backend/uploads/。
3. 配置 /uploads/** 静态资源映射。
4. 校验文件为空、文件大小、文件类型。
5. 返回 assetId、fileName、fileUrl、contentType、size。
6. 补充 Postman 或 curl 测试说明。

严格不做：
- 不接 MySQL
- 不建表
- 不新增 Mapper
- 不新增 Entity
- 不接 Redis
- 不接 RabbitMQ
- 不接真实模型 API
- 不做截图识别
- 不做任务创建接口

请先输出计划，说明会改哪些文件、如何验证，然后等待确认。
```

## 模板十一：Week 02 Day 2 后端任务接口

```text
你现在执行 Week 02 Day 2：后端任务接口日。

目标：
完成任务创建、任务状态查询、mock 结果查询接口。

请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- docs/tasks/week02-day2-generation-api.md
- docs/api-contracts.md
- docs/coding-rules.md
- 后端任务接口相关代码

本任务只做：
1. POST /api/generations
2. GET /api/generations/{jobId}
3. GET /api/generations/{jobId}/result
4. 使用内存 Map 保存任务
5. 返回 mock layoutJson、vueCode、cssCode
6. 保持统一 ApiResponse 结构

严格不做：
- 不接 MySQL
- 不创建数据库表
- 不新增 Mapper
- 不新增 Entity
- 不接 Redis
- 不接 RabbitMQ
- 不调用 Python Worker
- 不接真实模型 API
- 不做真实截图解析

请先输出计划，说明会改哪些文件、接口结构、验证方式，然后等待确认。
```

## 模板十二：Week 02 Day 3 前端创建任务页

```text
你现在执行 Week 02 Day 3：前端创建任务页日。

目标：
完成前端选择图片、预览图片、上传截图、创建任务、跳转详情页。

请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- docs/tasks/week02-day3-frontend-create-page.md
- docs/frontend-pages.md
- docs/api-contracts.md
- docs/coding-rules.md
- 前端路由、页面、接口调用相关代码

本任务只做：
1. 引入 vue-router。
2. 创建或完善创建任务页面。
3. 支持选择图片和本地预览。
4. 封装上传接口调用。
5. 封装创建任务接口调用。
6. 创建任务成功后跳转 /generation/:jobId。
7. 增加 loading 和错误提示。

严格不做：
- 不接真实模型 API
- 不做 Figma 页面
- 不做导出 zip
- 不做拖拽编辑器
- 不做在线编辑器
- 不做复杂 UI 大改版

请先输出计划，说明会改哪些文件、页面流程、验证方式，然后等待确认。
```

## 模板十三：Week 02 Day 4 前端任务详情与结果页

```text
你现在执行 Week 02 Day 4：前端任务详情与结果页日。

目标：
完成任务详情页和 mock 生成结果展示。

请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- docs/tasks/week02-day4-generation-detail-page.md
- docs/frontend-pages.md
- docs/api-contracts.md
- docs/coding-rules.md
- 前端任务详情页、路由、接口调用相关代码

本任务只做：
1. 根据 jobId 查询任务状态。
2. 展示任务状态、进度、assetId。
3. 请求并展示 mock layoutJson。
4. 请求并展示 mock vueCode。
5. 请求并展示 mock cssCode。
6. 增加返回创建页按钮。
7. 可选增加复制代码按钮。

严格不做：
- 不做真实代码预览 iframe
- 不做在线编辑器
- 不做导出 zip
- 不接真实模型 API
- 不接 Figma

请先输出计划，说明会改哪些文件、页面结构、验证方式，然后等待确认。
```

## 模板十四：Week 02 Day 5 端到端联调与收口

```text
你现在执行 Week 02 Day 5：端到端联调与收口日。

目标：
完成第二周完整验收和文档收口。

请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- docs/tasks/week02-day5-smoke-and-docs.md
- docs/week/02-status.md
- docs/api-contracts.md
- docs/frontend-pages.md
- tests/smoke/README.md

本任务只做：
1. 从零验证前端、后端、worker smoke。
2. 验证完整流程：上传截图 -> 创建任务 -> 查看状态 -> 查看 mock 结果。
3. 更新 tests/smoke/README.md。
4. 更新 docs/week/02-status.md。
5. 更新 README 中必要的 Week 02 运行说明。
6. 记录风险和第三周输入。

重点检查：
- 是否误接 MySQL
- 是否误接 Redis
- 是否误接 RabbitMQ
- 是否误接真实模型 API
- 是否误接 Figma
- 是否创建数据库表或 Mapper
- 是否有残留 dev server
- 是否误提交构建产物

请先输出验收计划，然后执行验证。
```

## 模板十五：Week 03 Day 1 Layout JSON 设计文档

```text
你现在执行 Week 03 Day 1：Layout JSON 设计文档。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day1-layout-design.md
4. docs/layout-schema-design.md（如已存在）

本任务只做：
- docs/layout-schema-design.md

严格不做：
- 不写 Schema
- 不写 examples
- 不改 worker / backend / frontend 业务代码
- 不接真实 AI / 模型 API / Figma / Redis / RabbitMQ / MySQL
- 不新增 Entity / Mapper
- 不做 Vue 页面代码生成

请先输出文档修改计划，等待确认。
```

## 模板十六：Week 03 Day 2 Schema

```text
你现在执行 Week 03 Day 2：JSON Schema。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day2-schema.md
4. docs/layout-schema-design.md
5. schema/layout.schema.json（如已存在）

本任务只做：
- schema/layout.schema.json

严格不做：
- 不写 examples
- 不写 worker 校验器
- 不改 backend / frontend 业务代码
- 不接真实 AI / 模型 API / Figma / Redis / RabbitMQ / MySQL
- 不新增 Entity / Mapper
- 不做 Vue 页面代码生成

请先输出 Schema 修改计划，等待确认。
```

## 模板十七：Week 03 Day 3 示例

```text
你现在执行 Week 03 Day 3：Layout JSON 示例。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day3-examples.md
4. docs/layout-schema-design.md
5. schema/layout.schema.json
6. examples/ 目录下已有示例（如存在）

本任务只做：
- examples/valid 下 5 个合法示例
- examples/invalid 下 3 个非法示例

严格不做：
- 不写 worker 校验器
- 不改 backend / frontend 业务代码
- 不接真实 AI / 模型 API / Figma / Redis / RabbitMQ / MySQL
- 不新增 Entity / Mapper
- 不做 Vue 页面代码生成

请先输出示例编写计划，等待确认。
```

## 模板十八：Week 03 Day 4 Worker 校验器

```text
你现在执行 Week 03 Day 4：Worker Layout JSON 校验器。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day4-validator.md
4. docs/layout-schema-design.md
5. schema/layout.schema.json
6. examples/valid 和 examples/invalid
7. worker/README.md
8. 当前任务相关 worker 代码

本任务只做：
- worker/layout_validator.py
- worker/test_layout_validator.py

严格不做：
- 不改 backend / frontend 业务代码
- 不接真实 AI / 模型 API / Figma / Redis / RabbitMQ / MySQL
- 不新增 Entity / Mapper
- 不做真实截图解析
- 不做 Vue 页面代码生成
- 不安装依赖，除非计划中说明原因并等待确认

请先输出实现计划，等待确认。
```

## 模板十九：Week 03 Day 5 校验器 Smoke 和修复

```text
你现在执行 Week 03 Day 5：校验器 smoke 和修复。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day5-validator-fix-and-smoke.md
4. docs/layout-schema-design.md
5. schema/layout.schema.json
6. examples/valid 和 examples/invalid
7. worker/layout_validator.py
8. worker/test_layout_validator.py

本任务只做：
- 校验器测试
- 校验器最小修复
- smoke 记录

严格不做：
- 不做 P1 mock 保存
- 不做前端查看页
- 不接真实 AI / 模型 API / Figma / Redis / RabbitMQ / MySQL
- 不新增 Entity / Mapper
- 不做 Vue 页面代码生成

请先输出 smoke 与修复计划，等待确认。
```

## 模板二十：Week 03 Day 6 可选 Mock 保存 / 前端查看

```text
你现在执行 Week 03 Day 6：P1 可选 mock 保存 / 前端基础查看。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day6-optional-mock-viewer.md
4. docs/layout-api-contracts.md
5. 当前任务相关前端或后端代码

前提：
- 必须先确认 Week 03 P0 已完成。

本任务只做 P1：
- 本地文件 mock 保存 Layout JSON
- 本地文件 mock 查询 Layout JSON
- 前端基础 Layout JSON 查看页

严格不做：
- 不连接 MySQL
- 不新增 Entity / Mapper
- 不写 MyBatis-Plus 持久层代码
- 不接 Redis / RabbitMQ
- 不接真实 AI / 模型 API / Figma
- 不做 Vue 页面代码生成
- 不做 JSON 在线编辑器、拖拽编辑器或导出 ZIP

请先输出实现计划，等待确认。
```

## 模板二十一：Week 03 Day 7 验收收口

```text
你现在执行 Week 03 Day 7：验收、文档收口和总结。

请只阅读：
1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/week03-day7-smoke-and-summary.md
4. docs/week/03-plan.md
5. docs/week/03-status.md
6. docs/week/03-summary.md
7. tests/smoke/README.md

本任务只做：
- Week 03 验收
- docs/week/03-status.md 更新
- docs/week/03-summary.md 填写
- 必要时更新 tests/smoke/README.md

严格不做：
- 不新增功能
- 不直接修复业务代码
- 不接真实 AI / 模型 API / Figma / Redis / RabbitMQ / MySQL
- 不新增 Entity / Mapper
- 不做 Vue 页面代码生成、拖拽编辑器、在线编辑器或导出 ZIP

请先输出验收计划，等待确认。
```
