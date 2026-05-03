# Prompt Templates

## 文件目的

本文件用于沉淀可复用的 Codex 提示词模板，减少每次开新任务时重复组织语言的成本。

当前适用于项目多阶段协作。Week 02 起，日常开发优先使用“轻量上下文任务提示词模板”，由 `AGENTS.md`、`docs/context/current-phase.md`、当前任务卡和相关代码驱动。

通用约束：

- 默认只阅读 `AGENTS.md`、`docs/context/current-phase.md`、当前任务卡和当前任务相关代码。
- 其它文档只在任务卡明确要求，或当前任务确实必须参考时读取。
- 只处理当前线程范围内的任务。
- 不接入真实模型 API、Figma API、Redis、RabbitMQ。
- 不实现真实截图解析、真实代码生成、拖拽编辑器、多页面编辑器或导出 zip。
- 如果修改目录、命令、接口约定、测试方式或当前周状态，必须同步更新相关文档。

## 模板零：轻量上下文任务提示词

```text
你现在在 screenshot-to-responsive-page-generator 仓库中工作。

当前任务：
【填写当前任务名称】

请只阅读：

1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/【当前任务卡文件名】.md
4. 当前任务相关模块代码

不要读取以下文件，除非当前任务卡明确要求，或当前任务确实必须参考：

- docs/prd.md
- docs/mvp-scope.md
- docs/architecture.md
- docs/testing.md
- docs/week/01-plan.md
- docs/week/01-status.md
- docs/week/02-plan.md
- docs/week/02-status.md
- docs/skills/*

请先输出开发计划，不要直接改代码。

开发计划必须包含：

1. 你理解的任务目标
2. 准备读取哪些文件
3. 准备修改哪些文件
4. 具体实现步骤
5. 测试方式
6. 是否存在越界风险
7. 如何确保不违反当前阶段禁止项

计划输出后停止，等待确认。
```

说明：后续每日开发优先使用本模板。下面保留的旧线程模板可作为专项任务参考，但不再要求每个任务默认读取完整周计划和全部项目文档。

## 模板一：项目经理下发任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前任务相关任务卡或状态看板

当前角色：
项目经理线程。

当前目标：
[写清楚本次要统筹的目标]

上下文：
[写清楚当前 Day、已完成内容、待拆分任务、约束和风险]

任务要求：
1. 明确本次任务目标和范围。
2. 拆分前端、后端、Worker / 模型预备、测试、文档线程的工作。
3. 标明每个线程的输入、输出、验收标准和风险。
4. 不直接扩大到当前阶段之外的功能。
5. 如状态变化，更新对应 `docs/week/*-status.md`。
6. 如果任务涉及多个线程，必须拆成多条单线程任务，并明确执行顺序；不要合并成一份大提示词。

完成条件：
1. 给出清晰任务拆分。
2. 给出验收标准。
3. 给出风险和待确认事项。
4. 如有文档变更，列出修改文件。
```

## 模板二：前端开发任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前前端任务卡
- docs/coding-rules.md
- docs/skills/frontend-task-skill.md
- 当前任务相关前端代码

当前角色：
前端开发线程。

当前目标：
[写清楚页面、组件、样式或前端验证目标]

任务要求：
1. 先输出计划，等待确认后再执行。
2. 计划中说明预计修改的文件、实施步骤、验证方式和风险。

任务范围：
1. 只修改 frontend/ 内与当前目标直接相关的文件。
2. 当前 MVP 阶段只做任务卡明确要求的页面、组件、基础响应式和接口联调。
3. 不接入真实生成能力。
4. 不实现真实截图解析。
5. 不实现真实代码生成。
6. 不实现拖拽编辑器、多页面编辑器或导出 zip。
7. 不引入组件库，除非用户明确确认。
8. 不提交 `node_modules/`、`dist/`、临时日志文件或其它构建产物。

验证方式：
1. 执行 npm install（如已安装可跳过）。
2. 执行 npm run build。
3. 必要时执行 npm run dev -- --host 127.0.0.1 --port 5173 并检查页面。
4. 如果启动 dev server，验证完成后必须停止进程，不留下后台服务。

完成后汇报：
- 改动文件
- 页面或组件变化
- 验证步骤和结果
- 风险 / 待确认事项
```

## 模板三：后端开发任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前后端任务卡
- docs/api-contracts.md（如涉及 Week 02 接口）
- docs/coding-rules.md
- docs/skills/backend-api-skill.md
- 当前任务相关后端代码

当前角色：
后端开发线程。

当前目标：
[写清楚接口、健康检查、mock 返回或后端验证目标]

计划要求：
1. 如果新增或修改接口，计划中必须说明是否涉及 Controller、Service、Mapper、DTO、VO。
2. 如果某一层不涉及，也要显式写“本次不涉及”。
3. 如涉及数据库能力，必须先说明原因并等待用户确认。

任务范围：
1. 只修改 backend/ 内与当前目标直接相关的文件。
2. 当前阶段优先完成任务卡明确要求的接口和验证。
3. MVP mock 阶段优先使用固定数据或简单内存数据，但必须说明 mock 边界。
4. 未确认前不设计数据库表、不接 MySQL、不接 Redis / RabbitMQ。
5. 未确认数据库任务前，不新增 Mapper、实体表映射或数据库配置。
6. mock 阶段不创建数据库访问层。
7. 不接入真实模型 API 或 Figma API。

验证方式：
1. 执行 mvn test。
2. 执行 mvn package -DskipTests。
3. 使用 java -jar target/backend-0.0.1-SNAPSHOT.jar 启动服务。
4. 访问 http://127.0.0.1:8080/api/health。

完成后汇报：
- 改动文件
- 接口路径、方法和返回结构
- 验证步骤和结果
- 前端联调注意事项
- 风险 / 待确认事项
```

## 模板四：Worker / 模型预备任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前 Worker 任务卡或相关任务说明
- worker/README.md
- 当前任务相关 worker 代码

当前角色：
Worker / 模型预备线程。

版本口径：
Worker 推荐目标版本为 Python 3.11；当前 smoke 脚本允许 Python 3.10+ 本地验证。

当前目标：
[写清楚 worker 入口、参数、mock 输出或 smoke 验证目标]

任务范围：
1. 只修改 worker/ 内与当前目标直接相关的文件。
2. 当前阶段只维护最小 smoke 入口和标准库脚本，除非任务卡另有明确要求。
3. 不接入真实模型 API。
4. 不接入 OpenAI 或其他模型 SDK。
5. 不接入 Figma API / Figma MCP。
6. 不实现真实截图解析。
7. 不实现真实页面代码生成。
8. 当前 smoke 阶段优先使用 Python 标准库，不引入额外依赖。

验证方式：
1. 执行 python --version。
2. 执行 python main.py --smoke。
3. 确认输出 worker smoke pass，退出码为 0。

完成后汇报：
- 改动文件
- 输入参数和输出结果
- 验证步骤和结果
- 后续扩展点
- 风险 / 待确认事项
```

## 模板五：测试验收任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前验收任务卡
- tests/smoke/README.md

当前角色：
测试线程。

当前目标：
[写清楚要验收的模块或 smoke 范围]

任务范围：
1. 只执行验证和记录结果。
2. 不直接修改 frontend/、backend/、worker/ 业务代码。
3. 如发现问题，记录复现步骤、实际结果、预期结果和影响范围。
4. 测试命令必须与 tests/smoke/README.md 保持一致。

验证清单：
1. 前端：npm run build，必要时短暂启动 dev 服务并访问页面。
2. 后端：mvn test、mvn package -DskipTests、java -jar 后访问 /api/health。
3. Worker：python --version、python main.py --smoke。
4. 文档：确认 README、current-phase、当前任务卡、状态看板和 smoke 文档没有明显冲突。

完成后汇报：
- 验收范围
- 执行命令
- 通过项
- 失败项和复现步骤
- 风险 / 待确认事项
```

## 模板六：文档更新任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前文档任务卡或目标文档说明
- 需要更新的目标文档

当前角色：
文档线程。

当前目标：
更新 [文档路径]

任务范围：
1. 使用中文表述。
2. 只更新与当前目标直接相关的文档。
3. 保持当前阶段边界。
4. 不写超出当前阶段的功能承诺。
5. 如果修改命令、目录、接口约定、测试方式或周状态，同步更新相关文档。

完成后汇报：
- 改动文件
- 主要内容变化
- 与哪些文档完成同步
- 风险 / 待确认事项
```

## 模板七：Bug 修复任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前任务卡或问题相关文档
- docs/skills/bugfix-skill.md
- 问题相关模块文档或代码

当前角色：
Bug 修复线程。

当前问题：
[描述问题现象、报错、复现步骤]

任务范围：
1. 先复现或确认问题。
2. 定位根因，区分前端、后端、Worker、测试命令或文档问题。
3. 只做最小必要修改。
4. 不借修复机会做无关重构。
5. 如测试线程只报告问题，本线程负责修复和验证。

完成后汇报：
- 根因
- 改动文件
- 修复内容
- 验证步骤和结果
- 剩余风险 / 待确认事项
```

## 模板八：每日验收总结

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前状态看板

当前角色：
项目经理线程 / 验收总结线程。

当前目标：
汇总 Day [数字] 验收结果，并更新对应 `docs/week/*-status.md`。

需要汇总：
1. 今日目标。
2. 各线程状态：待执行 / 执行中 / 待验收 / 通过 / 阻塞。
3. 已执行的验证命令。
4. 通过项。
5. 失败项或阻塞项。
6. 风险和下一步。

完成条件：
1. 对应 `docs/week/*-status.md` 与真实进展一致。
2. 不修改业务代码。
3. 最终汇报改动文件、验证方式、验证结果和风险。
```

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
