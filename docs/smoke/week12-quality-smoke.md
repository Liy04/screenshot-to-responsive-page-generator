# Week 12 Quality Smoke

## 1. 文件目的

记录 Week 12 三张 samples 的质量 smoke 结果。

本文件记录 Week 12 Day 6 tester-agent 质量 smoke 结果，以及随后 worker-agent 对质量阻塞的修复复测结果。

本轮结论：Worker direct smoke、Backend API smoke 与前端页面级 smoke 已通过。三张样例均能命中 `REAL_AI`，`fallbackUsed=false`，`previewHtml` 非空，二次生成命中 `artifact.reused=true`。前端 `/dev/image-to-layout` 已用 sample 01 完成浏览器级验证，iframe 正常渲染且保持 `sandbox=""`。

## 2. 环境要求

- Python：建议 `D:\environment\python11\python.exe`
- 后端真实 AI timeout：建议 `--imagepage.worker.timeout-seconds=180`
- `OPENAI_BASE_URL=https://api.siliconflow.cn/v1`
- `OPENAI_MODEL=Qwen/Qwen3-VL-32B-Instruct`
- `OPENAI_API_KEY` 只允许通过环境变量设置，不写入本文档

## 3. 评分标准

评分标准见：

```text
docs/quality/week12-quality.md
```

## 4. Smoke 记录

### 4.1 samples/01-simple-card-page.png

| 字段 | 记录 |
|---|---|
| 评分人 | Codex tester-agent |
| 评分日期 | 2026-05-20 |
| 模型 | Qwen/Qwen3-VL-32B-Instruct |
| promptVersion | `week12-v1` |
| sourceType | `REAL_AI` |
| fallbackUsed | `false` |
| artifact.reused | `true`，二次 generate 命中复用 |
| previewHtml 非空 | 是，backend smoke 长度约 `4457` |
| iframe 渲染 | 是，前端页面级 smoke 已验证 |
| 总分 / 35 | 约 `24` |
| 主要缺陷 | 关键文本已保留：`Mock Page`、`Responsive card page`、`Primary`、`Content block`。预览结构仍偏规则化，视觉细节不算高保真。 |

### 4.2 samples/02-simple-form-page.png

| 字段 | 记录 |
|---|---|
| 评分人 | Codex tester-agent |
| 评分日期 | 2026-05-20 |
| 模型 | Qwen/Qwen3-VL-32B-Instruct |
| promptVersion | `week12-v1` |
| sourceType | `REAL_AI` |
| fallbackUsed | `false` |
| artifact.reused | `true`，二次 generate 命中复用 |
| previewHtml 非空 | 是，backend smoke 长度约 `4130` |
| iframe 渲染 | 未做浏览器页面级复测 |
| 总分 / 35 | 约 `24` |
| 主要缺陷 | 关键文本已保留：`Mock Form`、`Request settings`、`Project label`、`Submit`。表单控件仍偏文本化，后续可继续增强 input / select 的视觉映射。 |

### 4.3 samples/03-dashboard-cards-page.png

| 字段 | 记录 |
|---|---|
| 评分人 | Codex tester-agent |
| 评分日期 | 2026-05-20 |
| 模型 | Qwen/Qwen3-VL-32B-Instruct |
| promptVersion | `week12-v1` |
| sourceType | `REAL_AI` |
| fallbackUsed | `false` |
| artifact.reused | `true`，二次 generate 命中复用 |
| previewHtml 非空 | 是，backend smoke 长度约 `7576` |
| iframe 渲染 | 未做浏览器页面级复测 |
| 总分 / 35 | 约 `25` |
| 主要缺陷 | 关键文本已保留：`Dashboard overview`、`Items`、`128`、`Activity table`、`Chart block`、`Status strip`。图表区域仍是粗粒度结构表达，不是视觉级图表复刻。 |

## 5. 汇总

| 指标 | 结果 |
|---|---|
| 平均分 | 约 `24.3 / 35` |
| 最低分 | 约 `24 / 35` |
| 是否达到 20 分基本通过线 | 是 |
| 是否达到 24 分理想通过线 | 是，按人工粗评刚过线 |
| 是否出现安全问题 | 未发现密钥泄漏；previewHtml 安全检查未发现禁用片段；iframe `sandbox=""`，无 `allow-scripts` |
| 是否建议 Week 12 Day 6 通过 | 建议通过 |

## 6. 执行记录

### 6.1 环境检查

- Python：`Python 3.11.9`
- `OPENAI_BASE_URL`：已设置，未打印真实值
- `OPENAI_MODEL`：已设置，未打印真实值
- `OPENAI_API_KEY`：已设置，未打印真实值
- 后端 smoke 临时注入：`IMAGEPAGE_WORKER_PYTHON_COMMAND=D:\environment\python11\python.exe`

### 6.2 worker-agent 修复摘要

worker-agent 做了以下修复：

1. 将 `week12-v1` prompt 从“直接生成布局中间结构”调整为“视觉清单提取”：优先返回 `texts`、`regions`、`components`。
2. 移除 prompt 中的 `Job ID` / `Image name` 元信息，避免后端保存名 `input.png` 污染模型输出。
3. 降低输出规模：`max_tokens=1200`，`temperature=0.0`。
4. 增强 JSON 解析，对模型偶发的 `},"{"role"` 这类轻微格式错误做最小修复。
5. 增强 intermediate mapper：
   - 支持 `regions` / `texts` / `components`。
   - 支持 top-level `texts`。
   - 支持嵌套 `sections` 和元素内 `elements`。
   - 支持 dashboard metric label/value 自动转成 card。

### 6.3 Worker direct smoke

| sample | status | sourceType | fallbackUsed | durationMs | previewHtml | 关键文本 |
|---|---|---|---:|---:|---:|---|
| `01-simple-card-page.png` | `SUCCESS` | `REAL_AI` | `false` | `16064` | `4457` | 通过 |
| `02-simple-form-page.png` | `SUCCESS` | `REAL_AI` | `false` | `12807` | `4130` | 通过 |
| `03-dashboard-cards-page.png` | `SUCCESS` | `REAL_AI` | `false` | `10794` | `7576` | 通过 |

说明：

- 曾尝试并发跑三张真实模型请求，其中 sample 03 出现一次命令超时。
- 单独顺序执行后 sample 03 正常返回，因此后续真实 AI smoke 建议顺序执行，不建议并发压模型服务。

### 6.4 Backend API smoke

启动方式：

```powershell
cd backend
java -jar target/backend-0.0.1-SNAPSHOT.jar --server.port=18080 --imagepage.worker.timeout-seconds=180
```

上传方式：

```powershell
curl.exe -s -X POST http://127.0.0.1:18080/api/image-page/upload -F "file=@samples/<sample>.png"
curl.exe -s -X POST http://127.0.0.1:18080/api/image-page/jobs/<jobId>/generate
```

首次 generate：

| sample | status | sourceType | fallbackUsed | promptVersion | previewHtml | sections |
|---|---|---|---:|---|---:|---:|
| `01-simple-card-page.png` | `SUCCESS` | `REAL_AI` | `false` | `week12-v1` | `4457` | `3` |
| `02-simple-form-page.png` | `SUCCESS` | `REAL_AI` | `false` | `week12-v1` | `4130` | `4` |
| `03-dashboard-cards-page.png` | `SUCCESS` | `REAL_AI` | `false` | `week12-v1` | `7576` | `6` |

二次 generate：

| sample | artifact.reused | 结果 |
|---|---:|---|
| `01-simple-card-page.png` | `true` | 通过 |
| `02-simple-form-page.png` | `true` | 通过 |
| `03-dashboard-cards-page.png` | `true` | 通过 |

### 6.5 Frontend page smoke

启动方式：

```powershell
cd frontend
set VITE_API_PROXY_TARGET=http://127.0.0.1:18080
npm run dev -- --host 127.0.0.1 --port 5174
```

页面：

```text
http://127.0.0.1:5174/dev/image-to-layout
```

验证样例：

```text
samples/01-simple-card-page.png
```

页面级结果：

| 指标 | 结果 |
|---|---|
| 上传 | 通过 |
| 生成 | 通过 |
| 页面状态 | `REAL_AI 成功` |
| `fallbackUsed` | `false` |
| `sourceType` | `REAL_AI` |
| `layoutJson` 展示 | 通过 |
| `previewHtml` 展示 | 通过 |
| iframe 数量 | `1` |
| iframe `sandbox` | `""` |
| iframe `allow-scripts` | 无 |
| iframe `srcdoc` | 非空，长度约 `4457` |
| iframe `srcdoc` 安全检查 | 未发现 `<script` / `javascript:` |

说明：

- 前端页面级 smoke 只跑了 sample 01。
- 三张样例的真实生成和 artifact 复用已在 Backend API smoke 中覆盖。

### 6.6 测试命令

```powershell
python -m unittest discover -s worker -p "test_*.py"
```

结果：

```text
Ran 80 tests ... OK
```

### 6.7 安全与副产物检查

- 未打印或写入真实 API key。
- 未将真实 API key 写入本文档。
- 临时后端 `18080` 已停止。
- `backend/storage/` 为运行副产物，应继续按忽略规则处理。
- 前端浏览器页面级 iframe 复测已执行。

## 7. tester-agent 结论

Week 12 Day 6：建议通过。

通过部分：

1. Worker 三样例 direct smoke 通过。
2. Backend 三样例 upload -> generate 通过。
3. 三样例均命中 `REAL_AI`。
4. 三样例均 `fallbackUsed=false`。
5. 三样例均输出非空 `previewHtml`。
6. 三样例二次 generate 均命中 `artifact.reused=true`。
7. Worker 单测通过。
8. 未发现密钥泄漏。
9. 前端 `/dev/image-to-layout` 浏览器页面级复测通过。
10. iframe 实际 DOM `sandbox=""` 且无 `allow-scripts`。

后续建议：

1. 如要更严格收口，可由 reviewer-agent 再审查 Worker 质量修复 diff。
2. 后续真实 AI smoke 建议顺序执行，不建议并发压模型服务。

## 8. reviewer-agent 初步检查

- 修改范围集中在 `worker/` 和 smoke 文档，符合本次质量修复方向。
- 未修改 backend / frontend 业务代码。
- 未新增依赖。
- 未放宽安全规则。
- 未提交运行副产物。
- 真实 AI 并发请求仍可能不稳定，后续 smoke 建议顺序执行。
