# ADR-0003: 先使用 mock 文件，再进入 MySQL

## 状态

Accepted

## 背景

项目早期需要快速验证 artifact 保存 / 查询链路，同时避免过早设计数据库表、Entity、Mapper 和持久层结构。

## 决策

当前阶段优先使用本地 mock 文件保存 artifact。

MySQL、数据库表、Entity、Mapper 和 MyBatis-Plus 持久层代码仅作为后续阶段方向，需产品负责人或项目经理确认后再执行。

## 影响

- 后端可以先验证接口契约和本地文件保存 / 查询。
- mock 文件是本地副产物，不提交 Git。
- 任务重启、文件清理或环境切换可能导致 mock 数据丢失，这是当前阶段可接受限制。

## 参考

- `docs/specs/layout-api-contracts.md`
- `docs/specs/generated-page-artifact-v0.1.md`

