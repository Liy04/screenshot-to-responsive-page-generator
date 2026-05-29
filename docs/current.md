# Current

## Current Cycle / Week

Week 14 / Cycle 14.

## Current Status

The active cycle plan is `docs/plan.md`.

Current single bet: productized MVP delivery loop for screenshot -> generated preview -> copy / download.

Week 14 Day 06 MVP smoke passed and is recorded in `docs/smoke/week14-mvp-smoke.md`.

Week 14 Day 07 docs-only closeout is complete: the productized MVP delivery loop is marked as passed for the current cycle, with the next handoff moving to Lead / Git closeout.

## Active Gate

Every active day card must map to the current single bet, its Must items, and its acceptance criteria in `docs/plan.md`.

New cycle planning belongs in `docs/mvp-roadmap.md` and `docs/plan.md`, not in this file.

## Current Task / Day Card

Use the active `docs/tasks/day-xx.md` card when present.

Latest active day card: `docs/tasks/day-07.md`.

Day 07 closeout does not create a Week 15 / Cycle 15 plan.

## Blockers

- Real AI smoke may depend on external model service, network, configured environment variables, and longer timeouts.
- If copy / download requires artifact fields that do not exist yet, the contract must be clarified inside the current single bet instead of expanding the roadmap.

## Latest Verified Facts

- Week 13 completed the prior output-quality stabilization work.
- Week 14 is focused on delivery-loop productization, not long-term roadmap planning.
- Week 14 Day 06 smoke completed upload, REAL_AI generation, preview, copy, download, safety checks, and service cleanup.
- Week 14 MVP productized delivery loop is accepted as passed based on the recorded smoke and current plan acceptance criteria.
- `docs/archive/` is not default context for current work.

## Next Handoff

Lead / Git closeout should review the final docs diff, preserve existing uncommitted docs changes, and stage / commit intentionally if accepted.

Before any future Week 15 / Cycle 15 planning, Lead must rerun the Cycle Plan Gate from `docs/mvp-roadmap.md`; this file does not carry roadmap candidates or next-cycle plans.
