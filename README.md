# 截图 / Figma 到响应式页面生成器

## 项目简介

本项目用于探索“截图 / Figma 设计信息 -> 响应式页面代码”的生成链路，并沉淀适合个人学习、Codex 执行和 MVP 推进的轻量协作方式。

当前阶段不是接入真实 AI 生成页面，而是 Week 04 的确定性规则编译闭环：

```text
Layout JSON v0.1
-> Worker 校验
-> Worker 静态编译 htmlCode / cssCode
-> generated-page artifact
-> 后端 mock 保存 / 查询
-> 前端 iframe sandbox 安全预览
```

## 快速入口

新任务优先阅读：

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/task.md`
4. 当前任务相关代码
5. 必要时读取 `docs/spec.md`

## 当前文档入口

| 类型 | 路径 |
|---|---|
| 当前阶段 | `docs/current.md` |
| 当前计划 | `docs/plan.md` |
| 当前任务 | `docs/task.md` |
| 当前规格 | `docs/spec.md` |
| 文档索引 | `docs/INDEX.md` |
| 上下文侦察流程 | `docs/playbooks/context-scout.md` |
| 历史归档 | `docs/archive/` |
| smoke 验证说明 | `tests/smoke/README.md` |

`docs/archive/` 只用于历史追溯，不参与默认上下文。

## 默认技术栈

- 前端：Vue3 + Vite + JavaScript
- 后端：Java 17 + Spring Boot + Maven
- 数据库：MySQL（长期方向；当前阶段不实际落库）
- 数据访问：MyBatis-Plus（长期方向；当前阶段不新增 Entity / Mapper）
- Worker：Python 3.11 推荐，早期 smoke 允许 Python 3.10+
- 测试：smoke test、接口测试、前端页面测试

## 当前禁止

- 不接真实 AI / OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL 实际落库。
- 不创建数据库表、Entity、Mapper。
- 不接 Redis / RabbitMQ。
- 不做真实截图解析。
- 不做 ZIP 导出、拖拽编辑器、在线编辑器。
- 不要求 `vueCode` 真正可运行。
- 不做 Playwright 视觉回归。

## 与 Codex 协作

日常任务采用 Lite 上下文：

```text
AGENTS.md
docs/current.md
docs/task.md
当前任务相关代码
必要时 docs/spec.md
```

大任务、跨模块任务、阶段边界不清或敏感边界任务，可按 `docs/playbooks/context-scout.md` 先生成临时 context-pack；Codex 必须验收后再计划、拆任务、编码或测试。

## 本地运行

本地启动和 smoke 命令以 `tests/smoke/README.md` 为准。

如启动 dev server 或后端服务，验证完成后需要停止进程，不留下后台服务。
