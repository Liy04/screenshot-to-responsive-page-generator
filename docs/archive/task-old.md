# Task

## 当前任务

Week 07 Day 4：实现 image-layout dev mock API。

线程：后端开发线程。

## 任务目标

新增后端 image-layout dev mock job API，用 Java 侧 mock 模板或固定 mock 数据，根据 `imageName + templateKey` 创建 image-layout mock job，并支持按 `jobId` 查询。

本日不接 MySQL，不创建 Entity / Mapper，不上传真实图片，不调用 Python Worker。

## 必须完成

1. 新增接口：
   - `POST /api/dev/image-layout-jobs`
   - `GET /api/dev/image-layout-jobs/{jobId}`
2. POST 请求体只接收：
   - `imageName`
   - `templateKey`
3. 后端生成 `jobId`。
4. 返回结构必须使用现有 `ApiResponse` 包装。
5. 支持 `landing-basic`。
6. 支持 `card-list`。
7. 支持 `invalid-layout` 作为已知失败测试模板。
8. unknown `templateKey` 返回 400。
9. GET 已存在 job 返回对应 job。
10. GET 不存在 job 返回 404。
11. 不影响已有 generated-page artifact 接口。

## 响应口径

成功响应必须符合现有 `ApiResponse`：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "img-layout-001",
    "status": "SUCCESS",
    "sourceType": "IMAGE_TEMPLATE_MOCK",
    "imageName": "demo-home.png",
    "templateKey": "landing-basic",
    "layoutArtifact": {
      "status": "SUCCESS",
      "layoutJson": {}
    },
    "errors": [],
    "warnings": []
  }
}
```

错误响应使用现有 `ApiResponse.error` 口径：

```json
{
  "code": 400,
  "message": "Unknown templateKey: unknown-template",
  "data": null
}
```

## 参数校验

需要校验：

- body 不能为空。
- body 不能是 array。
- `imageName` 不能为空。
- `imageName` 不能过长。
- `templateKey` 不能为空。
- `templateKey` 必须是已支持模板。

## 禁止事项

- 不修改 `frontend/`。
- 不修改 `worker/`。
- 不接真实 AI。
- 不接 Figma API / Figma MCP。
- 不接 MySQL。
- 不创建数据库表。
- 不创建 Entity / Mapper。
- 不新增数据库配置。
- 不接 Redis / RabbitMQ。
- 不上传真实图片到后端。
- 不做图片文件持久化。
- 不调用 Python Worker。
- 不做 Worker HTTP 服务。
- 不做 ZIP 导出。
- 不做拖拽编辑器 / 在线编辑器。
- 不做真实截图解析。
- 不改变已有 generated-page artifact 接口路径。

## 建议读取文件

- `AGENTS.md`
- `docs/current.md`
- `docs/tasks/day-04.md`
- `docs/spec.md`
- `backend/src/main/java/com/screenshot/generator/backend/common/ApiResponse.java`
- `backend/src/main/java/com/screenshot/generator/backend/layout/*`
- 已有 generated-page artifact controller / service / mock storage 代码

## 建议修改文件

建议新增或修改后端 image-layout 相关文件，例如：

- `backend/src/main/java/com/screenshot/generator/backend/layout/ImageLayoutJobController.java`
- `backend/src/main/java/com/screenshot/generator/backend/layout/ImageLayoutJobService.java`
- `backend/src/main/java/com/screenshot/generator/backend/layout/ImageLayoutJobRequest.java`
- `backend/src/main/java/com/screenshot/generator/backend/layout/ImageLayoutJobResponse.java`

具体文件可按现有后端结构决定。

不要修改：

- `frontend/`
- `worker/`
- 数据库相关代码

## 验收标准

- POST 可以创建 image-layout mock job。
- GET 可以查询已创建 job。
- unknown `templateKey` 返回 400。
- 不存在 job 返回 404。
- `invalid-layout` 作为已知模板返回失败状态或错误展示结构。
- 响应结构使用 `ApiResponse` 包装。
- 不影响原有 generated-page artifact 接口。
- 没有新增数据库相关代码。
- 没有新增 Entity / Mapper。
- 未修改前端。
- 未修改 Worker。

## 验证建议

本日可运行后端编译或测试：

```bash
mvn test
```

完整 API 测试放到 Day 5。

## Codex 执行要求

先输出后端实现计划，等待确认后再修改代码。完成后输出修改文件、接口说明、验证命令、验证结果、是否接触数据库相关内容、风险和未完成项。
