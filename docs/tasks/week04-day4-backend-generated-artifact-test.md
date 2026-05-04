# Week 04 Day 4B：后端 generated-page artifact 测试

## 任务目标

线程：后端测试线程。

补充 `GeneratedPageArtifactControllerTest`，验证 generated-page artifact PUT / GET mock 接口。

## 必须完成

- 新增或补充 `GeneratedPageArtifactControllerTest`。
- 覆盖保存成功。
- 覆盖查询成功。
- 覆盖查询不存在返回 404。
- 覆盖空请求体或空 artifact 返回 400。
- 覆盖非法 `jobId` 返回 400。
- 覆盖 `status=SUCCESS` 时 `htmlCode/cssCode` 不能为空。

## 禁止事项

- 不改前端。
- 不改 worker。
- 不接 MySQL。
- 不创建 Entity / Mapper。
- 不接 Redis / RabbitMQ。
- 不把测试线程变成功能开发线程。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day4-backend-generated-artifact-test.md`
- `docs/generated-page-artifact-design.md`
- 后端 generated-page API 相关代码
- 后端已有测试结构

## 建议修改文件

- 后端 generated-page controller 测试文件

## 验收标准

优先执行：

```bash
mvn test
```

如测试环境存在已知问题，记录原因，并至少执行：

```bash
mvn package
```

## Codex 执行要求

先输出计划，等待确认后再写测试。发现接口问题时先记录问题，必要修复需保持最小修改。
