# Week 14 MVP Smoke

## 文件目的

记录 Week 14 MVP 产品化交付闭环 smoke。

目标不是评估复杂页面还原质量，而是确认用户能完成：

```text
上传截图 -> 生成 -> 预览 -> 复制 -> 下载
```

## 前置条件

- 当前在项目根目录。
- Python 使用 3.11+，建议 `D:\environment\python11\python.exe`。
- `OPENAI_BASE_URL` 已通过环境变量设置。
- `OPENAI_MODEL` 已通过环境变量设置。
- `OPENAI_API_KEY` 已通过环境变量设置，但不得打印、写入文档或提交。
- 后端启动时使用足够 timeout，建议 `--imagepage.worker.timeout-seconds=180`。
- 前端 dev server 可访问。
- 使用公开安全样例图或本地非敏感截图。

## 禁止事项

- 不写入真实 API key。
- 不提交私人截图、账号信息、公司资料、密钥或敏感页面。
- 不提交 `backend/storage/`。
- 不提交 `frontend/dist/`。
- 不把 smoke 变成 Playwright 视觉回归系统。
- 不接 MySQL / Figma / 编辑器 / ZIP 复杂实现。

## 环境记录

| 项 | 记录 |
|---|---|
| 日期 | 2026-05-28 |
| 执行人 / Agent | tester-agent |
| 分支 | main |
| 提交 | c23a198 |
| Python | 3.11.9 |
| 后端端口 | 8080 |
| 前端端口 | 5173 |
| 样例图 | `samples/01-simple-card-page.png`，公开安全样例图，24,506 bytes |
| 模型 | `Qwen/Qwen3-VL-32B-Instruct` |

## 启动命令

### Backend

```powershell
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar --imagepage.worker.timeout-seconds=180
```

### Frontend

```powershell
cd frontend
npm run dev
```

## Smoke 步骤

### 1. 上传图片

| 检查项 | 结果 |
|---|---|
| 页面可访问 `/dev/image-to-layout` | 通过，HTTP 200 |
| 选择本地图片 | 通过，使用 `samples/01-simple-card-page.png` |
| 上传成功 | 通过 |
| 返回 jobId | 通过，页面已返回并显示 |
| 原图可展示 | 通过 |

### 2. 触发生成

| 检查项 | 结果 |
|---|---|
| 点击生成 | 通过 |
| generate 接口返回 | 通过，HTTP 200 |
| `status` | `SUCCESS` |
| `sourceType` | `REAL_AI` |
| `fallbackUsed` | `false` |
| `fallbackReason` | 无 |
| `promptVersion` | `week12-v1` |
| `layoutJson.version` | `0.1` |
| `previewHtml` 非空 | 通过 |

### 3. 预览检查

| 检查项 | 结果 |
|---|---|
| iframe 渲染出现 | 通过 |
| iframe `sandbox=""` | 通过 |
| 无 `allow-scripts` | 通过 |
| 原图 / 生成结果对比可见 | 通过 |
| FAILED 时有清晰错误说明 | 未触发，本轮为 `SUCCESS`；已有状态展示保留 |

### 4. 复制检查

| 检查项 | 结果 |
|---|---|
| 复制 HTML | 通过 |
| 复制 CSS | 通过 |
| 复制完整 HTML 文档 | 通过 |
| 复制失败有用户可读提示 | 未触发，成功路径通过 |
| 复制内容不包含 API key | 通过 |

### 5. 下载检查

| 检查项 | 结果 |
|---|---|
| 下载完整 HTML 文件 | 通过 |
| 下载文件可打开 | 通过 |
| 下载内容包含生成预览 | 通过 |
| 下载内容不包含 API key | 通过 |
| 未生成复杂 ZIP | 通过 |

### 6. 安全检查

| 检查项 | 结果 |
|---|---|
| 页面无真实 API key | 通过 |
| artifact 无真实 API key | 通过 |
| Git diff 无真实 API key | 通过 |
| previewHtml 无 `<script` | 通过 |
| previewHtml 无 inline event | 通过 |
| previewHtml 无 `javascript:` | 通过 |
| 未提交 `backend/storage/` | 通过 |
| 未提交 `frontend/dist/` | 通过 |

### 7. 服务清理

| 检查项 | 结果 |
|---|---|
| 停止 backend | 通过 |
| 停止 frontend | 通过 |
| 无本轮残留监听 | 通过 |

## Smoke 结论

结论：

```text
通过
```

原因：

```text
Week 14 MVP smoke 完成上传、真实 AI 生成、预览、复制、下载、安全检查和服务清理闭环。
```

## 发现的问题

### 高风险

- 无

### 中风险

- 无

### 低风险

- `promptVersion` 返回 `week12-v1`，与旧示例版本不同，但不影响 Week 14 交付闭环验收。
- 真实 AI 成功依赖环境变量、网络和模型服务可用性。

## 建议修复指派

- 无阻塞修复。
- 如后续要改善 `promptVersion` 命名一致性，可交给 worker-agent / docs-agent 评估；不是 Day 06 阻塞。

## Lead 验收结论

```text
通过
```

说明：

```text
tester-agent smoke 通过；reviewer-agent 复审无 Blocker，确认 smoke 结果已记录。`docs/agents/lead.md` 另有既有规则补丁，不属于 Day 06 smoke 越界修改。
```
