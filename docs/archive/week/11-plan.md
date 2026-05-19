# Week 11 计划：真实 AI 链路可复现验收与样例资产建设

项目名：`screenshot-to-responsive-page-generator`

当前阶段：Week 10 已完成并收口，项目进入 Week 11 规划前状态。

当前协作模式：Codex Lead + Lightweight Agents Workflow

---

## 1. Week 11 总主题

**真实 AI 链路可复现验收与样例资产建设**

一句话目标：

> 建立一套安全、可提交、可复现的 samples + smoke + 文档验收体系，让 Week 09 / Week 10 的真实 AI 能力变成后续每周都能稳定回归的项目资产。

---

## 2. Week 11 规划结论

Week 11 不建议立刻进入 MySQL、Figma、编辑器、多页面、Playwright 视觉回归等新方向。

当前项目已经完成：

- Week 09：真实 AI 最小闭环。
- Week 10：真实 AI 链路稳定化与可复现验收。
- Worker / Backend / Frontend 测试通过。
- REAL_AI / FALLBACK / FAILED 路径已验证。
- artifact 保存与 jobId 复用已完成。
- 前端可展示 promptVersion、fallbackReason、warnings、errors、artifact 信息。

因此，Week 11 的重点应该是：

> 把已经跑通的真实 AI 链路，沉淀成可复现、可验收、可展示、可复盘的项目资产。

---

## 3. Week 11 不做事项

本周明确不进入以下方向：

- 不接 MySQL。
- 不设计数据库表。
- 不创建 Entity / Mapper。
- 不接 Figma API / Figma MCP。
- 不接 Redis / RabbitMQ。
- 不做多页面生成。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。
- 不做登录注册 / 权限系统。
- 不做高保真截图还原。
- 不做 Playwright 视觉回归。

这些方向后续都可以做，但不适合作为 Week 11 的主线。

---

## 4. Week 11 总目标

到本周结束，项目应该达到以下状态：

1. 仓库中有一组公开安全的 `samples/` 图片。
2. 有一套固定的真实 AI smoke 输入和执行说明。
3. 真实 AI 链路的结果信息更清楚。
4. 前端能更好展示生成过程、状态和结果解释。
5. 文档能说明真实 AI 链路怎么跑、怎么验收、失败怎么看。
6. 所有测试继续通过。
7. API key、运行副产物、真实隐私截图不进入仓库。

---

## 5. Week 11 推荐排期

| Day | 主题 | Agent | 是否编码 | 优先级 |
|---|---|---|---|---|
| Day 1 | Week 11 任务卡与边界确认 | lead + docs-agent | 否 | 必做 |
| Day 2 | samples/ 安全样例集 | explorer-agent → docs-agent → tester-agent → reviewer-agent | 少量 | 必做 |
| Day 3 | 真实 AI smoke 文档 / 示例脚本 | docs-agent → tester-agent | 少量 | 必做 |
| Day 4 | metadata 可解释性小增强 | explorer-agent → worker/backend/frontend 分阶段 → tester-agent → reviewer-agent | 是 | 可做 |
| Day 5 | Week 11 验收归档与 Git 收口 | lead + tester-agent + reviewer-agent | 否 / 少量 | 必做 |

说明：

- Day 4 是唯一可能膨胀的任务。
- 如果 Day 2 / Day 3 没做完，Day 4 可以砍掉。
- Week 11 的主目标不是新功能，而是可复现验收和资产沉淀。
- `docs/week11-plan.md` 是原始长计划来源，Day 1 执行时应归档到 `docs/archive/week/11-plan.md`，日常默认上下文只保留 `docs/current.md`、`docs/plan.md` 和 `docs/tasks/day-xx.md`。

---

## 6. Day 1：Week 11 任务卡与边界确认

### 目标

让 Codex Lead 收口 Week 11 边界，并创建本周任务卡。

### 建议使用角色

- lead
- docs-agent

### 建议给 Codex Lead 的指令

```text
请按当前项目的 Codex Lead + Lightweight Agents Workflow，规划 Week 11。

读取：
- AGENTS.md
- docs/current.md
- docs/plan.md
- docs/spec.md（必要时）

不要默认读取：
- docs/archive/

目标：
Week 11 聚焦真实 AI 链路的可复现验收与 samples 建设。
不要进入 MySQL、Figma、编辑器、多页面、Playwright 视觉回归。

请输出：
1. Week 11 目标
2. Day 1 ~ Day 5 任务拆分
3. 每天使用哪个 agent
4. 每天交付物
5. 每天验收标准
6. 风险与不做事项
7. 生成 docs/tasks/day-01.md 到 docs/tasks/day-05.md 的建议
```

### 交付物

- 新的 `docs/tasks/day-01.md` 到 `docs/tasks/day-05.md`
- 更新 `docs/current.md`
- 必要时更新 `docs/plan.md`
- 将 `docs/week11-plan.md` 归档到 `docs/archive/week/11-plan.md`

### 验收标准

```text
[ ] docs/tasks/day-01.md 到 docs/tasks/day-05.md 创建完成
[ ] docs/current.md 更新到 Week 11
[ ] docs/plan.md 更新为 Week 11 摘要
[ ] docs/week11-plan.md 已归档到 docs/archive/week/11-plan.md
[ ] 明确本周不做 MySQL / Figma / 编辑器 / 多页面 / Playwright 视觉回归
[ ] 每天任务都有 agent、交付物、验收标准
[ ] 没有引入新的大模块
```

---

## 7. Day 2：建立 samples/ 安全样例集

### 目标

把 Week 10 smoke 输入固化成可提交、可复现、安全的样例资产。

### 建议使用角色

- explorer-agent
- docs-agent
- tester-agent
- reviewer-agent

### 建议给 Codex 的指令

```text
请进入 explorer-agent 阶段，先只读探索 samples/ 应该如何落地。

目标：
建立公开安全 samples 数据集，用于真实 AI 链路 smoke 和后续回归。

要求：
1. 不提交任何真实业务截图、手机号、账号、头像、公司隐私数据。
2. samples 图片必须是公开安全、可提交的测试素材。
3. 给每个 sample 增加说明文档。
4. 不修改真实 AI 业务逻辑。
5. 不写入 API key。
6. 如需生成图片资产，只能使用无品牌、无隐私、无版权争议的 mock UI 图。
7. 完成后由 tester-agent 检查图片是否可用于 smoke，由 reviewer-agent 检查隐私、密钥和版权风险。
```

### 建议目录结构

```text
samples/
  README.md
  image-to-layout/
    simple-card.png
    simple-form.png
    simple-dashboard.png
    expected-notes.md
```

### 建议样例类型

| 文件 | 用途 |
|---|---|
| `simple-card.png` | 验证基础卡片布局 |
| `simple-form.png` | 验证表单 / 输入框识别 |
| `simple-dashboard.png` | 验证多区域页面结构 |

### 交付物

- `samples/README.md`
- 至少 2~3 张公开安全样例图片
- 每个样例的用途说明
- smoke 推荐输入说明

### 验收标准

```text
[ ] samples/README.md 存在
[ ] 至少 2~3 张公开安全样例图
[ ] 每张图说明验证目标
[ ] 不含手机号、账号、真实业务数据、真实用户头像
[ ] 不含第三方品牌或版权不明素材
[ ] 可以用于真实 AI smoke
[ ] 不影响现有测试
[ ] reviewer-agent 未发现隐私 / 密钥 / 版权阻塞风险
```

---

## 8. Day 3：真实 AI smoke 文档与半自动脚本

### 目标

把“怎么跑真实 AI 链路”从口头经验变成文档和命令。

### 建议使用角色

- docs-agent
- tester-agent

### 建议给 Codex 的指令

```text
请按 docs-agent → tester-agent 顺序执行。

目标：
整理真实 AI 链路 smoke 的可复现执行方式。

要求：
1. docs-agent 只整理文档和可选 example 脚本，不修改业务代码。
2. 不泄漏 OPENAI_API_KEY。
3. 明确推荐 Python 版本、环境变量、后端启动命令。
4. 明确 timeout 建议。
5. 明确 REAL_AI / FALLBACK / FAILED 的判断标准。
6. 增加 artifact 检查说明。
7. tester-agent 只验证命令口径和安全边界，默认不修业务代码。
```

### 建议新增文档

```text
docs/smoke/
  real-ai-smoke.md
```

### 可选新增脚本

```text
scripts/
  smoke-real-ai.example.ps1
```

脚本中只能出现占位符，例如：

```powershell
$env:OPENAI_API_KEY="<set-your-key-here>"
```

不能写真实 key。
脚本不得自动提交、不得写入真实密钥、不得默认执行真实联网请求；真实联网 smoke 必须由任务卡明确允许。

### 文档必须包含

```text
[ ] Python 推荐版本：3.11.9
[ ] OPENAI_BASE_URL=https://api.siliconflow.cn/v1
[ ] OPENAI_MODEL=Qwen/Qwen3-VL-32B-Instruct
[ ] OPENAI_API_KEY 必须通过环境变量设置
[ ] IMAGEPAGE_WORKER_PYTHON_COMMAND 示例
[ ] 后端启动 timeout 建议 120 秒
[ ] REAL_AI / FALLBACK / FAILED 判断口径
[ ] artifact 文件检查方式
[ ] jobId 复用检查方式
```

### 验收标准

```text
[ ] 新人按文档能跑 smoke
[ ] 明确 120 秒 timeout 推荐
[ ] 明确 backend/storage/ 不提交
[ ] 明确 API key 只走环境变量
[ ] 明确真实 AI smoke 依赖外部模型服务和网络
[ ] smoke 文档能解释成功、fallback、失败三种情况
```

---

## 9. Day 4：增强结果可解释性

### 目标

在不大改架构的前提下，让真实 AI 生成结果更容易判断和展示。

### 建议使用角色

- explorer-agent
- worker-agent
- backend-agent
- frontend-agent
- tester-agent
- reviewer-agent

### Day 4 范围控制

Day 4 只能做：

```text
metadata polish
```

Day 4 必须拆成顺序阶段，不能交给一个角色一次性完成：

```text
4A explorer-agent：确认 Worker / Backend / Frontend metadata 影响范围
4B worker-agent：最小字段输出
4C backend-agent：透传 / 保存字段
4D frontend-agent：展示字段
4E tester-agent：测试和 smoke
4F reviewer-agent：安全、契约和边界审查
```

不做：

```text
完整调用链 tracing
复杂 metadata 表
数据库记录
新的 result schema 大改
架构重构
```

### 优先增强字段

第一优先级：

```text
durationMs
model
artifact.reused
```

注意：

- 默认不做 `sourceImageName`，避免泄漏本地文件名或隐私信息；如后续确实需要，只能使用 sanitized fileName，并单独验收。
- `baseUrlHost` 默认不做；如后续确实需要，只能展示 host 级别信息，不能展示完整 URL、query、token 或 key。
- 不能泄漏 `OPENAI_API_KEY`。
- 不要输出完整敏感配置。

### 建议给 Codex 的指令

```text
请先进入 explorer-agent 阶段，确认当前 Worker、Backend、Frontend 对 metadata 的传递链路。

目标：
在最小改动范围内增强真实 AI 结果的可解释性。

优先字段：
- durationMs
- model
- promptVersion
- fallbackReason
- warnings
- errors
- artifact.reused

要求：
1. 不引入 MySQL。
2. 不改变现有 API 主结构。
3. 不破坏 Week 10 已通过测试。
4. 不泄漏 OPENAI_API_KEY。
5. 实现后进入 tester-agent。
6. 代码变更后进入 reviewer-agent。
```

### 交付物

- Worker / Backend / Frontend 的最小字段增强
- 对应测试更新
- 前端展示优化

### 验收标准

```text
[ ] 不改变现有 API 主结构
[ ] 不引入 MySQL
[ ] 不破坏 Week 10 测试
[ ] 不泄漏 OPENAI_API_KEY
[ ] 前端展示 durationMs / model / artifact.reused
[ ] REAL_AI / FALLBACK / FAILED 展示仍正常
[ ] Worker 测试通过
[ ] Backend 测试通过
[ ] Frontend 测试通过
```

---

## 10. Day 5：Week 11 验收、总结与 Git 收口

### 目标

完成 Week 11 收口，不把半成品文档、运行副产物、敏感信息留进仓库。

### 建议使用角色

- lead
- tester-agent
- reviewer-agent
- docs-agent

### 建议给 Codex Lead 的指令

```text
请以 Codex Lead 身份做 Week 11 收口验收。

读取：
- AGENTS.md
- docs/current.md
- docs/plan.md
- docs/tasks/day-xx.md
- 本周变更文件

要求：
1. 汇总 Week 11 完成内容。
2. 检查是否误进入 MySQL / Figma / 编辑器 / 多页面等非本周范围。
3. 检查是否有 API key 泄漏风险。
4. 检查 backend/storage/、frontend/dist/ 等运行副产物是否未提交。
5. 汇总测试结果。
6. 给出 Git commit 建议。
```

### 建议归档文件

```text
docs/archive/week/11-summary.md
docs/archive/week/11-dev-smoke.md
docs/archive/week/11-acceptance-report.md
```

### 必须更新

```text
docs/current.md
```

### Git 收口前检查

```text
[ ] 没有 API key
[ ] 没有 backend/storage/
[ ] 没有 frontend/dist/
[ ] 没有真实隐私截图
[ ] 没有误提交运行副产物
[ ] 没有进入 Week 11 禁止范围
[ ] 测试结果已记录
[ ] smoke 结果已记录
```

---

## 11. Week 11 最终验收清单

```text
[ ] samples/ 已建立
[ ] samples 图片安全、可提交
[ ] samples/README.md 说明清楚
[ ] smoke 文档可复现
[ ] 真实 AI 启动命令明确
[ ] OPENAI_API_KEY 只通过环境变量配置
[ ] REAL_AI / FALLBACK / FAILED 判断标准清楚
[ ] artifact 文件检查清楚
[ ] jobId 复用检查清楚
[ ] 前端展示 promptVersion / fallbackReason / warnings / errors / artifact
[ ] 如增强 metadata，则 durationMs / model / reused 展示清楚
[ ] Worker tests pass
[ ] Backend tests pass
[ ] Frontend tests pass
[ ] backend/storage/ 未提交
[ ] frontend/dist/ 未提交
[ ] Week 11 summary 已归档
[ ] Week 11 acceptance report 已归档
```

---

## 12. Week 11 最大风险

### 风险 1：samples 图片不安全

不能放：

```text
真实后台截图
真实账号
手机号
邮箱
真实头像
公司内部页面
第三方版权不明页面截图
```

建议使用：

```text
自己手工画的简单 UI 图
本地 HTML 渲染后截图
无品牌、无隐私、无真实业务含义的 mock 页面
```

### 风险 2：Day 4 变成大重构

Day 4 只能做轻量增强。

如果 Codex 开始建议：

```text
重构 result schema
引入数据库
引入链路追踪系统
新增复杂 metadata 表
重写 Worker / Backend 返回结构
```

应该直接拒绝或改回小范围。

### 风险 3：真实 AI 依赖外部服务

真实 AI smoke 不是普通单元测试，它依赖：

```text
OPENAI_API_KEY
SiliconFlow 网络
模型服务可用性
模型输出稳定性
较长 timeout
```

失败时要区分：

```text
网络失败
模型失败
JSON 解析失败
fallback 成功
后端调用失败
前端展示失败
artifact 复用失败
```

---

## 13. Week 11 最终结论

Week 11 可以执行。

推荐定版为：

> Week 11 不开新主线，只做真实 AI 链路的可复现验收、samples 建设、smoke 文档化和轻量可解释性增强。

本周最重要的三个结果是：

1. `samples/` 正式落地。
2. 真实 AI smoke 可以被复现。
3. Week 09 / Week 10 的成果可以被文档化展示和长期回归。

计划验收评级：**A-**

扣分点：

- Day 4 的 metadata 增强存在范围膨胀风险。

控制方式：

- Day 4 只做小字段、小展示、小测试。
- 如果 Day 2 / Day 3 未完成，Day 4 可以砍掉。
- 不允许为了 Day 4 引入 MySQL、Figma、复杂 tracing 或 schema 大改。
