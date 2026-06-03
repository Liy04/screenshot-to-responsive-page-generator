# Week 15 Day 05

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Generated artifact fields for HTML / CSS must stay clear enough to support copy and download without expanding into full project export.

## Task Goal

Add minimal backend artifact metadata / quality fields only if Day 02-04 prove they are needed for the current fixed sample-set quality checks.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-05.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/backend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/engineering-baseline.md`
- Day 01 quality metrics
- Day 02-04 handoffs
- current backend endpoint / DTO / service files directly involved in generated artifact response only
- `docs/spec.md` if API contract wording is needed
- do not read `docs/archive/` by default

## Write Scope

- No-op docs note if backend change is not needed
- Backend DTO / service / controller files directly responsible for generated artifact metadata only if Lead approves
- Backend tests for changed API behavior
- `docs/spec.md` only for minimal approved contract sync
- `docs/smoke/week15-quality-smoke.md` only for evidence or blockers if needed
- `docs/current.md` only for handoff status if needed

Forbidden:

- MySQL persistence
- Entity / Mapper / MyBatis-Plus tables
- database schema or migration work
- `frontend/` unless Lead explicitly creates a follow-up task
- `worker/` unless Lead explicitly creates a follow-up task
- `docs/archive/`
- auth, permissions, history, multi-page, editor, or ZIP export
- real API keys, credentials, tokens, private screenshots, or sensitive materials
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead first decides whether backend work is actually needed; no-op is valid if current contracts already support the quality checks.
- If backend change is needed and subagent tools are available, Lead should spawn `backend-agent`.
- Lead should spawn `tester-agent` after backend code changes for API or service validation.
- Lead should spawn `reviewer-agent` after code changes for quality, security, and boundary review.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: decide no-op vs minimal backend metadata change.
- Explorer: optional if API ownership is unclear.
- Implementation: `backend-agent` only if approved.
- Tester: `tester-agent` only if backend code changes.
- Reviewer: `reviewer-agent` after backend code changes or for no-op boundary review if requested.

## Engineering Baseline

- 是否涉及新文件：可能，only for focused backend tests or DTO if search proves no existing fit.
- 是否涉及新 Controller / Service / component / pipeline：可能涉及 existing Controller / Service / DTO; new Controller is not expected.
- Pre-write search required：是，search existing backend Controller, Service, DTO, response wrapper, exception handling, and tests.
- Implementation placement check required：是。
- Existing file to be extended：To be determined after pre-write search.
- Why this belongs in existing file：Must be stated by `backend-agent` before writing.
- Existing-debt touch decision：Do not refactor historical backend debt unless it blocks the minimal metadata change.
- Reuse / extraction / keep-separate decision：Classify similar DTO / mapping / response logic and choose reuse, extraction, or keep-separate before writing.
- If extracted, proposed new file：Only a focused DTO / mapper / test file with Lead approval.
- Responsibility boundary：Minimal artifact metadata / quality fields only; no persistence or export expansion.
- File size risk：中。
- Test required：是 if code changes; no-op requires a validation note.
- Dependency change：否。
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- Lead decision is explicit: no backend change needed, or minimal approved metadata / quality fields added.
- If added, metadata fields are tied to the fixed sample-set quality checks and documented.
- Existing upload -> generate -> preview -> copy / download flow remains compatible.
- No MySQL, Entity, Mapper, migration, persistence, auth, editor, multi-page, or ZIP feature is introduced.
- Backend tests, API smoke, or unable-to-run explanation is recorded for any code change.

## Test / Smoke

- If no backend change: record why the existing contract is sufficient.
- If backend changes: run the narrowest backend API / service tests or smoke.
- Verify no database or persistence requirement was introduced.

## Stop Conditions

- Quality metadata would require persistence, schema migration, MySQL, or MyBatis-Plus work.
- API contract changes are broader than the current sample-set quality checks.
- Required docs/spec sync is needed but not approved.
- Required read / write scope exceeds the allowed files.
- The task requires reading or modifying `docs/archive/`.
- Multiple agents would modify the same directory at the same time.
- Tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Backend needed: yes / no
- Files changed
- Pre-write search result
- Implementation placement decision
- API contract note
- Test / smoke result
- Reviewer findings
- Blockers or risks
- Suggested next handoff: Day 06 full sample-set smoke

## Day 05 Result

- Backend needed: no.
- Files changed: none for backend code.
- API contract note: the existing `/api/image-page/jobs/{jobId}/generate` response already exposes the fields needed for Day 06 fixed sample-set smoke and the Day 04 quality panel: `status`, `sourceType`, `fallbackUsed`, `fallbackReason`, `promptVersion`, `layoutJson`, `previewHtml`, `validation`, `warnings`, `errors`, and `artifact`.
- Existing fields sufficient: yes.
- Reason: Week 15 quality metrics are recorded as human-readable smoke evidence, not machine-readable backend quality scores. Adding backend quality fields now would expand the API contract without a current single-bet need.
- Test / smoke result: no backend code changed; Day 06 should verify the existing fields through full fixed sample-set smoke.
- Reviewer findings: no backend technical blocker; reviewer requested this explicit no-op note.
- Next handoff: Day 06 full sample-set smoke.
