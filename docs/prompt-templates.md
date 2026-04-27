# Prompt Templates

## 文件目的

本文件用于沉淀可复用的 Codex 提示词模板，减少每次开新任务时重复组织语言的成本。

当前适用于 Week 01 初始化阶段，重点服务 Day 4 多线程协作：项目经理、前端、后端、Worker / 模型预备、测试、文档和 Bug 修复线程。

通用约束：

- 先阅读 `AGENTS.md`、`README.md`、`docs/week/01-plan.md` 和 `docs/week/01-status.md`。
- 只处理当前线程范围内的任务。
- 不接入真实模型 API、Figma API、Redis、RabbitMQ。
- 不实现真实截图解析、真实代码生成、拖拽编辑器、多页面编辑器或导出 zip。
- 如果修改目录、命令、接口约定、测试方式或当前周状态，必须同步更新相关文档。

## 模板一：项目经理下发任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md

当前角色：
项目经理线程。

当前目标：
[写清楚本次要统筹的目标]

上下文：
[写清楚当前 Day、已完成内容、待拆分任务、约束和风险]

任务要求：
1. 明确本次任务目标和范围。
2. 拆分前端、后端、Worker / 模型预备、测试、文档线程的工作。
3. 标明每个线程的输入、输出、验收标准和风险。
4. 不直接扩大到 Week 01 之外的功能。
5. 如状态变化，更新 docs/week/01-status.md。

完成条件：
1. 给出清晰任务拆分。
2. 给出验收标准。
3. 给出风险和待确认事项。
4. 如有文档变更，列出修改文件。
```

## 模板二：前端开发任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md
- docs/coding-rules.md
- docs/skills/frontend-task-skill.md
- tests/smoke/README.md

当前角色：
前端开发线程。

当前目标：
[写清楚页面、组件、样式或前端验证目标]

任务要求：
1. 先输出计划，等待确认后再执行。
2. 计划中说明预计修改的文件、实施步骤、验证方式和风险。

任务范围：
1. 只修改 frontend/ 内与当前目标直接相关的文件。
2. Week 01 / MVP 阶段只做页面骨架、占位展示、基础响应式和接口联调准备。
3. 不接入真实生成能力。
4. 不实现真实截图解析。
5. 不实现真实代码生成。
6. 不实现拖拽编辑器、多页面编辑器或导出 zip。
7. 不引入组件库，除非用户明确确认。
8. 不提交 `node_modules/`、`dist/`、临时日志文件或其它构建产物。

验证方式：
1. 执行 npm install（如已安装可跳过）。
2. 执行 npm run build。
3. 必要时执行 npm run dev -- --host 127.0.0.1 --port 5173 并检查页面。
4. 如果启动 dev server，验证完成后必须停止进程，不留下后台服务。

完成后汇报：
- 改动文件
- 页面或组件变化
- 验证步骤和结果
- 风险 / 待确认事项
```

## 模板三：后端开发任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md
- docs/mvp-scope.md
- docs/architecture.md
- docs/skills/backend-api-skill.md
- tests/smoke/README.md

当前角色：
后端开发线程。

当前目标：
[写清楚接口、健康检查、mock 返回或后端验证目标]

计划要求：
1. 如果新增或修改接口，计划中必须说明是否涉及 Controller、Service、Mapper、DTO、VO。
2. 如果某一层不涉及，也要显式写“本次不涉及”。
3. 如涉及数据库能力，必须先说明原因并等待用户确认。

任务范围：
1. 只修改 backend/ 内与当前目标直接相关的文件。
2. Week 01 优先保证服务可启动和 /api/health 可访问。
3. MVP mock 阶段优先使用固定数据或简单内存数据，但必须说明 mock 边界。
4. 未确认前不设计数据库表、不接 MySQL、不接 Redis / RabbitMQ。
5. 未确认数据库任务前，不新增 Mapper、实体表映射或数据库配置。
6. mock 阶段不创建数据库访问层。
7. 不接入真实模型 API 或 Figma API。

验证方式：
1. 执行 mvn test。
2. 执行 mvn package -DskipTests。
3. 使用 java -jar target/backend-0.0.1-SNAPSHOT.jar 启动服务。
4. 访问 http://127.0.0.1:8080/api/health。

完成后汇报：
- 改动文件
- 接口路径、方法和返回结构
- 验证步骤和结果
- 前端联调注意事项
- 风险 / 待确认事项
```

## 模板四：Worker / 模型预备任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md
- worker/README.md
- tests/smoke/README.md

当前角色：
Worker / 模型预备线程。

版本口径：
Worker 推荐目标版本为 Python 3.11；Week 01 smoke 脚本允许 Python 3.10+ 本地验证。

当前目标：
[写清楚 worker 入口、参数、mock 输出或 smoke 验证目标]

任务范围：
1. 只修改 worker/ 内与当前目标直接相关的文件。
2. Week 01 只维护最小 smoke 入口和标准库脚本。
3. 不接入真实模型 API。
4. 不接入 OpenAI 或其他模型 SDK。
5. 不接入 Figma API / Figma MCP。
6. 不实现真实截图解析。
7. 不实现真实页面代码生成。
8. Week 01 优先使用 Python 标准库，不引入额外依赖。

验证方式：
1. 执行 python --version。
2. 执行 python main.py --smoke。
3. 确认输出 worker smoke pass，退出码为 0。

完成后汇报：
- 改动文件
- 输入参数和输出结果
- 验证步骤和结果
- 后续扩展点
- 风险 / 待确认事项
```

## 模板五：测试验收任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md
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
4. 文档：确认 README、01-plan、01-status、smoke 文档没有明显冲突。

完成后汇报：
- 验收范围
- 执行命令
- 通过项
- 失败项和复现步骤
- 风险 / 待确认事项
```

## 模板六：文档更新任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md
- 需要更新的目标文档

当前角色：
文档线程。

当前目标：
更新 [文档路径]

任务范围：
1. 使用中文表述。
2. 只更新与当前目标直接相关的文档。
3. 保持 Week 01 初始化阶段边界。
4. 不写超出当前阶段的功能承诺。
5. 如果修改命令、目录、接口约定、测试方式或周状态，同步更新相关文档。

完成后汇报：
- 改动文件
- 主要内容变化
- 与哪些文档完成同步
- 风险 / 待确认事项
```

## 模板七：Bug 修复任务

```text
请先阅读：
- AGENTS.md
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md
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
- README.md
- docs/week/01-plan.md
- docs/week/01-status.md

当前角色：
项目经理线程 / 验收总结线程。

当前目标：
汇总 Day [数字] 验收结果，并更新 docs/week/01-status.md。

需要汇总：
1. 今日目标。
2. 各线程状态：待执行 / 执行中 / 待验收 / 通过 / 阻塞。
3. 已执行的验证命令。
4. 通过项。
5. 失败项或阻塞项。
6. 风险和下一步。

完成条件：
1. docs/week/01-status.md 与真实进展一致。
2. 不修改业务代码。
3. 最终汇报改动文件、验证方式、验证结果和风险。
```
