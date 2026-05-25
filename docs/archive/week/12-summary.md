# Week 12 Summary

## 1. 阶段名称

Week 12：AI 输出质量与静态预览还原增强。

## 2. 阶段目标

Week 12 的目标不是扩展新主线，而是解决一个核心问题：

```text
同一张简单截图 -> 生成结果更像原图
```

本周围绕三张公开安全 samples 做输出质量增强：

- `samples/01-simple-card-page.png`
- `samples/02-simple-form-page.png`
- `samples/03-dashboard-cards-page.png`

## 3. 完成内容

### 3.1 文档与质量标准

- 新增 `docs/quality/week12-quality.md`。
- 建立 35 分评分表。
- 明确 Week 13 判断标准。
- 新增 `docs/smoke/week12-quality-smoke.md` 记录质量 smoke。

### 3.2 Worker prompt 与真实 AI 输出

- promptVersion 升级到 `week12-v1`。
- 从“直接输出布局结构”调整为“视觉清单提取”：
  - `texts`
  - `regions`
  - `components`
- 去除 prompt 中的 `jobId` / `imageName`，避免 `input.png` 或文件名污染页面内容。
- 使用 `temperature=0.0` 和较小 `max_tokens`，降低漂移和超时。

### 3.3 Worker 映射与 repair

- 支持将视觉清单映射为 Layout JSON v0.1。
- 支持 top-level `texts`。
- 支持 `regions` / `components`。
- 支持 nested sections / elements。
- 支持 dashboard metric label/value 转 card。
- 增强 JSON 清洗，兼容模型轻微格式错误。
- 增强 style key 白名单和 style value sanitizer。

### 3.4 静态编译器样式增强

- 增强 card / button / input / text 基础样式。
- 保持 HTML escape。
- 保持禁止 script / inline event / javascript URL / CSS unsafe value。

### 3.5 前端对比体验

- `/dev/image-to-layout` 增加原图 / iframe 对比区域。
- 成功状态展示 generated preview。
- FAILED / TIMEOUT / 无 previewHtml 时不展示 iframe。
- iframe 继续使用 `sandbox=""`，无 `allow-scripts`。

## 4. 验收结果

### Worker

- Worker 全量测试：`80 / 80` 通过。
- 三张 samples direct smoke 均通过。
- 三张 samples 均 `sourceType=REAL_AI`。
- 三张 samples 均 `fallbackUsed=false`。
- 三张 samples 均 `previewHtml` 非空。

### Backend

- 三张 samples `upload -> generate` 均通过。
- 三张 samples 二次 generate 均命中 `artifact.reused=true`。
- 后端 smoke 使用 `--imagepage.worker.timeout-seconds=180`。

### Frontend

- sample 01 页面级 smoke 通过。
- 页面显示 `REAL_AI 成功`。
- 页面展示 Layout JSON 和 previewHtml。
- iframe 数量为 1。
- iframe `sandbox=""`。
- iframe 无 `allow-scripts`。

## 5. 质量评分

| sample | 粗评分 |
|---|---:|
| `01-simple-card-page.png` | 约 24 / 35 |
| `02-simple-form-page.png` | 约 24 / 35 |
| `03-dashboard-cards-page.png` | 约 25 / 35 |
| 平均 | 约 24.3 / 35 |

结论：

```text
达到 Week 12 “简单截图还原雏形”通过线。
```

## 6. 安全检查

- 未写入真实 API key。
- 未发现真实密钥泄漏。
- 未直接使用模型原始 HTML。
- previewHtml 仍由 Worker 静态编译器生成。
- iframe sandbox 未放宽。
- 未提交 `backend/storage/`、`frontend/dist/` 或运行副产物。

## 7. 未完成事项

- 还不是高保真还原。
- dashboard 图表仍是粗粒度结构表达。
- form 控件视觉仍偏规则化。
- 真实模型并发请求不稳定，后续建议顺序 smoke。
- 复杂整站截图仍不作为当前验收目标。

## 8. Week 13 建议

Week 13 建议继续输出质量增强：

1. 提升视觉清单提取稳定性。
2. 提升 Layout JSON 映射质量。
3. 增强 preview 样式表达。
4. 固化轻量视觉验收流程。
5. 暂不急于进入 MySQL、Figma、编辑器或持久化主线。
