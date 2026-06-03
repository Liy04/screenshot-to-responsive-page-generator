# Week 15 Day 07

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Fixed sample-set quality work must produce a clear pass / fail handoff for the MVP loop without becoming a new roadmap.

## Task Goal

Close Week 15 by summarizing the fixed sample-set quality results, smoke evidence, accepted risks, and next handoff. Do not generate Week 16 / Cycle 16 planning.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-07.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/engineering-baseline.md`
- `docs/smoke/week15-quality-smoke.md`
- Day 01-06 handoffs
- necessary current task-related docs only
- do not read `docs/archive/` by default

## Write Scope

- `docs/current.md`
- `docs/plan.md` only for Week 15 closeout status after Lead acceptance
- `docs/tasks/day-07.md`
- `docs/smoke/week15-quality-smoke.md` only for final evidence notes if needed

Forbidden:

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- `docs/archive/` unless Lead explicitly authorizes a separate archive task
- Week 16 / Cycle 16 plan generation
- real API keys, credentials, tokens, private screenshots, or sensitive materials
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead should spawn `docs-agent` for closeout docs when subagent tools are available.
- Lead should spawn `reviewer-agent` to review Week 15 evidence and scope boundaries.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: decide pass / conditional pass / fail and final handoff.
- Explorer: not required.
- Implementation: not required.
- Tester: not required unless Day 06 evidence is incomplete.
- Reviewer: `reviewer-agent`.
- Docs: `docs-agent`.

## Engineering Baseline

- 是否涉及新文件：否 by default.
- 是否涉及新 Controller / Service / component / pipeline：否。
- Pre-write search required：否，docs closeout only; read current smoke and handoffs.
- Implementation placement check required：否。
- Existing file to be extended：`docs/current.md`, `docs/plan.md`, and `docs/tasks/day-07.md`.
- Why this belongs in existing file：Current status and cycle closeout belong in active docs, not roadmap or archive.
- Existing-debt touch decision：Do not rewrite old task cards or archive records.
- Reuse / extraction / keep-separate decision：Keep Week 15 closeout in active docs unless Lead creates a separate archive task.
- If extracted, proposed new file：None.
- Responsibility boundary：Closeout summary and next handoff only; no new planning.
- File size risk：低。
- Test required：否，review of smoke evidence is required.
- Dependency change：否。
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- Week 15 result is marked as pass / conditional pass / fail based on `docs/plan.md` Acceptance Criteria and Day 06 smoke evidence.
- `docs/current.md` reflects one-screen live state and next handoff.
- `docs/plan.md` records Week 15 closeout status only after Lead acceptance.
- Any open risks are listed without creating Week 16 / Cycle 16 plans.
- No backend, frontend, worker, schema, archive, Claude Code config, secret, or runtime artifact is modified.

## Test / Smoke

- Review Day 06 smoke evidence.
- Reviewer checks that Week 15 stayed within the fixed sample-set quality bet.
- Lead checks that unfinished Should / Could items are not automatically rolled forward.

## Stop Conditions

- Closeout would require business-code fixes.
- Evidence is too incomplete to decide pass / conditional pass / fail.
- The task requires reading or modifying `docs/archive/` without explicit approval.
- The task starts generating Week 16 / Cycle 16 planning.
- Multiple agents would modify the same directory at the same time.
- Tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Week 15 summary
- Files changed
- Smoke result
- Review result
- Cycle result: pass / conditional pass / fail
- Accepted risks
- Next handoff, without Week 16 / Cycle 16 planning

## Day 07 Result

- Status: complete.
- Cycle result: pass with known risks.
- Evidence reviewed: `docs/smoke/week15-quality-smoke.md` post-fix retest and current Week 15 closeout facts.
- Smoke result accepted: W15-S1, W15-S2, and W15-S3 passed the fixed sample-set smoke after the W15-S2 form fidelity repair.
- Review result accepted: reviewer-agent final review passed with no Blocker, Major, or Minor findings.
- Week 16 / Cycle 16 planning: not generated.

## Closeout Notes

- Day 06 initial smoke found W15-S2 form component fidelity failed because generated form content rendered as plain text rows.
- worker-agent's targeted repair to `worker/layout_quality_repair.py` and `worker/test_image_layout_pipeline.py` was retested successfully.
- Post-fix tester evidence passed Worker unittest discover (91 tests), frontend `ImageToLayoutDev` tests (11 tests), backend `mvn test` (45 tests), `mvn package -DskipTests`, Worker smoke, API REAL_AI smoke for W15-S1/W15-S2/W15-S3, and W15-S2 Chrome headless page smoke.
- W15-S2 now renders a semantic form with recognizable `input` and `button` controls; W15-S1 and W15-S3 showed no API / preview / quality regression.
- Accepted risks: REAL_AI latency remains variable and may need longer timeout; headless copy can fail because of clipboard permission while reporting a readable failure; download succeeded; ignored `frontend/dist` build output may exist locally and should not be submitted.

## Final Handoff

Lead may proceed with Week 15 Git closeout or wait for the user to decide the next cycle direction.

Do not create Week 16 / Cycle 16 planning from this Day 07 closeout.
