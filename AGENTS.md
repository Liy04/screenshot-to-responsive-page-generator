# AGENTS.md

## 文件目的

本文件用于为 Codex 提供本仓库的长期工作规则。

进入本仓库执行任务时，Codex 必须先阅读本文件，再按轻量上下文规则读取当前阶段上下文、当前任务卡和相关代码。

本文件只保留长期有效内容，不记录完整 PRD、完整周计划、历史状态、临时需求、每日待办或阶段性细节。

## 项目目标

本项目是一个“截图 / Figma 到响应式页面生成器”。

长期目标：

- 输入页面截图或 Figma 设计信息
- 输出可运行、可维护、可继续迭代的响应式前端页面代码
- 使用 Codex 以“先计划、再实现、最后验证”的方式协作开发

## 默认技术栈

除非用户明确要求，不要擅自替换技术栈。

- 前端：Vue3 + Vite + JavaScript
- 后端：Java 17 + Spring Boot + Maven
- 数据库：MySQL
- 数据访问：MyBatis-Plus
- Worker：Python 3.11（推荐目标版本）；Week 01 smoke 脚本允许使用 Python 3.10+ 本地验证
- 测试：smoke test、接口测试、前端页面测试
- 版本管理：Git

## 推荐目录结构

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
    mvp-scope.md
    prd.md
    architecture.md
    coding-rules.md
    testing.md
    api-contracts.md
    frontend-pages.md
    prompt-templates.md
    skills/
  frontend/
  backend/
  worker/
  tests/
  design-inputs/
```

## 目录职责

- `frontend/`：前端项目，负责页面展示、交互和接口联调
- `backend/`：后端项目，负责 RESTful API、任务管理和数据访问
- `worker/`：Python worker，负责后续生成任务处理
- `docs/`：项目文档、当前阶段上下文、任务卡、周计划、规范、提示词模板和 skills
- `tests/`：测试脚本、冒烟测试和验证说明
- `design-inputs/`：截图、Figma 导出物等设计输入

## 默认读取方式

从 Week 02 开始，Codex 日常开发任务采用轻量上下文方式。

每次任务默认只读取：

1. `AGENTS.md`
2. `docs/context/current-phase.md`
3. `docs/tasks/当前任务卡.md`
4. 当前任务相关模块代码

其它文档只在任务卡明确要求，或当前任务确实必须参考时读取。

不要让开发线程默认读取完整 PRD、完整周计划、全部历史状态和全部 skills。

## 按需文档入口

以下文档作为按需参考，不作为每日任务默认上下文：

- 项目介绍、启动方式、目录概览：`README.md`
- 当前阶段上下文：`docs/context/current-phase.md`
- 单任务卡：`docs/tasks/*.md`
- Week 01 任务、交付物、验收标准：`docs/week/01-plan.md`
- Week 01 实际进展、验收结果、风险和下一步：`docs/week/01-status.md`
- Week 02 周执行安排：`docs/week/02-plan.md`
- Week 02 实际进展、验收结果、风险和下一步：`docs/week/02-status.md`
- MVP 范围、做什么和不做什么：`docs/mvp-scope.md`
- 长期产品愿景和后续演进方向：`docs/prd.md`
- 系统架构、模块关系、数据流：`docs/architecture.md`
- Week 02 接口契约：`docs/api-contracts.md`
- Week 02 前端页面、路由和交互说明：`docs/frontend-pages.md`
- 前端、后端、Worker 编码规范：`docs/coding-rules.md`
- 测试方式、smoke test、接口测试：`docs/testing.md`
- 常用 Codex 提示词：`docs/prompt-templates.md`
- 可复用工作流：`docs/skills/*.md`

如果找不到对应文档，必须在计划中说明缺失，不要自行假设。

## 工作流程

每次任务必须遵守以下流程：

1. 阅读 `AGENTS.md`
2. 阅读 `docs/context/current-phase.md`
3. 阅读 `docs/tasks/当前任务卡.md`
4. 根据任务卡读取相关模块代码和必要专项文档
5. 先输出计划，等待用户确认后再编码或执行复杂修改
6. 只修改与当前任务直接相关的文件
7. 修改完成后进行最小验证
8. 最后汇报改动内容、验证结果和风险

## 计划要求

复杂任务的计划必须包含：

- 任务目标
- 预计修改的文件
- 实施步骤，建议 3 到 5 步
- 验证方式
- 风险或待确认事项

不要输出只有一句话的空泛计划。

## 多线程任务拆分规则

如果一个任务同时涉及多个线程，必须先拆分为多个单线程任务，不要合并成一份大提示词。

常见线程边界：

- 测试线程：只执行验证、记录问题和输出验收结果，不修改业务代码。
- 文档线程：只更新文档、状态看板、总结和任务卡，不修改业务代码。
- 后端开发线程：只处理后端接口、服务、mock、后端验证，不修改前端业务代码。
- 前端开发线程：只处理页面、路由、组件、前端 API 调用，不修改后端业务代码。
- Worker / 校验器线程：只处理 worker 脚本、校验器和 worker 测试。
- 项目经理线程：负责拆任务、控范围、验收、风险判断和最终收口。

如果计划同时包含测试和文档、后端和前端、Worker 和后端、功能开发和收口验收，必须拆成 A / B / C 多条任务，并明确执行顺序。

示例：

```text
先发 Day 7A 给测试线程
↓
测试通过后
↓
发 Day 7B 给文档线程
↓
最后由项目经理线程做最终验收
```

## 开发约束

Codex 必须遵守以下约束：

- 不允许无关重构
- 不允许擅自扩大任务范围
- 不允许擅自替换技术栈
- 不允许擅自引入大型依赖
- 新增依赖前必须说明原因
- 能用现有依赖完成的任务，不要额外引入新库
- 不要把占位实现擅自升级成完整系统
- 不要在没有用户确认的情况下修改项目整体架构

## 文档同步规则

如果以下内容发生变化，必须同步更新相关文档：

- 目录结构变化
- 启动方式变化
- 技术栈变化
- 接口约定变化
- 测试方式变化
- 当前周计划变化

文档更新位置：

- 周计划更新到 `docs/week/*.md`
- MVP 范围更新到 `docs/mvp-scope.md`
- 架构变化更新到 `docs/architecture.md`
- 编码规范更新到 `docs/coding-rules.md`
- 测试方式更新到 `docs/testing.md`
- 当前阶段口径更新到 `docs/context/current-phase.md`
- 单任务执行要求更新到 `docs/tasks/*.md`
- 常用提示词更新到 `docs/prompt-templates.md`
- 可复用流程更新到 `docs/skills/*.md`

## 禁止事项

除非用户明确要求，否则禁止：

- 接入真实模型 API
- 接入 Figma API 或 Figma MCP
- 引入 Redis / RabbitMQ 作为运行前置依赖
- 实现真实截图解析与代码生成
- 实现多页面编辑器
- 实现拖拽编辑器
- 实现导出 zip
- 大范围重构仓库结构

如果任务确实需要突破以上限制，必须先在计划中说明原因，并等待用户确认。

## 完成定义

任务只有同时满足以下条件，才算完成：

1. 改动符合当前任务范围
2. 改动文件清楚
3. 没有无关重构
4. 已完成最小验证，或明确说明无法验证的原因
5. 最终汇报包含改动内容、验证步骤、验证结果和风险

## 输出格式

任务完成后，按以下格式汇报：

```text
任务结果：
- 任务目标：
- 改动文件：
- 主要改动：
- 验证步骤：
- 验证结果：
- 风险 / 待确认事项：
```
