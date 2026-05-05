# 截图 / Figma 到响应式页面生成器

## 项目简介

本项目旨在把“截图”或“Figma 设计信息”转化为可运行、可维护的响应式页面代码，并逐步形成一套适合 Codex 多线程协作的工程方式。

当前阶段不是 AI 生成真实页面，而是 Week 04 的规则编译闭环：

```text
Layout JSON v0.1
-> Worker 校验
-> Worker 静态编译 htmlCode / cssCode
-> generated-page artifact
-> 后端 mock 保存 / 查询
-> 前端 iframe sandbox 安全预览
```

## 快速入口

新成员或 Codex 进入仓库时，优先阅读：

1. `AGENTS.md`
2. `docs/INDEX.md`
3. `docs/context/current-phase.md`
4. 当前任务卡：`docs/tasks/active/*.md`

完整 PRD、历史周计划、历史状态和全部 skills 只在任务卡明确要求，或任务确实必须参考时读取。

## 当前文档入口

| 类型 | 路径 |
|---|---|
| 文档总索引 | `docs/INDEX.md` |
| 当前阶段上下文 | `docs/context/current-phase.md` |
| 当前周计划 | `docs/plans/week-04.md` |
| 当前活跃任务卡 | `docs/tasks/active/week04-*.md` |
| generated-page artifact 契约 | `docs/specs/generated-page-artifact-v0.1.md` |
| Layout JSON 到 HTML/CSS 映射 | `docs/specs/layout-to-html-v0.1.md` |
| Layout JSON v0.1 设计 | `docs/specs/layout-json-v0.1.md` |
| Layout API 契约 | `docs/specs/layout-api-contracts.md` |
| context-scout 协作流程 | `docs/playbooks/context-scout.md` |
| 当前提示词模板 | `docs/prompts/current.md` |
| 架构决策记录 | `docs/decisions/ADR-*.md` |
| smoke 验证说明 | `tests/smoke/README.md` |

## 默认技术栈

- 前端：Vue3 + Vite + JavaScript
- 后端：Java 17 + Spring Boot + Maven
- 数据库：MySQL（长期方向；当前阶段不实际落库）
- 数据访问：MyBatis-Plus（长期方向；当前阶段不新增 Entity / Mapper）
- Worker：Python 3.11 推荐，当前 smoke 允许 Python 3.10+
- 测试：smoke test、接口测试、前端页面测试

## 当前禁止

- 不接真实 AI / OpenAI / Claude / Gemini SDK
- 不接 Figma API / Figma MCP
- 不接 MySQL 实际落库
- 不创建数据库表、Entity、Mapper
- 不接 Redis / RabbitMQ
- 不做真实截图解析
- 不做 ZIP 导出、拖拽编辑器、在线编辑器
- 不要求 `vueCode` 真正可运行
- 不做 Playwright 视觉回归

## 与 Codex 协作

日常任务采用轻量上下文：

```text
AGENTS.md
docs/context/current-phase.md
docs/tasks/active/当前任务卡.md
当前任务相关代码
```

大任务、跨模块任务、阶段边界不清或敏感边界任务，可按 `docs/playbooks/context-scout.md` 先生成临时 context-pack；Codex 必须验收后再计划、拆任务、编码或测试。

## 本地运行

本地启动和 smoke 命令以 `tests/smoke/README.md` 为准。

如启动 dev server 或后端服务，验证完成后需要停止进程，不留下后台服务。
