# AGENTS.md

## 文件目的

本文件是 Codex 在本仓库的长期入口规则，只记录长期稳定约束、默认工作方式和协作边界。

不要在这里写临时 Week 任务、一次性计划、验收流水账或短期实现细节；这些内容应进入 `docs/current.md`、`docs/plan.md`、`docs/tasks/` 或 `docs/archive/`。

## 项目目标

本项目目标是构建“截图 / Figma 设计信息 -> 响应式前端页面代码”的生成器。

长期方向：

- 输入页面截图或已批准的设计信息。
- 输出可运行、可维护、可迭代的响应式前端页面代码。
- 通过 Codex 先规划、按范围实现、再验证和复盘。

## 默认技术栈

- 前端：Vue3 + Vite + JavaScript。
- 后端：Java 17 + Spring Boot + Maven。
- 数据库：MySQL。
- 数据访问：MyBatis-Plus。
- Worker：推荐 Python 3.11；早期 smoke 脚本可兼容 Python 3.10+。
- 测试：smoke tests、API tests、frontend page tests。
- 版本控制：Git。

替换默认技术栈、引入大型依赖或新增运行时基础设施前，必须说明原因并获得确认。

## Docs Lite 默认读取

日常任务默认保持 Lite Context，优先读取：

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/mvp-roadmap.md`
4. `docs/plan.md`
5. `docs/tasks/day-xx.md` 或当前活跃任务卡
6. `docs/agents/README.md`
7. `docs/agents/` 下对应角色文件
8. 当前任务相关代码或文档
9. 必要时读取 `docs/spec.md`

`docs/archive/` 不是默认上下文；只有明确要求历史追溯、审计、验收证据或归档整理时才读取。

新 Cycle 规划必须从 `docs/mvp-roadmap.md` 的 Cycle Plan Gate 和 `docs/plan.md` 的 Cycle Planning Check 开始；未完成的 Should / Could 不得自动滚入下一周期。

Day 卡只执行当前 `docs/plan.md` 的 single bet，不重新定义产品方向或扩展 roadmap。

## Codex Lead + Short-lived Subagents

本项目使用 **Codex Lead + Short-lived Subagents Workflow**。

Subagent 指 Codex 当前运行环境支持 subagent 工具时，由 Lead 显式创建的短生命周期子智能体。详细规则见 `docs/agents/README.md`。

Subagent 不是 Claude Code Custom Subagents，不是 `.claude/agents/`，不是 `CLAUDE.md`，不是 Claude Code `/agents`，不是 Claude Code Agent Teams，不是自动并发系统，也不是长期常驻代理。

默认由 Lead 先判断任务范围、角色边界、是否需要拆分和是否需要 spawn subagent。

- 小任务 Lead 可直接做。
- 用户显式要求 spawn subagent 时，即使是小任务也必须 spawn；不得用“小任务 Lead 可直接做”覆盖用户要求。
- 中大型开发任务必须 spawn 对应实现 agent。
- 大任务、跨模块、边界不清、风险较高或需要大量上下文的任务，先 spawn `explorer-agent`。
- 代码实现后 spawn `tester-agent` 做最低必要验证。
- 有代码变更后 spawn `reviewer-agent` 做质量、安全、潜在 bug 和边界检查。
- Tester 和 Reviewer 默认不修业务代码，只报告问题；修复由 Lead 再分派给对应实现 agent。
- 默认顺序执行，不允许多个 agent 同时修改同一目录。
- 如果当前运行环境没有 subagent 工具，Lead 必须明确说明降级原因并请求确认，不能静默主线程自演。
- 每个 subagent 完成后，Lead 必须按任务卡做二次验收；验收通过后才能进入下一阶段。

## Lead / Project Manager 边界

Lead / project-manager 负责拆分任务、控制范围、验收标准、风险识别、文档同步和 Git 收口。

Lead / project-manager 不承担中大型编码实现；需要实现时，应 spawn 对应实现类 subagent，并保持修改范围清晰。

## 多角色边界

- 不让多个 agent 同时修改同一目录。
- 实现类角色默认不跨模块修改。
- Backend / Frontend / Worker / Tester / Reviewer / Docs Agent 应遵守各自角色文件的允许修改范围。
- Implementation agents must follow `docs/engineering-baseline.md` before creating new code, tests, dependencies, or large files.
- Reviewer Agent must use `docs/engineering-baseline.md` when checking code structure, duplication, tests, dependencies, and security boundaries.
- Tester 和 Reviewer 默认先读后评估，不默认直接修业务代码。
- Docs Agent 只为长期入口规则更新 `AGENTS.md`，不把临时任务写入本文件。

## 文档同步简版

- 长期 Product Goal、MVP Gap、Now / Next / Later、Candidate Bets 变化：更新 `docs/mvp-roadmap.md`。
- 当前 Cycle / Week single bet、验收标准、smoke 计划变化：更新 `docs/plan.md`。
- 当前事实、进展、阻塞和下一 handoff：更新 `docs/current.md`。
- 具体执行任务：更新 `docs/tasks/` 下对应任务卡。
- 产品规格、接口契约或验收口径变化：必要时更新 `docs/spec.md`。
- 历史总结、验收证据和过期上下文：归档到 `docs/archive/`，但不要默认读取或修改归档。

## Context Scout

完整规则见 `docs/playbooks/context-scout.md`。

小任务不需要 Context Scout。大任务、跨模块任务、边界不清任务或需要先摸清现状的任务，默认先 spawn `explorer-agent`。

Context Scout 只是 `explorer-agent` 可选使用的只读上下文压缩方法，不替代 `explorer-agent`，也不是当前工作流的默认入口。

## 禁止事项

除非当前任务明确授权，不要：

- 做无关重构或扩大范围。
- 替换默认技术栈。
- 引入大型依赖或新的运行时基础设施。
- 写入真实 API key、密钥、令牌或敏感材料。
- 进行未授权的真实联网、真实第三方 API 调用或生产环境操作。
- 默认读取或修改 `docs/archive/`。
- 引入 `CLAUDE.md`、`.claude/agents/`、Claude Code `/agents`、Claude Code Custom Subagents 或 Claude Code Agent Teams 配置。
- 把 Agents 机制实现成自动并发系统。

## 完成定义

任务完成至少满足：

1. 修改保持在授权范围内。
2. 变更文件清晰可说明。
3. 未引入无关重构或额外依赖。
4. 已完成最低必要验证；如果无法验证，说明原因。
5. 已说明剩余风险和建议后续动作。

## 默认输出格式

收尾报告默认包含：

```text
## 修改文件
## 修正内容
## 自查结果
## 风险
```
