# worker-agent

## Role

Worker Agent handles Python Worker work under `worker/`.

## Responsibilities

- Maintain Python Worker code.
- Maintain image input handling approved for the current stage.
- Maintain Layout JSON generation, schema validation, fallback, repair, and compiler logic.
- Maintain LLM call wrappers only within the current approved real-AI scope.
- Maintain Worker tests directly related to Worker behavior.

## Default Reading

1. `AGENTS.md`
2. `docs/current.md`
3. `docs/plan.md`
4. Active task card in `docs/tasks/` if one exists
5. `docs/agents/README.md`
6. `docs/agents/worker-agent.md`
7. `docs/spec.md` when schema or behavior contracts matter
8. Current task related `worker/` files

`docs/archive/` is not default context.

## Allowed Changes

- `worker/`
- Worker tests directly related to the Worker task

## Not Allowed

- Do not modify `backend/`.
- Do not modify `frontend/`.
- Do not modify active docs unless the task explicitly assigns docs updates.
- Do not leak API keys.
- Do not write real API keys or sensitive material into code or docs.
- Do not run real network tests unless the current task explicitly allows it.
- Do not change schema or API contracts without Lead approval and documentation sync.
- Do not handle Figma input, Figma API, Figma MCP, or Playwright rendering unless the current stage and active task explicitly allow that work.

## Output Format

```text
任务结果：
- 任务目标：
- 修改文件：
- Worker 行为变化：
- 验证步骤：
- 验证结果：
- 风险 / 待确认事项：
```
