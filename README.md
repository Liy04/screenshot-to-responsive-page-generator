# 截图 / Figma 到响应式页面生成器

## 项目简介

本项目用于探索“截图 / Figma 设计信息 -> 响应式页面代码”的生成链路，并沉淀适合个人学习、Codex 执行和 MVP 推进的轻量协作方式。

当前阶段为 Week 14 MVP 产品化交付闭环。Week 14 聚焦围绕 MVP 交付链路完成产品化补齐、验证和收口。

项目协作采用 **Codex Lead + Short-lived Subagents Workflow**，仍然保持 Docs Lite 原则，不回到重文档体系。

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
3. `docs/mvp-roadmap.md`
4. `docs/plan.md`
5. `docs/agents/README.md`
6. 当前活跃 `docs/tasks/day-xx.md`，如存在
7. 当前任务相关代码
8. 必要时读取 `docs/spec.md`

## 当前文档入口

| 类型 | 路径 |
|---|---|
| 当前阶段 | `docs/current.md` |
| 当前计划 | `docs/plan.md` |
| 当前任务 | `docs/tasks/day-xx.md`（有活跃任务时） |
| 当前规格 | `docs/spec.md` |
| 文档索引 | `docs/INDEX.md` |
| Codex 角色边界 | `docs/agents/README.md` |
| context-scout playbook | `docs/playbooks/context-scout.md` |
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
- 不做复杂截图解析系统 / 多页面截图理解 / 未批准新输入链路。
- 不做 ZIP 导出、拖拽编辑器、在线编辑器。
- 不要求 `vueCode` 真正可运行。
- 不做 Playwright 视觉回归。

## 与 Codex 协作

日常任务采用 Lite 上下文：

```text
AGENTS.md
docs/current.md
docs/mvp-roadmap.md
docs/plan.md
docs/agents/README.md
当前活跃 docs/tasks/day-xx.md，如存在
当前任务相关代码
必要时 docs/spec.md
```

大任务、跨模块任务、阶段边界不清或敏感边界任务，先 spawn `explorer-agent`；必要时由 `explorer-agent` 按 `docs/playbooks/context-scout.md` 生成临时 context-pack，并回到 Lead 验收后再计划、拆任务、编码或测试。

## Codex Lead + Short-lived Subagents

本项目的 subagent 指 Codex 当前运行环境支持 subagent 工具时，由 Lead 显式创建的短生命周期子智能体。

它不是 Claude Code Custom Subagents，不是 `.claude/agents/`，不是 `CLAUDE.md`，不是 Claude Code `/agents`，不是 Claude Code Agent Teams，也不是自动并发或长期常驻代理。

当前角色：

- `lead`：范围判断、任务拆分、顺序控制、验收收口
- `explorer-agent`：大任务、跨模块、边界不清任务的上下文侦察
- `docs-agent`：文档维护
- `backend-agent`：后端开发
- `frontend-agent`：Vue3 + Vite + JavaScript 前端开发
- `worker-agent`：Python Worker 开发
- `tester-agent`：测试、smoke、问题复现和结果记录
- `reviewer-agent`：代码质量、安全、潜在 bug 和边界审查

详细规则见 `docs/agents/README.md`。默认新任务仍优先读取 Docs Lite 文件，不默认读取 `docs/archive/`；小任务 Lead 可直接做，但用户显式要求 spawn 时必须 spawn；中大型开发任务必须 spawn 对应实现 agent；大任务、跨模块任务、边界不清任务先 spawn `explorer-agent`。如果当前运行环境没有 subagent 工具，Lead 必须明确说明降级原因并请求确认。

## 本地运行

本地启动和 smoke 命令以 `tests/smoke/README.md` 为准。

如需执行 Week 09 Real AI smoke：

- 需要 Python 3.11+。
- 需要 SiliconFlow `OPENAI_*` 环境变量。
- backend 启动时需要 `--imagepage.worker.timeout-seconds=120`。
- 详细运行配置见 `docs/spec.md`。

如需复现 Week 15 fixed sample REAL_AI full smoke：

- 使用公开固定样例 `samples/01-simple-card-page.png`、`samples/02-simple-form-page.png`、`samples/03-dashboard-cards-page.png`。
- backend 推荐启动参数为 `--imagepage.worker.timeout-seconds=420`；已验证 180 秒可能返回 504，不建议用 120 / 180 秒作为 Week 15 全量复测口径。
- `420s` 只是当前真实多模态固定样例 smoke 的复现配置，不是产品级稳定性修复；真正的延迟 / 异步稳定性应作为后续 single bet 评估。
- 不写入真实 API key，不提交生成产物或运行副产物。

如启动 dev server 或后端服务，验证完成后需要停止进程，不留下后台服务。
