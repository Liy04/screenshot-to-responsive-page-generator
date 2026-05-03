# 截图 / Figma 到响应式页面生成器

## 文件目的

本文件是仓库入口说明，主要面向人类开发者，同时也帮助 Codex 快速理解项目背景、当前阶段、目录结构和启动方式。

如果你刚进入本仓库，建议按下面顺序阅读：

1. `README.md`
2. `AGENTS.md`
3. `docs/context/current-phase.md`
4. 当前任务对应的 `docs/tasks/*.md`
5. 当前任务相关模块代码

`docs/week/02-plan.md`、`docs/week/03-plan.md`、`docs/week/03-status.md`、`docs/mvp-scope.md` 等文档作为按需参考，不再作为每日开发任务的默认上下文。

## 项目一句话说明

本项目旨在把“截图”或“Figma 设计信息”转化为可运行、可维护的响应式页面代码，并逐步形成一套适合 Codex 协作开发的工程方式。

## 当前阶段

当前处于 **Week 03 Layout JSON v0.1 收口阶段**。

Week 01 初始化阶段已完成。Week 02 已跑通 mock 最小闭环：

```text
上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果
```

Week 03 聚焦 Layout JSON v0.1 稳定落地：

```text
手写 Layout JSON -> Schema 校验 -> 业务规则校验 -> 示例验证
```

## 当前阶段结果

Week 02 已完成：

- 实现截图上传接口和本地文件保存。
- 实现生成任务创建、状态查询和 mock 结果查询接口。
- 实现前端工作台、创建任务页和任务详情页。
- 跑通前后端最小闭环。
- 更新 smoke 文档和 Week 02 状态看板。

Week 03 当前收口结果：

- P0 已完成 Layout JSON 设计文档、JSON Schema、合法 / 非法示例、Python 校验器和校验器测试。
- P1 后端 mock 保存 / 查询接口已完成基础 smoke。
- P1 前端 Layout JSON 查看页仍需结合 Day 6B / Day 7A 输出做最终确认。
- 当前仍不代表已经接入真实 AI、Figma、数据库落库或 Vue 页面生成。

## 本周不做什么

以下内容不是当前阶段目标：

- 不接入真实模型 API
- 不接入 Figma API / MCP
- 不做真实截图解析
- 不做真实代码生成
- 不做拖拽编辑器
- 不做导出 zip
- 不接 MySQL 实际落库
- 不做 Redis / RabbitMQ 的运行时接入
- 不做复杂自动化回归体系

## 技术选型

| 层级 | 选型 | 当前阶段说明 |
|---|---|---|
| 前端 | Vue3 + Vite + JavaScript | 优先快速起步，先不强制 TypeScript |
| 后端 | Java 17 + Spring Boot + Maven | 提供基础服务与任务骨架 |
| 数据层 | MyBatis-Plus + MySQL | 长期方向；当前阶段不实际落库、不新增 Mapper / Entity |
| Worker | Python 3.11 | 后续承接生成任务；当前 smoke 脚本允许使用 Python 3.10+ 本地验证 |
| 测试 | smoke test | 先验证“能启动、能访问、能输出” |

## 为什么这样选

这套选型优先考虑两件事：

1. 贴合当前开发者已有技术栈，降低学习额外框架的成本
2. 为后续的 Codex 协作留出清晰的前后端边界与 worker 扩展空间

## 建议目录结构

```text
project-root/
  AGENTS.md
  README.md
  docs/
    context/
      current-phase.md
    tasks/
      week02-day1-upload-api.md
      week02-day2-generation-api.md
      week02-day3-frontend-create-page.md
      week02-day4-generation-detail-page.md
      week02-day5-smoke-and-docs.md
    week/
      01-plan.md
      01-status.md
      02-plan.md
      02-status.md
      03-plan.md
      03-status.md
      03-summary.md
    mvp-scope.md
    prd.md
    architecture.md
    coding-rules.md
    testing.md
    api-contracts.md
    frontend-pages.md
    layout-schema-design.md
    layout-api-contracts.md
    database-artifact-draft.md
    prompt-templates.md
    skills/
      frontend-task-skill.md
      backend-api-skill.md
      bugfix-skill.md
  frontend/
  backend/
  worker/
  tests/
    smoke/
      README.md
  design-inputs/
```

## 本地启动示例

以下命令是三端工程初始化完成后的推荐最小启动方式。

当前如果对应目录内还只有 `.gitkeep` 等占位文件，说明该端工程尚未初始化，需先完成 Day 2 / Day 3 的工程骨架任务，再执行下面命令。

### 前端

进入 `frontend/` 目录后执行：

1. 安装依赖（如已安装可跳过）
   `npm install`

2. 构建验证
   `npm run build`

3. 启动开发服务
   `npm run dev -- --host 127.0.0.1 --port 5173`

4. 预期结果
   - 本地出现开发地址
   - 页面能打开，并展示当前阶段相关入口或占位信息

### 后端

进入 `backend/` 目录后执行：

说明：当前 Windows 中文路径下，`mvn spring-boot:run` 存在已知启动失败风险。smoke 推荐使用先打包、再运行 jar 的稳定路径。

1. 运行测试
   `mvn test`

2. 打包
   `mvn package -DskipTests`

3. 启动服务
   `java -jar target/backend-0.0.1-SNAPSHOT.jar`

4. 预期结果
   - 服务启动成功
   - 可以访问 `/api/health`
   - 返回 200 状态码与基础 JSON 结果

风险记录：`mvn spring-boot:run` 暂作为后续待排查项，不作为当前 Windows 中文路径下的主验收命令。

### Week 02 最小闭环验证

Week 02 端到端 smoke 以 `tests/smoke/README.md` 为准，覆盖：

```text
上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果
```

验证时后端使用 jar 启动，前端使用 Vite dev server；如果 `5173` 被占用，可以改用 `5174` 或 `5175`。

### Week 03 Layout JSON 验证

Week 03 smoke 以 `tests/smoke/README.md` 为准，覆盖：

```text
Layout JSON 示例 -> Schema 校验 -> 业务规则校验 -> 后端 mock 保存 / 查询
```

前端 Layout JSON 查看页属于 Week 03 P1，需要结合 Day 6B / Day 7A 输出单独确认；当前阶段不接数据库、不接真实 AI、不做 Vue 页面代码生成。

### Worker

进入 `worker/` 目录后执行：

说明：项目推荐目标版本为 Python 3.11。当前 worker smoke 脚本只使用标准库，允许使用 Python 3.10+ 完成本地验证。

1. 创建虚拟环境（可选）
   `python -m venv .venv`

2. 启动最小脚本
   `python main.py --smoke`

3. 预期结果
   - 控制台打印 `worker smoke pass`
   - 退出码为 0

## 与 Codex 的协作方式

从 Week 02 开始，推荐使用轻量上下文协作方式：

1. 先让 Codex 阅读 `AGENTS.md`
2. 再让 Codex 阅读 `docs/context/current-phase.md`
3. 然后读取当前任务对应的 `docs/tasks/*.md`
4. 最后读取当前任务相关模块代码
5. 对开发任务，要求 Codex 先输出计划，确认后再编码
6. 改动完成后，要求 Codex 执行最小验证并汇报结果
7. 如果目录、命令、接口约定、测试方式或阶段口径变了，要同步更新文档

完整 PRD、完整周计划、历史状态和全部 skills 只在任务卡明确要求，或任务确实必须参考时读取。

## 文档索引

| 文档 | 作用 |
|---|---|
| `AGENTS.md` | 仓库长期规则，主要给 Codex 看 |
| `docs/context/current-phase.md` | 当前阶段目标、禁止项和推荐实现方式 |
| `docs/tasks/*.md` | 单任务卡，日常开发优先读取 |
| `docs/week/01-plan.md` | 第一周任务说明与每日拆解 |
| `docs/week/01-status.md` | 第一周实际进展、验收结果、风险和下一步 |
| `docs/week/02-plan.md` | 第二周周执行安排 |
| `docs/week/02-status.md` | 第二周实际进展、验收结果、风险和下一步 |
| `docs/week/03-plan.md` | 第三周 Layout JSON v0.1 周计划 |
| `docs/week/03-status.md` | 第三周实际进展、验收结果、风险和下一步 |
| `docs/week/03-summary.md` | 第三周收口总结和 Week 04 输入 |
| `docs/mvp-scope.md` | MVP 第一版范围 |
| `docs/prd.md` | 长期产品愿景和后续演进方向 |
| `docs/architecture.md` | 系统架构与模块关系 |
| `docs/api-contracts.md` | Week 02 接口契约 |
| `docs/frontend-pages.md` | Week 02 前端页面、路由和交互说明 |
| `docs/layout-schema-design.md` | Week 03 Layout JSON v0.1 设计依据 |
| `docs/layout-api-contracts.md` | Week 03 Layout JSON P1 mock 接口契约 |
| `docs/database-artifact-draft.md` | 后续数据库 artifact 设计草案，Week 03 不执行 |
| `docs/coding-rules.md` | 前端、后端、Worker 编码规范 |
| `docs/testing.md` | 测试方式与验证策略 |
| `docs/prompt-templates.md` | 常用提示词模板 |
| `docs/skills/frontend-task-skill.md` | 前端任务技能草案 |
| `docs/skills/backend-api-skill.md` | 后端接口任务工作流 |
| `docs/skills/bugfix-skill.md` | Bug 修复任务工作流 |
| `tests/smoke/README.md` | Week 01 / Week 02 / Week 03 最小 smoke 测试步骤 |

## Week 02 交付物

第二周结束时，仓库应至少包括：

- `docs/week/02-plan.md`
- `docs/week/02-status.md`
- `docs/context/current-phase.md`
- `docs/tasks/week02-day1-upload-api.md`
- `docs/tasks/week02-day2-generation-api.md`
- `docs/tasks/week02-day3-frontend-create-page.md`
- `docs/tasks/week02-day4-generation-detail-page.md`
- `docs/tasks/week02-day5-smoke-and-docs.md`
- `docs/api-contracts.md`
- `docs/frontend-pages.md`
- 更新后的 `tests/smoke/README.md`
- 后端上传接口、任务接口和 mock 结果接口
- 前端工作台、创建任务页和任务详情页

## Week 03 交付物

第三周收口时，仓库应至少包括：

- `docs/week/03-plan.md`
- `docs/week/03-status.md`
- `docs/week/03-summary.md`
- `docs/layout-schema-design.md`
- `docs/layout-api-contracts.md`
- `docs/database-artifact-draft.md`
- `schema/layout.schema.json`
- `examples/valid/*.layout.json`
- `examples/invalid/*.layout.json`
- `worker/layout_validator.py`
- `worker/test_layout_validator.py`
- 更新后的 `tests/smoke/README.md`

## 关键字段说明

| 字段 | 含义 | 什么时候更新 |
|---|---|---|
| 当前阶段 | 仓库所处里程碑 | 每进入新周或新阶段更新 |
| 技术选型 | 当前默认实现方式 | 技术栈调整时更新 |
| 建议目录结构 | 当前标准目录 | 目录有重大变化时更新 |
| 本地启动示例 | 本地运行命令 | 命令变更时更新 |
| 文档索引 | 主要文档入口 | 新增核心文档时更新 |

## 示例内容

### 示例：如何开始一个新任务

你可以对 Codex 发送类似提示：

请先阅读：

1. `AGENTS.md`
2. `docs/context/current-phase.md`
3. `docs/tasks/week02-day1-upload-api.md`
4. 后端上传接口相关代码

当前任务：
执行 Week 02 Day 1：后端上传接口。

要求：
1. 先输出计划
2. 只改后端上传接口相关文件
3. 不接 MySQL、Redis、RabbitMQ、真实模型 API、Figma API
4. 完成后给出验证步骤和验证结果

## 验收标准

本文件满足以下条件时，视为可用：

- 新成员打开仓库，能在 5 分钟内知道项目在做什么
- 新成员知道当前阶段只做 Layout JSON v0.1 稳定落地，不会误以为已经进入真实生成能力开发
- 新成员能按本文件找到关键文档与建议目录
- Codex 能根据本文件快速总结仓库入口信息
