# AGENTS.md

## 文件目的

本文件用于为 Codex 提供本仓库的长期工作规则。

进入本仓库执行任务时，Codex 必须先阅读本文件，再根据任务类型阅读相关文档。

本文件只保留长期有效内容，不记录本周任务、临时需求、每日待办或阶段性细节。

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
- `docs/`：项目文档、周计划、规范、提示词模板和 skills
- `tests/`：测试脚本、冒烟测试和验证说明
- `design-inputs/`：截图、Figma 导出物等设计输入

## 详细文档入口

Codex 不需要一次性读取所有文档，但必须根据任务类型读取对应文档。

- 项目介绍、启动方式、目录概览：读取 `README.md`
- 当前周任务、交付物、验收标准：读取 `docs/week/01-plan.md`
- 当前周实际进展、验收结果、风险和下一步：读取 `docs/week/01-status.md`
- MVP 范围、做什么和不做什么：读取 `docs/mvp-scope.md`
- 长期产品愿景和后续演进方向：读取 `docs/prd.md`
- 系统架构、模块关系、数据流：读取 `docs/architecture.md`
- 前端、后端、Worker 编码规范：读取 `docs/coding-rules.md`
- 测试方式、smoke test、接口测试：读取 `docs/testing.md`
- 常用 Codex 提示词：读取 `docs/prompt-templates.md`
- 可复用工作流：读取 `docs/skills/*.md`

如果找不到对应文档，必须在计划中说明缺失，不要自行假设。

## 工作流程

每次任务必须遵守以下流程：

1. 阅读 `AGENTS.md`
2. 阅读 `README.md`
3. 根据任务类型阅读相关 `docs/*` 文档
4. 如果任务复杂，先输出计划，等待用户确认后再执行
5. 只修改与当前任务直接相关的文件
6. 修改完成后进行最小验证
7. 最后汇报改动内容、验证结果和风险

## 计划要求

复杂任务的计划必须包含：

- 任务目标
- 预计修改的文件
- 实施步骤，建议 3 到 5 步
- 验证方式
- 风险或待确认事项

不要输出只有一句话的空泛计划。

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
