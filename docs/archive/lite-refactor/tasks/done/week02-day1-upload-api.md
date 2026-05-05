# Week 02 Day 1：后端上传接口

## 任务目标

实现截图上传接口，让前端可以上传图片，并获得可用于后续创建任务的 `assetId` 和静态访问路径。

## 必须完成

- 实现 `POST /api/assets/upload`。
- 将图片保存到 `backend/uploads/`。
- 配置 `/uploads/**` 静态资源映射。
- 校验文件为空、文件大小和文件类型。
- 成功返回 `assetId`、`fileName`、`fileUrl`、`contentType`、`size`。
- 补充或确认 curl 验证方式：

```bash
curl -X POST http://127.0.0.1:8080/api/assets/upload -F "file=@你的本地图片路径.png"
```

## 禁止事项

- 不创建生成任务接口。
- 不接 MySQL。
- 不创建数据库表。
- 不新增 Mapper。
- 不新增 Entity 或实体表映射。
- 不接 Redis / RabbitMQ。
- 不接真实模型 API。
- 不接 Figma API / Figma MCP。
- 不做真实截图解析。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week02-day1-upload-api.md`
- `docs/api-contracts.md`
- `docs/coding-rules.md`
- `backend/` 中与接口、配置、统一响应相关的代码

## 建议修改文件

- `backend/` 中上传接口相关 Controller / Service / DTO / VO / 配置文件。
- `tests/smoke/README.md`，仅在需要补充上传接口验证说明时修改。

## 验收标准

- 上传 PNG / JPG / JPEG / WebP 成功。
- 上传空文件、超大文件或不支持类型时返回明确错误。
- 成功响应结构与 `docs/api-contracts.md` 一致。
- 上传成功后可以通过 `/uploads/**` 访问文件。
- `mvn package -DskipTests` 通过。

## Codex 执行要求

- 先输出计划，等待确认后再编码。
- 计划中说明是否涉及 Controller、Service、Mapper、DTO、VO；未涉及的层也要写明。
- 编码后执行最小验证。
- 不修改 `frontend/`、`worker/` 业务代码。
- 不提交 `backend/uploads/` 内上传文件。
