# Week 11 Day 02

## 负责角色

explorer-agent -> docs-agent -> tester-agent -> reviewer-agent

## 任务目标

建立公开安全、可提交、可用于真实 AI smoke 的 `samples/` 样例集。

## 默认读取

- `AGENTS.md`
- `docs/current.md`
- `docs/plan.md`
- `docs/tasks/day-02.md`
- `docs/agents/explorer-agent.md`
- `docs/agents/docs-agent.md`
- `docs/agents/tester-agent.md`
- `docs/agents/reviewer-agent.md`
- 必要时 `docs/spec.md`

不默认读取 `docs/archive/`。

## 允许修改

- `samples/`
- 必要时新增样例说明文档
- 必要时更新 `docs/tasks/day-02.md` 的执行记录

## 禁止修改

- `backend/`
- `frontend/`
- `worker/`
- `tests/`
- 真实业务截图、手机号、账号、邮箱、真实头像、公司内部页面
- 第三方品牌或版权不明素材
- 真实 API key

## 实施步骤

1. explorer-agent 只读确认 `samples/` 落地范围和风险。
2. docs-agent 创建 `samples/README.md` 和样例用途说明。
3. 准备 2 到 3 张无品牌、无隐私、无版权争议的 mock UI 样例图。
4. tester-agent 检查样例是否可用于真实 AI smoke。
5. reviewer-agent 检查隐私、密钥和版权风险。

## 验收标准

- [ ] `samples/README.md` 存在。
- [ ] 至少 2 到 3 张公开安全样例图。
- [ ] 每张图说明验证目标。
- [ ] 不含手机号、账号、真实业务数据、真实用户头像。
- [ ] 不含第三方品牌或版权不明素材。
- [ ] 可以用于真实 AI smoke。
- [ ] 不影响现有测试。
- [ ] reviewer-agent 未发现隐私 / 密钥 / 版权阻塞风险。

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
