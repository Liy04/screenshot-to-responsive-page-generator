# API Contracts

## 文件目的

本文档记录 Week 02 MVP 最小闭环开发的接口契约。

接口契约以本文档为准；周执行安排以 `docs/week/02-plan.md` 为准；实际进度以 `docs/week/02-status.md` 为准。

## Week 02 范围边界

本周只做 4 个接口：

| 接口 | 方法 | 作用 | 本周实现方式 |
|---|---:|---|---|
| `/api/assets/upload` | POST | 上传截图 | 保存到本地 `backend/uploads/` |
| `/api/generations` | POST | 创建生成任务 | 内存创建 job |
| `/api/generations/{jobId}` | GET | 查询任务状态 | mock 状态 |
| `/api/generations/{jobId}/result` | GET | 获取生成结果 | 返回 mock 代码 |

本周不创建数据库表、不创建 Mapper、不创建 Entity、不引入 MySQL 实际落库。

本周可以使用 DTO / VO，让接口入参和返回结构更清晰。

## 通用响应结构

建议统一响应结构：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

错误响应结构：

```json
{
  "code": 400,
  "message": "错误说明",
  "data": null
}
```

## 错误状态码

| 场景 | HTTP 状态码 | 示例 |
|---|---:|---|
| 请求参数错误、文件类型不支持、文件为空、文件过大 | 400 | 上传 txt 文件 |
| 资源不存在 | 404 | 查询不存在的 `assetId` / `jobId` |
| 服务端未知异常 | 500 | 文件保存失败、未捕获异常 |

## 静态资源访问

后端需要明确 `/uploads/**` 静态资源映射：

```text
backend/uploads/              本地上传文件目录
/uploads/**                   浏览器可访问的静态资源路径
```

示例：

```text
backend/uploads/asset_001.png
↓
http://127.0.0.1:8080/uploads/asset_001.png
```

`backend/uploads/` 必须加入 `.gitignore`，不提交用户上传图片或测试上传文件。

## POST /api/assets/upload

### 请求

```http
POST /api/assets/upload
Content-Type: multipart/form-data

file: screenshot.png
```

### 支持格式

| 格式 | 是否支持 |
|---|---|
| PNG | 支持 |
| JPG / JPEG | 支持 |
| WebP | 支持 |
| GIF | 不支持 |
| PDF | 不支持 |
| TXT | 不支持 |

### 校验规则

- 文件不能为空。
- 文件大小不能超过 10MB。
- 文件类型必须是 PNG / JPG / JPEG / WebP。
- 文件名需要避免直接使用用户原始文件名作为最终存储名。
- 上传成功后返回 `assetId`。

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "assetId": "asset_001",
    "fileName": "screenshot.png",
    "fileUrl": "/uploads/asset_001.png",
    "contentType": "image/png",
    "size": 123456
  }
}
```

### 错误响应

HTTP 状态码：`400`

```json
{
  "code": 400,
  "message": "只支持 PNG、JPG、JPEG、WebP 图片",
  "data": null
}
```

### curl 示例

```bash
curl -X POST http://127.0.0.1:8080/api/assets/upload -F "file=@你的本地图片路径.png"
```

## POST /api/generations

### 请求

```http
POST /api/generations
Content-Type: application/json
```

```json
{
  "assetId": "asset_001",
  "mode": "screenshot",
  "targetStack": "vue3-css",
  "responsive": true
}
```

### 字段说明

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| assetId | string | 是 | 上传截图后返回的资源 ID |
| mode | string | 是 | 第二周固定为 `screenshot` |
| targetStack | string | 是 | 第二周固定为 `vue3-css` |
| responsive | boolean | 是 | 是否生成响应式 mock 结果 |

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "job_001",
    "status": "success"
  }
}
```

### 本周处理逻辑

第二周为了快速闭环，可以直接返回 `success`，不做真实异步队列：

```text
校验 assetId 是否存在
↓
创建 jobId
↓
写入内存 Map
↓
状态设置为 success
↓
返回 jobId
```

内存 Map 数据在后端服务重启后会丢失，这是 Week 02 可接受限制。

## GET /api/generations/{jobId}

### 请求

```http
GET /api/generations/job_001
```

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "job_001",
    "assetId": "asset_001",
    "mode": "screenshot",
    "status": "success",
    "progress": 100,
    "createdAt": "2026-04-28 20:00:00"
  }
}
```

### 状态设计

```text
pending   待处理
running   生成中
success   成功
failed    失败
```

第二周可以直接返回 `success`，但字段设计要保留后续扩展空间。

### 错误响应

HTTP 状态码：`404`

```json
{
  "code": 404,
  "message": "任务不存在",
  "data": null
}
```

## GET /api/generations/{jobId}/result

### 请求

```http
GET /api/generations/job_001/result
```

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": "job_001",
    "artifactId": "artifact_001",
    "layoutJson": {
      "pageName": "MockLandingPage",
      "layoutType": "landing",
      "sections": [
        {
          "id": "hero",
          "type": "hero",
          "title": "Mock 页面标题",
          "description": "这是一个模拟生成结果",
          "buttonText": "立即开始"
        }
      ]
    },
    "vueCode": "<template>\\n  <main class=\"generated-page\">\\n    <section class=\"hero-section\">\\n      <h1>Mock 页面标题</h1>\\n      <p>这是一个模拟生成结果</p>\\n      <button>立即开始</button>\\n    </section>\\n  </main>\\n</template>",
    "cssCode": ".generated-page { min-height: 100vh; }\\n.hero-section { padding: 64px 24px; text-align: center; }"
  }
}
```

这里的 `layoutJson`、`vueCode` 和 `cssCode` 是 mock 数据，不代表真实截图解析结果。

### 错误响应

HTTP 状态码：`404`

```json
{
  "code": 404,
  "message": "任务不存在",
  "data": null
}
```

## 后端实现边界

允许：

- Controller。
- Service。
- 内存模型。
- DTO / VO。
- 统一 `ApiResponse`。
- 本地上传目录。
- `/uploads/**` 静态资源映射。

不允许：

- Entity。
- Mapper。
- 数据库表。
- 数据库配置。
- MySQL 实际落库。
- Redis / RabbitMQ。
- 真实模型 API。
- Figma API / Figma MCP。

