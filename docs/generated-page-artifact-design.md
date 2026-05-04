# Generated Page Artifact 契约

## 文件目的

本文档定义 Week 04 `generated-page` artifact 的字段、状态、保存方式和失败处理口径。

Week 04 的 `generated-page` 来自确定性规则编译，不是 AI 生成结果。

## artifact 示例

```json
{
  "version": "0.1",
  "artifactType": "generated-page",
  "jobId": "job_001",
  "generator": {
    "name": "layout-static-generator",
    "version": "0.1"
  },
  "source": {
    "layoutVersion": "0.1",
    "layoutHash": "sha256:example",
    "layoutSourceType": "manual"
  },
  "validation": {
    "passed": true,
    "errors": [],
    "warnings": []
  },
  "status": "SUCCESS",
  "htmlCode": "<div class=\"lg-page\">...</div>",
  "cssCode": ".lg-page { box-sizing: border-box; }",
  "vueCode": "<template>...</template>",
  "unsupportedNodes": [],
  "createdAt": "2026-05-04T00:00:00+08:00"
}
```

## 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `version` | 是 | artifact 契约版本，Week 04 使用 `0.1` |
| `artifactType` | 是 | 固定为 `generated-page` |
| `jobId` | 是 | 任务 id，建议只允许字母、数字、下划线、短横线 |
| `generator.name` | 是 | 固定为 `layout-static-generator` |
| `generator.version` | 是 | 静态编译器版本，Week 04 使用 `0.1` |
| `source.layoutVersion` | 是 | 来自 Layout JSON 的 `version` |
| `source.layoutHash` | 是 | Layout JSON 的稳定 hash，用于判断源内容是否变更 |
| `source.layoutSourceType` | 是 | Week 04 默认 `manual` |
| `validation.passed` | 是 | validator 是否通过 |
| `validation.errors` | 是 | validator errors，失败时非空 |
| `validation.warnings` | 是 | validator warning 与 generator warning 合并后的 warning |
| `status` | 是 | `SUCCESS` 或 `FAILED` |
| `htmlCode` | 是 | 可预览 HTML 片段 |
| `cssCode` | 是 | 可预览 CSS 文本 |
| `vueCode` | 是 | Vue 文本展示字段，不要求可运行 |
| `unsupportedNodes` | 是 | 静态编译器未支持的节点列表 |
| `createdAt` | 是 | artifact 创建时间 |

## status 规则

### SUCCESS

满足以下条件时，`status` 为 `SUCCESS`：

- Layout JSON validator 通过。
- 静态编译器能输出非空 `htmlCode`。
- 静态编译器能输出非空 `cssCode`。
- `validation.errors` 为空。

### FAILED

validator 失败时，Week 04 统一采用以下口径：

- CLI 仍输出一份 `status=FAILED` 的 `generated-page` artifact。
- `validation.errors` 非空。
- `validation.passed=false`。
- `htmlCode` 为空字符串。
- `cssCode` 为空字符串。
- `vueCode` 为空字符串。
- 命令退出码为 1。
- 这份 FAILED artifact 只用于调试和记录失败原因，不用于前端可视化预览。

不要同时写“失败时输出 FAILED artifact”和“失败时不写 artifact”两种口径。

## warnings 合并规则

`validation.warnings` 可以包含两类 warning：

- validator warning：来自 `worker/layout_validator.py`。
- generator warning：来自静态编译器，例如未知 style 字段、缺少 image src、暂不支持节点类型。

合并后保持数组结构，建议每条 warning 至少包含：

```json
{
  "code": "UNKNOWN_STYLE_FIELD",
  "message": "style 字段暂不支持",
  "path": "layout.children[0].style.unknown"
}
```

## 后端保存契约

Week 04 后端 mock 保存接口：

```text
PUT /api/dev/generation-jobs/{jobId}/artifacts/generated-page
GET /api/dev/generation-jobs/{jobId}/artifacts/generated-page
```

PUT 请求体提交完整 `generated-page` artifact，不再额外包一层 `generatedPage`：

```json
{
  "version": "0.1",
  "artifactType": "generated-page",
  "jobId": "job_001",
  "generator": {
    "name": "layout-static-generator",
    "version": "0.1"
  },
  "source": {
    "layoutVersion": "0.1",
    "layoutHash": "sha256:example",
    "layoutSourceType": "manual"
  },
  "validation": {
    "passed": true,
    "errors": [],
    "warnings": []
  },
  "status": "SUCCESS",
  "htmlCode": "<div class=\"lg-page\">...</div>",
  "cssCode": ".lg-page { box-sizing: border-box; }",
  "vueCode": "",
  "unsupportedNodes": [],
  "createdAt": "2026-05-04T00:00:00+08:00"
}
```

## 后端 mock 存储约束

- 存储路径：`backend/mock-data/generated-page-artifacts/{jobId}.generated-page.json`。
- Week 04 不连接 MySQL。
- Week 04 不创建数据库表。
- Week 04 不创建 Entity / Mapper。
- `backend/mock-data/` 是本地副产物，不提交 Git。
- `jobId` 使用白名单校验：`^[A-Za-z0-9_-]{1,64}$`。
- 不允许使用路径拼接绕过白名单。
- generated-page artifact JSON 文件大小限制建议为 2MB。

## 前端使用约束

- 前端可以展示 `htmlCode`、`cssCode`、`vueCode` 文本。
- 前端预览只使用 `htmlCode + cssCode`。
- 前端 iframe 必须使用 `sandbox=""`，不加 `allow-scripts`。
- `vueCode` 只作为文本展示，不要求可运行，不要求构建。
