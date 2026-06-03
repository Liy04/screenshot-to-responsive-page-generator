# Week 15 Day 03

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Generated output must be understandable enough for a user to decide whether to copy, download, retry, or inspect debug data.

## Task Goal

Add or improve a bounded Worker repair / normalization quality pass for common fixed-sample issues discovered in Day 01 and Day 02.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-03.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/worker-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/engineering-baseline.md`
- Day 01 quality metrics
- Day 02 Worker handoff
- current Worker repair, normalization, validator, compiler, tests, and fixtures only
- do not read `docs/archive/` by default

## Write Scope

- Worker repair / normalization / validation files directly tied to the fixed sample set
- Worker tests or fixtures for the repair / normalization behavior
- `docs/smoke/week15-quality-smoke.md` only for evidence or blockers if needed
- `docs/current.md` only for handoff status if needed

Forbidden:

- `backend/`
- `frontend/`
- `schema/` unless Lead approves a minimal contract sync
- `docs/archive/`
- broad Worker refactors unrelated to the fixed sample set
- real API keys, credentials, tokens, private screenshots, or sensitive materials
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead should spawn `worker-agent` for implementation when subagent tools are available.
- Lead should spawn `tester-agent` after code changes for the narrowest relevant validation.
- Lead should spawn `reviewer-agent` after code changes for quality, security, and boundary review.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: approve the exact repair / normalization target and reject broad quality drift.
- Explorer: optional if repair ownership is unclear.
- Implementation: `worker-agent`.
- Tester: `tester-agent`.
- Reviewer: `reviewer-agent`.

## Engineering Baseline

- 是否涉及新文件：可能，only for a focused helper, fixture, or test with search evidence.
- 是否涉及新 Controller / Service / component / pipeline：可能涉及 Worker pipeline / helper.
- Pre-write search required：是，search existing repair, normalization, validation, compiler, and fixture patterns.
- Implementation placement check required：是。
- Existing file to be extended：To be determined after pre-write search.
- Why this belongs in existing file：Must be stated by `worker-agent` before writing.
- Existing-debt touch decision：Do not refactor historical Worker debt unless Lead approves it as required for the current repair.
- Reuse / extraction / keep-separate decision：Classify similar logic and choose reuse, extraction, or keep-separate before writing.
- If extracted, proposed new file：Only a focused Worker helper / test fixture with Lead approval.
- Responsibility boundary：Repair / normalize fixed-sample layout quality issues only.
- File size risk：中。
- Test required：是。
- Dependency change：否 by default.
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- Repair / normalization handles named fixed-sample issues from Day 01 / Day 02.
- The pass is deterministic enough for smoke comparison and does not hide FAILED state.
- Existing previewHtml safety and copy / download compatibility are preserved.
- No broad visual-regression platform, schema overhaul, persistence, Figma API / MCP, multi-page, editor, or ZIP feature is introduced.
- Tests, fixtures, or smoke notes cover the changed repair / normalization behavior.

## Test / Smoke

- Run relevant Worker tests, fixture checks, or targeted smoke for each repaired / normalized issue.
- Record any unable-to-run reason and the alternative validation used.
- Do not record full Week 15 pass until Day 06.

## Stop Conditions

- The repair would mask invalid or unsafe output instead of reporting a readable failure.
- The task requires a broad schema rewrite or Layout JSON v0.2 upgrade without Lead approval.
- Required read / write scope exceeds the allowed files.
- The task requires reading or modifying `docs/archive/`.
- Multiple agents would modify the same directory at the same time.
- Tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Files changed
- Pre-write search result
- Implementation placement decision
- Existing-debt touch decision
- Reuse / extraction decision
- Test / smoke result
- Reviewer findings
- Blockers or risks
- Suggested next handoff: Day 04 Frontend preview / result comparison UX
