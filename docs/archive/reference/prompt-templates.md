# Prompt Templates

## 文件目的

本文件保留为提示词模板入口，不再承载全部长模板内容。

Docs Refactor 第二阶段已将当前模板、通用任务模板、验收模板和历史阶段提示词拆分到 `docs/prompts/` 与 `docs/archive/prompts/`。

## 当前推荐入口

| 文档 | 说明 |
|---|---|
| `docs/prompts/current.md` | 当前推荐的轻量上下文任务提示词 |
| `docs/prompts/task-template.md` | 通用任务下发模板 |
| `docs/prompts/review-template.md` | 测试验收、Bug 修复、每日总结模板 |
| `docs/archive/prompts/week02-week03-prompts.md` | Week 02 / Week 03 历史长提示词归档 |

## 使用建议

- 日常任务优先使用 `docs/prompts/current.md`。
- 按线程下发任务时参考 `docs/prompts/task-template.md`。
- 验收、复盘和 Bug 修复交接参考 `docs/prompts/review-template.md`。
- 历史 Week 02 / Week 03 提示词只用于追溯，不作为当前默认上下文。

## 当前协作规则

日常任务仍遵循轻量上下文：

```text
AGENTS.md
docs/context/current-phase.md
docs/tasks/active/当前任务卡.md
当前任务相关代码
```

大任务、跨模块任务、阶段边界不清或敏感边界任务，按 `docs/playbooks/context-scout.md` 先做 Context 策略判断。
