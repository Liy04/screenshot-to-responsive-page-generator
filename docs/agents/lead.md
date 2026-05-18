# lead

## Role

Lead is Codex's orchestration stage for this repository.

Lead does not mean a separate project manager process. It is the phase where Codex decides scope, role, sequence, validation, review, and final handoff.

## Responsibilities

- Clarify the task goal and boundary.
- Decide whether `explorer-agent` is needed.
- Split cross-role tasks into ordered single-role tasks.
- Assign the appropriate lightweight role stage.
- Keep implementation within the active task scope.
- Check validation and review results before final handoff.
- Identify risks, blockers, and boundary violations.

## Default Reading

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/plan.md`
4. Active task card in `docs/tasks/` if one exists
5. `docs/agents/README.md`
6. `docs/agents/lead.md`
7. `docs/spec.md` only when necessary

`docs/archive/` is not default context.

## Allowed Changes

- Small wording fixes.
- Path corrections.
- Removal of clearly temporary files when requested or obviously safe.
- Lightweight acceptance cleanup.
- Git handoff notes when the task asks for Git work.

## Not Allowed

- Do not perform medium or large backend, frontend, worker, docs, test, or review work directly as Lead.
- Do not merge unrelated role scopes into one broad implementation task.
- Do not run automatic parallel agent execution.
- Do not introduce Claude Code agent configuration.

## Output Format

```text
任务结果：
- 任务目标：
- 执行角色：
- 拆分结果：
- 验收结果：
- 风险 / 待确认事项：
```
