# Codex Lead + Lightweight Agents Workflow

## Purpose

This directory defines role stages and boundary rules for Codex when working in this repository.

These agents are not real long-running subagents, not an automatic spawn system, and not a Claude Code mechanism. They are lightweight execution modes used by Codex to keep context, ownership, edits, validation, and review small enough to reason about.

Do not introduce:

- `CLAUDE.md`
- `.claude/agents/`
- Claude Code Custom Subagents
- Claude Code `/agents`
- Claude Code Agent Teams
- Automatic parallel agent execution

## Core Model

Codex normally acts as **Lead** first. Lead decides whether the task is small enough to execute directly or should move through a specialized role stage.

Available role stages:

| Role | File | Main responsibility |
|---|---|---|
| Lead | `docs/agents/lead.md` | Scope, split, sequencing, acceptance, final handoff |
| Explorer | `docs/agents/explorer-agent.md` | Context scouting for large, cross-module, or unclear tasks |
| Docs Agent | `docs/agents/docs-agent.md` | Current docs, indexes, task cards, summaries |
| Backend Agent | `docs/agents/backend-agent.md` | Spring Boot backend work |
| Frontend Agent | `docs/agents/frontend-agent.md` | Vue3 + Vite + JavaScript frontend work |
| Worker Agent | `docs/agents/worker-agent.md` | Python Worker, validator, fallback, repair |
| Tester Agent | `docs/agents/tester-agent.md` | Tests, smoke, reproduction, result records |
| Reviewer Agent | `docs/agents/reviewer-agent.md` | Code quality, security, potential bug, and boundary review |

## Default Reading

Keep the default context small:

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/plan.md`
4. Active task card in `docs/tasks/` if one exists
5. Current role file under `docs/agents/`
6. Current task related code or docs
7. `docs/spec.md` only when necessary

`docs/archive/` is not default context. Read it only when the task explicitly requires history lookup, audit, or acceptance evidence.

## When To Use Explorer

Enter `explorer-agent` before implementation when a task is:

- Large or cross-module.
- Boundary-unclear.
- Sensitive to current stage constraints.
- Likely to require reading many files.
- Related to acceptance, migration, or architectural direction.

Explorer produces a compact context pack or findings summary. Lead must check that summary before planning implementation.

## Execution Flow

1. **Lead** confirms goal, scope, role, and whether Explorer is needed.
2. **Explorer** runs only when the task needs context scouting.
3. One specialized role executes the scoped task.
4. **Tester** validates implemented behavior when execution changes runnable code or testable behavior.
5. **Reviewer** reviews code changes when quality, security, bug risk, or boundary risk matters.
6. **Lead** closes with changed files, validation result, residual risk, and next recommendation.

Do not merge multiple role scopes into one broad prompt when the task clearly crosses role boundaries. Split into ordered tasks instead.

## Editing Boundaries

- A role may only modify files listed in its role document unless the active task explicitly allows more.
- Do not let multiple role stages modify the same directory at the same time.
- Tester and Reviewer are read-first roles and default to no business-code fixes.
- Docs Agent may update `AGENTS.md` only for stable long-term entry rules.
- Business directories are `backend/`, `frontend/`, `worker/`, and `tests/`.
- `docs/archive/` is not touched unless the task explicitly asks for archive work.

## Task Cards

Task cards should name the active role and scope. Do not create fake current day cards. If a template is needed, use `docs/tasks/_template.md`.

Recommended fields:

```text
负责角色：
任务目标：
默认读取：
允许修改：
禁止修改：
实施步骤：
验收标准：
输出格式：
```

## Stable Forbidden Items

Unless the current stage and task explicitly allow it, do not:

- Connect a real Figma API or Figma MCP.
- Add Redis or RabbitMQ as a runtime prerequisite.
- Implement real screenshot parsing and AI code generation beyond the approved stage.
- Implement a multi-page editor.
- Implement a drag-and-drop editor.
- Implement ZIP export.
- Make broad repository architecture changes.
- Write real API keys or sensitive material into code or docs.

## Completion Definition

A task is complete only when:

1. The changes stay within the assigned role scope.
2. Changed files are clear.
3. No unrelated refactor was introduced.
4. Minimum validation is completed, or the reason for not validating is stated.
5. The final report includes changes, validation, and risks.
