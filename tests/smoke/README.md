# Smoke Tests

## 文件目的

本文件用于定义 Week 01 / Week 02 最小 smoke 测试步骤，验证项目已经具备继续开发和最小闭环联调的基础条件。

## 适用阶段

本文档保留 Week 01 基础 smoke 步骤；当前主要用于 Week 02 MVP 最小闭环开发阶段的基础验证。

## 使用方式

本文件是测试线程执行 smoke 验收的唯一命令依据。测试线程只负责执行命令、记录结果和报告问题，不直接修改 `frontend/`、`backend/`、`worker/` 业务代码。

如果实际命令与本文档不一致，应先报告不一致点；确认后再由文档线程或对应开发线程同步更新。

## 前置条件

建议本地具备以下环境：

- Node.js 20+
- Java 17+
- Maven 3.9+
- Python 3.10+（项目推荐目标版本为 Python 3.11）

Week 01 / Week 02 默认不要求：

- MySQL 必须启动
- Redis 必须启动
- RabbitMQ 必须启动
- 真实模型 API 必须可用
- Figma API / Figma MCP 必须可用

如果 `frontend/`、`backend/` 或 `worker/` 目录内还只有 `.gitkeep` 等占位文件，说明对应工程尚未初始化；请先完成 Day 2 / Day 3 的工程骨架任务，再执行对应 smoke 步骤。

## Smoke 1：前端启动

### 步骤
1. 进入 `frontend/`
2. 执行 `npm install`（如已安装可跳过）
3. 执行 `npm run build`
4. 短暂启动 `npm run dev -- --host 127.0.0.1 --port 5173`
5. 访问 `http://127.0.0.1:5173/`

### 预期结果
- 终端输出本地开发地址
- 浏览器可打开页面
- 页面能看到项目标题或初始化占位内容

## Smoke 2：后端启动

### 步骤
1. 进入 `backend/`
2. 执行 `mvn test`
3. 执行 `mvn package -DskipTests`
4. 执行 `java -jar target/backend-0.0.1-SNAPSHOT.jar`
5. 访问 `http://127.0.0.1:8080/api/health`

说明：当前 Windows 中文路径下，`mvn spring-boot:run` 存在已知启动失败风险，暂不作为主验收命令；后续可单独排查。

### 预期结果
- 服务启动成功
- `/api/health` 返回 200
- 返回结果至少包含 `status` 字段

## Smoke 2.1：Week 02 后端上传接口

### 步骤
1. 进入 `backend/`
2. 执行 `mvn test`
3. 执行 `mvn package -DskipTests`
4. 执行 `java -jar target/backend-0.0.1-SNAPSHOT.jar`
5. 上传 PNG 图片：
   `curl -X POST http://127.0.0.1:8080/api/assets/upload -F "file=@你的本地图片路径.png"`
6. 访问返回的 `fileUrl`：
   `http://127.0.0.1:8080/uploads/返回的文件名`
7. 上传不支持的格式，例如 TXT：
   `curl -X POST http://127.0.0.1:8080/api/assets/upload -F "file=@你的本地文本路径.txt"`
8. 上传空文件，例如空 PNG：
   `curl -X POST http://127.0.0.1:8080/api/assets/upload -F "file=@你的本地空文件路径.png"`

### 预期结果
- PNG / JPG / JPEG / WebP 上传成功
- 成功响应包含 `assetId`、`fileName`、`fileUrl`、`contentType`、`size`
- `fileUrl` 可以通过 `/uploads/**` 访问
- TXT / PDF / GIF 等非支持格式返回 400
- 空文件返回 400
- 验证完成后停止后端服务，不留下 8080 后台进程

## Smoke 2.2：Week 02 最小闭环接口验收

### 步骤
1. 进入 `backend/`
2. 执行 `mvn test`
3. 执行 `mvn package -DskipTests`
4. 执行 `java -jar target/backend-0.0.1-SNAPSHOT.jar`
5. 上传 PNG / JPG / JPEG / WebP 图片到 `POST /api/assets/upload`
6. 访问上传响应中的 `fileUrl`，确认 `/uploads/**` 可访问
7. 使用 `assetId` 创建任务：
   `POST /api/generations`
8. 查询任务状态：
   `GET /api/generations/{jobId}`
9. 查询 mock 生成结果：
   `GET /api/generations/{jobId}/result`

### 预期结果
- 支持格式上传成功，响应包含 `assetId` 和 `fileUrl`
- `fileUrl` 返回 200
- 创建任务响应包含 `jobId`，状态为 `success`
- 查询任务状态返回 `progress` 为 100
- 查询任务结果返回 `layoutJson`、`vueCode`、`cssCode`

## Smoke 2.3：Week 02 异常接口验收

### 步骤
1. 上传 TXT 文件到 `POST /api/assets/upload`
2. 查询不存在的任务：
   `GET /api/generations/job_missing`

### 预期结果
- TXT 上传返回 400，错误信息明确说明只支持 PNG、JPG、JPEG、WebP 图片
- 不存在的 `jobId` 返回 404，错误信息为任务不存在

## Smoke 3：Worker 启动

### 步骤
1. 进入 `worker/`
2. 执行 `python --version`
3. 执行 `python main.py --smoke`

说明：当前 worker smoke 脚本只验证最小入口，允许使用 Python 3.10+；后续接入真实处理依赖时再统一评估是否升级到 Python 3.11。

### 预期结果
- 控制台输出 `worker smoke pass`
- 进程正常结束
- 退出码为 0

## Smoke 4：文档协作验证

### 步骤
1. 新开一个 Codex 任务
2. 发送：请先阅读 `AGENTS.md`、`docs/context/current-phase.md`、`docs/tasks/week02-day1-upload-api.md`
3. 让 Codex 总结当前阶段目标与非目标

### 预期结果
- Codex 能正确回答“当前是 Week 02 MVP 最小闭环开发阶段”
- Codex 能说明日常任务优先读取当前阶段上下文和单任务卡，不默认读取完整 PRD、完整周计划和全部历史状态
- Codex 不会直接建议接模型、接 Figma、接队列
- Codex 能给出“先计划、再执行、再验证”的工作顺序

## 关键字段说明

| 字段 | 含义 |
|---|---|
| Smoke 1 | 验证前端骨架是否可启动 |
| Smoke 2 | 验证后端骨架是否可启动 |
| Smoke 3 | 验证 worker 是否具备最小独立运行能力 |
| Smoke 4 | 验证文档是否能真正指导 Codex |

## 验收标准

只要以下基础项都通过，就判定当前阶段 smoke 基础验证通过：

- 前端可启动
- 后端可启动
- worker 可运行
- 文档可指导 Codex 正确理解当前阶段

Week 02 进入功能验收后，还需要补充验证上传接口和完整最小闭环流程。

## Smoke 5：Week 02 前端端到端验收

### 步骤
1. 启动后端：
   `java -jar target/backend-0.0.1-SNAPSHOT.jar`
2. 进入 `frontend/`
3. 执行 `npm run build`
4. 启动前端：
   `npm run dev -- --host 127.0.0.1 --port 5173`
5. 如果 5173 被占用，可改用 5174 或 5175
6. 打开首页 `/`
7. 进入 `/generation/create`
8. 选择 PNG / JPG / JPEG / WebP 图片，确认本地预览
9. 点击“开始生成”
10. 确认跳转 `/generation/{jobId}`
11. 确认详情页展示 `jobId`、`status`、`progress`、`assetId`、`layoutJson`、`vueCode`、`cssCode`
12. 访问 `/generation/job_missing`
13. 点击返回创建页

### 预期结果
- 首页可访问
- 创建页可选择图片并显示预览
- 点击开始生成后完成上传和任务创建
- 详情页展示任务状态与 mock 结果
- 不存在任务页面展示明确错误提示
- 返回创建页可用
- 验证完成后停止前端 dev server 和后端服务

## Week 02 已知风险

- 后端 `mvn test` 当前仍没有测试用例，只能验证 Maven 生命周期。
- 任务数据暂存在内存 Map，后端重启后已创建的 `assetId` / `jobId` 会失效。
- 上传文件保存在 `backend/uploads/`，该目录为本地验证副产物，不应提交。
- 当前结果为 mock 数据，不代表真实截图解析或真实页面代码生成。
