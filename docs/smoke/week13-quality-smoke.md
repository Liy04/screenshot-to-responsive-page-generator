# Week 13 Quality Smoke

## 1. 文件目的

记录 Week 13 三张 samples 的顺序 smoke 结果。

本文件用于记录顺序执行、人工评分和轻量验收，不用于沉淀重型测试系统。

## 2. 顺序规则

Week 13 smoke 默认顺序：

1. `samples/01-simple-card-page.png`
2. `samples/02-simple-form-page.png`
3. `samples/03-dashboard-cards-page.png`

本轮按上述顺序串行执行，没有并发压模型服务。

## 3. 环境

| 项 | 结果 |
|---|---|
| 日期 | 2026-05-25 |
| 执行者 | tester-agent / Codex Lead |
| Python | `D:\environment\python11\python.exe` / Python 3.11.9 |
| 后端端口 | `18080` |
| 前端端口 | `5174` |
| 后端启动参数 | `--imagepage.worker.timeout-seconds=180` |
| 模型 | `Qwen/Qwen3-VL-32B-Instruct` |
| API key | 仅通过环境变量读取，未写入文档 |

## 4. Smoke 结果

### 4.1 samples/01-simple-card-page.png

| 字段 | 记录 |
|---|---|
| 运行顺序 | 1 |
| 评分人 | tester-agent / Codex Lead |
| 评分日期 | 2026-05-25 |
| jobId | `imgjob_972dcfe3cc404b728b6ac63890713dfa` |
| status | `SUCCESS` |
| sourceType | `REAL_AI` |
| fallbackUsed | `false` |
| fallbackReason | `null` |
| 模型 | `Qwen/Qwen3-VL-32B-Instruct` |
| promptVersion | `week12-v1` |
| duration | 约 40.57s |
| previewHtml 非空 | 是，5977 chars |
| layout 节点数 | 22 |
| section 数 | 3 |
| artifact.reused | 首次 `false`，二次 generate `true` |
| iframe 渲染 | 通过，页面实测 1 个 iframe；sandbox=""；无 allow-scripts |
| 安全标记 | 未发现 `<script` / inline event / `<iframe` / `<object` / `<embed` / `javascript:` |
| warnings | 17 |
| 总分 / 35 | 27 |
| 主要缺陷 | 文本与组件清单仍偏通用，局部内容还原不足；warnings 数量偏多。 |

### 4.2 samples/02-simple-form-page.png

| 字段 | 记录 |
|---|---|
| 运行顺序 | 2 |
| 评分人 | tester-agent / Codex Lead |
| 评分日期 | 2026-05-25 |
| jobId | `imgjob_c116552707ed46b89ec5d8f3acc392ac` |
| status | `SUCCESS` |
| sourceType | `REAL_AI` |
| fallbackUsed | `false` |
| fallbackReason | `null` |
| 模型 | `Qwen/Qwen3-VL-32B-Instruct` |
| promptVersion | `week12-v1` |
| duration | 约 53.32s |
| previewHtml 非空 | 是，5394 chars |
| layout 节点数 | 21 |
| section 数 | 4 |
| artifact.reused | 首次 `false`，二次 generate `true` |
| iframe 渲染 | 通过，sandbox iframe 渲染检查通过；无 allow-scripts |
| 安全标记 | 未发现 `<script` / inline event / `<iframe` / `<object` / `<embed` / `javascript:` |
| warnings | 18 |
| 总分 / 35 | 26 |
| 主要缺陷 | 表单语义已出现，但字段层次和输入控件细节仍不够贴近原图；warnings 数量偏多。 |

### 4.3 samples/03-dashboard-cards-page.png

| 字段 | 记录 |
|---|---|
| 运行顺序 | 3 |
| 评分人 | tester-agent / Codex Lead |
| 评分日期 | 2026-05-25 |
| jobId | `imgjob_5d5885f8c0bd405ea5d7591b90504189` |
| status | `SUCCESS` |
| sourceType | `REAL_AI` |
| fallbackUsed | `false` |
| fallbackReason | `null` |
| 模型 | `Qwen/Qwen3-VL-32B-Instruct` |
| promptVersion | `week12-v1` |
| duration | 约 50.31s |
| previewHtml 非空 | 是，11092 chars |
| layout 节点数 | 41 |
| section 数 | 6 |
| artifact.reused | 首次 `false`，二次 generate `true` |
| iframe 渲染 | 通过，sandbox iframe 渲染检查通过；无 allow-scripts |
| 安全标记 | 未发现 `<script` / inline event / `<iframe` / `<object` / `<embed` / `javascript:` |
| warnings | 24 |
| 总分 / 35 | 28 |
| 主要缺陷 | Dashboard 结构和分区更丰富，但细粒度数据与局部视觉仍有漂移；warnings 数量偏多。 |

## 5. 汇总

| 指标 | 结果 |
|---|---|
| 平均分 | 27.0 / 35 |
| 最低分 | 26 / 35 |
| 是否全部顺序通过 | 是 |
| 是否全部命中 REAL_AI | 是 |
| 是否出现 fallback | 否 |
| 是否二次 generate 命中复用 | 是，三张样例二次 generate 均 `artifact.reused=true` |
| previewHtml 是否全部非空 | 是 |
| iframe 是否可渲染 | 是 |
| 是否出现安全问题 | 未发现 |
| 是否建议 Week 13 通过 | 建议通过，达到 25~28 稳定通过线 |

## 6. 验证步骤

1. 启动后端：

```bash
java -jar target/backend-0.0.1-SNAPSHOT.jar --server.port=18080 --imagepage.worker.timeout-seconds=180
```

2. 按顺序执行三张样例：

```text
upload -> generate -> second generate reuse check
```

3. 启动前端：

```bash
npm run dev -- --host 127.0.0.1 --port 5174
```

4. 页面级检查：

- `samples/01-simple-card-page.png` 通过 `/dev/image-to-layout` 实际上传、生成并渲染 iframe。
- 三张样例的 `previewHtml` 均在浏览器环境中创建 sandbox iframe 检查。

5. 安全检查：

- `sandbox=""`
- 无 `allow-scripts`
- 无 `<script`
- 无 inline event
- 无 `<iframe` / `<object` / `<embed`
- 无 `javascript:`

## 7. 结论

Week 13 Day 06 顺序 smoke 通过。

当前结果说明：

- 三张固定样例都可以按顺序完成真实 AI 生成。
- 输出均为 `REAL_AI`，未触发 fallback。
- `previewHtml` 全部非空并可通过 sandbox iframe 渲染。
- 二次 generate 均命中 artifact 复用。
- 平均分 27.0，最低分 26，达到 Week 13 稳定通过线。

剩余风险：

- 评分仍是人工轻量评分，不是视觉回归。
- warnings 数量仍偏多，说明 mapper / compiler 仍有继续优化空间。
- `promptVersion` 当前仍显示 `week12-v1`，后续如要严格区分 Week 13 prompt，可单独调整。
