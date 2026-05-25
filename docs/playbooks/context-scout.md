# Context Scout Playbook

## 定位

Context Scout 是 `explorer-agent` 可选使用的只读上下文压缩方法。

它用于在任务上下文较大、边界不清、跨模块或风险较高时，帮助 `explorer-agent` 生成临时 context-pack，供 Lead 二次验收和后续拆分使用。

当前默认入口不是 context-scout。大任务、跨模块任务、边界不清任务或需要先摸清现状的任务，默认先由 Lead spawn `explorer-agent`，再由 `explorer-agent` 判断是否需要使用本 playbook。

Context Scout 不是：

- Claude Code Custom Subagents。
- `.claude/agents/`。
- `CLAUDE.md`。
- Claude Code `/agents`。
- Claude Code Agent Teams。
- 自动并发系统。
- 项目决策机制。
- 替代 `explorer-agent` 的默认入口。

不得因为使用了 context-scout，就跳过 Lead 对 explorer 输出和 context-pack 的验收。

---

## 使用条件

`explorer-agent` 可以在以下情况选择使用 context-scout：

1. 不确定应该读取哪些文件。
2. 需要压缩 3 个以上相关文件的上下文。
3. 涉及前端 / 后端 / Worker / 测试 / 文档中的多个范围。
4. 需要判断当前阶段边界或禁止项。
5. 涉及敏感边界：数据库、Entity、Mapper、Redis、RabbitMQ、Worker、AI、Figma。
6. 用户明确要求先做上下文侦察。
7. `explorer-agent` 对修改范围不确定，需要先形成只读事实包。

小任务不需要 context-scout。目标文件明确、只需读取 1 到 2 个文件、修改范围清楚且不涉及敏感边界时，`explorer-agent` 或 Lead 可直接读取目标文件。

---

## 当前阶段约束来源

context-scout 必须以正式文档为准：

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/mvp-roadmap.md`
4. `docs/plan.md`
5. 当前任务卡
6. 必要时读取 `docs/spec.md`

`docs/archive/` 不是默认上下文。只有用户明确要求历史追溯、审计、验收证据或归档整理时，才允许读取。

---

## 输出物

context-scout 的输出是临时 context-pack，默认路径为：

```text
.context/codex-context-pack.md
```

context-pack 不是正式项目文档，不得提交，不得写入项目源码目录。

context-pack 只能作为只读事实压缩材料。它不能直接升级为项目决策，不能覆盖 `AGENTS.md`、`docs/current.md`、当前任务卡或 Lead 验收结论。

---

## 必须回到 Lead 验收

context-pack 生成后，`explorer-agent` 必须先自检并向 Lead 汇报：

- 读取了哪些文件。
- 确认了哪些事实。
- 当前阶段约束是什么。
- 禁止修改项是什么。
- 仍有哪些不确定项。
- 是否建议继续实现、拆分任务或停止确认。

Lead 必须对 `explorer-agent` 的汇报和 context-pack 做二次验收。验收通过前，不得继续计划、拆任务、编码或测试。

如果 context-pack 涉及以下内容，必须由 Lead 明确验收，不能由 context-pack 自行决定：

1. 阶段边界判断。
2. 跨前端 / 后端 / Worker / 测试 / 文档多个范围。
3. 数据库、Entity、Mapper、Redis、RabbitMQ、AI、Figma 等敏感边界。
4. 是否扩大任务范围。
5. 是否修改当前计划或任务卡。
6. 是否改变技术方案。
7. 是否进入下一天 / 下一周任务。

---

## Legacy Helper

仓库中可能保留旧 context-scout 脚本或旧说明，例如：

```powershell
pwsh -NoProfile -File scripts/codex-context-scout.ps1 -Task "<当前任务描述>"
```

```bash
bash scripts/codex-context-scout.sh "<当前任务描述>"
```

这些脚本只是 legacy helper，用于生成临时 context-pack。它们不是当前默认入口，不代表 Claude Code agent 机制，也不能替代 Lead spawn `explorer-agent`。

如果使用 legacy helper：

1. 必须由 `explorer-agent` 在只读场景下使用。
2. 输出路径必须位于 `.context/` 下。
3. 不得读取敏感文件内容。
4. 不得把 context-pack 写入正式文档或源码目录。
5. 生成后必须回到 Lead 验收。

---

## Context Pack 验收标准

Lead 验收 context-pack 时至少检查：

1. 是否列出了相关文件路径。
2. 是否明确当前阶段约束。
3. 是否区分 Facts 和 Suggestions。
4. 是否包含 Must Not Touch。
5. 是否存在 Uncertainties。
6. 是否有越权建议。
7. 是否建议修改禁止修改内容。
8. 是否和任务目标一致。

验收结论只能是：

```text
通过 / 条件通过 / 不通过
```

不通过时必须停止，并说明原因。

---

## context-pack 输出限制

context-pack 必须满足：

1. 150 行以内。
2. 不输出完整源码。
3. 不输出超过 30 行的连续文件片段。
4. 不把猜测写成事实。
5. 没有证据就写“不确定”。
6. 不输出密钥、令牌、密码、私钥或真实敏感材料。

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

## 简短判断格式

当 `explorer-agent` 判断是否需要使用 context-scout 时，可使用：

```md
# Context Scout 判断

- 是否为大任务 / 跨模块 / 边界不清：
- 是否已有明确目标文件：
- 是否涉及敏感边界：
- 是否需要压缩上下文：
- 决策：直接读取 / 使用 context-scout legacy helper
```
