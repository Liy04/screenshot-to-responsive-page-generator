# Layout JSON Mock API Contracts

## 文件目的

本文档记录 Week 03 P1 mock 保存 / 查询 Layout JSON 的接口契约。

Week 03 默认不落库，不连接 MySQL，不新增 Entity / Mapper，不新增数据库配置。

## P1 范围

P1 只在 P0 全部完成后考虑。

接口使用本地文件 mock：

```text
mock-data/layout-artifacts/{jobId}.layout.json
```

## 通用响应结构

继续使用统一 `ApiResponse`：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

错误响应：

```json
{
  "code": 400,
  "message": "错误说明",
  "data": null
}
```

## PUT /api/dev/generation-jobs/{jobId}/artifacts/layout-json

### 作用

把 Layout JSON 保存到本地 mock 文件。

### 请求

```http
PUT /api/dev/generation-jobs/job_001/artifacts/layout-json
Content-Type: application/json
```

```json
{
  "layoutJson": {},
  "status": "created",
  "errorMessage": null
}
```

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "job_001",
    "artifactType": "layout_json",
    "mockPath": "mock-data/layout-artifacts/job_001.layout.json",
    "status": "created"
  }
}
```

## GET /api/dev/generation-jobs/{jobId}/artifacts/layout-json

### 作用

从本地 mock 文件读取 Layout JSON。

### 请求

```http
GET /api/dev/generation-jobs/job_001/artifacts/layout-json
```

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "job_001",
    "artifactType": "layout_json",
    "layoutJson": {},
    "status": "created",
    "errorMessage": null
  }
}
```

## 错误状态码

| 场景 | HTTP 状态码 |
|---|---:|
| 请求体为空或 Layout JSON 为空 | 400 |
| 本地 mock 文件不存在 | 404 |
| 本地文件读写失败 | 500 |

## 实现边界

允许：

- DTO。
- Controller。
- MockStorageService。
- 本地 mock 文件读写。

不允许：

- MySQL 实际落库。
- Entity / Mapper。
- MyBatis-Plus 持久层代码。
- Redis / RabbitMQ。
- 真实 AI 或 Figma 接入。
