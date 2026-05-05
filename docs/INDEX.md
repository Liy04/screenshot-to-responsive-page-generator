# Docs Index

## 文件目的

本文档是项目文档入口。Docs Refactor 第二阶段后，当前上下文优先使用 `docs/context/`、`docs/plans/`、`docs/tasks/active/`、`docs/specs/`、`docs/prompts/` 和 `docs/decisions/`。

历史内容已按类型归档，保留原文用于追溯。

## 推荐阅读顺序

1. `AGENTS.md`
2. `README.md`
3. `docs/context/current-phase.md`
4. 当前任务卡：`docs/tasks/active/*.md`
5. 当前任务相关专项文档或代码

## 活跃文档

| 类型 | 路径 | 说明 |
|---|---|---|
| 当前阶段上下文 | `docs/context/current-phase.md` | 当前目标、禁止项、推荐实现 |
| 当前周计划 | `docs/plans/week-04.md` | Week 04 总纲 |
| 当前任务卡 | `docs/tasks/active/week04-*.md` | Week 04 单线程任务卡 |
| generated-page artifact 契约 | `docs/specs/generated-page-artifact-v0.1.md` | Week 04 产物契约 |
| Layout JSON 到 HTML/CSS 映射 | `docs/specs/layout-to-html-v0.1.md` | Week 04 编译映射规则 |
| Layout JSON v0.1 设计 | `docs/specs/layout-json-v0.1.md` | Layout JSON v0.1 设计依据 |
| Layout API 契约 | `docs/specs/layout-api-contracts.md` | Layout JSON mock API 契约 |
| context-scout 流程 | `docs/playbooks/context-scout.md` | 大任务上下文侦察流程 |
| 当前提示词模板 | `docs/prompts/current.md` | 轻量上下文提示词 |
| 通用任务模板 | `docs/prompts/task-template.md` | 多线程任务下发模板 |
| 验收和修复模板 | `docs/prompts/review-template.md` | 测试、Bug 修复和总结模板 |
| 架构决策记录 | `docs/decisions/ADR-*.md` | 核心工程决策 |

## 新目录职责

- `docs/specs/`：长期或阶段性规格文档。
- `docs/playbooks/`：协作流程、操作流程和可复用工作法。
- `docs/plans/`：当前和后续周计划总纲。
- `docs/tasks/active/`：当前活跃任务卡。
- `docs/tasks/done/`：已完成任务卡归档。
- `docs/prompts/`：当前提示词模板。
- `docs/decisions/`：ADR 架构决策记录。
- `docs/archive/`：历史周文档、历史 prompts、历史状态等归档材料。

## 归档入口

| 类型 | 路径 |
|---|---|
| Week 01 / Week 02 / Week 03 历史周文档 | `docs/archive/week/` |
| Week 04 旧周计划副本 | `docs/archive/week/04-plan.md` |
| Week 02 / Week 03 已完成任务卡 | `docs/tasks/done/` |
| Week 04 旧任务卡副本 | `docs/archive/tasks/week04/` |
| 历史规格和旧根目录专项文档 | `docs/archive/specs/` |
| Week 02 / Week 03 历史长提示词 | `docs/archive/prompts/week02-week03-prompts.md` |
| 历史状态归档入口 | `docs/archive/status/README.md` |

## 迁移说明

- 当前规格文档优先使用 `docs/specs/`。
- 当前周计划优先使用 `docs/plans/`。
- 当前任务卡优先使用 `docs/tasks/active/`。
- 已完成任务卡归档到 `docs/tasks/done/`。
- 历史周文档归档到 `docs/archive/week/`。
- 历史规格和被新版本覆盖的旧根目录专项文档归档到 `docs/archive/specs/`。
- 历史提示词归档到 `docs/archive/prompts/`。
- Context Scout 完整流程已提取到 `docs/playbooks/context-scout.md`。

## 路径优先级

新任务优先引用新路径：

1. `docs/context/current-phase.md`
2. `docs/plans/week-04.md`
3. `docs/tasks/active/week04-*.md`
4. `docs/specs/*.md`
5. `docs/prompts/*.md`
6. `docs/decisions/*.md`
7. `docs/playbooks/*.md`

归档文档中的旧路径允许保留，用于历史追溯。
