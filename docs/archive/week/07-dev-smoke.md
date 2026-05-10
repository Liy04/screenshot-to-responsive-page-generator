# Week 07 Dev Smoke

## 1. 目标

验证 Week 07 的 image-to-layout mock 链路可复现、可演示、可验收：

```text
本地选择图片
-> 浏览器本地预览
-> 选择 templateKey
-> 创建 image-layout mock job
-> 返回 mock Layout JSON
-> 前端展示 Layout JSON / errors / warnings
```

本链路只做 mock / 本地验证，不接真实 AI、不接 Figma、不接 MySQL。

## 2. 前置条件

- Java 17
- Maven
- Node.js
- Python 3.11 或兼容的本地验证环境
- 当前不接真实 AI / Figma / MySQL / Redis / RabbitMQ
- 后端 image-layout API 仅使用 Java 侧 mock
- Worker resolver 仅作为离线 mock

## 3. Worker 验证命令

```bash
python -m unittest worker.test_layout_validator worker.test_layout_static_generator
```

## 4. 后端测试命令

```bash
mvn test
```

## 5. 前端构建与测试命令

```bash
cd frontend
npm run test
npm run build
```

## 6. 后端启动方式

优先使用 jar：

```bash
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

如 8080 被占用，可使用备用端口：

```bash
cd backend
java -jar target/backend-0.0.1-SNAPSHOT.jar --server.port=18080
```

## 7. 前端启动方式

默认情况：

```bash
cd frontend
npm run dev
```

如后端改为备用端口 18080，前端代理也要同步切换：

```powershell
cd frontend
$env:VITE_API_PROXY_TARGET='http://127.0.0.1:18080'
npm run dev
```

## 8. API smoke 示例

### 8.1 创建 mock job

```bash
curl.exe -X POST http://localhost:8080/api/dev/image-layout-jobs ^
  -H "Content-Type: application/json" ^
  -d "{\"imageName\":\"demo-home.png\",\"templateKey\":\"landing-basic\"}"
```

### 8.2 查询 mock job

```bash
curl.exe http://localhost:8080/api/dev/image-layout-jobs/img-layout-001
```

### 8.3 备用端口示例

如果后端使用 18080，上传 / 查询地址也要改成同一个端口。

## 9. 页面访问路径

- 前端任务详情页：用于查看 generated-page / image-layout 相关展示
- 独立页面：`/dev/image-to-layout`

## 10. 验收点

### SUCCESS

- `status=SUCCESS`
- 展示 `Layout JSON`
- 展示 `errors`
- 展示 `warnings`
- 展示 `source`
- 展示 `templateKey`
- 展示 `jobId`
- iframe 使用 `sandbox=""`
- iframe 不包含 `allow-scripts`

### FAILED

- `status=FAILED`
- 不展示 iframe
- 只展示失败原因和 `validation` / 错误信息

### HTTP 口径

- `invalid-layout` 返回 `200 + FAILED`
- `unknown-template` 返回 `400`
- 不存在 `jobId` 返回 `404`

## 11. Day 7A 实际验收结果

根据项目经理验收结果，Week 07 Day 7A 已通过：

1. Worker 全量相关测试通过：45 tests OK。
2. 后端测试通过：20 tests, 0 failures。
3. 前端构建通过：`npm run build`。
4. 前端测试通过：4 tests passed。
5. 后端 jar 启动成功，8080 可用。
6. 前端 dev server 启动成功，5174 可访问。
7. `/dev/image-to-layout` 页面入口返回 200。
8. Vite proxy 调 `/api/dev/image-layout-jobs` 成功。
9. `landing-basic` 返回 SUCCESS。
10. `card-list` 返回 SUCCESS。
11. `invalid-layout` 返回 200 且 FAILED。
12. `unknown-template` 返回 400。
13. 不存在 `jobId` 返回 404。
14. iframe 使用 `sandbox=""`。
15. 未发现运行时代码包含 `allow-scripts`。
16. 后台 8080 / 5174 服务已停止。
17. 未做 Playwright 视觉回归，符合边界。
18. `/dev/image-to-layout` 的 iframe 是前端基于 Layout JSON 的 mock 安全预览，不是 generated-page 静态编译产物。

## 12. 常见问题排查

- 后端 404：先确认 jobId 是否创建成功。
- 后端 400：先检查 `templateKey` 是否为支持模板。
- 前端无法访问：先确认 `npm run dev` 是否起来，以及代理目标端口是否一致。
- Worker 找不到示例文件：检查示例路径是否使用项目根目录。
- iframe 未展示：检查返回状态是否为 `SUCCESS`。
- 安全策略异常：检查 iframe 是否仍然是 `sandbox=""`，且没有 `allow-scripts`。
