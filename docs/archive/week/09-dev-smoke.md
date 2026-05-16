# Week 09 Dev Smoke

## 1. 环境准备

- Java 17
- Maven
- Node.js
- Python 3.11+
- 当前已验证 Python 版本：`Python 3.11.9`
- 当前已验证 Python 路径：`D:\environment\python11\python.exe`

## 2. 必需环境变量

PowerShell 示例：

```powershell
$env:OPENAI_BASE_URL="https://api.siliconflow.cn/v1"
$env:OPENAI_MODEL="Qwen/Qwen3-VL-32B-Instruct"
$env:OPENAI_API_KEY="<your-api-key>"
$env:IMAGEPAGE_WORKER_PYTHON_COMMAND="D:\environment\python11\python.exe"
```

注意：

- 不写入真实 `OPENAI_API_KEY`
- `OPENAI_API_KEY` 只通过环境变量提供

## 3. backend 启动命令

```powershell
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar --imagepage.worker.timeout-seconds=120
```

说明：

- 真实多模态调用建议 120 秒
- 默认 30 秒不适合 Week 09 REAL_AI smoke

## 4. frontend 启动命令

```powershell
cd frontend
npm run dev
```

## 5. Worker 直接 smoke 命令

```powershell
& "D:\environment\python11\python.exe" worker/main.py --job-id job_demo --image-path storage/temp/job_demo/input.png --mode real-ai --fallback true
```

## 6. backend API smoke 步骤

1. 调 `POST /api/image-page/upload` 上传单张真实图片
2. 记录返回的 `jobId`、`fileName`、`sourceUrl`
3. 调 `GET /api/image-page/jobs/{jobId}/source` 验证原图可访问
4. 调 `POST /api/image-page/jobs/{jobId}/generate`
5. 检查返回的 `status`、`mode`、`fallbackUsed`、`sourceType`、`layoutJson.version`、`validation.ok`、`previewHtml`

## 7. frontend 页面 smoke 步骤

1. 打开 `/dev/image-to-layout`
2. 选择一张真实图片
3. 确认原图预览正常
4. 执行上传和生成
5. 检查页面能展示 Layout JSON
6. 检查页面能展示 `previewHtml`
7. 检查 iframe 能正常渲染结果

## 8. REAL_AI 通过标准

- `HTTP 200`
- `status=SUCCESS`
- `mode=real-ai`
- `fallbackUsed=false`
- `sourceType=REAL_AI`
- `layoutJson.version=0.1`
- `validation.ok=true`
- `previewHtml` 非空
- 页面 iframe 渲染成功

## 8A. 最终 smoke 结果

Week 09 最终 smoke 已通过，最终确认口径如下：

- 真实图片上传成功
- 后端成功调用 Python Worker
- Worker 成功调用 SiliconFlow Qwen3-VL
- `REAL_AI` 命中
- `sourceType=REAL_AI`
- `fallbackUsed=false`
- `layoutJson.version=0.1`
- `validation.ok=true`
- `previewHtml` 非空
- 前端页面 iframe 正常渲染
- iframe 使用 `sandbox=""`
- 运行时代码中未发现 `allow-scripts`

## 9. fallback 可接受但需说明的标准

以下情况可以继续记录为“可接受但未命中 REAL_AI”：

- `status=SUCCESS`
- `mode=fallback-rule` 或等价口径
- `fallbackUsed=true`
- 仍能返回合法 Layout JSON v0.1
- 仍能返回可预览的 `previewHtml`

但这类结果不能算作 Week 09 真实 AI 命中成功，需要单独注明原因。

## 10. iframe 安全检查

- iframe 必须使用 `sandbox=""`
- 不允许 `allow-scripts`
- 预览内容中不得出现可执行脚本

## 11. 常见问题

### OPENAI_* 未设置

- 现象：generate 失败或直接 fallback
- 检查：`OPENAI_BASE_URL`、`OPENAI_MODEL`、`OPENAI_API_KEY`

### Python 版本错误

- 现象：Worker 启动失败或依赖不兼容
- 检查：是否使用 Python 3.11+
- 当前已验证版本：`3.11.9`

### 30 秒超时

- 现象：backend 调 Worker 超时，REAL_AI 无法命中
- 处理：使用 `--imagepage.worker.timeout-seconds=120`

### 图片损坏

- 现象：Worker 无法读取图片，可能 fallback 或直接失败
- 处理：更换合法图片重新验证

### fallbackUsed=true

- 现象：接口成功但未命中真实 AI
- 处理：检查 `OPENAI_*`、Python 路径、超时时间、模型可用性，并记录为 fallback 成功而非 REAL_AI 成功

## 12. 最终复测配置摘要

- Python：`D:\environment\python11\python.exe`
- Python 版本：`3.11.9`
- backend 启动参数：`--imagepage.worker.timeout-seconds=120`
- 环境变量：
  - `OPENAI_BASE_URL=https://api.siliconflow.cn/v1`
  - `OPENAI_MODEL=Qwen/Qwen3-VL-32B-Instruct`
  - `OPENAI_API_KEY` 仅通过环境变量提供，文档不写真实值
  - `IMAGEPAGE_WORKER_PYTHON_COMMAND=D:\environment\python11\python.exe`
