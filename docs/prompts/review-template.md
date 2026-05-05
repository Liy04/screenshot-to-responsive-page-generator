# Review Prompt Templates

本文件保留测试验收、Bug 修复和每日验收总结模板。

来源：从旧版长提示词入口拆分而来。

## 模板五：测试验收任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前验收任务卡
- tests/smoke/README.md

当前角色：
测试线程。

当前目标：
[写清楚要验收的模块或 smoke 范围]

任务范围：
1. 只执行验证和记录结果。
2. 不直接修改 frontend/、backend/、worker/ 业务代码。
3. 如发现问题，记录复现步骤、实际结果、预期结果和影响范围。
4. 测试命令必须与 tests/smoke/README.md 保持一致。

验证清单：
1. 前端：npm run build，必要时短暂启动 dev 服务并访问页面。
2. 后端：mvn test、mvn package -DskipTests、java -jar 后访问 /api/health。
3. Worker：python --version、python main.py --smoke。
4. 文档：确认 README、current-phase、当前任务卡、状态看板和 smoke 文档没有明显冲突。

完成后汇报：
- 验收范围
- 执行命令
- 通过项
- 失败项和复现步骤
- 风险 / 待确认事项
```

## 模板七：Bug 修复任务

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前任务卡或问题相关文档
- docs/skills/bugfix-skill.md
- 问题相关模块文档或代码

当前角色：
Bug 修复线程。

当前问题：
[描述问题现象、报错、复现步骤]

任务范围：
1. 先复现或确认问题。
2. 定位根因，区分前端、后端、Worker、测试命令或文档问题。
3. 只做最小必要修改。
4. 不借修复机会做无关重构。
5. 如测试线程只报告问题，本线程负责修复和验证。

完成后汇报：
- 根因
- 改动文件
- 修复内容
- 验证步骤和结果
- 剩余风险 / 待确认事项
```

## 模板八：每日验收总结

```text
请先阅读：
- AGENTS.md
- docs/context/current-phase.md
- 当前状态看板

当前角色：
项目经理线程 / 验收总结线程。

当前目标：
汇总 Day [数字] 验收结果，并更新对应 `docs/week/*-status.md`。

需要汇总：
1. 今日目标。
2. 各线程状态：待执行 / 执行中 / 待验收 / 通过 / 阻塞。
3. 已执行的验证命令。
4. 通过项。
5. 失败项或阻塞项。
6. 风险和下一步。

完成条件：
1. 对应 `docs/week/*-status.md` 与真实进展一致。
2. 不修改业务代码。
3. 最终汇报改动文件、验证方式、验证结果和风险。
```
