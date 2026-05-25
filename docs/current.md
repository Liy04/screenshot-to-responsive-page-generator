# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、当前活跃任务卡和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段

Week 13 已完成收口：继续做输出质量增强，重点是视觉清单稳定性、Layout JSON v0.1 映射质量、preview 样式表达、顺序 smoke 和轻量验收。

项目当前已经完成：

- Week 09：真实 AI 最小闭环。
- Week 10：真实 AI 链路稳定化、artifact 复用和可复现验收。
- Week 11：samples 建设、真实 AI smoke 文档化、metadata 增强和验收归档。
- Week 12：围绕三张简单 samples 提升真实 AI 输出质量和静态预览还原度。
- Week 13：继续提升三张 samples 的输出质量，完成顺序 smoke 和人工评分记录。

## Week 12 完成内容

Week 12 没有扩展数据库、Figma、多页面、编辑器或持久化主线，而是聚焦：

```text
同一张简单截图 -> 生成结果更像原图
```

已完成：

- 建立 Week 12 输出质量标准和 35 分评分表。
- 将真实 AI promptVersion 升级到 `week12-v1`。
- 将真实 AI 输出调整为“视觉清单提取”：`texts / regions / components`。
- Worker 将视觉清单确定性映射为 Layout JSON v0.1。
- 增强 JSON 清洗和轻量 repair。
- 增强 style key 白名单和 style value sanitizer。
- 增强静态编译器 card / button / input / text 基础样式。
- 前端 `/dev/image-to-layout` 增加原图 / iframe 对比。
- 三张 samples 完成 Worker direct smoke。
- 三张 samples 完成 Backend API smoke。
- sample 01 完成前端页面级 iframe smoke。

## Week 13 完成内容

Week 13 继续围绕同一条链路做质量增强，但没有进入 MySQL、Figma、复杂编辑器或持久化主线。

```text
更稳定的视觉清单
-> 更准的 Layout JSON v0.1 映射
-> 更像原图的 preview 样式
-> 可复现的顺序 smoke
-> 轻量验收
```

已完成：

- 建立 Week 13 输出质量标准和顺序 smoke 模板。
- 稳定真实 AI 视觉清单 shape，减少结构漂移。
- 增强 intermediate repair 和 Layout JSON v0.1 映射。
- 增强静态 preview 样式表达，但保持安全 sanitizer。
- 前端 `/dev/image-to-layout` 增加 smoke 摘要和原图 / iframe 对比。
- 三张 samples 完成顺序真实 AI smoke。
- 三张 samples 二次 generate 均命中 artifact 复用。
- 三张 samples 均完成 sandbox iframe 渲染检查。
- Week 13 平均分 27.0 / 35，最低分 26 / 35，达到稳定通过线。

## 当前不做

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
- 不做复杂真实整站截图。
- 不追求 1:1 高保真。
- 不升级 Layout JSON schema v0.2，除非 Week 13 明确规划。
- 不把模型原始 HTML 直接作为最终页面代码。
- 不提交真实 API key、私人截图、账号信息、公司资料、密钥或敏感页面。

## 当前风险 / 遗留项

- 真实 AI smoke 依赖外部模型服务、网络、环境变量和较长 timeout。
- 真实模型并发请求不稳定，后续 smoke 继续建议顺序执行。
- 复杂整页截图可能超时或质量很低，当前只验证简单样例。
- 同图多次生成仍可能有轻微差异；`jobId` artifact 复用已缓解重复生成漂移。
- `IMAGEPAGE_WORKER_PYTHON_COMMAND` 建议显式设置为 `D:\environment\python11\python.exe`。
- 后端真实 AI smoke 推荐至少使用 `--imagepage.worker.timeout-seconds=180`。
- `backend/storage/`、`frontend/dist/` 及其他运行副产物不能提交。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前规格：`docs/spec.md`
- 输出质量标准：`docs/quality/week13-quality.md`
- Week 13 smoke 记录：`docs/smoke/week13-quality-smoke.md`
- 文档索引：`docs/INDEX.md`
- Codex 角色边界：`docs/agents/README.md`
- Week 12 总结：`docs/archive/week/12-summary.md`
- Week 12 验收报告：`docs/archive/week/12-acceptance-report.md`
- 历史归档：`docs/archive/`

## Week 13 执行结果

执行位置：隔离 worktree `.worktrees/week13-quality`，分支 `week13-quality`。

代码实现和 smoke 文档主要在 worktree，尚未合并回 `main`。

| Day | 状态 | 说明 |
|---|---|---|
| Day 1 | 已完成 | Week 13 计划、任务卡、质量标准、smoke 模板已写入 docs |
| Day 2 | 已完成 | 视觉清单稳定性：prompt 固定 shape、intermediate 归一化 |
| Day 3 | 已完成 | Layout JSON v0.1 映射：input label、metric card 样式、form repair |
| Day 4 | 已完成 | 静态 preview 样式增强，Worker 全量 unittest 通过 |
| Day 5 | 已完成 | 前端 `/dev/image-to-layout` smoke 摘要与原图 / iframe 对比，frontend test/build 通过 |
| Day 6 | 已完成 | 三张 samples 顺序 smoke 与评分记录，平均 27.0 / 35 |
| Day 7 | 已完成 | 文档收口、Reviewer 检查与 Lead 二次验收 |

主要改动文件（worktree）：

- `worker/real_ai_layout_client.py`
- `worker/image_layout_pipeline.py`
- `worker/layout_static_generator.py`
- `worker/test_real_ai_layout_client.py`
- `worker/test_image_layout_pipeline.py`
- `worker/test_layout_static_generator.py`
- `frontend/src/views/ImageToLayoutDev.vue`
- `frontend/src/views/__tests__/ImageToLayoutDev.test.js`
- `frontend/src/style.css`
- `docs/quality/week13-quality.md`
- `docs/smoke/week13-quality-smoke.md`

验证（worktree）：

- `python -m unittest worker.test_real_ai_layout_client worker.test_image_layout_pipeline`：通过
- `python -m unittest discover -s worker -p "test_*.py"`：`87` 个测试通过
- `python -m unittest worker.test_layout_static_generator`：`30` 个测试通过
- `npm test -- --run`：`11` 个测试通过
- `npm run build`：通过
- 三张 samples 顺序 smoke：通过
- API key 精确扫描：未发现泄漏

Week 13 结论：

- 建议通过。
- 当前达到 25~28 稳定通过线，可以进入 Git 收口与合并评估。
- 后续如果继续质量主线，优先减少 warnings、提升文本和组件清单准确度，再考虑扩大样例集。

## 下一步状态

Week 13 已在 `.worktrees/week13-quality` 完成收口。下一步建议先做 Git diff 审查和必要测试复核，再决定是否合并回 `main`。
