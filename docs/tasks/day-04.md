# Week 11 Day 04

## 负责角色

explorer-agent -> worker-agent -> backend-agent -> frontend-agent -> tester-agent -> reviewer-agent

## 任务目标

可选执行轻量 metadata 可解释性增强。只有 Day 2 / Day 3 完成后才执行。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-04.md`
- `docs/agents/explorer-agent.md`
- 当前阶段对应角色文件
- 必要时 `docs/spec.md`
- 当前任务相关模块代码

不默认读取 `docs/archive/`。

## 允许修改

按阶段顺序分别允许：

- worker-agent：`worker/`
- backend-agent：`backend/`
- frontend-agent：`frontend/`
- tester-agent：测试和 smoke 记录
- reviewer-agent：review 结果记录

同一时间只允许一个实现类角色修改对应目录。

## 禁止修改

- 不接 MySQL。
- 不设计数据库表。
- 不创建 Entity / Mapper。
- 不改 API 主结构。
- 不做复杂 tracing。
- 不新增复杂 metadata 表。
- 不泄漏 `OPENAI_API_KEY`。
- 默认不做 `sourceImageName`。
- 默认不做 `baseUrlHost`。

## 实施步骤

1. 4A explorer-agent：确认 Worker / Backend / Frontend metadata 影响范围。
2. 4B worker-agent：最小字段输出。
3. 4C backend-agent：透传 / 保存字段。
4. 4D frontend-agent：展示字段。
5. 4E tester-agent：测试和 smoke。
6. 4F reviewer-agent：安全、契约和边界审查。

## 验收标准

- [ ] 只增强 `durationMs`、`model`、`artifact.reused`。
- [ ] 不改变现有 API 主结构。
- [ ] 不引入 MySQL。
- [ ] 不破坏 Week 10 测试。
- [ ] 不泄漏 `OPENAI_API_KEY`。
- [ ] 前端展示 `durationMs` / `model` / `artifact.reused`。
- [ ] `REAL_AI` / `FALLBACK` / `FAILED` 展示仍正常。
- [ ] Worker 测试通过。
- [ ] Backend 测试通过。
- [ ] Frontend 测试通过。
- [ ] reviewer-agent 未发现阻塞问题。

## 输出格式

```text
任务结果：
- 任务目标：
- 修改文件：
- 主要改动：
- 验证步骤：
- 验证结果：
- 风险 / 待确认事项：
```
