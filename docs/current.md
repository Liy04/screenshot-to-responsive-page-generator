# Current

## 文件目的

本文档是当前阶段事实源。Codex 日常任务默认读取 `AGENTS.md`、本文档、`docs/task.md` 和当前任务相关代码即可；必要时再读取 `docs/spec.md`。

`docs/archive/` 只做历史归档，不参与默认上下文。

## 当前阶段状态

Week 04 Layout JSON 静态编译器 v0.1 与安全预览闭环。

Week 04 主链路已完成，并已通过 Day 6 集成 smoke。当前处于 Day 7 文档收口与总结阶段，下一阶段准备进入 Week 05 规划。

## 当前目标

已跑通 Layout JSON v0.1 到静态预览产物的确定性规则编译链路：

```text
Layout JSON v0.1
-> Worker 校验
-> Worker 静态编译 htmlCode / cssCode
-> generated-page artifact
-> 后端 mock 保存 / 查询
-> 前端 iframe sandbox 安全预览
```

这里的“生成”不是 AI 生成，而是基于 Layout JSON 的规则编译。

## 当前允许

- Worker 使用 Python 标准库实现静态编译器。
- Worker 复用 `worker/layout_validator.py`。
- Worker 输出 `generated-page` artifact。
- 后端继续使用本地 mock 文件保存 / 查询。
- 前端使用 `iframe sandbox=""` 预览 `htmlCode + cssCode`。
- `vueCode` 只作为文本展示，不要求可运行。

## Week 04 完成摘要

- Worker 静态编译器已完成。
- Worker 静态编译器测试已完成。
- 后端 generated-page artifact mock PUT / GET 接口已完成。
- 前端 generated-page 展示与 `iframe sandbox` 预览已完成。
- Day 6 集成 smoke 已通过。
- Week 04 建议判定为通过。

## 当前禁止

- 不接真实 AI。
- 不接 OpenAI / Claude / Gemini SDK。
- 不接 Figma API / Figma MCP。
- 不接 MySQL 实际落库。
- 不创建数据库表。
- 不新增 Entity / Mapper。
- 不新增数据库配置。
- 不接 Redis / RabbitMQ。
- 不做 ZIP 导出。
- 不做拖拽编辑器或在线编辑器。
- 不做真实截图解析。
- 不做登录注册、历史记录持久化或复杂权限。
- 不要求 `vueCode` 真正可运行。
- 不做 Playwright 视觉回归。

## 推荐实现

- Worker 输入 Layout JSON v0.1，先调用既有 validator。
- validator 通过后，静态编译输出 `htmlCode`、`cssCode`、`vueCode`、`validation`、`unsupportedNodes`。
- validator 失败时输出 `status=FAILED` artifact，`htmlCode/cssCode/vueCode` 为空字符串，退出码为 1。
- 后端 mock 文件大小建议限制为 2MB。
- 前端 iframe 必须使用 `sandbox=""`，不加 `allow-scripts`。

## Day 6 smoke 记录

- Worker smoke 通过。
- 后端 PUT / GET / 404 / 400 通过。
- 前端 build 通过。
- 前端页面联调通过。
- iframe 使用 `sandbox=""`，且无 `allow-scripts`。
- 未做 Playwright 视觉回归，符合当前限制。
- 无残留后台服务。

## 风险 / 待确认事项

- 详情页旧 Week 02 generation 查询失败时，会显示“加载失败 / 任务不存在”，但 Week 04 generated-page 区域仍可正常展示；这是 UX / 联调口径待确认项。
- `backend/target`、`frontend/dist` 是构建副产物，按忽略规则处理。
- `backend/mock-data` 是本地 mock 副产物，按忽略规则处理。
- 当前 generated-page 保存仍是本地 mock 文件，不是数据库持久化。
- 当前 Layout JSON 仍来自手写 / 示例，不是真实截图解析。
- 当前静态编译器是规则编译，不是真实 AI 生成。

## Week 05 候选方向

- 方向 A：修正前端详情页 UX，让 generated-page dev 预览不依赖 Week 02 generation job。
- 方向 B：补后端 / 前端更稳定的自动化测试。
- 方向 C：增强静态编译器支持更多 Layout JSON 节点和 style subset。
- 方向 D：如用户确认，再规划 MySQL 持久化；当前不直接进入。

## 当前文档入口

- 当前计划：`docs/plan.md`
- 当前任务：`docs/task.md`
- 当前规格：`docs/spec.md`
- 文档索引：`docs/INDEX.md`
- context-scout 流程：`docs/playbooks/context-scout.md`
- 历史归档：`docs/archive/`
