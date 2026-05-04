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

# Context Scout Workflow

## 目标

当 Codex 需要读取较多项目上下文、判断阶段约束、确认修改范围，或者任务可能触碰敏感边界时，应使用 context-scout 流程。

context-scout 的职责是调用 Claude Code 只读扫描项目，并生成 `.context/codex-context-pack.md`。

Codex 必须读取并验收 context-pack 后，才能继续计划、拆任务、编码或测试。

context-scout 是“大任务上下文压缩 / 侦察流程”，不是所有任务的默认前置流程。

---

## 角色分工

- Claude Code：上下文侦察员，只读、总结、生成 context-pack。
- Codex：项目经理 / 工程协作者。在本项目中，Codex 负责验收 context-pack、制定计划、拆任务、风险控制和验收。是否直接编码取决于用户当前角色设定和任务授权。如果用户指定 Codex 只做项目经理，则 Codex 不直接修改业务代码。
- 用户：最终批准人和最终验收人。

---

## 当前阶段约束来源

当前阶段约束以以下文件为准：

```text
docs/context/current-phase.md
```

context-scout 必须读取 `docs/context/current-phase.md`，并在 context-pack 中总结：

1. 当前阶段目标；
2. 当前阶段禁止项；
3. 当前阶段推荐实现方式；
4. 当前阶段允许修改范围。

不要在 AGENTS.md 中写死 Week 03 / Week 04 等临时约束。

---

## 使用前判断：避免过度调用

Codex 在决定是否调用 context-scout 前，必须先做低成本判断。

### 小任务：直接读取，不调用 context-scout

如果满足以下条件，Codex 应直接读取目标文件：

1. 用户已经明确目标文件；
2. 只需要读取 1～2 个文件；
3. 文件预计总行数少于 300 行；
4. 修改范围明确；
5. 不涉及数据库、Entity、Mapper、RabbitMQ、Redis、Worker、AI、Figma 等敏感边界。

小任务仍然可以直接读取：

- `AGENTS.md`
- `docs/context/current-phase.md`
- 当前任务卡
- 当前任务相关代码

### 大任务：提议调用 context-scout

如果满足以下任一条件，Codex 应先提议调用 context-scout：

1. 不确定应该读取哪些文件；
2. 涉及 3 个以上文件；
3. 跨前端 / 后端 / Worker / 测试 / 文档多个线程；
4. 涉及阶段边界判断；
5. 涉及敏感边界：数据库、Entity、Mapper、Redis、RabbitMQ、Worker、AI、Figma；
6. 进入新周计划；
7. 用户明确要求先做上下文侦察；
8. Codex 对修改范围不确定。

---

## 脚本执行前必须用户批准

Codex 不能自动运行 context-scout。

Codex 必须先输出 Context 策略判断。

如果决策是调用 context-scout，必须等待用户批准后再运行脚本。

---

## Context 策略判断输出格式

在调用 context-scout 前，Codex 必须先输出简短判断：

```md
# Context 策略判断

- 目标文件数量：
- 是否已经明确目标文件：
- 是否涉及敏感边界：
- 是否涉及阶段边界判断：
- 预计上下文规模：
- 决策：直接读取 / 提议调用 context-scout
```

判断必须简短，不要长篇分析。

---

## context-scout 执行方式

如果需要调用 context-scout，Codex 应提议执行以下命令之一。

### Windows PowerShell

```powershell
pwsh -NoProfile -File scripts/codex-context-scout.ps1 -Task "<当前任务描述>"
```

如果多个线程可能并行调用，可以指定不同输出文件：

```powershell
pwsh -NoProfile -File scripts/codex-context-scout.ps1 -Task "<当前任务描述>" -OutputPath ".context/context-pack-week04-day2-worker.md"
```

### Git Bash / WSL / Linux / macOS

```bash
bash scripts/codex-context-scout.sh "<当前任务描述>"
```

如果多个线程可能并行调用，可以指定不同输出文件：

```bash
bash scripts/codex-context-scout.sh --output ".context/context-pack-week04-day2-worker.md" "<当前任务描述>"
```

执行命令前必须等待用户批准。

---

## context-pack 输出路径

默认执行完成后，context-pack 输出到：

```text
.context/codex-context-pack.md
```

该文件是临时上下文包，不是正式项目文档。

`.context/` 必须加入 `.gitignore`，避免提交上下文包。

默认脚本每次运行会覆盖 `.context/codex-context-pack.md`。

如果多个线程可能并行调用 context-scout，建议使用不同文件名，例如：

```text
.context/context-pack-week04-day2-worker.md
.context/context-pack-week04-day4-backend.md
.context/context-pack-week04-day6-smoke.md
```

脚本输出路径必须位于 `.context/` 下，不允许写到项目源码目录。

---

## 多线程 context-pack 流转规则

哪个线程调用 context-scout，哪个线程必须先读取并验收返回的 context-pack。

验收通过前，该线程不得直接把 context-pack 当成事实依据。

验收通过后，该线程才可以继续：

- 输出计划；
- 拆任务；
- 编码；
- 测试；
- 或向项目经理汇报。

context-pack 不会被项目经理线程自动处理。如果需要项目经理判断，调用线程必须明确汇报。

---

## 项目经理最终确认规则

如果 context-pack 涉及以下内容，调用线程必须在自检后交给项目经理最终确认：

1. 阶段边界判断；
2. 跨前端 / 后端 / Worker / 测试 / 文档多个线程；
3. 数据库、Entity、Mapper、Redis、RabbitMQ、AI、Figma 等敏感边界；
4. 是否扩大任务范围；
5. 是否修改当前周计划或任务卡；
6. 是否改变技术方案；
7. 是否进入下一天 / 下一周任务。

项目经理最终确认前，普通线程只能汇报观察、风险和建议，不能把 context-pack 结论升级为项目决策。

---

## 普通线程可自行继续的情况

如果 context-pack 只涉及调用线程自己的局部上下文，并且不涉及阶段边界、跨线程范围、敏感模块或任务扩大，该线程可以在自检验收通过后继续执行自己的任务。

例如：

- 前端线程只理解 3 个前端文件；
- 后端线程只理解一个 Controller 和一个 DTO；
- Worker 线程只理解一个 worker 脚本和一个测试文件；
- 测试线程只理解 smoke 文档和测试结果。

---

## context-pack 过期规则

以下情况 context-pack 视为过期，不能继续直接使用：

1. 相关文件已被修改；
2. 当前阶段变化；
3. 任务目标变化；
4. 任务从一个线程切换到另一个线程；
5. 用户新增了限制条件；
6. context-pack 与 `AGENTS.md`、`docs/context/current-phase.md` 或当前任务卡冲突。

过期后必须重新生成，或重新验收并说明仍可使用的理由。

---

## 正式文档优先级

如果 context-pack 与正式文档冲突，以正式文档为准：

1. `AGENTS.md`
2. `docs/context/current-phase.md`
3. 当前任务卡
4. 相关专项设计文档

context-pack 只是临时侦察材料，不能覆盖正式项目规则。

---

## Codex 验收规则

Codex 读取 context-pack 后，必须先验收，不能直接信任，不能直接开始编码。

必须检查：

1. 是否列出了相关文件路径；
2. 是否明确当前阶段约束；
3. 是否区分 Facts 和 Suggestions；
4. 是否包含 Must Not Touch；
5. 是否存在 Uncertainties；
6. 是否有越权建议；
7. 是否建议修改禁止修改内容；
8. 是否和任务目标一致。

只有验收通过后，Codex 才能继续计划、拆任务、编码或测试。

---

## Codex 验收输出格式

Codex 必须先输出：

```md
# Context Pack 验收结果

## 结论
通过 / 不通过

## 我确认的事实
- ...

## 当前阶段约束
- ...

## 禁止修改项
- ...

## 风险
- ...

## 不确定项
- ...

## 下一步
- ...
```

---

## context-pack 不通过时

如果 context-pack 不合格，Codex 必须停止，并说明原因。

不合格情况包括：

1. 没有列出相关文件路径；
2. 没有明确阶段约束；
3. 把建议写成事实；
4. 输出了敏感信息；
5. 建议修改禁止修改内容；
6. 内容太长；
7. 与任务无关；
8. 仍然无法判断下一步修改范围。

---

## context-pack 输出限制

context-pack 必须满足：

1. 150 行以内；
2. 不输出完整源码；
3. 不输出超过 30 行的连续文件片段；
4. 不把猜测写成事实；
5. 没有证据就写“不确定”。

---

## 禁止读取或输出的敏感内容

除非用户明确允许，否则不得读取或输出：

- `.claude/settings.local.json`
- `.claude/*.local.json`
- `.env`
- `.env.*`
- `*.pem`
- `*.key`
- `*.p12`
- `*.jks`
- `application-prod.yml`
- `application-prod.yaml`
- 任何包含 `password`
- 任何包含 `secret`
- 任何包含 `token`
- 任何包含 `apiKey`
- 任何包含 `privateKey`

如果发现敏感文件，只能报告：

```text
发现敏感配置文件路径，但未读取内容。
```

---

## 禁止读取的低价值目录和副产物

不要读取以下内容：

- `.context/`
- `frontend/dist/`
- `frontend/node_modules/`
- `backend/target/`
- `backend/uploads/`
- `backend/mock-data/`
- `worker/__pycache__/`
- `*.log`

---

## 小任务示例：不调用 context-scout

以下任务不应调用 context-scout：

- 只检查 `schema/layout.schema.json`
- 只修改一个 enum
- 只补一个 required 字段
- 只修一个明显拼写错误
- 用户已经明确只允许修改单个文件

---

## 大任务示例：应调用 context-scout

以下任务应先提议调用 context-scout：

- 进入新的一周任务；
- 判断当前阶段哪些能改、哪些不能改；
- 修改后端架构；
- 修改数据库相关内容；
- 修改 Worker 链路；
- 修改前端多个页面；
- 不确定应该读哪些文件；
- 用户要求“先查看上下文侦察”。

---

## 标准提示词

当用户要求先判断是否需要 context-scout 时，Codex 应遵循以下提示词：

```text
本次任务请先判断是否需要 context-scout。

要求：
1. 先输出 Context 策略判断。
2. 如果只涉及 1～2 个明确小文件，直接读取，不调用 context-scout。
3. 如果涉及多个文件、阶段边界或敏感模块，先提议调用 context-scout。
4. 如果需要调用 context-scout，必须先等待用户批准，不得自动运行脚本。
5. 用户批准后，才运行脚本生成 .context/codex-context-pack.md。
6. Codex 读取 .context/codex-context-pack.md 后，必须先输出 Context Pack 验收结果。
7. 验收通过后，只输出实施计划，不要直接改代码。
8. 验收不通过时，停止并说明原因。
```

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
