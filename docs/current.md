# Current

## Current Cycle / Week

Week 15 / Cycle 15.

## Current Status

The active cycle plan is `docs/plan.md`.

Current single bet: Sample-set based generated page quality improvement.

Week 15 Day 07 docs-only closeout is ready to pass with known risks. Day 06 post-fix smoke evidence shows the fixed sample-set quality pass is complete enough for the Week 15 single bet.

Week 15 remains closed around the fixed sample set only. Week 16 / Cycle 16 planning has not been generated.

## Active Gate

Every active day card must map to the Week 15 single bet, its Must items, and its acceptance criteria in `docs/plan.md`.

Day cards execute the current plan only. They do not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 plans, or promote Should / Could items into Must work.

## Current Task / Day Card

Day 07 closeout is recorded in `docs/tasks/day-07.md`.

Current handoff: Lead may proceed with Git closeout for Week 15, or wait for the user to decide the next cycle. Do not create Week 16 / Cycle 16 planning from this handoff.

## Blockers

- Real AI smoke may depend on external model service, network, configured environment variables, and longer timeouts.
- Fixed sample screenshots or fixtures must not include private, sensitive, licensed, or secret material.
- If quality metadata requires API contract changes, the change must stay minimal and be documented before implementation continues.
- If the runtime lacks subagent tools, Lead must state the downgrade reason and ask for confirmation instead of silently role-playing required agents.

## Latest Verified Facts

- Week 14 completed the productized MVP delivery loop for upload -> generate -> preview -> copy / download.
- Week 15 is a bounded quality cycle based on a fixed sample set.
- Week 15 fixed samples are `samples/01-simple-card-page.png`, `samples/02-simple-form-page.png`, and `samples/03-dashboard-cards-page.png`.
- Week 15 lightweight quality metrics are documented in `docs/quality/week15-quality.md` and do not promise pixel-perfect or 1:1 fidelity.
- Week 15 smoke scaffold is `docs/smoke/week15-quality-smoke.md`.
- The active MVP path remains `/dev/image-to-layout`.
- Day 02 and Day 03 Worker changes completed prompt/schema constraints and bounded repair / normalization.
- Day 04 frontend comparison UX passed frontend tests, build, and review after sourceUrl empty-state repair.
- Day 05 backend assessment concluded no backend metadata change is needed; the existing generate response is sufficient for Week 15 quality smoke.
- Day 06 initial smoke ran all three fixed samples through API and `/dev/image-to-layout`; W15-S1 and W15-S3 passed, while W15-S2 initially failed form component fidelity because the generated form section rendered as plain text rows.
- After worker-agent's targeted repair to `worker/layout_quality_repair.py` and `worker/test_image_layout_pipeline.py`, the post-fix tester retest passed Worker unittest discover (91 tests), frontend `ImageToLayoutDev` tests (11 tests), backend `mvn test` (45 tests), `mvn package -DskipTests`, Worker smoke, API REAL_AI smoke for W15-S1/W15-S2/W15-S3, and W15-S2 Chrome headless page smoke.
- W15-S2 form fidelity blocker is fixed in the retest: REAL_AI output now contains a semantic form with recognizable `input` and `button` controls (`layoutFormCount=1`, `layoutInputCount=2`, `layoutButtonCount=4`).
- W15-S1 and W15-S3 showed no API / preview / quality regression in the retest.
- Reviewer-agent final evidence review passed with no Blocker, Major, or Minor findings.
- Real AI latency remains variable; the first 180 second timeout attempt returned 504, and the successful full retest used a 420 second Worker timeout.
- Headless Chrome copy can fail because of clipboard permission, but the UI reports a readable failure and download succeeded.
- `frontend/dist` may exist locally as ignored build output and should not be submitted.
- Strict iframe sandbox must be preserved without `allow-scripts`.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.
- Multiple agents must not modify the same directory at the same time.
- `docs/archive/` is not default context for current work.

## Next Handoff

Lead can perform Week 15 Git closeout or wait for the user to choose the next cycle direction.

Do not create Week 16 / Cycle 16 planning from this file.
