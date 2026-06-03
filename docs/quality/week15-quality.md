# Week 15 Sample Set and Lightweight Quality Metrics

## Purpose

Week 15 improves generated page quality on a small fixed sample set.

This document defines the sample set and lightweight checks for the current cycle only. It does not create a pixel-perfect standard, a visual regression platform, or a Week 16 plan.

## Fixed Sample Set

Use only the following public-safe repository samples for Week 15 smoke and quality work:

| Sample ID | Input | Intent | Expected visual / structural traits | Acceptable deviations |
|---|---|---|---|---|
| W15-S1 Simple card | `samples/01-simple-card-page.png` | Check whether the generator preserves a simple marketing / content card layout. | One clear page container, a prominent card or hero block, visible title/body/action hierarchy, rounded card or panel styling, centered or balanced spacing. | Exact text wrapping, color values, shadow strength, and pixel spacing may differ if hierarchy and grouping remain clear. |
| W15-S2 Simple form | `samples/02-simple-form-page.png` | Check whether the generator preserves a basic form page with labels, inputs, and submit action. | Form container is recognizable, labels stay near matching fields, inputs and button are visually distinct, vertical rhythm is stable, primary action is easy to identify. | Exact field width, border color, and form copy may differ if the form structure remains understandable. |
| W15-S3 Dashboard cards | `samples/03-dashboard-cards-page.png` | Check whether the generator preserves a dashboard-like layout with repeated cards / metrics. | Header or top section is recognizable, repeated cards form a grid or stable rows, card titles / values / supporting text are grouped, main dashboard hierarchy is clear. | Exact number wrapping, chart-like detail, icon fidelity, and precise card dimensions may differ if repeated-card structure is preserved. |

Do not add private screenshots, uploaded runtime images, licensed material, API keys, credentials, or generated artifacts to satisfy this sample set.

## Lightweight Quality Metrics

Score each sample with `pass`, `partial`, `fail`, or `blocked` for each metric. These checks are intentionally human-readable and may be supported by smoke scripts later.

| Metric | Pass signal | Fail signal |
|---|---|---|
| Structure | Main regions from the sample are present and ordered similarly. | Output collapses into unrelated sections, raw text dump, or missing main region. |
| Main visual hierarchy | Primary title / action / card or dashboard focus is visibly stronger than secondary content. | All content has the same weight or the wrong element becomes dominant. |
| Spacing and grouping | Related elements stay grouped, with readable padding / gaps and no severe overlap. | Inputs, cards, text, or buttons overlap, scatter, or lose their group relationship. |
| Typography | Headings, body text, labels, values, and buttons use distinguishable sizes / weights. | Text hierarchy is flat, unreadable, or mismatched to the sample role. |
| Component fidelity | Core components for the sample type are recognizable: card, form fields, button, repeated dashboard cards. | Core components are absent, replaced by unrelated elements, or rendered as plain unstructured text. |
| Responsive sanity | The generated preview remains inspectable at a normal desktop viewport and does not depend on fixed private runtime assets. | Layout requires hidden/private assets, horizontal overflow dominates, or the preview is unusable. |
| Safety and delivery | Strict preview sandbox remains unchanged, result state is readable, and copy / download are still available or report clear failure. | `allow-scripts` is required, state is hidden, copy/download disappears without explanation, or secrets/runtime artifacts are introduced. |

## Overall Result Guide

- `pass`: All safety and delivery checks pass, and at most one visual metric is `partial`.
- `conditional pass`: Safety and delivery checks pass, but two or more visual metrics are `partial`.
- `fail`: Any safety issue, missing core sample structure, broken preview, or broken copy / download without a readable failure.
- `blocked`: The sample cannot be run because required local service, model access, environment, or public-safe input is unavailable.

## Explicit Non-Goals

- MySQL persistence.
- Figma API / Figma MCP.
- Multi-page generation.
- Drag-and-drop or online editor workflows.
- Complex ZIP export.
- Week 16 / Cycle 16 planning.
- Pixel-perfect or 1:1 high-fidelity guarantee.
