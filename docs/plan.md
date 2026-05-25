# Plan

## 当前阶段

Week 12 已完成，Week 13 已完成输出质量增强阶段。

当前项目已经从“真实 AI 链路能跑通”推进到：

```text
三张简单 samples
-> 真实 AI 识别视觉清单
-> Worker 映射 Layout JSON v0.1
-> static generator 编译 previewHtml
-> 前端 iframe 预览
```

## Week 12 结果

Week 12 的三张样例：

- `samples/01-simple-card-page.png`
- `samples/02-simple-form-page.png`
- `samples/03-dashboard-cards-page.png`

最终 smoke：

- 三张样例均 `sourceType=REAL_AI`。
- 三张样例均 `fallbackUsed=false`。
- 三张样例均输出非空 `previewHtml`。
- 三张样例二次 generate 均 `artifact.reused=true`。
- sample 01 前端页面级 iframe smoke 通过。
- iframe 保持 `sandbox=""`，无 `allow-scripts`。

质量粗评：

| sample | 分数 |
|---|---:|
| 01 simple card | 约 24 / 35 |
| 02 simple form | 约 24 / 35 |
| 03 dashboard cards | 约 25 / 35 |
| 平均 | 约 24.3 / 35 |

结论：

```text
Week 12 达到“简单截图还原雏形”通过线。
```

## Week 13 目标

Week 13 不进入 MySQL、Figma、复杂编辑器或持久化主线，而是继续围绕输出质量推进。

重点目标：

1. 让视觉清单提取更稳定，减少同图多次生成的结构漂移。
2. 让 Layout JSON v0.1 映射更准确、更可解释。
3. 让 preview 样式表达更接近原图，而不是规则化裸 HTML。
4. 让顺序 smoke 可复现、可记录、可回溯。
5. 让验收口径保持轻量，不引入重型视觉回归系统。

## Week 13 Day 计划

| Day | 角色 | 目标 |
|---|---|---|
| Day 1 | docs-agent -> reviewer-agent -> lead | 定义 Week 13 质量标准、评分表和顺序 smoke 模板 |
| Day 2 | worker-agent -> tester-agent -> reviewer-agent -> lead | 稳定视觉清单输出，降低 prompt 和结构漂移 |
| Day 3 | worker-agent -> tester-agent -> reviewer-agent -> lead | 提升 Layout JSON v0.1 映射质量和 deterministic repair |
| Day 4 | worker-agent -> tester-agent -> reviewer-agent -> lead | 增强 preview 静态样式表达，但保持安全边界 |
| Day 5 | frontend-agent -> tester-agent -> reviewer-agent -> lead | 让预览和对照更适合顺序 smoke 与人工检查 |
| Day 6 | tester-agent -> reviewer-agent -> docs-agent -> lead | 顺序 smoke、人工评分和结果记录 |
| Day 7 | lead -> docs-agent -> reviewer-agent | 汇总 Week 13 结果，判断下一步方向 |

## Week 13 结果

Week 13 已完成：

- Day 1：质量标准、评分表和顺序 smoke 模板。
- Day 2：真实 AI 视觉清单稳定性增强。
- Day 3：Layout JSON v0.1 映射和 deterministic repair 增强。
- Day 4：静态 preview 样式增强。
- Day 5：前端原图 / iframe 对比和 smoke 摘要。
- Day 6：三张 samples 顺序 smoke、artifact 复用检查、iframe 检查和人工评分。
- Day 7：当前文档收口和 Lead 二次验收。

Day 6 最终结果：

| sample | sourceType | fallbackUsed | previewHtml | artifact.reused | score |
|---|---|---:|---|---|---:|
| `01-simple-card-page.png` | `REAL_AI` | `false` | 非空 | 二次 generate `true` | 27 / 35 |
| `02-simple-form-page.png` | `REAL_AI` | `false` | 非空 | 二次 generate `true` | 26 / 35 |
| `03-dashboard-cards-page.png` | `REAL_AI` | `false` | 非空 | 二次 generate `true` | 28 / 35 |

汇总：

- 平均分：27.0 / 35。
- 最低分：26 / 35。
- 三张样例全部命中 `REAL_AI`。
- 三张样例全部未触发 fallback。
- 三张样例全部通过 sandbox iframe 渲染检查。
- 未发现真实 API key 泄漏。

结论：

```text
Week 13 达到稳定通过线，建议通过。
```

## Week 13 质量重点

- 视觉清单稳定性：`texts / regions / components` 的结构输出尽量一致。
- Layout JSON 映射质量：结构层级、默认样式和语义角色更准确。
- preview 样式表达：card / button / input / text 更像实际 UI。
- 顺序 smoke：三张 samples 按固定顺序执行，避免并发压测模型服务。
- 轻量验收：重点看可复现性、安全性和简单样例的质量提升。

## Week 13 验收口径

- 三张 simple samples 顺序 smoke 全部通过。
- 每张记录都包含 sample、顺序、模型、`promptVersion`、`sourceType`、`fallbackUsed`、`artifact.reused`、`previewHtml`、iframe 和主要缺陷。
- 平均分目标保持在 `25 / 35` 左右或更高；如果仍在 `24` 附近，必须由 Lead 给出条件通过说明。
- 不允许为了提高分数而放宽安全边界。
- 不允许引入 MySQL、Figma、复杂编辑器、拖拽编辑器、多页面生成、ZIP 导出或持久化主线。
- 不升级 Layout JSON schema v0.2，除非 Week 13 后续专门立项。

## 安全边界

继续保持：

- 不提交真实 API key。
- 不把模型原始 HTML 直接作为最终页面代码。
- 不放宽 iframe sandbox。
- 不允许 `<script>`、inline event、`javascript:`、CSS `url()`、`expression()`、`@import`。
- 不提交 `backend/storage/`、`frontend/dist/` 或其他运行副产物。

## 下一步

Week 13 下一步不建议立刻扩展到 MySQL、Figma、复杂编辑器或多页面。

建议优先：

1. 做 Git diff 审查，确认 worktree 改动边界清晰。
2. 必要时补一次关键测试复核。
3. 将 `.worktrees/week13-quality` 的成果合并回 `main`。
4. 后续如果继续质量主线，优先减少 warnings、提升文本和组件清单准确度，再考虑扩大 samples 覆盖。
