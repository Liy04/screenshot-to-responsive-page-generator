# Week 12 Acceptance Report

## 1. 验收结论

Week 12：通过。

通过性质：

```text
达到简单截图还原雏形，不是高保真还原。
```

## 2. 验收范围

本次验收覆盖：

- Worker prompt v2 / `week12-v1`
- 视觉清单到 Layout JSON v0.1 映射
- style 白名单和 sanitizer
- static generator 基础样式增强
- 前端原图 / iframe 对比
- 三张 samples 真实 AI smoke
- artifact 复用
- iframe 安全策略
- API key 泄漏检查

## 3. 样例范围

- `samples/01-simple-card-page.png`
- `samples/02-simple-form-page.png`
- `samples/03-dashboard-cards-page.png`

## 4. 核心验收项

| 验收项 | 结果 |
|---|---|
| 三张 samples Worker direct smoke | 通过 |
| 三张 samples Backend API smoke | 通过 |
| `sourceType=REAL_AI` | 通过 |
| `fallbackUsed=false` | 通过 |
| `promptVersion=week12-v1` | 通过 |
| `previewHtml` 非空 | 通过 |
| 二次 generate 命中 `artifact.reused=true` | 通过 |
| Worker 全量测试 | 通过，`80 / 80` |
| 前端页面级 iframe smoke | 通过，sample 01 |
| iframe `sandbox=""` | 通过 |
| iframe 无 `allow-scripts` | 通过 |
| 未提交真实 API key | 通过 |
| 未提交运行副产物 | 通过 |

## 5. 质量评分

| sample | 分数 | 结论 |
|---|---:|---|
| 01 simple card | 约 24 / 35 | 通过 |
| 02 simple form | 约 24 / 35 | 通过 |
| 03 dashboard cards | 约 25 / 35 | 通过 |
| 平均 | 约 24.3 / 35 | 通过 |

## 6. 风险与限制

- 当前只是刚过 Week 12 质量线。
- 真实模型并发请求不稳定。
- dashboard 图表区域仍非视觉级复刻。
- form 控件视觉仍偏基础。
- 复杂整页截图仍可能超时或质量低。
- 后续 smoke 建议顺序执行，不建议并发请求模型。

## 7. 安全结论

安全边界保持：

- 不直接使用模型原始 HTML。
- 不放宽 iframe sandbox。
- 不允许 script / inline event / javascript URL。
- API key 仍只通过环境变量读取。

## 8. Week 13 决策建议

根据 Week 12 平均分约 `24.3 / 35`，项目可以考虑进入更高阶方向。

但由于用户当前优先关注输出质量，建议 Week 13 继续质量增强，而不是立刻进入 MySQL、Figma、复杂编辑器或持久化。

推荐 Week 13 方向：

```text
继续提升视觉清单 -> Layout JSON -> previewHtml 的还原质量和可验收性。
```
