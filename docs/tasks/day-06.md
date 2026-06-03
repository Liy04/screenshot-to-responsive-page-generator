# Week 15 Day 06

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Smoke evidence must prove the minimum upload -> generate -> preview -> copy / download loop, now with fixed sample-set quality checks.

## Task Goal

Run and record the full Week 15 fixed sample-set smoke across the current MVP flow.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-06.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/engineering-baseline.md`
- Day 01 quality metrics
- Day 02-05 handoffs
- current smoke scripts, frontend page, backend API, Worker generation path, and fixtures required to run the smoke
- do not read `docs/archive/` by default

## Write Scope

- `docs/smoke/week15-quality-smoke.md`
- `docs/current.md` only for handoff status if needed
- no business code changes

Forbidden:

- modifying `backend/`
- modifying `frontend/`
- modifying `worker/`
- modifying `schema/`
- modifying `docs/archive/`
- committing generated output, downloaded files, private screenshots, secrets, or runtime artifacts
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead should spawn `tester-agent` for smoke execution when subagent tools are available.
- Lead may spawn `reviewer-agent` after smoke to review evidence quality and remaining risk.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: confirm smoke scope, accept or reject final evidence, and decide whether blockers stop the cycle.
- Explorer: not required unless smoke setup is unclear.
- Implementation: not required; tester does not fix business code.
- Tester: `tester-agent`.
- Reviewer: optional `reviewer-agent` for smoke evidence review.

## Engineering Baseline

- 是否涉及新文件：否 if `docs/smoke/week15-quality-smoke.md` already exists; otherwise the file should have been created on Day 01.
- 是否涉及新 Controller / Service / component / pipeline：否。
- Pre-write search required：是，check existing smoke scripts and records before running or recording.
- Implementation placement check required：否，no business implementation.
- Existing file to be extended：`docs/smoke/week15-quality-smoke.md`.
- Why this belongs in existing file：Week 15 sample-set smoke evidence belongs in the current smoke record.
- Existing-debt touch decision：Do not refactor tests or scripts during smoke unless Lead creates a separate task.
- Reuse / extraction / keep-separate decision：Reuse existing smoke commands and fixtures where possible.
- If extracted, proposed new file：None.
- Responsibility boundary：Smoke execution and evidence recording only.
- File size risk：低。
- Test required：是，this task is the smoke.
- Dependency change：否。
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- Every fixed Week 15 sample has a recorded result.
- Each sample records generation state: REAL_AI / FALLBACK / FAILED.
- Each sample records preview render status, strict iframe sandbox check, quality metric result, copy result, and download result.
- Any failure includes a readable blocker, likely responsible area, and suggested next agent.
- No tester-agent business-code fix is made directly.
- No secrets, private screenshots, generated runtime artifacts, or downloaded files are committed.

## Test / Smoke

Execute the Smoke Plan from `docs/plan.md`:

```text
prepare fixed Week 15 sample set
-> generate each sample through the current MVP path
-> verify REAL_AI / FALLBACK / FAILED state is readable for each sample
-> verify generated preview renders safely in strict sandbox
-> compare output against the sample quality metrics
-> verify copy action still works or reports a readable failure
-> verify download action still creates the expected minimal file
-> verify any quality metadata is present only when needed and documented
-> verify no secret, private screenshot, generated runtime artifact, or out-of-scope file is staged
```

## Stop Conditions

- Smoke requires real API keys or secrets that are not already safely configured in the local environment.
- Smoke would commit private screenshots, generated output, downloaded files, or runtime artifacts.
- Required read / write scope exceeds the allowed files.
- The task requires reading or modifying `docs/archive/`.
- Tester-agent would need to fix business code directly instead of reporting issues.
- Multiple agents would modify the same directory at the same time.

## Handoff Output

- Smoke command / manual steps run
- Sample-by-sample result
- Overall pass / conditional pass / fail
- Validation not run and why, if applicable
- Blockers or risks
- Suggested responsible agent for each failure
- Suggested next handoff: Day 07 closeout
