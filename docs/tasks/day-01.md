# Week 15 Day 01

## Source Bet

- Current single bet from `docs/plan.md`: Sample-set based generated page quality improvement.
- This day card only executes the current single bet. It does not redefine product direction, expand the roadmap, generate Week 16 / Cycle 16 planning, or promote Should / Could items into Must work.

## Related MVP Gap

- Gap from `docs/mvp-roadmap.md`: Generated output must become more understandable and stable enough for a user to decide whether to copy, download, retry, or inspect debug data.

## Task Goal

Define the Week 15 fixed sample set, lightweight quality metrics, and the initial smoke record structure for sample-set based generated page quality improvement.

## Read Scope

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/current.md`
- `docs/mvp-roadmap.md`
- `docs/plan.md`
- current task card: `docs/tasks/day-01.md`
- `docs/tasks/_template.md`
- `docs/agents/README.md`
- `docs/agents/lead.md`
- `docs/agents/docs-agent.md`
- `docs/agents/reviewer-agent.md`
- necessary sample or fixture docs only
- do not read `docs/archive/` by default

## Write Scope

- `docs/current.md`
- `docs/tasks/day-01.md`
- `docs/smoke/week15-quality-smoke.md`
- optional lightweight quality or fixture notes under `docs/quality/` or `docs/samples/` if Lead confirms the entry is missing

Forbidden:

- `backend/`
- `frontend/`
- `worker/`
- `schema/`
- `docs/archive/`
- real API keys, credentials, tokens, private screenshots, or sensitive materials
- Claude Code config, `CLAUDE.md`, `.claude/agents`, Claude Code `/agents`, Custom Subagents, or Agent Teams

## Spawn Decision

- Lead decides whether to spawn `docs-agent` and `reviewer-agent`.
- This task is docs-only; no implementation agent is required.
- If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation before continuing in the main thread.
- Multiple agents must not modify the same directory at the same time.
- Tester-agent and reviewer-agent report issues by default and do not fix business code directly.

## Required Agents

- Lead: confirm sample-set boundaries, accept metrics, and keep the cycle to one bet.
- Explorer: not required unless sample location or fixture ownership is unclear.
- Implementation: not required.
- Tester: not required on Day 01.
- Reviewer: review the sample set, metrics, smoke scaffold, and scope boundaries.
- Docs: create or update the Week 15 quality notes and smoke scaffold.

## Engineering Baseline

- 是否涉及新文件：是，`docs/smoke/week15-quality-smoke.md` and optional docs-only quality notes.
- 是否涉及新 Controller / Service / component / pipeline：否。
- Pre-write search required：是，search existing `docs/smoke/`, `docs/quality/`, and sample fixture docs before adding new docs.
- Implementation placement check required：否，docs-only placement check is enough.
- Existing file to be extended：`docs/smoke/week15-quality-smoke.md` if it already exists.
- Why this belongs in existing file：Week 15 smoke evidence belongs in the current smoke record, not in roadmap or archive.
- Existing-debt touch decision：Do not refactor old smoke records or archive material.
- Reuse / extraction / keep-separate decision：Keep Week 15 smoke separate from Week 12-14 smoke records.
- If extracted, proposed new file：None.
- Responsibility boundary：Sample-set definition and smoke scaffold only; no business implementation.
- File size risk：低。
- Test required：否，docs review is required.
- Dependency change：否。
- Engineering baseline reference：`docs/engineering-baseline.md`

## Acceptance

- Fixed Week 15 sample set is documented with each sample's intent and expected visual / structural traits.
- Lightweight quality metrics are documented and do not promise pixel-perfect or 1:1 fidelity.
- `docs/smoke/week15-quality-smoke.md` exists with fields for every sample, result state, preview safety, copy / download, and pass / fail notes.
- Scope explicitly excludes MySQL, Figma API / MCP, multi-page generation, editor workflows, complex ZIP export, and Week 16 planning.
- No private screenshot, real API key, secret, generated runtime artifact, or out-of-scope file is added.

## Day 01 Result

Status: docs scaffold prepared; implementation smoke not run on Day 01.

Fixed sample set:

| Sample ID | Input | Intent |
|---|---|---|
| W15-S1 Simple card | `samples/01-simple-card-page.png` | Preserve a simple card / content-page hierarchy. |
| W15-S2 Simple form | `samples/02-simple-form-page.png` | Preserve a basic form layout with labels, inputs, and primary action. |
| W15-S3 Dashboard cards | `samples/03-dashboard-cards-page.png` | Preserve repeated dashboard-card grouping and visual hierarchy. |

Quality metrics:

- Documented in `docs/quality/week15-quality.md`.
- Use lightweight `pass` / `partial` / `fail` / `blocked` checks.
- Cover structure, main visual hierarchy, spacing and grouping, typography, component fidelity, responsive sanity, safety, and delivery.
- Explicitly do not promise pixel-perfect or 1:1 fidelity.

Smoke scaffold:

- `docs/smoke/week15-quality-smoke.md` contains one section per fixed sample.
- Each sample section includes generation state, preview rendering, preview safety, strict iframe sandbox, quality metric result, copy result, download result, artifacts check, secrets/private artifact check, result, and pass / fail notes.

Scope exclusions confirmed:

- MySQL persistence.
- Figma API / Figma MCP.
- Multi-page generation.
- Drag-and-drop or online editor workflows.
- Complex ZIP export.
- Week 16 / Cycle 16 planning.
- Pixel-perfect or 1:1 high-fidelity guarantee.

Safety note:

- No private screenshot, real API key, secret, generated runtime artifact, backend / frontend / worker / schema change, Claude Code config, or `docs/archive/` modification is part of Day 01.

## Test / Smoke

- Docs self-check against `docs/plan.md` Must items and Acceptance Criteria.
- Reviewer checks that sample metrics are bounded, testable, and tied to the current single bet.

## Stop Conditions

- The sample set requires private, sensitive, licensed, or secret material.
- The task requires reading or modifying `docs/archive/`.
- The task expands into product direction, persistence, Figma API / MCP, multi-page, editor, or ZIP work.
- Multiple agents would modify the same directory at the same time.
- Tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.

## Handoff Output

- Files changed
- Fixed sample set summary
- Quality metrics summary
- Smoke scaffold location
- Review result
- Blockers or risks
- Suggested next handoff: Day 02 Worker prompt / schema quality constraints
