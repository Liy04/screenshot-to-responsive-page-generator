# Task Card Template

Day cards execute the current single bet in `docs/plan.md`. They do not redefine product direction, expand the roadmap, or promote Should / Could items into Must work.

If a task discovers a new idea, record it as a Candidate Bet or Later item through the appropriate docs flow. Do not implement it directly from the day card.

```text
Source Bet:
  - Current single bet from docs/plan.md:

Related MVP Gap:
  - Gap from docs/mvp-roadmap.md:

Task Goal:

Read Scope:
  - AGENTS.md
  - docs/INDEX.md
  - docs/current.md
  - docs/mvp-roadmap.md
  - docs/plan.md
  - current task card
  - docs/agents/README.md
  - matching docs/agents/<role>.md
  - current task-related files only
  - do not read docs/archive/ by default

Write Scope:

Spawn Decision:
  - Lead decides whether the task requires subagent spawn.
  - If the user explicitly requests spawn, Lead must spawn when the environment supports it.
  - If subagent tools are unavailable, Lead must state the downgrade reason and ask for confirmation.
  - Day cards execute the current plan; they do not redefine product direction.
  - Day cards do not expand the roadmap.
  - Day cards do not promote Should / Could items into Must work.
  - Multiple agents must not modify the same directory at the same time.

Required Agents:
  - Lead:
  - Explorer:
  - Implementation:
  - Tester:
  - Reviewer:

Engineering Baseline:
  - 是否涉及新文件：
  - 是否涉及新 Controller / Service / component / pipeline：
  - Pre-write search required：是 / 否
  - Implementation placement check required：是 / 否
  - Existing file to be extended：
  - Why this belongs in existing file：
  - Existing-debt touch decision：
  - Reuse / extraction / keep-separate decision：
  - If extracted, proposed new file：
  - Responsibility boundary：
  - File size risk：低 / 中 / 高
  - Test required：是 / 否
  - Dependency change：是 / 否
  - Engineering baseline reference：docs/engineering-baseline.md

Acceptance:

Test / Smoke:

Stop Conditions:

## Hard Stop
  - Secrets, real API keys, credentials, tokens, or sensitive material are required or exposed.
  - Unauthorized docs/archive/ access or modification would be required.
  - Claude Code config, CLAUDE.md, .claude/agents, Claude Code /agents, Custom Subagents, or Agent Teams would be introduced.
  - Requested work no longer maps to the Source Bet, redefines product direction, expands the roadmap, or auto-upgrades Should / Could items into Must work.
  - Required read / write scope exceeds allowed files.
  - Sandbox, iframe safety, or security boundaries would be weakened.
  - API contract would change without docs/spec.md, active task, or Lead approval.

## Lead Decision Required
  - Non-trivial behavior lacks an Implementation Placement Check.
  - Target file already exceeds a size trigger and new non-trivial behavior would be added.
  - Obvious duplication or copy-paste is found.
  - Similar implementation exists but the reuse / extraction / keep-separate decision is unclear.
  - New files are required but similar implementations or nearby structures were not searched first.
  - New behavior introduces an independent responsibility but would still be placed in an existing file.
  - Code would be mechanically split into Part1 / Part2 only to reduce line count.
  - File or function exceeds a baseline trigger without split rationale or a reason to defer.
  - Dependency change requires dependency-file or docs sync.
  - Required tests / smoke cannot be run.
  - Multiple agents would touch the same directory.
  - tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.
  - New Controller / Service / Worker behavior lacks a test plan, fixture, smoke, or validation note.
  - New business behavior has no test, smoke, or unable-to-validate explanation.

## Report in Handoff
  - Pre-write search result.
  - Implementation placement decision.
  - Existing-debt touch decision.
  - Reuse / extraction decision.
  - Split rationale.
  - Test gaps.
  - Validation not run and why.
  - Dependency changes.
  - Tech debt recorded.

Handoff Output:
  - Files changed
  - Acceptance result
  - Test / smoke result
  - Blockers or risks
  - Suggested next handoff
```
