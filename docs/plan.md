# Plan

## Current Cycle / Week

Week 15 / Cycle 15.

This file is the current Cycle / Week single-bet plan. It is not the long-term roadmap, candidate backlog, or next-cycle plan.

## Cycle Planning Check

Week 15 was selected from `docs/mvp-roadmap.md` through the Cycle Plan Gate:

1. Current MVP Goal: screenshot -> layout recognition -> safe generated preview -> user-takeable output.
2. Most blocking MVP gap: after Week 14, the MVP delivery loop can be demonstrated, but generated pages still need a fixed-sample quality pass so output is more similar to the input and easier to accept.
3. Cycle size: one single bet.
4. Still-Must from prior work: preserve the Week 14 upload -> generate -> preview -> copy / download loop and strict iframe sandbox while improving quality.
5. Inertia leftovers: unfinished Week 14 Should / Could details do not automatically roll into Week 15.
6. Later / Won't This Time: persistence, Figma API / MCP, multi-page generation, editor workflows, auth, complex ZIP export, and complex visual regression stay outside this cycle.
7. User gain after this cycle: a user can run the same fixed sample set and see generated pages that more consistently resemble the input pages, with documented quality checks.
8. Reason not to continue Week 14 leftovers: Week 14 closed delivery mechanics; Week 15 improves the trustworthiness of the delivered output on a bounded sample set instead of expanding features.

## Current Single Bet

Sample-set based generated page quality improvement.

## Why This Bet

The MVP loop is now usable enough to upload a screenshot, generate a preview, inspect state, copy output, and download a minimal file. The next user-facing gap is confidence: generated pages must look closer to the input page and fail in predictable, reviewable ways.

This bet keeps the quality work bounded by a fixed sample set and measurable acceptance notes. It is not a general visual-regression platform, not a multi-page exporter, and not an editor.

## Must / Should / Could / Won't This Time

Must:

- Define a small fixed sample set for Week 15 quality work, including expected page traits for each sample.
- Define lightweight quality metrics that can be checked by humans and smoke scripts without promising 1:1 fidelity.
- Improve Worker prompt / schema output constraints so generated layout is more stable for the fixed sample set.
- Add or improve Worker repair / normalization quality pass for common fixed-sample issues.
- Preserve `/dev/image-to-layout` as the active MVP demonstration path.
- Preserve REAL_AI / FALLBACK / FAILED state visibility.
- Preserve copy / download delivery actions from Week 14.
- Preserve strict iframe preview sandbox without `allow-scripts`.
- Run and record a full fixed-sample smoke.

Should:

- Add frontend preview/result comparison UX only when it helps inspect the fixed sample set.
- Add backend artifact metadata / quality fields only if the frontend or smoke needs them for the current sample-set quality checks.
- Keep quality notes readable enough for Lead, tester-agent, and reviewer-agent to agree on pass / fail.

Could:

- Add small per-sample notes for known acceptable deviations.
- Add a lightweight retry or repair reason label if it already fits the current contracts.

Won't This Time:

- MySQL persistence.
- Entity / Mapper / MyBatis-Plus tables.
- Figma API / Figma MCP.
- Redis / RabbitMQ.
- Drag-and-drop editor.
- Online editor.
- Complex ZIP export.
- Full project export.
- Multi-page generation.
- Login / registration.
- Permission system.
- Complex visual regression platform.
- Pixel-perfect or 1:1 high-fidelity guarantee.
- Layout JSON v0.2 upgrade unless required by the fixed sample-set quality pass and approved by Lead.
- Replacing the default stack.

## Acceptance Criteria

- Week 15 fixed sample set is documented with sample intent, expected visual / structural traits, and out-of-scope traits.
- Quality metrics are documented and map to the fixed sample set.
- Worker output for the fixed sample set is more stable in structure, spacing, typography, and main visual hierarchy based on the agreed checks.
- Generated preview remains safe and inspectable through the existing MVP flow.
- Copy / download behavior remains available after quality changes.
- REAL_AI / FALLBACK / FAILED state remains visible.
- If artifact metadata / quality fields are added, they are minimal, documented, and used by the current flow.
- Full fixed-sample smoke is executed and recorded in `docs/smoke/week15-quality-smoke.md`, or the exact blocker is recorded.
- No real API key, secret, private screenshot, or sensitive generated artifact is committed.
- No backend storage, frontend build output, generated download artifact, or private sample screenshot is committed.
- No out-of-scope infrastructure, stack change, editor, persistence, Figma API / MCP, multi-page, or complex ZIP feature is introduced.

## Smoke Plan

Run one full fixed-sample smoke after implementation:

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

Smoke record: `docs/smoke/week15-quality-smoke.md`.

## Exit Criteria

- Must items are complete or explicitly rejected by Lead.
- Acceptance Criteria are checked.
- Full fixed-sample Smoke Plan is executed, or the exact blocker is recorded.
- Tester and reviewer reports are addressed or accepted as known risk.
- `docs/current.md` points to the active day card or next handoff without planning Week 16 / Cycle 16.

## Week 15 Closeout Status

- Result: pass with known risks.
- Date: 2026-06-01.
- Evidence: `docs/smoke/week15-quality-smoke.md` records the post-fix full fixed-sample retest.
- Smoke outcome: Worker unittest discover passed 91 tests; frontend `ImageToLayoutDev` passed 11 tests; backend `mvn test` passed 45 tests; `mvn package -DskipTests` passed; Worker smoke passed; API REAL_AI smoke passed for W15-S1, W15-S2, and W15-S3; W15-S2 Chrome headless page smoke passed.
- Quality outcome: W15-S2 form fidelity blocker is fixed with semantic form / input / button output; W15-S1 and W15-S3 showed no API, preview, or quality regression in the retest.
- Review outcome: reviewer-agent final review passed with no Blocker, Major, or Minor findings.
- Accepted risks: REAL_AI latency remains variable and needed a 420 second Worker timeout after a 180 second timeout returned 504; headless copy can fail because of clipboard permissions but reports a readable failure and download succeeds; ignored `frontend/dist` build output may exist locally and must not be submitted.
- Scope guard: no Week 16 / Cycle 16 plan is created here, and unfinished Should / Could items are not rolled forward automatically.

## Next Cycle Rule

- The next cycle must not be generated directly from unfinished Week 15 items.
- Unfinished Should / Could items return to the candidate pool by default and do not automatically roll into the next cycle.
- An unfinished Must may enter the next cycle candidate set only if it still blocks the MVP loop.
- Before writing the next cycle plan, Lead must rerun the Cycle Plan Gate in `docs/mvp-roadmap.md` and choose one single bet again.
