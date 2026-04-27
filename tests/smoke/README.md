# Smoke Tests

## 文件目的

本文件用于定义第一周最小 smoke 测试步骤，验证项目已经具备继续开发的基础条件。

## 适用阶段

当前仅适用于 Week 01 初始化阶段。

## 使用方式

本文件是测试线程执行 smoke 验收的唯一命令依据。测试线程只负责执行命令、记录结果和报告问题，不直接修改 `frontend/`、`backend/`、`worker/` 业务代码。

如果实际命令与本文档不一致，应先报告不一致点；确认后再由文档线程或对应开发线程同步更新。

## 前置条件

建议本地具备以下环境：

- Node.js 20+
- Java 17+
- Maven 3.9+
- Python 3.10+（项目推荐目标版本为 Python 3.11）

第一周默认不要求：

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

说明：当前 Windows 中文路径下，`mvn spring-boot:run` 存在已知启动失败风险，暂不作为 Week 01 Day 3 主验收命令；后续可单独排查。

### 预期结果
- 服务启动成功
- `/api/health` 返回 200
- 返回结果至少包含 `status` 字段

## Smoke 3：Worker 启动

### 步骤
1. 进入 `worker/`
2. 执行 `python --version`
3. 执行 `python main.py --smoke`

说明：Week 01 的 worker smoke 脚本只验证最小入口，允许使用 Python 3.10+；后续接入真实处理依赖时再统一评估是否升级到 Python 3.11。

### 预期结果
- 控制台输出 `worker smoke pass`
- 进程正常结束
- 退出码为 0

## Smoke 4：文档协作验证

### 步骤
1. 新开一个 Codex 任务
2. 发送：请先阅读 `AGENTS.md`、`README.md`、`docs/week/01-plan.md`、`docs/week/01-status.md`
3. 让 Codex 总结当前阶段目标与非目标

### 预期结果
- Codex 能正确回答“当前是 Week 01 初始化阶段”
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

只要以下四项都通过，就判定第一周 smoke 测试通过：

- 前端可启动
- 后端可启动
- worker 可运行
- 文档可指导 Codex 正确理解当前阶段
