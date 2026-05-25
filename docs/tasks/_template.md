# Task Card Template

```text
负责角色：
执行方式：
  - 当前运行环境支持 subagent 工具时，Lead 必须显式 spawn 上述 agent。
  - 用户显式要求 spawn subagent 时，即使是小任务也必须 spawn，不得用“小任务 Lead 可直接做”覆盖用户要求。
  - 如不支持，Lead 必须说明降级原因并请求用户确认，不得静默主线程自演。
  - 默认顺序执行。
  - 不允许多个 agent 同时修改同一目录。
  - tester-agent / reviewer-agent 默认不修业务代码，只报告问题；修复由 Lead 分派给对应实现 agent。
是否需要 spawn subagent：
Lead 是否可直接执行：
必须 spawn 的 agent：
是否允许并行：
任务目标：
默认读取：
  - 默认不读取 docs/archive/。
允许修改：
禁止修改：
实施步骤：
验收标准：
Lead 二次验收：
  - 对照任务目标和验收标准检查
  - 检查修改范围是否越界
  - 检查测试 / smoke / review 是否完成或说明原因
  - 检查安全边界和密钥风险
  - 检查是否需要同步文档
  - 结论：通过 / 条件通过 / 不通过
输出格式：
```
