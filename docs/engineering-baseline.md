# Engineering Baseline

## Purpose

This file defines the minimum engineering quality baseline that AI agents must follow before writing code, while writing code, and during review. It does not replace `docs/mvp-roadmap.md`, `docs/plan.md`, or `docs/spec.md`.

The baseline mainly applies to new code and code touched by the current task. Historical large files or duplicated code should be recorded as tech debt during ordinary tasks, not automatically refactored, unless the current single bet or Lead explicitly requires it.

## 1. Pre-write Search

Before creating any new Controller, Service, DTO, util, component, composable, pipeline, helper, or test, search for similar structures in the project.

- If a similar implementation exists, prefer reuse, extraction of shared logic, or a short explanation of why reuse is not appropriate.
- Do not copy large similar blocks without explanation.
- Before adding a new file, the output must state the search keywords or paths, similar files found, and why the task creates a new file or reuses existing code.

## Reuse and Extraction Decision

After similar implementations are found, an agent must not stop at "found similar file" and continue copying. The handoff must classify the similarity and state the reuse decision.

Similarity classifications:

1. Same workflow, different names only: prefer reuse or extract a focused shared helper / service.
2. Same orchestration shape but different domain rules: keep domain logic separate and extract only stable shared utilities.
3. Same error handling / mapping / validation: extract a mapper, validator, exception helper, or unified handling path.
4. Superficial similarity only: do not abstract; explain why keeping the code separate is acceptable.

Do not create an abstract base class, vague common util, or `common/` bucket only to reduce repeated lines. Shared code must have a clear name, stable responsibility, and at least one current real call site, unless Lead explicitly approves it as a reuse point.

The handoff must include:

- Searched files or keywords.
- Similarity classification.
- Decision: reuse, extract, or keep separate.
- Reason for the decision.

## 2. Implementation Placement and Responsibility-based Splitting

Before adding any non-trivial behavior, run an Implementation Placement Check.

The check must decide whether the behavior belongs in an existing file or should become a new component, composable, service, helper, pipeline stage, test fixture, or equivalent focused structure.

Use these primary criteria:

- Responsibility: does the behavior belong to the same responsibility as the existing file?
- Cohesion: will the existing file remain easier to understand with this behavior included?
- Reuse: is the behavior likely to be reused by another view, service, pipeline, or test?
- Change reason: will this behavior usually change for the same reason as the existing file?
- Testability: can the behavior be tested clearly where it is placed?

Do not wait for a file to exceed a size threshold before considering extraction. Do not mechanically split code by line count into `Part1`, `Part2`, or similar fragments. A split should create a clearer responsibility boundary, not only reduce line count.

Line count is a smell detector and review trigger, not the main splitting rule.

Secondary size triggers:

- Vue view over 300 lines.
- Java Controller or Service over 300 lines.
- Python pipeline over 500 lines.
- Single function or method over 80 lines.

When a touched file or new code crosses a secondary trigger, reconsider the placement and split rationale. If it is not split now, explain why the current responsibility boundary is still acceptable and where any follow-up tech debt is recorded.

## Existing Debt Touch Policy

Historical large files, historical duplicated code, and historical technical debt are not automatically refactored during ordinary tasks. Record them as tech debt unless the active task, current single bet, or Lead explicitly asks for refactoring.

If the current task touches a target file that already exceeds a size trigger, an implementation agent must not default to adding non-trivial behavior to that file. Before writing, the agent must output a placement decision that states one of:

- The new behavior still belongs in the current file, with the responsibility and change reason explained.
- The task should first extract or split specific responsibilities.
- The change is a small local modification that does not add responsibility.

Lead must decide before implementation continues. Lead may:

- Allow the small local modification.
- Spawn a separate refactor task first.
- Defer the requested feature.
- Record the debt and explicitly approve continuing in the current file.

Without explicit Lead approval, do not add a new workflow, API call, UI section, pipeline stage, or side effect to an already over-threshold file.

## 3. Backend Baseline

- Before creating a Controller, Service, DTO, exception, or util, search existing backend structures.
- Prefer reuse of existing Controller, Service, exception handler, and DTO patterns.
- Controllers should not add local `@ExceptionHandler` by default.
- Exception handling should prefer unified `@ControllerAdvice` or `GlobalExceptionHandler`.
- Server errors should use the project unified exception type when available; do not casually use `IllegalStateException` instead of a business exception.
- New Controllers need corresponding tests or an explicit explanation.
- New Service core methods need tests or smoke evidence.
- Do not change API contracts unless `docs/spec.md` or the active task card explicitly allows it.

## 4. Frontend Baseline

- Continue using Vue3 + Vite + JavaScript. Do not migrate to TypeScript during ordinary tasks.
- Before creating a view, component, composable, or API helper, search existing frontend structures.
- Large views should be split into child components or composables when practical.
- For complex API response structures, use lightweight compensation such as JSDoc typedefs, Prop validation, response normalizers, or small helpers.
- Do not bypass iframe sandbox safety.
- Do not add `allow-scripts` to iframe previews unless the active task explicitly allows it.
- New UI behavior needs minimum manual smoke, test, or a clear validation note.

## 5. Worker Baseline

- Before creating a pipeline, helper, or client, search existing Worker modules.
- Pipelines over the threshold should consider splitting.
- New Python dependencies must be synchronized to `requirements.txt`.
- If no dependency is added, say so in the output.
- New Worker behavior needs a test, fixture, smoke check, or an explanation.
- New parameters, environment variables, or external dependencies must be synchronized to `README.md`, `docs/spec.md`, or the relevant docs.

## 6. Test Baseline

- New Controllers default to corresponding tests.
- New Service core methods default to tests.
- New frontend behavior defaults to a test, build check, or manual smoke.
- New Worker behavior defaults to a test, fixture, or smoke.
- If tests cannot be run, explain the reason, impact, and alternative validation.
- Missing tests must not be silently accepted; report the gap so Lead can decide whether it blocks the task.

## 7. Review Baseline

`reviewer-agent` must check:

- Whether the implementation searched before writing.
- Whether non-trivial new behavior had an Implementation Placement Check.
- Whether touched over-threshold files had an Existing Debt Touch Policy decision before non-trivial behavior was added.
- Whether new behavior was placed by responsibility, cohesion, reuse, change reason, and testability rather than by line count.
- Whether similar implementations were classified and resolved with a reuse / extraction / keep-separate decision.
- Obvious duplication or copy-paste.
- Giant files or functions and missing split rationale.
- Missing tests, build checks, smoke, or validation notes.
- Scattered local Controller exception handling.
- New dependencies without dependency-file synchronization.
- Sandbox, security, or API contract violations.
- Whether Should or Could work was upgraded into Must work without approval.
- Any touch to `docs/archive/` or Claude Code configuration.

## 8. Tooling Baseline

Must:

- Keep existing build and test commands explainable and reproducible.
- Synchronize new dependencies to dependency files.
- Every task output must state validation performed or why validation was not run.

Should:

- Gradually add frontend lint or format coverage.
- Gradually add stable backend test commands.
- Gradually add Worker `requirements.txt` and test entry points.
- Future GitHub Actions may provide minimum lint and test checks.

Later:

- Docker or docker-compose.
- Full CI/CD.
- Full type migration.
- Complex quality gates.
