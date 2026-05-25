# Codex Lead + Short-lived Subagents Workflow

## Purpose

This directory defines how Codex coordinates project work through Lead and short-lived subagents.

Subagent means a short-lived child agent explicitly spawned by Lead when the current Codex runtime provides a subagent tool. A subagent receives a scoped task, reads only the needed context, works within its allowed files, returns a compact handoff, then stops.

Subagent is not:

- Claude Code Custom Subagents.
- `.claude/agents/`.
- `CLAUDE.md`.
- Claude Code `/agents`.
- Claude Code Agent Teams.
- An automatic parallel execution system.
- A long-running resident agent.

Do not introduce Claude Code configuration or files for this workflow.

## Runtime Capability Gate

Lead must check whether the current runtime supports explicit subagent spawning.

- If subagent tools are available, Lead uses them for tasks that require spawn.
- If subagent tools are not available, Lead must state the downgrade reason and request confirmation before continuing in the main thread.
- Lead must not silently role-play `frontend-agent`, `tester-agent`, `reviewer-agent`, or any other required subagent in the main thread for medium or large work.

## Direct Work vs Spawn Rules

Lead may directly handle small, low-risk tasks when the change is narrow and does not need role separation.

### User Explicit Spawn Override

When the user explicitly asks Lead to spawn a subagent, Lead must spawn that subagent even if the task looks small.

Lead must not use the "small tasks may be handled directly" rule to override an explicit user spawn request.

Lead must spawn:

- `explorer-agent` for large, cross-module, boundary-unclear, high-risk, or context-heavy tasks.
- The matching implementation agent for medium or large development work.
- `tester-agent` after code implementation to run minimum necessary validation.
- `reviewer-agent` after code changes to check quality, security, potential bugs, and boundaries.
- `docs-agent` when active docs, indexes, task cards, or stable entry docs need non-trivial updates.

Tester and Reviewer default to reporting only. They do not fix business code by default. Fixes are assigned by Lead to the responsible implementation agent.

## Explorer Agent and Context Scout

For large, cross-module, boundary-unclear, high-risk, or context-heavy tasks, Lead defaults to spawning `explorer-agent` first.

`context-scout` is only an optional read-only context compression playbook that `explorer-agent` may use when it needs a compact context pack. It does not replace `explorer-agent`, is not the default entry point, and is not a Claude Code agent mechanism.

`context-scout` is not Claude Code Custom Subagents, not `.claude/agents/`, not `CLAUDE.md`, not Claude Code `/agents`, not Claude Code Agent Teams, and not an automatic parallel execution system.

## Available Subagents

| Subagent | File | Main responsibility |
|---|---|---|
| Lead | `docs/agents/lead.md` | Scope, split, spawn decisions, acceptance, final handoff |
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
3. `docs/mvp-roadmap.md`
4. `docs/plan.md`
5. Active task card in `docs/tasks/` if one exists
6. `docs/agents/README.md`
7. Current role file under `docs/agents/`
8. Current task related code or docs
9. `docs/spec.md` only when necessary

`docs/archive/` is not default context. Read it only when the task explicitly requires history lookup, audit, or acceptance evidence.

## Standard Flow

1. Lead confirms the goal, scope, active task card, and spawn requirements.
2. Lead spawns `explorer-agent` when context scouting is required.
3. Lead reviews Explorer output and narrows the task.
4. Lead spawns one implementation agent for the scoped work.
5. Lead performs second-pass acceptance of the implementation result.
6. Lead spawns `tester-agent` for minimum necessary validation after code implementation.
7. Lead reviews Tester output and decides whether fixes are needed.
8. Lead spawns `reviewer-agent` after code changes.
9. Lead assigns any fixes to the responsible implementation agent, then repeats validation or review as needed.
10. Lead closes with changed files, validation, review result, residual risk, and next recommendation.

## Parallelism Policy

Default execution is sequential.

- Do not allow multiple agents to modify the same directory at the same time.
- Do not run parallel implementation agents unless Lead explicitly proves the directories and contracts do not overlap.
- Tester and Reviewer may read after implementation, but they should not race with implementation edits.
- If a parallel read-only check is useful, Lead must state that it is read-only and non-overlapping.

## Subagent Handoff Contract

Every spawned subagent task must include:

- Task goal.
- Default reading.
- Allowed changes.
- Forbidden changes.
- Expected validation or review.
- Stop rules.
- Required return format.

Every subagent must return:

- Files read or changed.
- Main result.
- Validation or review performed.
- Problems found.
- Suggested next responsible agent when fixes are needed.
- Risks or open questions.

Lead must perform second-pass acceptance before spawning the next agent.

## Stop Rules

A subagent must stop and report instead of continuing when:

- The task requires files outside its allowed scope.
- The task would modify `docs/archive/` without explicit authorization.
- The task would introduce Claude Code configuration.
- The task would write API keys, credentials, tokens, or sensitive material.
- The task would change backend / frontend / worker contracts without Lead approval.
- Tester or Reviewer finds business-code fixes are needed.
- Required context is contradictory or insufficient.

## Stable Forbidden Items

Unless the current stage and task explicitly allow it, do not:

- Connect a real Figma API or Figma MCP.
- Add Redis or RabbitMQ as a runtime prerequisite.
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
5. Tester and Reviewer were spawned when required, or Lead explains the confirmed exception.
6. The final report includes changes, validation, review status, and risks.
