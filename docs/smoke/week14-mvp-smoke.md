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
| 日期 | 待填写 |
| 执行人 / Agent | tester-agent |
| 分支 | 待填写 |
| 提交 | 待填写 |
| Python | 待填写 |
| 后端端口 | 待填写 |
| 前端端口 | 待填写 |
| 样例图 | 待填写 |
| 模型 | 不写真实 key，只记录模型名 |

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
| 页面可访问 `/dev/image-to-layout` | 待填写 |
| 选择本地图片 | 待填写 |
| 上传成功 | 待填写 |
| 返回 jobId | 待填写 |
| 原图可展示 | 待填写 |

### 2. 触发生成

| 检查项 | 结果 |
|---|---|
| 点击生成 | 待填写 |
| generate 接口返回 | 待填写 |
| `status` | 待填写 |
| `sourceType` | 待填写 |
| `fallbackUsed` | 待填写 |
| `fallbackReason` | 待填写 |
| `promptVersion` | 待填写 |
| `layoutJson.version` | 待填写 |
| `previewHtml` 非空 | 待填写 |

### 3. 预览检查

| 检查项 | 结果 |
|---|---|
| iframe 渲染出现 | 待填写 |
| iframe `sandbox=""` | 待填写 |
| 无 `allow-scripts` | 待填写 |
| 原图 / 生成结果对比可见 | 待填写 |
| FAILED 时有清晰错误说明 | 待填写 |

### 4. 复制检查

| 检查项 | 结果 |
|---|---|
| 复制 HTML | 待填写 |
| 复制 CSS | 待填写 |
| 复制完整 HTML 文档 | 待填写 |
| 复制失败有用户可读提示 | 待填写 |
| 复制内容不包含 API key | 待填写 |

### 5. 下载检查

| 检查项 | 结果 |
|---|---|
| 下载完整 HTML 文件 | 待填写 |
| 下载文件可打开 | 待填写 |
| 下载内容包含生成预览 | 待填写 |
| 下载内容不包含 API key | 待填写 |
| 未生成复杂 ZIP | 待填写 |

### 6. 安全检查

| 检查项 | 结果 |
|---|---|
| 页面无真实 API key | 待填写 |
| artifact 无真实 API key | 待填写 |
| Git diff 无真实 API key | 待填写 |
| previewHtml 无 `<script` | 待填写 |
| previewHtml 无 inline event | 待填写 |
| previewHtml 无 `javascript:` | 待填写 |
| 未提交 `backend/storage/` | 待填写 |
| 未提交 `frontend/dist/` | 待填写 |

### 7. 服务清理

| 检查项 | 结果 |
|---|---|
| 停止 backend | 待填写 |
| 停止 frontend | 待填写 |
| 无本轮残留监听 | 待填写 |

## Smoke 结论

结论：

```text
通过 / 条件通过 / 不通过
```

原因：

```text
待填写
```

## 发现的问题

### 高风险

- 待填写

### 中风险

- 待填写

### 低风险

- 待填写

## 建议修复指派

- frontend-agent：
- backend-agent：
- worker-agent：
- docs-agent：

## Lead 验收结论

```text
通过 / 条件通过 / 不通过
```

说明：

```text
待填写
```
