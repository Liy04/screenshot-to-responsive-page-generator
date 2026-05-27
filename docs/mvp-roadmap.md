# MVP Roadmap

## Product Goal

Build a generator that turns a page screenshot or approved Figma design information into runnable, maintainable, iterative responsive frontend page code.

The MVP starts with screenshot input:

```text
real screenshot
-> AI-recognized page structure
-> Layout JSON v0.1
-> safe previewHtml
-> user-takeable page code / files
```

## Desired Outcome

A user can complete one minimal product loop:

1. Upload a real page screenshot.
2. Generate structured layout information.
3. Preview the generated page safely.
4. Understand whether the result came from REAL_AI, FALLBACK, or FAILED.
5. Copy or download the generated output.

## MVP Scope

- Screenshot upload.
- Real AI layout recognition.
- Layout JSON v0.1.
- Worker static compilation to preview HTML.
- Frontend preview with original image and generated result.
- User-readable generation state and failure reason.
- Minimal copy / download delivery path.
- Smoke evidence for the end-to-end MVP loop.
- No API key, secret, private screenshot, account data, or sensitive page content in Git.

## MVP Gap Pool

- The current screenshot-to-preview path must become a user-takeable delivery loop, not only a debug demo.
- Generated output must be understandable enough for a user to decide whether to copy, download, retry, or inspect debug data.
- Smoke evidence must prove the minimum upload -> generate -> preview -> copy / download loop.
- Generated artifact fields for HTML / CSS must stay clear enough to support copy and download without expanding into full project export.

## Now

- Productize the screenshot-to-generated-preview path into a demonstrable MVP delivery loop.

## Next

- Clarify the minimal generated artifact contract for HTML / CSS.
- Improve generated output quality only when tied to a measurable user-facing MVP gap.
- Expand smoke coverage for common simple page types.

## Later

- Project template export.
- Layout JSON schema evolution.
- Persistence and history.
- Failure retry guidance.
- Editing workflows.

## Won’t This Time

- MySQL persistence.
- Entity / Mapper / MyBatis-Plus tables.
- Figma API / Figma MCP input.
- Multi-page generation.
- Drag-and-drop editor.
- Online editor.
- Login / registration.
- Permission system.
- Complex visual regression.
- Redis / RabbitMQ.
- Complex ZIP export.
- 1:1 high-fidelity guarantee.
- Replacing the default stack.

## Candidate Bets

Candidate bets are options for future Cycle Planning Check. They are not the next cycle plan until the gate chooses one.

- Productized result page and delivery actions.
- Reliable MVP smoke for upload -> generate -> preview -> copy / download.
- User-readable REAL_AI / FALLBACK / FAILED state.
- Minimal generated artifact contract for HTML / CSS.
- Focused output-quality pass for one approved sample set.

## Cycle Plan Gate

Before any new Cycle / Week plan is written, answer these questions in `docs/plan.md`:

1. What is the current MVP Goal?
2. What gap most blocks the MVP loop right now?
3. How many problems will this cycle solve? Default maximum: one single bet.
4. Which unfinished items from the last cycle are still Must because they block the MVP loop?
5. Which unfinished items are only inertia from the last cycle?
6. Which ideas move to Later or Won't This Time?
7. After this cycle, what can the user do that they could not do before?
8. Why is this bet better than continuing to polish last cycle's leftover details?

## Drift Guard

- A new cycle plan must not be generated only by extending the previous `docs/plan.md` or day cards.
- Unfinished Should / Could items do not automatically roll into the next cycle.
- A new cycle must choose one single bet again from MVP Gap Pool, Now, or Candidate Bets.
- Candidate Bets remain candidates until selected through the Cycle Plan Gate.
- Day cards execute the current `docs/plan.md`; they do not redefine product direction or expand the roadmap.
