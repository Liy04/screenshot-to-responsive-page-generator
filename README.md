# 截图 / Figma 到响应式页面生成器

## 项目简介

本项目用于探索“截图 / Figma 设计信息 -> 响应式页面代码”的生成链路，并沉淀适合个人学习、Codex 执行和 MVP 推进的轻量协作方式。

当前项目已完成 Week 10 收口，可进入 Week 11 规划阶段。Week 10 已把真实 AI 链路稳定化、artifact 复用、前端状态展示和可复现 smoke 收口完成。

Week 11 开始试运行 **Codex Lead + Lightweight Agents Workflow**，仍然保持 Docs Lite 原则，不回到重文档体系。

当前核心链路：

```text
单张真实图片
-> 后端保存临时文件
-> 后端调用 Python Worker
-> Worker 调真实 AI / fallback
-> Layout JSON v0.1
-> generated-page HTML
-> 前端 iframe sandbox 安全预览
```

## 快速入口

新任务优先阅读：

1. `AGENTS.md`
2. `docs/current.md`
3. 当前活跃 `docs/tasks/day-xx.md`，如存在
4. 当前任务相关代码
5. 必要时读取 `docs/spec.md`

## 当前文档入口

| 类型 | 路径 |
|---|---|
| 当前阶段 | `docs/current.md` |
| 当前计划 | `docs/plan.md` |
| 当前任务 | `docs/tasks/day-xx.md`（有活跃任务时） |
| 当前规格 | `docs/spec.md` |
| 文档索引 | `docs/INDEX.md` |
| Codex 角色边界 | `docs/agents/README.md` |
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
当前活跃 docs/tasks/day-xx.md，如存在
当前任务相关代码
必要时 docs/spec.md
```

大任务、跨模块任务、阶段边界不清或敏感边界任务，先进入 `explorer-agent` 阶段；必要时可按 `docs/playbooks/context-scout.md` 生成临时 context-pack，Codex 必须验收后再计划、拆任务、编码或测试。

## Codex Lead + Lightweight Agents

本项目的 agents 是 Codex 执行任务时使用的角色阶段和边界规则，不是 Claude Code Custom Subagents，不是 Claude Code `/agents`，也不是自动并发系统。

Week 11 开始试运行以下轻量角色：

- `lead`：范围判断、任务拆分、顺序控制、验收收口
- `explorer-agent`：大任务、跨模块、边界不清任务的上下文侦察
- `docs-agent`：文档维护
- `backend-agent`：后端开发
- `frontend-agent`：Vue3 + Vite + JavaScript 前端开发
- `worker-agent`：Python Worker 开发
- `tester-agent`：测试、smoke、问题复现和结果记录
- `reviewer-agent`：代码质量、安全、潜在 bug 和边界审查

详细规则见 `docs/agents/README.md`。默认新任务仍优先读取 Docs Lite 文件，不默认读取 `docs/archive/`；大任务、跨模块任务、边界不清任务先进入 `explorer-agent` 阶段。

## 本地运行

本地启动和 smoke 命令以 `tests/smoke/README.md` 为准。

如需执行 Week 09 Real AI smoke：

- 需要 Python 3.11+。
- 需要 SiliconFlow `OPENAI_*` 环境变量。
- backend 启动时需要 `--imagepage.worker.timeout-seconds=120`。
- 详细运行配置见 `docs/spec.md`。

如启动 dev server 或后端服务，验证完成后需要停止进程，不留下后台服务。
