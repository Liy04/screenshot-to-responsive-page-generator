# Week 15 Day 04

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Generated output must be understandable enough for a user to decide whether to copy, download, retry, or inspect debug data.

## Task Goal

Improve the frontend preview / result comparison UX only as needed to inspect the fixed Week 15 sample set and quality metrics.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-04.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/frontend-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- `docs/engineering-baseline.md`
- Day 01 quality metrics
- Day 02 / Day 03 Worker handoffs
- current frontend MVP page, preview, copy, download, state display, and related tests only
- do not read `docs/archive/` by default

## Write Scope

- Frontend files directly responsible for `/dev/image-to-layout`, original / generated preview, result state, copy / download, or quality comparison display
- Frontend tests or smoke notes if present
- `docs/smoke/week15-quality-smoke.md` only for evidence or blockers if needed
- `docs/current.md` only for handoff status if needed

Forbidden:

- `backend/` unless Lead explicitly retargets to Day 05
- `worker/`
- `schema/`
- `docs/archive/`
- adding an editor, drag-and-drop workflow, multi-page UI, auth, or complex ZIP export
- weakening iframe sandbox or adding `allow-scripts`
- real API keys, credentials, tokens, private screenshots, or sensitive materials
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead should spawn `frontend-agent` for implementation when subagent tools are available.
- Lead should spawn `tester-agent` after frontend code changes for build or manual smoke validation.
- Lead should spawn `reviewer-agent` after code changes for quality, security, and boundary review.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: approve whether frontend UX is needed and keep it limited to comparison / inspection.
- Explorer: optional if frontend ownership is unclear.
- Implementation: `frontend-agent`.
- Tester: `tester-agent`.
- Reviewer: `reviewer-agent`.

## Engineering Baseline

- 是否涉及新文件：可能，only if a focused component or helper is justified.
- 是否涉及新 Controller / Service / component / pipeline：可能涉及 Vue component / helper.
- Pre-write search required：是，search current frontend view, components, API helpers, preview iframe, copy, and download behavior.
- Implementation placement check required：是。
- Existing file to be extended：To be determined after pre-write search.
- Why this belongs in existing file：Must be stated by `frontend-agent` before writing.
- Existing-debt touch decision：Do not refactor historical frontend debt unless it blocks the current comparison UX.
- Reuse / extraction / keep-separate decision：Classify similar UI / helper code and choose reuse, extraction, or keep-separate before writing.
- If extracted, proposed new file：Only a focused component / helper with Lead approval.
- Responsibility boundary：Sample-set preview / result comparison only; no editor or product expansion.
- File size risk：中。
- Test required：是。
- Dependency change：否 by default.
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- The UI helps compare original sample screenshot and generated preview against Week 15 metrics without becoming an editor.
- REAL_AI / FALLBACK / FAILED state remains visible and readable.
- Copy / download actions from Week 14 remain available.
- iframe preview remains strictly sandboxed without `allow-scripts`.
- Debug data remains available without dominating the result flow.
- No multi-page, auth, editor, complex ZIP, or visual-regression platform is introduced.

## Test / Smoke

- Run the narrowest frontend validation available, such as build, page smoke, or manual browser smoke.
- Verify original / generated preview, state display, copy, download, and strict iframe sandbox.
- Record blockers if validation cannot run.

## Stop Conditions

- The UX change requires weakening iframe sandbox safety.
- The task becomes an editor, multi-page workflow, auth, or project export feature.
- API fields needed by the frontend are missing and cannot be added without Lead-approved contract docs.
- Required read / write scope exceeds the allowed files.
- The task requires reading or modifying `docs/archive/`.
- Multiple agents would modify the same directory at the same time.
- Tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Files changed
- Pre-write search result
- Implementation placement decision
- Reuse / extraction decision
- Frontend validation result
- Sandbox check result
- Reviewer findings
- Blockers or risks
- Suggested next handoff: Day 05 Backend artifact metadata / quality fields if needed
