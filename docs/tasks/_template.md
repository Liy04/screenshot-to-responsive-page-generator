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
  - If extracted, proposed new file：
  - Responsibility boundary：
  - File size risk：低 / 中 / 高
  - Test required：是 / 否
  - Dependency change：是 / 否
  - Engineering baseline reference：docs/engineering-baseline.md

Acceptance:

Test / Smoke:

Stop Conditions:
  - Requested work no longer maps to the Source Bet.
  - Required read / write scope would touch unauthorized files.
  - Multiple agents would modify the same directory at the same time.
  - The task requires reading docs/archive/ without explicit approval.
  - The task requires secrets, real API keys, or sensitive materials.
  - The task would add Claude Code config, CLAUDE.md, or .claude/agents.
  - The task would redefine product direction or expand the roadmap.
  - The task would auto-upgrade Should / Could items into Must work.
  - tester-agent or reviewer-agent would need to fix business code directly instead of reporting issues.
  - New files are required but similar implementations were not searched first.
  - New code clearly copies an existing structure without explaining reuse or extraction.
  - New non-trivial behavior would be added before an implementation placement check.
  - New behavior introduces an independent responsibility but is still directly stuffed into an existing file.
  - Code would be mechanically split into Part1 / Part2 only to reduce line count.
  - A new file would be created without checking nearby existing structure.
  - A file exceeds the baseline threshold without split rationale or a reason to defer.
  - A dependency is added without synchronizing the dependency file.
  - New business behavior has no test, smoke, or unable-to-validate explanation.

Handoff Output:
  - Files changed
  - Acceptance result
  - Test / smoke result
  - Blockers or risks
  - Suggested next handoff
```
