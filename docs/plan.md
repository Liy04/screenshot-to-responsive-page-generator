# Plan

## Current Cycle / Week

Week 14 / Cycle 14.

This file is the current Cycle / Week single-bet plan. It is not the long-term roadmap, candidate backlog, or next-cycle plan.

## Cycle Planning Check

Week 14 was selected from `docs/mvp-roadmap.md`:

- Current MVP Goal: screenshot -> layout recognition -> safe generated preview -> user-takeable output.
- Most blocking MVP gap: the working screenshot-to-preview path still needs a clear copy / download delivery loop.
- Cycle size: one single bet.
- Still-Must from prior work: preserve the working MVP demo path and make result state readable.
- Inertia leftovers: broad output-quality tuning and extra artifact polish are not Week 14 Must work unless they directly block copy / download.
- Later / Won’t This Time: persistence, Figma API / MCP, multi-page, editor workflows, auth, and complex visual regression stay outside this cycle.
- User gain after this cycle: a user can preview, copy, and download the generated result from the MVP flow.
- Reason not to continue prior leftovers: delivery closes the MVP loop more directly than another open-ended quality pass.

## Current Single Bet

Productized MVP delivery loop for screenshot -> generated preview -> copy / download.

## Why This Bet

The project already has a working real-AI screenshot-to-preview path. The current product gap is that users need a clear, demonstrable way to understand, preview, copy, and download the generated result.

This bet keeps Week 14 focused on delivery rather than continuing an open-ended output-quality track.

## Must / Should / Could / Won’t This Time

Must:

- Keep `/dev/image-to-layout` as the active MVP demonstration path.
- Show original screenshot and generated preview in a user-readable result flow.
- Preserve Layout JSON and previewHtml visibility for debugging.
- Show REAL_AI / FALLBACK / FAILED state clearly.
- Provide minimal copy action for generated output.
- Provide minimal download action for generated output.
- Keep iframe preview sandboxed without `allow-scripts`.
- Run and record a minimum MVP smoke.

Should:

- Provide separate HTML / CSS copy actions if current artifacts support it cleanly.
- Add concise user-facing delivery hints after generation succeeds.
- Clarify generated artifact fields in docs if implementation changes the contract.

Could:

- Improve small result-page labels or grouping if it reduces user confusion.
- Add lightweight failure guidance if the existing error state is unclear.

Won’t This Time:

- MySQL persistence.
- Entity / Mapper / MyBatis-Plus tables.
- Figma API / Figma MCP.
- Redis / RabbitMQ.
- Drag-and-drop editor.
- Online editor.
- Complex ZIP export.
- Vue SFC or full project export.
- Multi-page generation.
- Login / registration.
- Permission system.
- Playwright visual regression system.
- Layout JSON v0.2 upgrade.

## Acceptance Criteria

- A user can upload a screenshot and trigger generation.
- A user can see the original image and generated preview.
- A user can identify REAL_AI / FALLBACK / FAILED state.
- A user can copy generated output.
- A user can download a minimal generated file.
- Debug information remains available without dominating the result flow.
- The iframe remains `sandbox=""` and does not use `allow-scripts`.
- No real API key, secret, private screenshot, or generated sensitive artifact is committed.
- No backend storage, frontend build output, or downloaded file artifact is committed.
- No out-of-scope infrastructure or stack change is introduced.

## Smoke Plan

Run one minimum MVP smoke after implementation:

```text
upload sample
-> generate
-> verify REAL_AI / FALLBACK / FAILED state is readable
-> verify iframe preview renders
-> verify copy action works or reports a readable failure
-> verify download action creates the expected minimal file
-> verify iframe sandbox remains strict
-> verify no secret or generated runtime artifact is staged
```

## Exit Criteria

- Must items are complete or explicitly rejected by Lead.
- Acceptance Criteria are checked.
- Smoke Plan is executed, or the exact blocker is recorded.
- Tester and reviewer reports are addressed or accepted as known risk.
- `docs/current.md` points to the active day card or next handoff without planning the next cycle.

## Next Cycle Rule

- The next cycle must not be generated directly from unfinished Week 14 items.
- Unfinished Should / Could items return to the candidate pool by default and do not automatically roll into the next cycle.
- An unfinished Must may enter the next cycle candidate set only if it still blocks the MVP loop.
- Before writing the next cycle plan, Lead must rerun the Cycle Plan Gate in `docs/mvp-roadmap.md` and choose one single bet again.
