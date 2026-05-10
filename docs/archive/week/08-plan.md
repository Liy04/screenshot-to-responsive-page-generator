项目：screenshot-to-responsive-page-generator

当前任务：
对 Week 08 做完整验收。不要新增功能，不要大改代码，不要扩展范围。
本次目标是检查 Week 08 是否真正完成，而不是继续开发 Week 09。

Week 08 核心目标：
验证 imageName + templateKey -> Layout JSON -> generated-page artifact -> generated-page iframe 预览 这条 mock 链路是否完整跑通。

当前项目阶段：
Week 07 已完成，Week 08 的目标是把 Week 07 的 image-to-layout mock 链路继续推进到 generated-page mock 预览链路。

Week 07 已有能力：
1. Worker 已有 Layout JSON validator。
2. Worker 已有 static generator。
3. Worker 已有 image template layout resolver。
4. 后端已有 image-layout dev mock API。
5. 前端已有 /dev/image-to-layout 页面。
6. 前端支持本地图片选择与浏览器本地预览。
7. 前端支持 templateKey：
   - landing-basic
   - card-list
   - invalid-layout
8. 后端 image-layout mock API 只接收 imageName 和 templateKey，不上传真实图片。
9. invalid-layout 是已知失败链路。
10. unknown templateKey 应返回 400。
11. 不存在 jobId 应返回 404。

Week 08 目标：
将 image-to-layout mock 链路升级为 image-to-page mock 链路。

目标链路如下：

用户选择本地图片
  -> 前端只读取 imageName，用于本地预览
  -> 前端选择 templateKey
  -> POST /api/dev/image-page-jobs
  -> 后端返回 layoutArtifact
  -> 后端返回 generatedPageArtifact
  -> 前端展示 Layout JSON
  -> 前端展示 generated-page artifact
  -> 前端用 iframe sandbox="" 安全预览 generated-page

重要边界：
本周仍然是 mock 链路，不是真实 AI 链路。
本周不做真实图片解析。
本周不做真实图片上传。
本周不做真实 Worker 调用。
本周不做数据库持久化。

请严格按照以下验收流程执行。

==================================================
一、先阅读项目上下文
==================================================

请先阅读以下文件，理解当前项目规则和 Week 08 边界：

- AGENTS.md
- docs/current.md
- docs/plan.md
- docs/spec.md
- docs/INDEX.md
- docs/archive/week/07-plan.md
- docs/archive/week/08-plan.md

如果某些文件不存在，请在最终验收报告中标记为“缺失”，但不要因为文档缺失就直接停止验收。

阅读时重点确认：
1. 当前是否处于 Docs Lite 模式。
2. 当前活跃文档有哪些。
3. Week 08 是否明确以 image-to-page mock 闭环为目标。
4. 禁止事项是否仍然有效。
5. Week 08 是否没有引入真实 AI、MySQL、Redis、RabbitMQ、Figma、真实图片上传、后端调用 Python Worker 等能力。

==================================================
二、检查禁止事项
==================================================

请检查 Week 08 是否违反以下禁止事项。

禁止事项：

1. 不接真实 AI / OpenAI / Claude / Gemini。
2. 不接 Figma API / Figma MCP。
3. 不接 MySQL 实际落库。
4. 不创建数据库表。
5. 不创建 Entity / Mapper。
6. 不接 Redis。
7. 不接 RabbitMQ。
8. 不做真实截图解析。
9. 不上传真实图片到后端。
10. 不让后端调用 Python Worker。
11. 不做 ZIP 导出。
12. 不做拖拽编辑器 / 在线编辑器。
13. 不做复杂权限 / 登录注册。
14. 不做 Playwright 视觉回归。
15. 不引入新的外部服务依赖。

请搜索以下关键词，判断是否存在越界：

AI 相关：
- OpenAI
- Claude
- Gemini
- apiKey
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GEMINI_API_KEY

数据库相关：
- Entity
- Mapper
- TableName
- MyBatis
- DataSource
- schema.sql
- migration
- liquibase
- flyway

Redis / RabbitMQ 相关：
- Redis
- RabbitMQ
- RabbitTemplate
- Queue
- Exchange

图片上传相关：
- multipart/form-data
- MultipartFile
- base64
- image upload
- file upload
- FormData

后端调用 Worker 相关：
- ProcessBuilder
- Runtime.getRuntime
- python
- worker

安全相关：
- allow-scripts
- allow-same-origin
- <script
- onclick
- onerror
- onload
- javascript:

注意：
文档中出现“禁止接入真实 AI”等说明是允许的。
历史说明中出现 MySQL / Redis / RabbitMQ 是允许的。
但 Week 08 新增代码中不允许真正引入这些能力。

最终报告中请明确输出：

禁止事项检查：
- AI 接入：PASS / FAILED
- Figma 接入：PASS / FAILED
- MySQL 接入：PASS / FAILED
- Redis 接入：PASS / FAILED
- RabbitMQ 接入：PASS / FAILED
- 真实图片上传：PASS / FAILED
- 后端调用 Python Worker：PASS / FAILED
- ZIP 导出：PASS / FAILED
- 拖拽编辑器：PASS / FAILED
- 登录注册 / 权限：PASS / FAILED
- Playwright 视觉回归：PASS / FAILED

==================================================
三、后端接口验收
==================================================

Week 08 期望存在以下接口：

POST /api/dev/image-page-jobs
GET  /api/dev/image-page-jobs/{jobId}

请检查后端是否实现了这两个接口。

接口目标：
1. POST 接收 imageName 和 templateKey。
2. 后端不接收真实图片文件。
3. 后端不接收 multipart/form-data。
4. 后端不接收 base64 图片。
5. 后端不调用 Python Worker。
6. 后端使用内存 Map 保存 job。
7. 后端使用项目现有 ApiResponse 包装风格。
8. SUCCESS 时返回 layoutArtifact 和 generatedPageArtifact。
9. FAILED 时不返回 generatedPageArtifact。
10. unknown templateKey 返回 400。
11. 不存在 jobId 返回 404。

--------------------------------------------------
3.1 验收 POST landing-basic
--------------------------------------------------

请求：

POST /api/dev/image-page-jobs
Content-Type: application/json

请求体：

{
  "imageName": "landing-demo.png",
  "templateKey": "landing-basic"
}

预期结果：

1. HTTP 状态码：200。
2. data.status：SUCCESS。
3. data.sourceType：IMAGE_TEMPLATE_MOCK。
4. data.imageName：landing-demo.png。
5. data.templateKey：landing-basic。
6. data.layoutArtifact：不为空。
7. data.generatedPageArtifact：不为空。
8. data.errors：为空数组或不存在错误。
9. data.warnings：允许为空数组。

通过标准：
landing-basic 可以成功生成 Layout JSON 和 generated-page artifact。

--------------------------------------------------
3.2 验收 POST card-list
--------------------------------------------------

请求：

POST /api/dev/image-page-jobs
Content-Type: application/json

请求体：

{
  "imageName": "card-list-demo.png",
  "templateKey": "card-list"
}

预期结果：

1. HTTP 状态码：200。
2. data.status：SUCCESS。
3. data.sourceType：IMAGE_TEMPLATE_MOCK。
4. data.imageName：card-list-demo.png。
5. data.templateKey：card-list。
6. data.layoutArtifact：不为空。
7. data.generatedPageArtifact：不为空。
8. data.errors：为空数组或不存在错误。

通过标准：
card-list 可以成功生成 Layout JSON 和 generated-page artifact。

--------------------------------------------------
3.3 验收 POST invalid-layout
--------------------------------------------------

请求：

POST /api/dev/image-page-jobs
Content-Type: application/json

请求体：

{
  "imageName": "invalid-demo.png",
  "templateKey": "invalid-layout"
}

预期结果：

1. HTTP 状态码：200。
2. data.status：FAILED。
3. data.sourceType：IMAGE_TEMPLATE_MOCK。
4. data.imageName：invalid-demo.png。
5. data.templateKey：invalid-layout。
6. data.generatedPageArtifact：必须为空。
7. data.errors：必须不为空。
8. 不应该返回 SUCCESS。
9. 不应该生成 generated-page artifact。

通过标准：
invalid-layout 作为失败链路可以被正确识别，并且不会生成 generated-page artifact。

--------------------------------------------------
3.4 验收 POST unknown-template
--------------------------------------------------

请求：

POST /api/dev/image-page-jobs
Content-Type: application/json

请求体：

{
  "imageName": "unknown-demo.png",
  "templateKey": "unknown-template"
}

预期结果：

1. HTTP 状态码：400。
2. 不返回 SUCCESS。
3. 不创建成功 job。
4. 不生成 layoutArtifact。
5. 不生成 generatedPageArtifact。
6. message 中应体现 unknown templateKey 或类似错误说明。

通过标准：
未知 templateKey 会被拒绝，不会被伪造成成功结果。

--------------------------------------------------
3.5 验收 GET 已存在 jobId
--------------------------------------------------

步骤：

1. 先通过 landing-basic 创建一个成功 job。
2. 从响应中取出 jobId。
3. 请求：

GET /api/dev/image-page-jobs/{jobId}

预期结果：

1. HTTP 状态码：200。
2. data.jobId 与创建时一致。
3. data.status 与创建时一致。
4. data.imageName 与创建时一致。
5. data.templateKey 与创建时一致。
6. 如果是 SUCCESS，layoutArtifact 不为空。
7. 如果是 SUCCESS，generatedPageArtifact 不为空。

通过标准：
创建后的 job 可以通过 jobId 查询。

--------------------------------------------------
3.6 验收 GET 不存在 jobId
--------------------------------------------------

请求：

GET /api/dev/image-page-jobs/not-exist-job-id

预期结果：

1. HTTP 状态码：404。
2. 不返回 SUCCESS。
3. data 为空或 null。
4. message 中应体现 job 不存在或 not found。

通过标准：
不存在的 jobId 不会返回伪造成功结果。

==================================================
四、后端自动化测试验收
==================================================

请检查后端测试是否覆盖以下用例：

1. landing-basic 创建成功。
2. card-list 创建成功。
3. invalid-layout 返回 HTTP 200，但 data.status=FAILED。
4. unknown-template 返回 HTTP 400。
5. GET 已存在 jobId 返回 200。
6. GET 不存在 jobId 返回 404。
7. SUCCESS 时 layoutArtifact 不为空。
8. SUCCESS 时 generatedPageArtifact 不为空。
9. FAILED 时 generatedPageArtifact 为空。
10. FAILED 时 errors 不为空。

请运行：

mvn test

验收标准：

1. BUILD SUCCESS。
2. 测试失败数为 0。
3. 错误数为 0。
4. 没有因为数据库、Redis、RabbitMQ、Worker 未启动导致测试失败。

最终报告中请记录：

Backend test result:
- Command: mvn test
- Result: PASS / FAILED
- Tests: xx tests
- Failures: x
- Errors: x
- Notes: xxx

==================================================
五、Worker 回归验收
==================================================

Week 08 不应该新增真实 Worker 调用。
但必须保证 Worker 旧能力没有被破坏。

请确认：

1. 后端 image-page dev mock API 不调用 Python Worker。
2. 后端不通过命令行启动 Python。
3. 后端不依赖 worker 服务进程。
4. 后端不使用 ProcessBuilder 或 Runtime.getRuntime 调 Python。
5. Week 08 的 generatedPageArtifact 可以是 Java dev mock artifact，不要求真实 Worker 编译产物。

请运行 Worker 回归测试：

python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver

预期结果：

1. 所有测试通过。
2. 不破坏 Week 07 的 resolver 能力。
3. 不破坏 Layout JSON validator。
4. 不破坏 static generator。

如果之前是 45 tests OK，那么 Week 08 应至少保持这些测试通过。
测试数量增加也可以，但不能减少关键覆盖。

最终报告中请记录：

Worker test result:
- Command: python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver
- Result: PASS / FAILED
- Tests: xx tests
- Notes: xxx

==================================================
六、前端页面验收
==================================================

页面地址：

/dev/image-to-layout

Week 08 推荐继续增强这个页面，而不是必须新建 /dev/image-to-page。

页面应支持：

1. 本地图片选择。
2. 本地图片浏览器预览。
3. templateKey 选择。
4. 请求后端时只发送 imageName 和 templateKey。
5. 不上传真实图片文件。
6. 不发送 base64 图片。
7. SUCCESS 时展示 job 信息。
8. SUCCESS 时展示 Layout JSON。
9. SUCCESS 时展示 generatedPageArtifact。
10. SUCCESS 时展示 generated-page iframe 预览。
11. FAILED 时展示 errors。
12. FAILED 时不展示 iframe。
13. unknown-template 或 400 错误时展示错误信息。
14. 页面无白屏。
15. 控制台无明显运行时报错。

--------------------------------------------------
6.1 前端 landing-basic 验收
--------------------------------------------------

操作：

1. 访问 /dev/image-to-layout。
2. 选择任意本地图片。
3. templateKey 选择 landing-basic。
4. 点击运行按钮。

预期：

1. 页面显示 jobId。
2. 页面显示 status=SUCCESS。
3. 页面显示 sourceType=IMAGE_TEMPLATE_MOCK。
4. 页面显示 imageName。
5. 页面显示 templateKey=landing-basic。
6. 页面显示 layoutArtifact。
7. 页面显示 Layout JSON。
8. 页面显示 generatedPageArtifact。
9. 页面显示 generated-page iframe 预览。
10. iframe 中有页面内容。

通过标准：
landing-basic 在前端完整展示成功链路。

--------------------------------------------------
6.2 前端 card-list 验收
--------------------------------------------------

操作：

1. templateKey 选择 card-list。
2. 点击运行按钮。

预期：

1. 页面显示 status=SUCCESS。
2. 页面显示 templateKey=card-list。
3. 页面显示 Layout JSON。
4. 页面显示 generatedPageArtifact。
5. 页面显示 generated-page iframe 预览。
6. iframe 中有页面内容。

通过标准：
card-list 在前端完整展示成功链路。

--------------------------------------------------
6.3 前端 invalid-layout 验收
--------------------------------------------------

操作：

1. templateKey 选择 invalid-layout。
2. 点击运行按钮。

预期：

1. HTTP 请求成功。
2. 页面显示 status=FAILED。
3. 页面显示 errors。
4. 页面不展示 generated-page iframe。
5. 页面不误导用户以为生成成功。
6. generatedPageArtifact 为空或不展示。

通过标准：
失败链路能被用户看懂，失败时不会展示页面预览。

--------------------------------------------------
6.4 前端 unknown-template 验收
--------------------------------------------------

如果页面下拉框里没有 unknown-template，可以通过测试模拟或接口工具验证。

预期：

1. 后端返回 400。
2. 前端展示错误提示。
3. 不展示 Layout JSON。
4. 不展示 generatedPageArtifact。
5. 不展示 iframe。

通过标准：
前端能处理后端 400 错误。

==================================================
七、iframe 安全验收
==================================================

这是 Week 08 的重点。

请检查 generated-page iframe 是否满足：

1. iframe 必须使用 sandbox=""。
2. 不允许 allow-scripts。
3. 不允许 allow-same-origin。
4. 不允许 allow-forms。
5. 不允许 allow-popups。
6. generated-page mock HTML 不允许出现 <script>。
7. generated-page mock HTML 不允许出现 onclick。
8. generated-page mock HTML 不允许出现 onerror。
9. generated-page mock HTML 不允许出现 onload。
10. generated-page mock HTML 不允许出现 javascript:。

建议搜索：

allow-scripts
allow-same-origin
allow-forms
allow-popups
<script
onclick
onerror
onload
javascript:

通过标准：

1. iframe 存在 sandbox=""。
2. 项目新增代码中不出现 allow-scripts。
3. generated-page mock artifact 不包含可执行脚本。
4. iframe 不具备脚本执行权限。

最终报告中请记录：

Iframe security check:
- sandbox="": PASS / FAILED
- no allow-scripts: PASS / FAILED
- no allow-same-origin: PASS / FAILED
- no script tag in generated artifact: PASS / FAILED
- no inline event handler: PASS / FAILED

==================================================
八、前端自动化测试验收
==================================================

请检查前端测试是否覆盖以下用例：

1. landing-basic 成功后展示 generated-page preview。
2. card-list 成功后展示 generated-page preview。
3. invalid-layout 失败后不展示 iframe。
4. FAILED 时展示错误信息。
5. iframe 使用 sandbox=""。
6. 页面中不出现 allow-scripts。
7. 请求后端时只发送 imageName 和 templateKey。
8. 不上传真实图片文件。

请运行：

npm run test

通过标准：

1. 所有测试通过。
2. 没有组件渲染异常。
3. 没有请求 mock 异常。
4. 没有 snapshot 异常。

请运行：

npm run build

通过标准：

1. 构建成功。
2. 无 TypeError。
3. 无 unresolved import。
4. 无 Vite build error。

最终报告中请记录：

Frontend test result:
- Command: npm run test
- Result: PASS / FAILED
- Tests: xx passed
- Notes: xxx

Frontend build result:
- Command: npm run build
- Result: PASS / FAILED
- Notes: xxx

==================================================
九、联调 Smoke 验收
==================================================

Smoke 是最终手动验收。
请按以下顺序执行。

--------------------------------------------------
9.1 启动后端
--------------------------------------------------

运行：

mvn spring-boot:run

或启动 jar：

java -jar target/xxx.jar

验收：

1. 8080 启动成功。
2. 无端口冲突。
3. 无数据库连接依赖错误。
4. 无 Redis 依赖错误。
5. 无 RabbitMQ 依赖错误。
6. 无 Worker 未启动导致的错误。

注意：
Week 08 仍是 mock 链路，因此不应该因为 MySQL / Redis / RabbitMQ / Worker 没启动导致后端启动失败。

--------------------------------------------------
9.2 启动前端
--------------------------------------------------

运行：

npm run dev

验收：

1. Vite 启动成功。
2. 5174 可访问。
3. 代理到后端 API 正常。

--------------------------------------------------
9.3 访问页面
--------------------------------------------------

访问：

http://localhost:5174/dev/image-to-layout

验收：

1. 页面返回 200。
2. 页面无白屏。
3. 本地图片选择正常。
4. templateKey 选择正常。
5. 控制台无明显运行时报错。

--------------------------------------------------
9.4 landing-basic smoke
--------------------------------------------------

操作：

1. 选择任意本地图片。
2. templateKey 选择 landing-basic。
3. 点击运行。

预期：

1. status=SUCCESS。
2. 显示 Layout JSON。
3. 显示 layoutArtifact。
4. 显示 generatedPageArtifact。
5. 显示 iframe。
6. iframe 中有页面内容。
7. Network 中请求体只包含 imageName 和 templateKey。
8. 没有上传真实图片。

记录：

landing-basic: PASS / FAILED

--------------------------------------------------
9.5 card-list smoke
--------------------------------------------------

操作：

1. templateKey 选择 card-list。
2. 点击运行。

预期：

1. status=SUCCESS。
2. 显示 Layout JSON。
3. 显示 layoutArtifact。
4. 显示 generatedPageArtifact。
5. 显示 iframe。
6. iframe 中有页面内容。

记录：

card-list: PASS / FAILED

--------------------------------------------------
9.6 invalid-layout smoke
--------------------------------------------------

操作：

1. templateKey 选择 invalid-layout。
2. 点击运行。

预期：

1. status=FAILED。
2. 显示 errors。
3. 不显示 generated-page iframe。
4. generatedPageArtifact 为空或不展示。
5. 不误导用户以为生成成功。

记录：

invalid-layout: PASS / FAILED

--------------------------------------------------
9.7 unknown-template smoke
--------------------------------------------------

可以用 Postman、curl 或测试模拟。

请求：

POST /api/dev/image-page-jobs
Content-Type: application/json

{
  "imageName": "unknown.png",
  "templateKey": "unknown-template"
}

预期：

1. HTTP 400。
2. 不返回 SUCCESS。
3. 不创建成功 job。
4. 不返回 generatedPageArtifact。

记录：

unknown-template: PASS / FAILED

--------------------------------------------------
9.8 nonexistent jobId smoke
--------------------------------------------------

请求：

GET /api/dev/image-page-jobs/not-exist-job-id

预期：

1. HTTP 404。
2. 不返回 SUCCESS。
3. 不返回伪造 job。

记录：

not-found jobId: PASS / FAILED

--------------------------------------------------
9.9 停止服务
--------------------------------------------------

验收结束后停止：

1. 后端 8080 服务。
2. 前端 5174 服务。

记录：

Backend stopped: YES / NO
Frontend stopped: YES / NO

==================================================
十、文档验收
==================================================

Week 08 结束后，文档必须同步更新。

请检查并补齐以下活跃文档：

- AGENTS.md
- docs/current.md
- docs/plan.md
- docs/spec.md
- docs/INDEX.md

验收标准：

1. current.md 反映 Week 08 已完成状态。
2. plan.md 说明下一步方向。
3. spec.md 记录 image-page mock API 协议。
4. INDEX.md 能找到 Week 08 归档文档。
5. AGENTS.md 仍然说明当前禁止事项。
6. 文档中明确说明 Week 08 未接真实 AI / Figma / MySQL / Redis / RabbitMQ / Worker 调用 / 真实图片上传。

请检查并补齐以下归档文档：

- docs/archive/week/08-plan.md
- docs/archive/week/08-summary.md
- docs/archive/week/08-dev-smoke.md
- docs/archive/week/08-report-material.md

--------------------------------------------------
10.1 08-summary.md 必须包含
--------------------------------------------------

1. Week 08 目标。
2. Week 08 已完成内容。
3. 新增或改造的后端接口。
4. 前端页面改动。
5. 测试结果。
6. smoke 结果。
7. 明确未做事项。
8. 当前风险。
9. Week 09 建议方向。

建议内容结构：

# Week 08 Summary

## Goal

打通 image-to-layout mock 与 generated-page mock 预览链路。

## Completed

- 新增 image-page dev mock API。
- 支持 landing-basic / card-list 成功链路。
- 支持 invalid-layout 失败链路。
- 支持 unknown-template 400。
- 支持不存在 jobId 404。
- 前端 /dev/image-to-layout 展示 generated-page artifact。
- SUCCESS 时展示 generated-page iframe。
- FAILED 时不展示 iframe。

## Test Results

- Backend: mvn test PASS / FAILED
- Worker: python unittest PASS / FAILED
- Frontend: npm run test PASS / FAILED
- Frontend build: npm run build PASS / FAILED

## Smoke Results

- landing-basic: PASS / FAILED
- card-list: PASS / FAILED
- invalid-layout: PASS / FAILED
- unknown-template: PASS / FAILED
- nonexistent jobId: PASS / FAILED

## Not Done

- 未接真实 AI。
- 未接 Figma。
- 未接 MySQL。
- 未上传真实图片。
- 未调用 Python Worker。
- 未做 ZIP 导出。
- 未做拖拽编辑器。
- 未做登录注册 / 权限。

## Risks

- Java mock 与 Python fixture 仍可能双写。
- generated-page 仍是 mock artifact。
- 还没有真实图片解析能力。
- 还没有持久化能力。
- image-to-page 仍然是 dev mock 链路。

## Next Direction

Week 09 建议优先处理：
1. 统一 Java mock 与 Python fixture 的协议来源。
2. 或者增强 Layout JSON 样式表达能力。
3. 暂不建议直接接 AI。

--------------------------------------------------
10.2 08-dev-smoke.md 必须包含
--------------------------------------------------

建议内容结构：

# Week 08 Dev Smoke

## Environment

- Backend: 8080
- Frontend: 5174
- Worker: not started
- MySQL: not used
- Redis: not used
- RabbitMQ: not used
- AI: not used
- Figma: not used

## Cases

### landing-basic

Result: PASS / FAILED
Notes:

### card-list

Result: PASS / FAILED
Notes:

### invalid-layout

Result: PASS / FAILED
Notes:

### unknown-template

Result: PASS / FAILED
Notes:

### nonexistent jobId

Result: PASS / FAILED
Notes:

## Security Check

- iframe sandbox="": PASS / FAILED
- no allow-scripts: PASS / FAILED
- no real image upload: PASS / FAILED
- no backend Python Worker call: PASS / FAILED

## Final Result

Week 08 smoke result: PASS / PARTIAL / FAILED

--------------------------------------------------
10.3 08-report-material.md 必须包含
--------------------------------------------------

用于后续汇报或简历包装的材料。

建议包含：

1. Week 08 完成了什么。
2. 技术亮点。
3. 关键接口。
4. 前端页面能力。
5. 测试与质量保障。
6. 安全控制点。
7. 项目边界意识。
8. 下一阶段计划。

示例：

# Week 08 Report Material

## 本周成果

本周完成 image-to-layout mock 与 generated-page mock 预览链路打通，实现从图片场景 mock 输入到页面产物 mock 预览的完整闭环。

## 核心能力

- 支持 imageName + templateKey 创建 image-page dev mock job。
- 支持 landing-basic / card-list 成功生成 layoutArtifact 与 generatedPageArtifact。
- 支持 invalid-layout 失败链路验证。
- 支持 unknown-template 400 与不存在 jobId 404。
- 前端支持 generated-page iframe 安全预览。

## 技术亮点

- 使用 dev mock API 验证生成链路，避免过早接入真实 AI。
- 使用 ApiResponse 统一接口响应。
- 使用 iframe sandbox="" 控制预览安全。
- 保持真实图片不上传，仅在浏览器本地预览。
- 保持后端不调用 Python Worker，降低 Week 08 集成复杂度。

## 测试结果

- Backend mvn test: PASS / FAILED
- Worker unittest: PASS / FAILED
- Frontend npm run test: PASS / FAILED
- Frontend npm run build: PASS / FAILED

## 当前边界

- 未接真实 AI。
- 未接 Figma。
- 未接数据库。
- 未接 Redis / RabbitMQ。
- 未上传真实图片。
- 未调用 Python Worker。
- 未做 ZIP 导出。

## 下一步方向

Week 09 建议优先处理协议统一或 Layout JSON 表达能力增强。

==================================================
十一、最终验收命令清单
==================================================

请按以下顺序执行：

1. 查看 Git 状态：

git status

2. Worker 回归测试：

python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver

3. 后端测试：

mvn test

4. 前端测试：

npm run test

5. 前端构建：

npm run build

6. 启动后端：

mvn spring-boot:run

或：

java -jar target/xxx.jar

7. 启动前端：

npm run dev

8. 浏览器访问：

http://localhost:5174/dev/image-to-layout

9. 手动验收：

- landing-basic
- card-list
- invalid-layout
- unknown-template
- 不存在 jobId
- iframe sandbox
- 真实图片未上传
- 后端未调用 Worker

10. 停止服务：

- 停止 8080 后端服务
- 停止 5174 前端服务

==================================================
十二、最终通过标准
==================================================

只有全部满足下面条件，Week 08 才算完整验收通过：

1. 后端 image-page dev mock API 可用。
2. POST /api/dev/image-page-jobs 可用。
3. GET /api/dev/image-page-jobs/{jobId} 可用。
4. landing-basic 成功链路通过。
5. card-list 成功链路通过。
6. invalid-layout 失败链路通过。
7. unknown-template 400 通过。
8. 不存在 jobId 404 通过。
9. 前端可以展示 Layout JSON。
10. 前端可以展示 layoutArtifact。
11. 前端可以展示 generatedPageArtifact。
12. SUCCESS 时 iframe 出现。
13. FAILED 时 iframe 不出现。
14. iframe 使用 sandbox=""。
15. 项目新增代码中没有 allow-scripts。
16. generated-page mock HTML 不包含 script。
17. generated-page mock HTML 不包含 onclick / onerror / onload / javascript:。
18. 没有上传真实图片到后端。
19. 前端请求后端时只发送 imageName 和 templateKey。
20. 没有接真实 AI。
21. 没有接 Figma。
22. 没有接 MySQL。
23. 没有创建 Entity / Mapper / 数据库表。
24. 没有接 Redis。
25. 没有接 RabbitMQ。
26. 没有让后端调用 Python Worker。
27. 没有做 ZIP 导出。
28. 没有做拖拽编辑器。
29. 没有做登录注册 / 权限。
30. 没有做 Playwright 视觉回归。
31. Worker 旧测试通过。
32. 后端 mvn test 通过。
33. 前端 npm run test 通过。
34. 前端 npm run build 通过。
35. Week 08 smoke 文档完成。
36. Week 08 summary 文档完成。
37. Week 08 report material 文档完成。
38. docs/current.md 已同步。
39. docs/plan.md 已同步。
40. docs/spec.md 已同步。
41. docs/INDEX.md 已同步。

==================================================
十三、验收结论等级
==================================================

请按以下标准输出验收结论。

PASS：
所有功能、测试、构建、smoke、文档、安全检查全部通过。
可以进入 Week 09。

PARTIAL：
主链路通过，但存在少量非阻塞问题。
例如：
- 文档没补齐。
- 某个非核心测试缺失。
- 页面展示字段不够完整。
- report material 未完善。
需要补齐后再进入 Week 09。

FAILED：
出现以下任意情况，必须判定为 FAILED：

1. landing-basic 跑不通。
2. card-list 跑不通。
3. generatedPageArtifact 为空。
4. SUCCESS 时 iframe 不显示。
5. FAILED 时 iframe 仍然显示。
6. mvn test 失败。
7. npm run build 失败。
8. 接入了真实 AI。
9. 接入了 MySQL。
10. 接入了 Redis。
11. 接入了 RabbitMQ。
12. 上传了真实图片到后端。
13. 后端调用了 Python Worker。
14. iframe 出现 allow-scripts。
15. unknown-template 没有返回 400。
16. 不存在 jobId 没有返回 404。

==================================================
十四、最终报告格式
==================================================

请最终输出一份 Week 08 验收报告，格式如下：

# Week 08 Final Acceptance Report

## 1. Overall Result

Result: PASS / PARTIAL / FAILED

一句话总结本次验收结果。

## 2. Scope

本次验收范围：
- image-page dev mock API
- image-to-page mock 链路
- 前端 /dev/image-to-layout 页面
- generated-page iframe 预览
- 自动化测试
- smoke
- 文档
- 禁止事项

本次不验收：
- 真实 AI
- Figma
- MySQL
- Redis
- RabbitMQ
- 真实图片上传
- 后端调用 Python Worker
- ZIP 导出
- 拖拽编辑器

## 3. Backend API Check

- POST /api/dev/image-page-jobs: PASS / FAILED
- GET /api/dev/image-page-jobs/{jobId}: PASS / FAILED
- landing-basic: PASS / FAILED
- card-list: PASS / FAILED
- invalid-layout: PASS / FAILED
- unknown-template: PASS / FAILED
- nonexistent jobId: PASS / FAILED

说明发现的问题。

## 4. Frontend Check

- /dev/image-to-layout accessible: PASS / FAILED
- local image preview: PASS / FAILED
- request only sends imageName + templateKey: PASS / FAILED
- Layout JSON display: PASS / FAILED
- generatedPageArtifact display: PASS / FAILED
- SUCCESS iframe preview: PASS / FAILED
- FAILED hides iframe: PASS / FAILED
- error display: PASS / FAILED

说明发现的问题。

## 5. Security Check

- iframe sandbox="": PASS / FAILED
- no allow-scripts: PASS / FAILED
- no allow-same-origin: PASS / FAILED
- no script in generated artifact: PASS / FAILED
- no real image upload: PASS / FAILED
- no backend Python Worker call: PASS / FAILED

说明发现的问题。

## 6. Forbidden Scope Check

- real AI: PASS / FAILED
- Figma: PASS / FAILED
- MySQL: PASS / FAILED
- Entity / Mapper: PASS / FAILED
- Redis: PASS / FAILED
- RabbitMQ: PASS / FAILED
- ZIP export: PASS / FAILED
- drag editor: PASS / FAILED
- auth / permission: PASS / FAILED
- Playwright visual regression: PASS / FAILED

说明发现的问题。

## 7. Test Results

Backend:
- Command: mvn test
- Result: PASS / FAILED
- Summary:

Worker:
- Command: python -m unittest worker.test_layout_validator worker.test_layout_static_generator worker.test_image_layout_resolver
- Result: PASS / FAILED
- Summary:

Frontend:
- Command: npm run test
- Result: PASS / FAILED
- Summary:

Frontend build:
- Command: npm run build
- Result: PASS / FAILED
- Summary:

## 8. Smoke Results

- Backend 8080 started: PASS / FAILED
- Frontend 5174 started: PASS / FAILED
- /dev/image-to-layout returned 200: PASS / FAILED
- landing-basic: PASS / FAILED
- card-list: PASS / FAILED
- invalid-layout: PASS / FAILED
- unknown-template: PASS / FAILED
- nonexistent jobId: PASS / FAILED
- services stopped: PASS / FAILED

## 9. Documentation Check

- AGENTS.md updated: PASS / FAILED
- docs/current.md updated: PASS / FAILED
- docs/plan.md updated: PASS / FAILED
- docs/spec.md updated: PASS / FAILED
- docs/INDEX.md updated: PASS / FAILED
- docs/archive/week/08-plan.md exists: PASS / FAILED
- docs/archive/week/08-summary.md exists: PASS / FAILED
- docs/archive/week/08-dev-smoke.md exists: PASS / FAILED
- docs/archive/week/08-report-material.md exists: PASS / FAILED

说明缺失或需要补齐的文档。

## 10. Issues Found

列出发现的问题。
每个问题请包含：
- 问题描述
- 严重程度：BLOCKER / MAJOR / MINOR
- 建议修复方式
- 是否已修复

## 11. Minimal Fixes Applied

如果你做了最小修复，请列出：
- 修改文件
- 修改原因
- 修改内容摘要
- 对应测试结果

如果没有修复，请写：
No fixes applied.

## 12. Final Decision

结论：
- PASS：可以进入 Week 09。
- PARTIAL：需要补齐以下事项后再进入 Week 09。
- FAILED：必须继续修 Week 08，不能进入 Week 09。

## 13. Week 09 Recommendation

根据验收结果，给出 Week 09 建议方向。
优先级建议：
1. 如果 Week 08 不完整，先修 Week 08。
2. 如果 Week 08 完整，Week 09 优先考虑统一 Java mock 与 Python fixture 的协议来源。
3. 或者增强 Layout JSON 节点 / 样式表达能力。
4. 暂不建议直接接真实 AI。
5. 暂不建议直接接 MySQL。
6. 暂不建议做 ZIP 导出。

==================================================
十五、执行要求
==================================================

请注意：

1. 不要直接进入 Week 09 开发。
2. 不要新增需求。
3. 不要大规模重构。
4. 不要因为发现小问题就顺手扩展功能。
5. 如果发现问题，只做最小修复。
6. 每个修复必须有对应测试。
7. 最终必须给出 PASS / PARTIAL / FAILED 结论。
8. 最终报告必须清楚说明是否可以进入 Week 09。
9. 如果不能进入 Week 09，请明确列出阻塞项。
10. 如果可以进入 Week 09，请明确建议 Week 09 做什么。