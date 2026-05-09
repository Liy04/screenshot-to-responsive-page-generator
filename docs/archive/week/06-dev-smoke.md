# Week 06 Dev Smoke

## 1. 目标

验证 Worker -> Backend -> Frontend 的 generated-page artifact 预览闭环。

本 smoke 流程用于确认：

1. Worker 可以从 Layout JSON 示例生成 generated-page artifact。
2. 后端可以保存 generated-page artifact。
3. 后端可以查询 generated-page artifact。
4. 前端任务详情页可以展示 generated-page artifact。
5. 前端独立 dev preview 页面可以展示 generated-page artifact。
6. `status=SUCCESS` 时可以安全预览。
7. `status=FAILED` 时不会展示 iframe。
8. iframe 使用 `sandbox=""`，且不包含 `allow-scripts`。

## 2. 前置条件

- 当前在项目根目录。
- 已安装 Java 17。
- 已安装 Maven。
- 已安装 Node.js。
- 已安装 Python，推荐 Python 3.11。
- 当前是学习型 MVP，不接真实 AI / Figma / MySQL。
- 当前使用本地 mock artifact。
- 后端 mock-data 按忽略规则处理，不提交构建副产物。
- 如果 8080 已被占用，改用备用后端端口 18080。
- 前端 Vite dev server 端口和后端端口不是同一个概念，不要混淆。

### 2.1 检查 8080 是否被占用

在 Windows PowerShell 中可以先检查 8080 端口是否已有进程占用：

```powershell
netstat -ano | findstr :8080
```

如果输出中出现 `LISTENING`，说明 8080 已被占用。

也可以直接查看对应 PID：

```powershell
tasklist /FI "PID eq <PID>"
```

如果 8080 已被占用，优先走备用后端端口流程。

## 3. 首次安装前端依赖

首次运行前端前执行：

```bash
cd frontend
npm install
```

之后日常 smoke 不需要每次执行 `npm install`。

回到项目根目录：

```bash
cd ..
```

## 4. 启动后端

推荐方式：

```bash
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

说明：

```text
该方式优先用于 Week 06 smoke。
原因是之前记录过 Windows 中文路径下 mvn spring-boot:run 存在风险。
```

如果 8080 被占用，改用备用后端端口：

```bash
cd backend
mvn package -DskipTests
java -jar target/backend-0.0.1-SNAPSHOT.jar --server.port=18080
```

可选方式：

```bash
cd backend
mvn spring-boot:run
```

回到项目根目录：

```bash
cd ..
```

## 5. 启动前端

```bash
cd frontend
npm run dev
```

默认访问地址通常为：

```text
http://localhost:5173
```

如果后端切到备用端口 18080，前端需要把代理目标改到同一个后端端口。Windows PowerShell 可写为：

```powershell
cd frontend
$env:VITE_API_PROXY_TARGET='http://127.0.0.1:18080'
npm run dev
```

如果仍然使用默认后端端口 8080，则前端代理目标保持默认值 `http://127.0.0.1:8080`。

回到项目根目录：

```bash
cd ..
```

## 6. 运行 Worker 编译器

注意：

```text
当前 examples 在项目根目录下，不在 worker/examples/ 下。
```

在项目根目录执行：

```bash
python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
```

预期结果：

```text
项目根目录生成 generated-page-valid.json。
该文件内容应包含 generated-page artifact。
status 应为 SUCCESS。
htmlCode / cssCode 应有内容。
vueCode 仅作为文本展示，不要求可运行。
```

## 7. 上传 generated-page artifact

在项目根目录执行：

```powershell
curl.exe -X PUT `
  http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page `
  -H "Content-Type: application/json" `
  --data-binary "@generated-page-valid.json"
```

如果后端使用备用端口 18080，上传和查询地址也要改成同一个后端端口：

```powershell
curl.exe -X PUT `
  http://localhost:18080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page `
  -H "Content-Type: application/json" `
  --data-binary "@generated-page-valid.json"
```

如果使用 Git Bash / macOS / Linux，可使用：

```bash
curl -X PUT \
  http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page \
  -H "Content-Type: application/json" \
  --data-binary @generated-page-valid.json
```

也可以使用 PowerShell 的 `Invoke-RestMethod`：

```powershell
Get-Content .\generated-page-valid.json -Raw | Invoke-RestMethod `
  -Method Put `
  -Uri http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page `
  -ContentType 'application/json'
```

预期结果：

```text
后端返回保存成功。
```

## 8. 查询 generated-page artifact

```bash
curl http://localhost:8080/api/dev/generation-jobs/demo-job-001/artifacts/generated-page
```

如果后端使用备用端口 18080，查询地址也要同步改成 18080。

预期结果：

```text
能查询到刚才上传的 generated-page artifact。
status=SUCCESS。
htmlCode / cssCode / vueCode 字段存在。
validation / source / generator 信息存在。
```

## 9. 打开独立 dev preview 页面

访问：

```text
http://localhost:5173/dev/generated-page-preview/demo-job-001
```

预期结果：

```text
页面可以展示 generated-page artifact。
```

## 10. 相关测试命令口径

### 10.1 Worker 测试

```bash
python -m unittest worker.test_layout_validator worker.test_layout_static_generator
```

### 10.2 后端测试

```bash
cd backend
mvn test
```

### 10.3 前端测试

```bash
cd frontend
npm run test
```

### 10.4 前端构建

```bash
cd frontend
npm run build
```

### 10.5 建议执行顺序

```text
1. 先跑 Worker unittest。
2. 再跑后端 mvn test。
3. 再跑前端 npm run test。
4. 最后跑前端 npm run build。
```

## 11. SUCCESS 状态验收点

需要确认：

```text
1. status=SUCCESS。
2. htmlCode 正常展示。
3. cssCode 正常展示。
4. vueCode 作为文本展示。
5. validation.errors 为空或符合预期。
6. validation.warnings 正常展示。
7. unsupportedNodes 正常展示。
8. source.layoutHash 正常展示。
9. generator 信息正常展示。
10. iframe 预览正常展示。
11. iframe sandbox=""。
12. iframe 不包含 allow-scripts。
```

## 12. FAILED 状态验收点

使用 invalid 示例生成失败 artifact 后，需要确认：

```text
1. status=FAILED。
2. 不展示 iframe 预览。
3. 展示 validation.errors。
4. 展示 validation.warnings。
5. htmlCode / cssCode / vueCode 为空或符合失败状态约定。
```

## 13. 常见问题排查

### 13.1 后端 404

检查：

```text
1. jobId 是否正确。
2. artifact 是否已经 PUT 保存。
3. 后端是否正常启动。
```

### 13.2 后端 400

检查：

```text
1. jobId 是否非法。
2. 请求体是否超过 2MB。
3. JSON 是否有效。
```

### 13.3 8080 被占用

检查：

```text
1. 是否有其它 Java 服务占用了 8080。
2. 后端是否已经切换到 18080。
3. 前端代理是否已设置为 http://127.0.0.1:18080。
4. 上传 / 查询 URL 是否也同步切到 18080。
```

### 13.4 前端无法访问

检查：

```text
1. 前端 dev server 是否启动。
2. 端口是否为 5173。
3. 路由是否为 /dev/generated-page-preview/:jobId。
```

### 13.5 Worker 找不到示例文件

确认当前在项目根目录，并使用：

```bash
python worker/layout_static_generator.py examples/valid/landing-page.layout.json > generated-page-valid.json
```

不要使用 Worker 目录内的 examples 路径。

### 13.6 iframe 未展示

检查：

```text
1. artifact status 是否为 SUCCESS。
2. 如果 status=FAILED，前端不应该展示 iframe。
```

### 13.7 安全策略异常

检查：

```text
1. iframe 是否仍为 sandbox=""。
2. iframe 是否不包含 allow-scripts。
3. Worker 是否继续禁止 script / inline event / javascript URL。
```
