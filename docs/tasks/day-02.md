# Week 15 Day 02

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Generated artifact fields and layout output must stay clear enough to support copy, download, and user acceptance.

## Task Goal

Improve Worker prompt and schema output constraints so generated layout is more stable for the fixed Week 15 sample set.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-02.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/worker-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/engineering-baseline.md`
- Day 01 sample-set and quality notes
- current Worker prompt, schema, validator, fallback, repair, and related tests / fixtures only
- do not read `docs/archive/` by default

## Write Scope

- Worker files directly responsible for prompt, schema output constraints, validation, or related tests / fixtures
- `docs/current.md` only for handoff status if needed
- `docs/smoke/week15-quality-smoke.md` only for notes or blockers if needed
- `docs/spec.md` only if Lead approves a contract wording update

Forbidden:

- `backend/` unless Lead explicitly retargets to Day 05
- `frontend/`
- `schema/` unless the active task and Lead approve a minimal contract sync
- `docs/archive/`
- new runtime infrastructure or large dependencies
- real API keys, credentials, tokens, private screenshots, or sensitive materials
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead should spawn `worker-agent` for implementation when subagent tools are available.
- After implementation, Lead should spawn `tester-agent` for minimum Worker validation when code changed.
- After code changes, Lead should spawn `reviewer-agent` for quality, security, and boundary review.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: confirm exact Worker scope and accept any contract implication.
- Explorer: optional if Worker prompt / schema ownership is unclear.
- Implementation: `worker-agent`.
- Tester: `tester-agent` runs the minimum Worker fixture or smoke validation.
- Reviewer: `reviewer-agent` reviews prompt constraints, schema safety, duplication, and scope.

## Engineering Baseline

- 是否涉及新文件：可能，only if a focused fixture or test file is justified.
- 是否涉及新 Controller / Service / component / pipeline：可能涉及 Worker pipeline / helper.
- Pre-write search required：是，search existing Worker prompt, schema, validator, repair, fallback, tests, and fixtures.
- Implementation placement check required：是。
- Existing file to be extended：To be determined after pre-write search.
- Why this belongs in existing file：Must be stated by `worker-agent` before writing.
- Existing-debt touch decision：Do not refactor historical Worker debt unless it blocks the current sample-set quality bet.
- Reuse / extraction / keep-separate decision：Classify similar Worker logic and choose reuse, extraction, or keep-separate before writing.
- If extracted, proposed new file：Only a focused Worker helper / fixture file with Lead approval.
- Responsibility boundary：Prompt and schema output constraints for the fixed sample set only.
- File size risk：中。
- Test required：是。
- Dependency change：否 by default; any dependency change requires Lead approval and dependency-file sync.
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- Worker prompt / schema constraints address the fixed sample-set quality metrics from Day 01.
- Output remains compatible with the current MVP preview, copy, and download flow.
- REAL_AI / FALLBACK / FAILED state behavior is not weakened.
- No broad schema upgrade, Layout JSON v0.2 work, persistence, Figma API / MCP, editor, multi-page, or ZIP feature is introduced.
- Worker tests, fixtures, or smoke notes cover the changed behavior, or the exact validation blocker is recorded.

## Test / Smoke

- Run the narrowest relevant Worker tests or fixture smoke for the changed prompt / schema path.
- If real AI cannot be run, record environment, network, key, or timeout blocker and provide fixture-level validation.
- Update `docs/smoke/week15-quality-smoke.md` only with evidence or blockers, not fabricated pass results.

## Stop Conditions

- Required behavior changes would break the Week 14 delivery loop.
- API contract changes are needed but not approved or documented.
- A new dependency or external service is required.
- The task requires reading or modifying `docs/archive/`.
- The work no longer maps to the Source Bet.
- Multiple agents would modify the same directory at the same time.
- Tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Files changed
- Pre-write search result
- Implementation placement decision
- Reuse / extraction decision
- Worker validation result
- Reviewer findings
- Blockers or risks
- Suggested next handoff: Day 03 Worker repair / normalization quality pass
