# Week 09 Summary

## 本周阶段

Week 09：真实 AI 最小接入，打通单张真实图片到 Layout JSON / generated-page 预览的最小闭环。

## 本周目标

把 Week 08 的 mock 链路推进到真实主链路：

```text
真实图片
-> 后端上传
-> 后端调用 Python Worker
-> Worker 调 SiliconFlow Qwen3-VL
-> REAL_AI 命中
-> Layout JSON v0.1
-> previewHtml
-> 前端 iframe 预览
```

## 完成内容

- 单张真实图片上传链路已完成。
- 原图访问接口已完成。
- 后端调用 Python Worker 链路已完成。
- Worker 已支持 `real-ai` / `fallback-only` CLI 模式。
- Worker 已接入 SiliconFlow OpenAI-compatible 接口。
- 当前已验证模型为 `Qwen/Qwen3-VL-32B-Instruct`。
- AI 输出会映射到当前 Layout JSON v0.1。
- validator 和 fallback 规则已接入真实主链路。
- generated-page `previewHtml` 已可返回给前端。
- 前端 `/dev/image-to-layout` 已接入真实链路，能展示原图、Layout JSON、previewHtml 和 iframe 预览。

## 最终真实 AI 闭环结果

最终关键复测结果：

- `POST /api/image-page/upload` 成功。
- `POST /api/image-page/jobs/{jobId}/generate` 成功。
- `HTTP 200`
- `status=SUCCESS`
- `mode=real-ai`
- `fallbackUsed=false`
- `sourceType=REAL_AI`
- `layoutJson.version=0.1`
- `validation.ok=true`
- `previewHtml` 非空
- 前端页面 iframe 渲染成功
- iframe 使用 `sandbox=""`
- 未发现 `allow-scripts`

## 关键接口

- `POST /api/image-page/upload`
- `GET /api/image-page/jobs/{jobId}/source`
- `POST /api/image-page/jobs/{jobId}/generate`

## Worker 变化

- 支持 `real-ai` / `fallback-only` CLI
- 接入 SiliconFlow OpenAI-compatible
- 验证模型为 `Qwen/Qwen3-VL-32B-Instruct`
- AI 输出先映射到 Layout JSON v0.1
- 接入 validator
- 输出 `previewHtml`

## 前端变化

- `/dev/image-to-layout` 已接入真实链路
- 支持原图展示
- 支持 Layout JSON 展示
- 支持 `previewHtml` 展示
- 支持 iframe sandbox 预览

## 验收结果

- 真实 AI 最小闭环已经打通。
- REAL_AI 已至少成功命中一次，不再只是 fallback 演示。
- 前端页面级 iframe 预览已验证成功。
- Week 09 已达到“可归档、可回看、可进入下一周规划”的状态。

## 风险

- 需要 Python 3.11+。
- 需要 `OPENAI_*` 环境变量。
- 需要 `IMAGEPAGE_WORKER_PYTHON_COMMAND`。
- 需要 `--imagepage.worker.timeout-seconds=120`。
- 损坏图片或异常模型输出时可能 fallback。
- 同一 `jobId` 重复生成时，真实 AI 结果可能有轻微差异。

## 后续建议

- 优先提升真实 AI 输出质量和稳定性。
- 可考虑固定生成参数或增加缓存结果机制。
- 可继续增强 Layout JSON 映射质量。
- 可继续完善测试、smoke 和实践报告素材。
- 暂不急于接 MySQL、Figma、编辑器或复杂历史记录系统。
