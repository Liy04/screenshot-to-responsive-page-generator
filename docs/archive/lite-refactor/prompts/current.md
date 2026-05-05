# Current Prompt Templates

本文件保留当前推荐使用的轻量上下文提示词。

来源：从旧版长提示词入口拆分而来。

# Prompt Templates

## 文件目的

本文件用于沉淀可复用的 Codex 提示词模板，减少每次开新任务时重复组织语言的成本。

当前适用于项目多阶段协作。Week 02 起，日常开发优先使用“轻量上下文任务提示词模板”，由 `AGENTS.md`、`docs/context/current-phase.md`、当前任务卡和相关代码驱动。

通用约束：

- 默认只阅读 `AGENTS.md`、`docs/context/current-phase.md`、当前任务卡和当前任务相关代码。
- 其它文档只在任务卡明确要求，或当前任务确实必须参考时读取。
- 只处理当前线程范围内的任务。
- 不接入真实模型 API、Figma API、Redis、RabbitMQ。
- 不实现真实截图解析、真实代码生成、拖拽编辑器、多页面编辑器或导出 zip。
- 如果修改目录、命令、接口约定、测试方式或当前周状态，必须同步更新相关文档。

## 模板零：轻量上下文任务提示词

```text
你现在在 screenshot-to-responsive-page-generator 仓库中工作。

当前任务：
【填写当前任务名称】

请只阅读：

1. AGENTS.md
2. docs/context/current-phase.md
3. docs/tasks/active/【当前任务卡文件名】.md
4. 当前任务相关模块代码

不要读取以下文件，除非当前任务卡明确要求，或当前任务确实必须参考：

- docs/prd.md
- docs/mvp-scope.md
- docs/architecture.md
- docs/testing.md
- docs/archive/week/01-plan.md
- docs/archive/week/01-status.md
- docs/archive/week/02-plan.md
- docs/archive/week/02-status.md
- docs/skills/*

请先输出开发计划，不要直接改代码。

开发计划必须包含：

1. 你理解的任务目标
2. 准备读取哪些文件
3. 准备修改哪些文件
4. 具体实现步骤
5. 测试方式
6. 是否存在越界风险
7. 如何确保不违反当前阶段禁止项

计划输出后停止，等待确认。
```

说明：后续每日开发优先使用本模板。下面保留的旧线程模板可作为专项任务参考，但不再要求每个任务默认读取完整周计划和全部项目文档。
