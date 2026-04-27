# 截图 / Figma 到响应式页面生成器

## 文件目的

本文件是仓库入口说明，主要面向人类开发者，同时也帮助 Codex 快速理解项目背景、当前阶段、目录结构和启动方式。

如果你刚进入本仓库，建议按下面顺序阅读：

1. `README.md`
2. `AGENTS.md`
3. `docs/week/01-plan.md`
4. `docs/week/01-status.md`

## 项目一句话说明

本项目旨在把“截图”或“Figma 设计信息”转化为可运行、可维护的响应式页面代码，并逐步形成一套适合 Codex 协作开发的工程方式。

## 当前阶段

当前处于 **Week 01 初始化阶段**。

这一周不追求页面生成效果，而追求三件事：

- 把项目边界写清楚
- 把工程骨架搭起来
- 把 Codex 的协作规则固化下来

## 当前阶段目标

本周目标如下：

- 明确 MVP 范围
- 建立 `frontend / backend / worker` 三层目录骨架
- 补齐基础文档
- 形成最小 smoke 测试路径
- 为第二周进入“任务闭环开发”做准备

## 本周不做什么

以下内容不是第一周目标：

- 不接入真实模型 API
- 不接入 Figma API / MCP
- 不做真实截图解析
- 不做真实代码生成
- 不做拖拽编辑器
- 不做导出 zip
- 不做 Redis / RabbitMQ 的运行时接入
- 不做复杂自动化回归体系

## 技术选型

| 层级 | 选型 | 第一周说明 |
|---|---|---|
| 前端 | Vue3 + Vite + JavaScript | 优先快速起步，先不强制 TypeScript |
| 后端 | Java 17 + Spring Boot + Maven | 提供基础服务与任务骨架 |
| 数据层 | MyBatis-Plus + MySQL | 第一周只保留方向，不要求完成数据库接入 |
| Worker | Python 3.11 | 后续承接生成任务；本周最小脚本允许使用 Python 3.10+ 本地验证 |
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
    week/
      01-plan.md
      01-status.md
    mvp-scope.md
    prd.md
    architecture.md
    coding-rules.md
    testing.md
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

以下命令是三端工程初始化完成后的第一周推荐最小启动方式。

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
   - 页面能打开
   - 页面至少展示项目标题和“Week 01 初始化中”的占位信息

### 后端

进入 `backend/` 目录后执行：

说明：当前 Windows 中文路径下，`mvn spring-boot:run` 存在已知启动失败风险。Week 01 Day 3 smoke 推荐使用先打包、再运行 jar 的稳定路径。

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

### Worker

进入 `worker/` 目录后执行：

说明：项目推荐目标版本为 Python 3.11。Week 01 的 worker smoke 脚本只使用标准库，允许使用 Python 3.10+ 完成本地验证。

1. 创建虚拟环境（可选）
   `python -m venv .venv`

2. 启动最小脚本
   `python main.py --smoke`

3. 预期结果
   - 控制台打印 `worker smoke pass`
   - 退出码为 0

## 与 Codex 的协作方式

第一周默认协作流程：

1. 先让 Codex 阅读 `AGENTS.md`
2. 再让 Codex 阅读 `README.md`、`docs/week/01-plan.md` 与 `docs/week/01-status.md`
3. 对复杂任务，要求 Codex 先输出计划
4. 计划确认后再允许 Codex 改代码
5. 改动完成后，要求 Codex 提供验证方式与结果
6. 如果目录、命令、约束变了，要同步更新文档

## 文档索引

| 文档 | 作用 |
|---|---|
| `AGENTS.md` | 仓库长期规则，主要给 Codex 看 |
| `docs/week/01-plan.md` | 第一周任务说明与每日拆解 |
| `docs/week/01-status.md` | 第一周实际进展、验收结果、风险和下一步 |
| `docs/mvp-scope.md` | MVP 第一版范围 |
| `docs/prd.md` | 长期产品愿景和后续演进方向 |
| `docs/architecture.md` | 系统架构与模块关系 |
| `docs/coding-rules.md` | 前端、后端、Worker 编码规范 |
| `docs/testing.md` | 测试方式与验证策略 |
| `docs/prompt-templates.md` | 常用提示词模板 |
| `docs/skills/frontend-task-skill.md` | 前端任务技能草案 |
| `docs/skills/backend-api-skill.md` | 后端接口任务工作流 |
| `docs/skills/bugfix-skill.md` | Bug 修复任务工作流 |
| `tests/smoke/README.md` | 第一周最小 smoke 测试步骤 |

## 本周交付物

第一周结束时，仓库应至少包括：

- `AGENTS.md`
- `README.md`
- `docs/week/01-plan.md`
- `docs/week/01-status.md`
- `docs/mvp-scope.md`
- `docs/prd.md`
- `docs/architecture.md`
- `docs/coding-rules.md`
- `docs/testing.md`
- `docs/prompt-templates.md`
- `docs/skills/frontend-task-skill.md`
- `docs/skills/backend-api-skill.md`
- `docs/skills/bugfix-skill.md`
- `tests/smoke/README.md`
- `frontend/` 初始工程
- `backend/` 初始工程
- `worker/` 初始脚本

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

请先阅读 `AGENTS.md`、`README.md`、`docs/week/01-plan.md`、`docs/week/01-status.md`。

当前任务：
初始化 `frontend/` 工程并提供首页占位页面。

要求：
1. 先输出计划
2. 只改前端相关文件
3. 不做组件库引入
4. 完成后给出启动命令和验证结果

## 验收标准

本文件满足以下条件时，视为可用：

- 新成员打开仓库，能在 5 分钟内知道项目在做什么
- 新成员知道第一周只做初始化，不会误以为已经进入生成能力开发
- 新成员能按本文件找到关键文档与建议目录
- Codex 能根据本文件快速总结仓库入口信息
