# Week 10 Summary

## 本周阶段

Week 10：真实 AI 链路稳定化与可复现验收。

## 本周目标

在 Week 09 已跑通真实 AI 最小闭环的基础上，完成稳定化、可解释性、artifact 保存与复用、前端状态展示和可重复 smoke 的收口。

## 完成内容

### Worker

- `promptVersion` 已加入输出，当前值 `week10-v1`。
- JSON 清洗支持纯 JSON、markdown code fence、前后带说明文字。
- 非 JSON 输出不会崩溃，可进入 fallback。
- 轻量 intermediate repair 已支持。
- `fallbackReason` 已加入输出。
- `REAL_AI` / `FALLBACK` / `FAILED` 路径已验证。

### 后端

- 已保存 artifact：
  - `layout.json`
  - `preview.html`
  - `metadata.json`
- 同一 `jobId` 成功 artifact 可复用。
- 第二次 generate 命中 `artifact.reused=true`，不重复调用 Worker。
- 返回结构包含 `promptVersion`、`fallbackReason`、`warnings`、`errors`、`artifact`。
- 未接 MySQL，未创建 Entity / Mapper。

### 前端

- 已展示 `REAL_AI` / `FALLBACK` / `FAILED` / `TIMEOUT`。
- 已展示 `promptVersion`、`fallbackReason`、`warnings`、`errors`、artifact 信息。
- iframe preview 保持稳定。
- iframe 使用 `sandbox=""`，无 `allow-scripts`。

## 测试与验收结果

- Worker：`67 / 67` 通过。
- Backend：`45 / 45` 通过。
- Frontend：`9 / 9` 通过。
- 真实链路 smoke 通过。
- `REAL_AI` / `FALLBACK` / `FAILED` 三种口径已验证。
- artifact 文件检查通过。
- `jobId` 复用检查通过。
- API key 未泄漏。
- `backend/storage/` 是运行副产物，已被 `backend/.gitignore` 忽略。

## 风险

1. `samples/` 目录尚未落地；本轮使用临时公开安全样例图完成 smoke。
2. `IMAGEPAGE_WORKER_PYTHON_COMMAND` 当前建议显式设置，虽然 PATH 上 Python 3.11.9 可用。
3. 真实 AI 调用仍依赖外部模型服务和网络。
4. 同图多次生成仍可能有轻微差异；`jobId` artifact 复用已缓解重复查询漂移。
5. 当前仍未进入 MySQL / Figma / 编辑器 / 多页面阶段。
6. `backend/storage/`、`frontend/dist/` 及其他运行副产物不能提交。

## 后续建议

- 可以进入 Week 11 规划。
- 优先考虑真实 AI 输出质量和一致性进一步提升。
- 继续补强测试覆盖、报告材料和可公开样例图管理方式。
