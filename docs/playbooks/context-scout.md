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
docs/current.md
```

context-scout 必须读取 `docs/current.md`，并在 context-pack 中总结：

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
- `docs/current.md`
- 当前任务卡
- 当前任务相关代码

### 大任务：调用 context-scout

如果满足以下任一条件，Codex 应在输出 Context 策略判断后直接运行 context-scout：

1. 不确定应该读取哪些文件；
2. 涉及 3 个以上文件；
3. 跨前端 / 后端 / Worker / 测试 / 文档多个线程；
4. 涉及阶段边界判断；
5. 涉及敏感边界：数据库、Entity、Mapper、Redis、RabbitMQ、Worker、AI、Figma；
6. 进入新周计划；
7. 用户明确要求先做上下文侦察；
8. Codex 对修改范围不确定。

### 超大任务：先拆分 context-pack

如果任务同时覆盖多个大型范围，不应把所有内容塞进一次 context-scout。

例如：

- 全量 docs 重构验收；
- 同时检查目录结构、路径引用、prompts、ADR、任务卡和测试文档；
- 同时跨前端、后端、Worker、测试和文档；
- 需要读取大量历史归档文档。

这类任务应优先拆成多个 context-pack，例如：

```text
.context/context-pack-docs-structure.md
.context/context-pack-docs-paths.md
.context/context-pack-prompts-adr.md
```

推荐拆分方式：

1. 结构验收：只看目录、`docs/INDEX.md`、`README.md`、`AGENTS.md`、`docs/current.md`。
2. 路径引用验收：只查旧路径、新路径、活跃文档和归档文档引用。
3. prompts / ADR 验收：只看 `docs/archive/lite-refactor/prompts/`、`docs/archive/prompts/`、`docs/archive/lite-refactor/decisions/`。

只有在拆分后仍然因为 turns 不足失败时，才考虑临时提高 `MaxTurns`。

---

## 脚本执行规则

Codex 不能跳过 Context 策略判断直接运行 context-scout。

Codex 必须先输出 Context 策略判断。

如果判断需要 context-scout，则可直接运行 context-scout，不需要用户再次确认。

运行后必须读取并验收 context-pack。

验收通过后，才能继续计划、拆任务、编码或测试。

验收不通过时，必须停止并说明原因。

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
- 决策：直接读取 / 运行 context-scout
```

判断必须简短，不要长篇分析。

---

## context-scout 执行方式

如果需要调用 context-scout，Codex 可执行以下命令之一。

### Windows PowerShell

```powershell
pwsh -NoProfile -File scripts/codex-context-scout.ps1 -Task "<当前任务描述>"
```

如果多个线程可能并行调用，可以指定不同输出文件：

```powershell
pwsh -NoProfile -File scripts/codex-context-scout.ps1 -Task "<当前任务描述>" -OutputPath ".context/context-pack-week04-day2-worker.md"
```

如拆分后仍然需要更多轮次，可以临时提高 `MaxTurns`，但不要超过脚本限制：

```powershell
pwsh -NoProfile -File scripts/codex-context-scout.ps1 -Task "<当前任务描述>" -OutputPath ".context/context-pack-docs-paths.md" -MaxTurns 12
```

### Git Bash / WSL / Linux / macOS

```bash
bash scripts/codex-context-scout.sh "<当前任务描述>"
```

如果多个线程可能并行调用，可以指定不同输出文件：

```bash
bash scripts/codex-context-scout.sh --output ".context/context-pack-week04-day2-worker.md" "<当前任务描述>"
```

如拆分后仍然需要更多轮次，可以临时提高 `--max-turns`，但不要超过脚本限制：

```bash
bash scripts/codex-context-scout.sh --output ".context/context-pack-docs-paths.md" --max-turns 12 "<当前任务描述>"
```

输出 Context 策略判断后，如决策为运行 context-scout，可直接执行对应命令。

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
6. context-pack 与 `AGENTS.md`、`docs/current.md` 或当前任务卡冲突。

过期后必须重新生成，或重新验收并说明仍可使用的理由。

---

## 正式文档优先级

如果 context-pack 与正式文档冲突，以正式文档为准：

1. `AGENTS.md`
2. `docs/current.md`
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

以下任务应在 Context 策略判断后运行 context-scout：

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
3. 如果涉及多个文件、阶段边界或敏感模块，判断需要 context-scout 后可直接运行脚本。
4. 运行脚本生成 .context/codex-context-pack.md。
5. Codex 读取 .context/codex-context-pack.md 后，必须先输出 Context Pack 验收结果。
6. 验收通过后，才能继续计划、拆任务、编码或测试。
7. 验收不通过时，停止并说明原因。
```

