# Week 01 状态看板

## 文件目的

本文件用于记录 Week 01 每日执行状态，辅助项目经理统筹多线程协作、验收结果、风险和下一步计划。

本文件记录实际进展；计划性内容仍以 `docs/week/01-plan.md` 为准。

## 当前日期 / Day

- 当前日期：2026-04-27
- 当前 Day：Week 01 已完成
- 当前阶段：Week 01 初始化阶段已完成

## 今日目标

Day 5 目标：执行 Week 01 文档一致性检查，统一 README、smoke、周计划、状态看板、MVP 范围、PRD、架构、编码规范、测试说明和 skills 的口径。

验收标准：

- `README.md` 中的启动命令与 `tests/smoke/README.md` 一致。
- `AGENTS.md`、`README.md`、`docs/week/01-plan.md`、`docs/week/01-status.md` 对 Week 01 阶段描述一致。
- `docs/prd.md` 明确为长期产品愿景草案，不覆盖 `docs/mvp-scope.md` 的当前 MVP 第一版范围。
- `docs/architecture.md` 仍说明 Week 01 不设计数据库表。
- `docs/coding-rules.md` 与 prompt templates / skills 口径一致。
- 不接入 MySQL、Redis、RabbitMQ、真实模型 API、Figma API。
- 不实现真实截图解析或真实代码生成。

## 线程分工

| 线程 | 职责 |
|---|---|
| 项目经理线程 | 统筹任务、确认边界、拆分任务、汇总验收结果和风险 |
| 前端开发线程 | 验证 `frontend/` 构建、启动和首页访问 |
| 后端开发线程 | 验证 `backend/` 打包、jar 启动和 `/api/health` |
| Worker / 模型预备线程 | 验证 `worker/` 最小 smoke 脚本，不接入真实模型 |
| 测试线程 | 独立执行三端 smoke 验收，不修改代码 |

## 线程状态

状态枚举：待执行 / 执行中 / 待验收 / 通过 / 阻塞

| 线程 | 当前状态 | 说明 |
|---|---|---|
| 项目经理线程 | 通过 | Day 4 协作规则二次修订已完成，进入 Day 5 收口 |
| 前端开发线程 | 通过 | 前端模板已补强：读取 coding rules、先计划、停 dev server、不提交构建产物 |
| 后端开发线程 | 通过 | 后端模板和 skill 已补强：未确认数据库前不新增 Mapper、实体映射或数据库配置 |
| Worker / 模型预备线程 | 通过 | 已将命名由 Worker / 模型端 收敛为 Worker / 模型预备线程，避免误导为真实模型接入 |
| 测试线程 | 通过 | smoke 文档命令仍沿用 Day 3 已验证路径 |
| 文档线程 | 通过 | Day 5 文档一致性检查和状态同步已完成 |

## 验收结果

Day 3 验收结论：通过。

Day 4 二次修订记录：

- 已根据前端、后端、worker 线程反馈补强模板自包含性。
- 已将 Worker / 模型端 命名收敛为 Worker / 模型预备线程，避免误导为真实模型接入。
- 已明确前端线程需读取 `docs/coding-rules.md`、先计划再执行、验证后停止 dev server、不提交构建产物。
- 已明确后端线程在未确认数据库任务前不新增 Mapper、实体表映射、数据库配置或数据库访问层。

Day 5 收口记录：

- 已检查 README 与 smoke 文档的三端启动命令，当前口径一致。
- 已检查 Week 01 阶段描述，AGENTS、README、01-plan、01-status 均保持“Week 01 初始化阶段”边界。
- 已检查 `docs/prd.md` 与 `docs/mvp-scope.md`，并将 PRD 明确修订为长期产品愿景草案，当前 MVP 第一版仍以 `docs/mvp-scope.md` 为准。
- 已将 PRD 中涉及 Figma、真实 AI、导出 ZIP、Redis、RabbitMQ、数据库表和完整业务流程的内容明确标注为后续产品方向。
- 已确认 `docs/architecture.md` 仍说明 Week 01 不设计数据库表。
- 已确认 `docs/coding-rules.md` 与 prompt templates / skills 对标准库、构建产物、先计划、mock 边界和数据库边界的口径一致。

Week 01 收口结论：通过。

第二周可以进入 MVP 最小闭环开发。

已验证内容：

- 前端：
  - Node `v22.14.0`
  - npm `10.9.2`
  - `npm run build` 成功
  - 首页访问返回 200
  - 页面标题为 `截图 / Figma 到响应式页面生成器`
- 后端：
  - Java `17.0.16`
  - Maven `3.9.11`
  - `mvn test` 成功，但当前无测试用例
  - `mvn package -DskipTests` 成功
  - `/api/health` 返回 200
  - 返回内容为 `{"service":"backend","status":"UP"}`
- Worker：
  - Python `3.10.1`
  - `python main.py --smoke` 输出 `worker smoke pass`
- 进程清理：
  - 未发现 `5173`、`8080` 残留监听
  - 未发现残留 `node`、`java` 测试进程

## 风险

- 当前目录不是 Git 仓库，`git status` 无法用于检查真实提交状态。
- 后端 `mvn spring-boot:run` 在当前 Windows 中文路径下存在已知启动失败风险，当前 smoke 主路径改为 `mvn package -DskipTests` + `java -jar`。
- 后端当前没有测试用例，`mvn test` 只能验证 Maven 生命周期。
- MySQL 是后续 MVP 任务闭环需要的方向，但 Week 01 不要求 `/api/health` 依赖数据库。
- 需要持续控制范围，避免提前接入真实模型 API、Figma API、Redis、RabbitMQ、真实截图解析或真实代码生成。
- Worker / 模型预备线程当前只做 smoke 和后续模型能力预备，不代表可以接入 OpenAI 或其他模型 SDK。
- `docs/prd.md` 包含较完整的长期产品愿景，后续执行任务时必须先判断当前阶段，不能直接把 PRD 的后续能力当作 Week 01 或当前 MVP 任务。

## 下一步

进入 Week 02 MVP 最小闭环开发准备。

建议任务：

- 继续以 `docs/mvp-scope.md` 为当前 MVP 范围锚点。
- 围绕“上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果”拆分 Week 02 开发任务。
- 继续遵守不接入真实模型 API、Figma API、Redis、RabbitMQ 的当前边界。
