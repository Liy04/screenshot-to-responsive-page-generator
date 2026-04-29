# Week 02 状态看板

## 文件目的

本文件用于记录 Week 02 MVP 最小闭环开发的实际进展、线程状态、验收结果、风险和下一步计划。

本文件记录实际进展；周执行安排以 `docs/week/02-plan.md` 为准。

## 当前日期 / Day

- 当前日期：2026-04-30
- 当前 Day：Week 02 Day 5 端到端联调与收口
- 当前阶段：Week 02 MVP 最小闭环已完成，下一阶段准备中

## 今日目标

完成 Week 02 MVP 最小闭环最终 smoke 验收与文档收口。

验收范围：

- 从零验证后端 `mvn test` 与 `mvn package -DskipTests`。
- 从零验证前端 `npm run build`。
- 验证 Worker `python main.py --smoke`。
- 启动后端 jar 与前端 dev server。
- 验证上传截图、创建任务、查询任务状态、查看 mock 生成结果。
- 验证上传不支持文件类型、不存在 `jobId` 和前端不存在任务提示。
- 同步 `tests/smoke/README.md`、本状态看板和必要 README 入口说明。

## 线程分工

| 线程 | 职责 |
|---|---|
| 项目经理线程 | 控制 Week 02 范围、拆分任务、确认验收 |
| 文档线程 | 维护周计划、接口契约、前端页面说明、状态看板 |
| 后端开发线程 | 实现上传接口、任务接口、mock 结果接口 |
| 前端开发线程 | 实现路由、创建任务页、任务详情页 |
| Worker / 模型预备线程 | 保持 smoke，必要时提供 mock-job，不参与真实生成 |
| 测试线程 | 执行 smoke 和端到端验收，只报告问题 |

## 线程状态

状态枚举：待执行 / 执行中 / 待验收 / 通过 / 阻塞

| 线程 | 当前状态 | 说明 |
|---|---|---|
| 项目经理线程 | 通过 | 已完成 Week 02 全量验收，确认本周可收口 |
| 文档线程 | 通过 | 已完成 smoke 文档、状态看板和 README 入口说明同步 |
| 后端开发线程 | 通过 | 上传接口、任务接口、状态接口和 mock 结果接口已通过 smoke 验收 |
| 前端开发线程 | 通过 | 工作台、创建页、详情页和错误提示已通过浏览器验收 |
| Worker / 模型预备线程 | 通过 | Worker smoke 通过，仍不参与真实生成 |
| 测试线程 | 通过 | Day 5 端到端 smoke 验收通过 |

## 验收结果

Day 5 端到端验收结论：通过。

Week 02 最终验收结论：通过，可收口。

文档与协作模式验收项：

- [x] `docs/week/02-plan.md` 职责回到周计划。
- [x] `docs/api-contracts.md` 包含 Week 02 四个接口契约。
- [x] `docs/frontend-pages.md` 包含三个页面和路由说明。
- [x] `docs/week/02-status.md` 符合状态看板结构。
- [x] `docs/context/current-phase.md` 包含 Week 02 当前目标、禁止项和推荐实现方式。
- [x] `docs/tasks/` 下 5 张 Week 02 任务卡均存在。
- [x] `AGENTS.md`、`README.md`、`docs/week/02-plan.md` 已说明轻量上下文执行方式。
- [x] `docs/prompt-templates.md` 已新增轻量上下文任务提示词模板。
- [x] 未出现旧版任务详情路由参数。
- [x] 未出现旧版示例图片路径。
- [x] README、smoke、coding-rules、testing、architecture、skills 已收敛 Week 02 当前阶段口径。
- [x] 未修改 `frontend/`、`backend/`、`worker/` 业务代码。

Day 5 smoke 验收项：

- [x] 后端 `mvn test` 成功；当前无测试用例。
- [x] 后端 `mvn package -DskipTests` 成功。
- [x] 前端 `npm run build` 成功。
- [x] Worker 使用 Python 3.10.1 执行 `python main.py --smoke` 成功，输出 `worker smoke pass`。
- [x] 后端 jar 启动成功，`/api/health` 返回 200。
- [x] 前端 dev server 使用 `127.0.0.1:5174` 启动成功；5173 验证前已被其它项目占用。
- [x] PNG / JPG / JPEG / WebP 上传成功，响应包含 `assetId` 和 `fileUrl`。
- [x] 上传响应中的 `/uploads/**` 可访问，返回 200。
- [x] 使用 `assetId` 创建任务成功，响应包含 `jobId`，状态为 `success`。
- [x] 查询任务状态成功，`progress` 为 100。
- [x] 查询任务结果成功，返回 `layoutJson`、`vueCode`、`cssCode`。
- [x] 上传 TXT 返回 400，错误信息明确说明只支持 PNG、JPG、JPEG、WebP 图片。
- [x] 查询不存在的 `jobId` 返回 404，错误信息为 `任务不存在`。
- [x] 浏览器端完成首页 -> 创建页 -> 图片预览 -> 开始生成 -> 详情页流程。
- [x] 浏览器端详情页展示 `jobId`、`assetId`、`progress`、`layoutJson`、`vueCode`、`cssCode`。
- [x] 浏览器访问 `/generation/job_missing` 显示错误提示，并可返回创建页。

## 风险

- 协作模式调整后，开发线程需要优先读取当前阶段上下文和单任务卡，避免继续从旧版长文档中复制过期细节。
- 接口契约以 `docs/api-contracts.md` 为准，若实现中修改字段或状态码，需要同步更新该文档。
- 前端页面和路由以 `docs/frontend-pages.md` 为准，统一使用 `/generation/:jobId`。
- 本周仍需严格控制范围，不接真实模型 API、Figma API / Figma MCP、Redis、RabbitMQ、MySQL 实际落库。
- 后端 `mvn test` 当前仍没有测试用例，只能验证 Maven 生命周期。
- 任务数据暂存在内存 Map，后端服务重启后已创建的 `assetId` / `jobId` 会失效。
- 上传文件保存在 `backend/uploads/`，该目录是本地验证副产物，必须保持忽略且不提交。
- Day 5 验证前发现 5173 被另一个前端项目占用，本次前端验收改用 5174。

## 下一步

- Week 02 已通过最终验收并可收口。
- 进入下一阶段前先决定是否补充后端测试用例。
- 后续进入真实持久化或真实生成能力前，必须另开任务并重新确认范围。
