# Real AI Smoke

## 文件目的

本文档记录 Week 11 真实 AI 链路 smoke 的可复现执行方式、环境变量、安全边界和验收口径。

真实 AI smoke 会依赖外部模型服务和网络。执行前必须确认本机环境、公开安全样例图、后端启动参数和密钥来源；失败时要区分网络、模型、JSON、fallback、后端、前端、artifact 复用等不同问题。

## 安全边界

- `OPENAI_API_KEY` 必须通过环境变量设置，禁止写入仓库、脚本、文档、日志或 artifact。
- 不提交 `backend/storage/`、`frontend/dist/`、真实隐私截图、真实 key 或其他运行副产物。
- 只使用 `samples/` 下公开安全、可提交的 mock UI 图片。
- 不使用客户页面、公司内部页面、账号信息、私人截图、真实头像、密钥、二维码或版权不清素材。
- 检查 key 时只能确认“是否存在”，不能打印真实值。

## 推荐环境

| 项 | 推荐值 |
|---|---|
| Python | `3.11.9` |
| `OPENAI_BASE_URL` | `https://api.siliconflow.cn/v1` |
| `OPENAI_MODEL` | `Qwen/Qwen3-VL-32B-Instruct` |
| `IMAGEPAGE_WORKER_PYTHON_COMMAND` | `D:\environment\python11\python.exe` |
| 后端 worker timeout | `120` 秒 |

PowerShell 环境变量示例：

```powershell
$env:OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"
$env:OPENAI_MODEL = "Qwen/Qwen3-VL-32B-Instruct"
$env:OPENAI_API_KEY = "<set-your-key-here>"
$env:IMAGEPAGE_WORKER_PYTHON_COMMAND = "D:\environment\python11\python.exe"
```

提交前不要把真实 key 写入任何文件。上面的 `OPENAI_API_KEY` 只能作为本地 shell 临时占位示例。

## 推荐输入

优先使用 `samples/README.md` 中的公开安全样例图，推荐顺序：

1. `samples/01-simple-card-page.png`
2. `samples/02-simple-form-page.png`
3. `samples/03-dashboard-cards-page.png`

先跑 `01-simple-card-page.png`，确认最小链路可用后，再跑表单和 dashboard 场景。

## 后端启动

真实 AI smoke 推荐后端启动时显式设置 worker timeout 为 120 秒。默认 30 秒不适合真实多模态调用。

示例：

```powershell
cd backend
java -jar target/backend-0.0.1-SNAPSHOT.jar --imagepage.worker.timeout-seconds=120
```

也可以使用项目当前可用的本地启动方式，但必须保证等效配置生效：

```text
imagepage.worker.timeout-seconds=120
```

## 示例流程

可参考 `scripts/smoke-real-ai.example.ps1`。该脚本是可选示例，默认不执行真实联网 generate，需要用户确认环境后再运行。

手动 smoke 的核心步骤：

1. 设置 `OPENAI_BASE_URL`、`OPENAI_MODEL`、`OPENAI_API_KEY`、`IMAGEPAGE_WORKER_PYTHON_COMMAND`。
2. 使用 Python 3.11.9，并确认 `IMAGEPAGE_WORKER_PYTHON_COMMAND` 指向可用解释器。
3. 启动后端，并设置 `--imagepage.worker.timeout-seconds=120`。
4. 上传 `samples/01-simple-card-page.png`。
5. 对返回的 `jobId` 调用 generate。
6. 检查响应状态、metadata、artifact 文件和前端预览。
7. 使用同一 `jobId` 第二次调用 generate，确认 artifact 复用。

真实链路接口：

```text
POST /api/image-page/upload
GET  /api/image-page/jobs/{jobId}/source
POST /api/image-page/jobs/{jobId}/generate
```

## 结果判断

### REAL_AI

满足以下条件时，可判定为 `REAL_AI`：

- 后端 generate 响应成功。
- `status=SUCCESS`。
- `sourceType=REAL_AI` 或等效字段显示真实 AI 模式。
- `mode=real-ai` 或 metadata 中显示真实 AI 模式。
- `fallbackUsed=false`。
- `layoutJson.version=0.1`。
- validator 通过，例如 `validation.ok=true` 或无 validation errors。
- `previewHtml` 非空。
- 前端 iframe 可展示预览，且 iframe 使用 `sandbox=""`，不包含 `allow-scripts`。

### FALLBACK

满足以下任一情况时，应判定为 `FALLBACK`：

- generate 响应成功，但 `fallbackUsed=true`。
- `sourceType`、`mode` 或 metadata 显示 fallback。
- `fallbackReason` 非空。
- `warnings` 或 `errors` 表明模型不可用、JSON 解析失败、schema 校验失败、图片读取失败、worker timeout 或预览编译失败，但系统仍返回可展示的 fallback layout / preview。

常见 `fallbackReason`：

- `MODEL_UNAVAILABLE`
- `MODEL_NON_JSON_OUTPUT`
- `JSON_PARSE_FAILED`
- `SCHEMA_VALIDATION_FAILED`
- `IMAGE_READ_FAILED`
- `WORKER_TIMEOUT`
- `PREVIEW_COMPILE_FAILED`

### FAILED

满足以下任一情况时，应判定为 `FAILED`：

- 上传失败、generate HTTP 失败或后端返回错误。
- Worker 进程启动失败、Python 路径错误或超时后没有 fallback 结果。
- `status=FAILED`。
- `layoutJson` 缺失或不是 v0.1。
- `previewHtml` 为空且没有可接受的 fallback 预览。
- artifact 文件缺失或无法读取。
- 前端无法加载结果，且问题不是单纯的视觉质量差异。

## Artifact 检查

真实 AI generate 成功后，同一 `jobId` 的本地 artifact 至少应包含：

```text
layout.json
preview.html
metadata.json
```

检查方式：

- `layout.json`：确认存在、可解析为 JSON、`version=0.1`、根节点字段为 `layout`，并包含 warnings / assumptions 等必要结构。
- `preview.html`：确认存在、非空，不包含 `script`、`onload`、`onerror`、`onclick`、`iframe`、`object`、`embed` 或 `javascript:`。
- `metadata.json`：确认存在、可解析为 JSON，检查 `promptVersion`、`sourceType` / `mode`、`fallbackUsed`、`fallbackReason`、`warnings`、`errors`、`artifact` 等字段。

artifact 通常位于后端本地存储目录下。`backend/storage/` 是运行副产物，不提交到仓库。

## jobId 复用检查

同一 `jobId` 已存在成功 artifact 时，第二次 generate 不应重复调用真实 AI，应命中本地 artifact。

检查步骤：

1. 上传样例图并记录返回的 `jobId`。
2. 第一次调用 `POST /api/image-page/jobs/{jobId}/generate`，确认生成成功。
3. 检查 `layout.json`、`preview.html`、`metadata.json` 已生成。
4. 第二次使用同一个 `jobId` 调用 generate。
5. 检查响应或 `metadata.json` 中的 `artifact.reused=true`。

如果第二次 generate 没有 `artifact.reused=true`，应记录为 artifact 复用问题，而不是简单归类为模型质量问题。

## 失败排查分类

真实 AI smoke 失败时，先按以下类别归因：

| 类别 | 典型表现 | 检查点 |
|---|---|---|
| 网络问题 | 请求外部模型服务超时、连接失败、DNS / TLS 异常 | 网络连通性、代理、供应商状态、timeout |
| 模型问题 | 模型不可用、鉴权失败、额度不足、返回非预期内容 | `OPENAI_BASE_URL`、`OPENAI_MODEL`、key 是否存在、供应商错误码 |
| JSON 问题 | 模型返回非 JSON、JSON parse failed、repair 后仍失败 | Worker errors、`fallbackReason=JSON_PARSE_FAILED` 或 `MODEL_NON_JSON_OUTPUT` |
| fallback 问题 | 进入 fallback 但原因不清或 fallback 结果不可展示 | `fallbackUsed`、`fallbackReason`、warnings、errors |
| 后端问题 | 上传失败、generate 接口失败、jobId 无效、Worker 调用失败 | 后端日志、HTTP 状态、timeout 配置、Python 命令 |
| 前端问题 | 后端成功但页面不展示、iframe 异常、状态展示错误 | 浏览器控制台、接口响应、iframe sandbox、安全过滤 |
| artifact 问题 | 文件缺失、内容为空、metadata 字段缺失 | `layout.json`、`preview.html`、`metadata.json` |
| artifact 复用问题 | 同一 `jobId` 第二次 generate 未命中复用 | `artifact.reused=true`、后端日志、metadata |

## 提交前检查

- 文档和脚本中没有真实 `OPENAI_API_KEY`。
- 没有提交 `backend/storage/`。
- 没有提交 `frontend/dist/`。
- 没有提交真实隐私截图或公司内部截图。
- example 脚本不会默认执行真实联网 smoke。
- smoke 结果能明确归类为 `REAL_AI`、`FALLBACK` 或 `FAILED`。
