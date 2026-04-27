# 后端接口任务工作流

本工作流用于指导 Codex 执行后端 API 任务。

API 是 Application Programming Interface（应用程序接口），本项目后端接口采用 RESTful API（面向资源的接口风格）。

## 适用场景

- 新增接口。
- 修改接口参数。
- 修改接口返回结构。
- 新增 Service 业务逻辑。
- 在用户明确确认数据库任务后，新增 Mapper 数据访问逻辑。

## 执行步骤

1. 阅读 `AGENTS.md`、`README.md`、`docs/week/01-plan.md`、`docs/week/01-status.md`、`docs/mvp-scope.md` 和相关架构文档。
2. 明确接口资源、路径、请求方法、请求参数和返回结构。
3. 检查是否需要数据库字段或表结构支持。
4. 输出计划，说明准备修改的 Controller、Service、Mapper、实体或 DTO。
5. 等待确认后执行。
6. 完成后运行后端测试或编译命令。
7. 汇报接口变化、验证结果和前端联调注意事项。

## 任务边界

- 后端接口任务优先只修改 `backend/`。
- Week 01 优先保证服务可启动、`/api/health` 可访问。
- MVP mock 阶段可以返回固定模拟数据或内存数据，但必须明确说明这是 mock，不代表真实生成结果。
- 不在未确认的情况下设计数据库表。
- 不在未确认的情况下接入 MySQL，或把 MySQL 作为启动前置依赖。
- 不在未确认数据库任务前新增 Mapper、实体表映射或数据库配置。
- 不在未确认的情况下引入 Redis、RabbitMQ 或 AI API。
- 不接入 Figma API / Figma MCP。

## Mock 与真实数据库边界

mock 接口用于验证前后端流程和响应结构，优先返回固定任务状态、固定结果或简单内存对象。

mock 阶段不创建数据库访问层，不新增 Mapper，不新增实体表映射，不新增数据库配置。

Mapper 仅在用户确认进入数据库任务后创建。

真实数据库接口需要在用户确认后再设计，至少应先明确：

- 表结构和字段。
- 实体、DTO、VO 的边界。
- Mapper 和 Service 职责。
- 数据迁移或初始化方式。
- 本地启动是否依赖 MySQL。

## 验证建议

后续后端工程初始化后，优先运行：

```bash
mvn test
mvn package -DskipTests
```

Week 01 当前 Windows 中文路径下，优先使用以下方式验证启动：

```bash
java -jar target/backend-0.0.1-SNAPSHOT.jar
```

接口完成后，再使用 Postman 或浏览器验证请求和响应。
