# Week 15 Quality Smoke

## Purpose

Record smoke evidence for Week 15 / Cycle 15: Sample-set based generated page quality improvement.

This file is for current smoke evidence only. It is not a roadmap, not a Week 16 plan, and not an archive.

## Scope

Current single bet:

- Sample-set based generated page quality improvement.

Smoke target:

```text
fixed sample set
-> generate through the current MVP path
-> verify REAL_AI / FALLBACK / FAILED state
-> verify safe generated preview
-> compare against lightweight quality metrics
-> verify copy / download still work
-> verify no secrets or generated runtime artifacts are staged
```

Out of scope:

- MySQL persistence.
- Figma API / Figma MCP.
- Multi-page generation.
- Drag-and-drop or online editor.
- Complex ZIP export.
- Pixel-perfect or 1:1 high-fidelity guarantee.
- Week 16 / Cycle 16 planning.

## Fixed Sample Set

Quality definition: `docs/quality/week15-quality.md`.

Use these repository samples only:

| Sample ID | Input | Intent |
|---|---|---|
| W15-S1 Simple card | `samples/01-simple-card-page.png` | Preserve a simple card / content-page hierarchy. |
| W15-S2 Simple form | `samples/02-simple-form-page.png` | Preserve a basic form layout with labels, inputs, and primary action. |
| W15-S3 Dashboard cards | `samples/03-dashboard-cards-page.png` | Preserve repeated dashboard-card grouping and visual hierarchy. |

## Pre-smoke Checklist

- [x] Day 01 fixed sample set is documented in `docs/quality/week15-quality.md`.
- [x] Day 01 quality metrics are documented in `docs/quality/week15-quality.md`.
- [x] Samples contain no private, sensitive, licensed, or secret material per `samples/README.md` and fixture inspection.
- [x] Required local services are known: backend jar on test port `8081`, frontend dev server on `5174`, Chrome headless for UI smoke.
- [x] Required environment variables were checked by presence only and were not written to Git.
- [x] `docs/archive/` was not read or modified during this retest.

## REAL_AI Timeout Note

- Week 15 fixed sample REAL_AI full smoke recommended backend startup timeout: `--imagepage.worker.timeout-seconds=420`.
- Do not use the older 120 second Week 09 single-sample smoke setting, or the failed 180 second attempt, as the Week 15 full fixed-sample retest baseline.
- The 420 second timeout is only the current reproduction setting for real multimodal fixed-sample smoke. It is not a product-level latency or async stability fix, and it does not change API contract, runtime defaults, or product direction.
- Real latency / async stability should be evaluated as a later single bet if Lead selects it through the cycle gate.

## Sample Results

### W15-S1 Simple card

- Input source: `samples/01-simple-card-page.png`
- Intent: preserve a simple card / content-page hierarchy.
- Expected traits: one clear page container, prominent card or hero block, visible title/body/action hierarchy, rounded card or panel styling, centered or balanced spacing.
- Command / manual steps:
  - API: uploaded `samples/01-simple-card-page.png` to `POST /api/image-page/upload`, then generated through `POST /api/image-page/jobs/{jobId}/generate` against backend `8081`.
  - Page delivery and iframe sandbox path were covered by `ImageToLayoutDev` frontend test and the W15-S2 page smoke in this retest; W15-S1 was kept to API / preview / quality lightweight防回归.
- Generation state: REAL_AI (`status=SUCCESS`, `sourceType=REAL_AI`, `fallbackUsed=false`, `promptVersion=week15-v1`, API job `imgjob_c7fda15348b94c859c261aa53171cf7b`)
- Preview renders: pass; API `previewHtml` length `6473`.
- Preview safety: pass; generated HTML scan found no `<script>`, inline event, or `javascript:` marker in the sampled API response.
- Iframe sandbox strict without `allow-scripts`: pass by unchanged frontend component path; frontend test asserts `sandbox=""`, no `allow`, and no `allow-scripts`. The W15-S2 page smoke also verified the live iframe path.
- Quality metric result:
  - Structure: pass; card-like layout remains present (`layoutCardCount=3`).
  - Main visual hierarchy: pass; main heading and content/card hierarchy are distinguishable.
  - Spacing and grouping: pass; related text and cards remain grouped.
  - Typography: pass; heading/body/card text roles are distinguishable.
  - Component fidelity: pass; card-like content blocks are recognizable.
  - Responsive sanity: pass; API preview is non-empty and safe for the existing preview path.
  - Safety and delivery: pass; state and previewHtml are present. Copy / download controls are covered by frontend test and the W15-S2 page smoke.
- Copy result: not clicked sample-specifically in this retest; frontend test passed, and W15-S2 live page copy produced the expected readable headless clipboard-permission failure.
- Download result: not clicked sample-specifically in this retest; frontend test passed, and W15-S2 live page download succeeded.
- Artifacts checked: API response fields and generated preview safety.
- Secrets / private artifacts check: pass; no key value printed or written, no generated artifact retained.
- Result: pass
- Pass / fail notes: fixed sample card structure is preserved well enough for Week 15 lightweight quality checks.
- Likely responsible area if failed: N/A

### W15-S2 Simple form

- Input source: `samples/02-simple-form-page.png`
- Intent: preserve a basic form layout with labels, inputs, and primary action.
- Expected traits: recognizable form container, labels near matching fields, distinct inputs and button, stable vertical rhythm, identifiable primary action.
- Command / manual steps:
  - API: uploaded `samples/02-simple-form-page.png` to `POST /api/image-page/upload`, then generated through `POST /api/image-page/jobs/{jobId}/generate` against backend `8081`.
  - UI: Chrome headless opened `/dev/image-to-layout`, selected the same sample, uploaded through the page, generated, inspected iframe and delivery actions.
- Generation state: REAL_AI (`status=SUCCESS`, `sourceType=REAL_AI`, `fallbackUsed=false`, `promptVersion=week15-v1`, API job `imgjob_793790a16e8a45b085c58dd2f9e1eb22`; UI job `imgjob_339b449180f846418c33a30de5992152`)
- Preview renders: pass; API `previewHtml` length `6385`, UI iframe `srcdoc` length `6382`, iframe box `432x460`.
- Preview safety: pass; generated HTML scan found no `<script>`, inline event, or `javascript:` marker in the sampled API response.
- Iframe sandbox strict without `allow-scripts`: pass; UI iframe `sandbox=""`, no `allow` attribute, no `allow-scripts`.
- Quality metric result:
  - Structure: pass; header, hero, form section, and sidebar are present.
  - Main visual hierarchy: pass; main title and form action hierarchy are distinguishable enough for Week 15.
  - Spacing and grouping: pass; labels, inputs, and action controls stay grouped in a form container.
  - Typography: pass; headings, labels, input placeholders, and buttons use distinguishable roles.
  - Component fidelity: pass; repaired output contains a semantic form with recognizable controls (`layoutFormCount=1`, `layoutInputCount=2`, `layoutButtonCount=4`; UI `srcdocInputCount=2`, `srcdocButtonCount=4`).
  - Responsive sanity: pass; desktop iframe rendered and remained inspectable.
  - Safety and delivery: pass; REAL_AI/SUCCESS state, iframe safety, and delivery area are visible.
- Copy result: operation visible; `复制完整 HTML` attempted in headless Chrome and produced readable failure text (`复制失败，请检查浏览器剪贴板权限`), treated as acceptable test-environment clipboard limitation.
- Download result: pass; `下载 HTML` created a temporary `.html` file (`6382` bytes), then the file was deleted.
- Artifacts checked: API response fields, UI iframe attributes, UI delivery actions, temporary download file.
- Secrets / private artifacts check: pass; no key value printed or written, no generated artifact retained.
- Result: pass
- Pass / fail notes: W15-S2 form fidelity blocker is fixed in this retest; plain form rows are now repaired into `form` / `input` / `button` nodes and render as recognizable controls.
- Likely responsible area if failed: N/A

### W15-S3 Dashboard cards

- Input source: `samples/03-dashboard-cards-page.png`
- Intent: preserve repeated dashboard-card grouping and visual hierarchy.
- Expected traits: recognizable header or top section, repeated cards in a grid or stable rows, grouped card titles / values / supporting text, clear dashboard hierarchy.
- Command / manual steps:
  - API: uploaded `samples/03-dashboard-cards-page.png` to `POST /api/image-page/upload`, then generated through `POST /api/image-page/jobs/{jobId}/generate` against backend `8081`.
  - Page delivery and iframe sandbox path were covered by `ImageToLayoutDev` frontend test and the W15-S2 page smoke in this retest; W15-S3 was kept to API / preview / quality lightweight防回归.
- Generation state: REAL_AI (`status=SUCCESS`, `sourceType=REAL_AI`, `fallbackUsed=false`, `promptVersion=week15-v1`, API job `imgjob_b53e256fd8f942f0aa5dfca5d5fd4905`)
- Preview renders: pass; API `previewHtml` length `11525`.
- Preview safety: pass; generated HTML scan found no `<script>`, inline event, or `javascript:` marker in the sampled API response.
- Iframe sandbox strict without `allow-scripts`: pass by unchanged frontend component path; frontend test asserts `sandbox=""`, no `allow`, and no `allow-scripts`. The W15-S2 page smoke also verified the live iframe path.
- Quality metric result:
  - Structure: pass; dashboard-card structure remains present (`layoutCardCount=11`).
  - Main visual hierarchy: pass; dashboard heading and metric values are stronger than supporting content.
  - Spacing and grouping: pass; repeated metrics are grouped as cards/rows.
  - Typography: pass; labels, metric values, and headings are distinguishable.
  - Component fidelity: partial; dashboard-card structure is recognizable, but metric cards appear duplicated and chart/table details are placeholder-level.
  - Responsive sanity: pass; API preview is non-empty and safe for the existing preview path.
  - Safety and delivery: pass; state and previewHtml are present. Copy / download controls are covered by frontend test and the W15-S2 page smoke.
- Copy result: not clicked sample-specifically in this retest; frontend test passed, and W15-S2 live page copy produced the expected readable headless clipboard-permission failure.
- Download result: not clicked sample-specifically in this retest; frontend test passed, and W15-S2 live page download succeeded.
- Artifacts checked: API response fields and generated preview safety.
- Secrets / private artifacts check: pass; no key value printed or written, no generated artifact retained.
- Result: pass
- Pass / fail notes: repeated-card dashboard structure is preserved; duplicate metric cards remain an acceptable quality note for this smoke because core dashboard hierarchy is still visible.
- Likely responsible area if failed: N/A

## Retest Summary Table

| Sample | State | previewHtml | iframe sandbox | Quality conclusion | Copy / download |
|---|---|---|---|---|---|
| W15-S1 | REAL_AI / SUCCESS | API length `6473`, safe scan pass | Strict sandbox path covered by frontend test and W15-S2 live page smoke | pass; card structure preserved | Covered by frontend test and W15-S2 live page smoke |
| W15-S2 | REAL_AI / SUCCESS | API length `6385`, UI `srcdoc` length `6382`, safe scan pass | Live UI `sandbox=""`, no `allow`, no `allow-scripts` | pass; blocker fixed with semantic form / inputs / buttons | Copy showed readable headless clipboard failure; download created and deleted `6382` byte HTML |
| W15-S3 | REAL_AI / SUCCESS | API length `11525`, safe scan pass | Strict sandbox path covered by frontend test and W15-S2 live page smoke | pass; dashboard cards preserved, duplicate cards remain accepted quality note | Covered by frontend test and W15-S2 live page smoke |

## Overall Result

- Status: pass
- Date: 2026-06-01
- Runner: tester-agent
- Environment:
  - Windows / PowerShell
  - Java `17.0.16`
  - Maven `3.9.11`
  - Node `v22.22.2`
  - npm `10.9.7`
  - Python default `3.11.9`
  - `OPENAI_BASE_URL`, `OPENAI_MODEL`, and `OPENAI_API_KEY` presence checked only; real values were not printed or written.
  - `IMAGEPAGE_WORKER_PYTHON_COMMAND` was not set; backend used default `python`, which resolves to Python `3.11.9` locally.
- Services started:
  - Backend jar on `8081`; first REAL_AI attempt with `--imagepage.worker.timeout-seconds=180` timed out, then retest continued with `--imagepage.worker.timeout-seconds=420`.
  - Frontend dev server on `5174` with proxy target `http://127.0.0.1:8081`.
  - Chrome headless remote debugging on `9223` for UI smoke.
  - All three test-owned ports were released after smoke.
- Commands:
  - `python -m unittest discover -s worker -p "test_*.py"` -> pass, 91 tests.
  - `npm test -- src/views/__tests__/ImageToLayoutDev.test.js` from `frontend/` -> pass, 1 file / 11 tests.
  - `mvn test` from `backend/` -> pass, 45 tests.
  - `mvn package -DskipTests` from `backend/` -> pass.
  - API upload/generate smoke for all three fixed samples through backend `8081` -> all returned `REAL_AI`, `SUCCESS`, `previewHtml` non-empty.
  - Chrome headless UI smoke through `/dev/image-to-layout` for W15-S2 -> REAL_AI/SUCCESS, iframe and delivery area visible.
  - `python worker/main.py --smoke` -> pass.
- Samples passed: W15-S1, W15-S2, W15-S3
- Samples failed: none
- Samples blocked: none

## Safety Checks

- [x] No real API key, secret, credential, or token is written to docs or code.
- [x] No private screenshot is committed; only repository samples were used.
- [x] No generated runtime artifact or downloaded file is committed; temporary downloaded HTML files were deleted.
- [x] `backend/storage` created during smoke/tests was deleted after validation.
- [x] No MySQL, Figma API / MCP, multi-page, editor, or complex ZIP work is introduced.
- [x] iframe preview remains strict and does not use `allow-scripts`.
- [x] `frontend/dist` was not created by this retest.

## Blockers

- No active blocker found in this retest.
- Note: the first REAL_AI attempt with a 180 second Worker timeout returned 504 before producing a sample result. Retest with a 420 second Worker timeout completed all samples; W15-S1 and W15-S3 still took longer than W15-S2.
- Headless Chrome could not write to clipboard during copy checks; the page displayed a readable clipboard-permission failure. Download checks passed.

## Handoff

- Suggested next responsible agent: reviewer-agent or Lead for Day 07 closeout evidence review.
- Required fix before closeout: none from tester-agent.
- Accepted risk:
  - W15-S3 has duplicated metric cards and placeholder-level chart/table detail, but still passes the current lightweight dashboard-card checks.
  - Copy action failure is attributed to headless browser clipboard permission because the UI reports a readable failure and download succeeds.
  - REAL_AI latency remains variable; longer Worker timeout was needed for the full fixed-sample retest.
