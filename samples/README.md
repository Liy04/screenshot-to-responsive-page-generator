# Samples

This directory contains public-safe mock UI screenshots for real AI smoke tests.

All images in this directory must be synthetic mock UI only. Do not add real product screenshots, private business pages, customer data, personal data, real avatars, third-party brand assets, trademarks, or copyright-unclear images.

## Sample Images

| File | Mock content | Validation target |
|---|---|---|
| `01-simple-card-page.png` | A simple card-based landing section with neutral placeholder copy and geometric image blocks. | Checks whether the AI path can identify a basic responsive page structure, card hierarchy, spacing, buttons, and text blocks. |
| `02-simple-form-page.png` | A simple form page with labels, inputs, toggles, and a summary panel using fictional values. | Checks whether the AI path can recover form layout, input grouping, labels, primary action, and two-column-to-stacked responsive behavior. |
| `03-dashboard-cards-page.png` | A dashboard-style page with metric cards, a table mock, chart blocks, and neutral fictional numbers. | Checks whether the AI path can describe dense UI regions, repeated cards, table rows, chart placeholders, and dashboard spacing. |

## Safety Rules

Do not commit images that contain:

- Real API keys, secrets, tokens, QR codes, invite links, or environment values.
- Real phone numbers, email addresses, account names, customer names, addresses, order IDs, or user identifiers.
- Real user avatars, employee photos, profile pictures, or face images.
- Company-internal pages, private admin screens, production dashboards, or client screenshots.
- Third-party logos, trademarks, app screenshots, branded UI, licensed icons, stock photos, or copyright-unclear illustrations.

Use only mock data, neutral labels, simple geometric shapes, and locally generated assets.

## Recommended Smoke Path

Recommended real AI smoke order:

1. Run `01-simple-card-page.png` first to verify the smallest page reconstruction path.
2. Run `02-simple-form-page.png` to verify form semantics and grouped controls.
3. Run `03-dashboard-cards-page.png` last to verify denser repeated regions and artifact stability.

For each run, inspect the generated artifacts and classify the result as `REAL_AI`, `FALLBACK`, or `FAILED` according to the active smoke documentation. These files are intentionally small PNGs and should remain below 5 MB each.
