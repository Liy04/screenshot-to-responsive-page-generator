# ADR-0004: 先做静态编译器，再考虑 AI 生成

## 状态

Accepted

## 背景

项目长期目标包含从截图 / Figma 到响应式页面代码，但当前阶段仍需要先验证确定性链路，避免过早接入真实模型 API。

## 决策

Week 04 优先实现 Layout JSON 静态编译器 v0.1。

这里的“生成”是确定性规则编译，不是 AI 生成。

静态编译器输入已通过校验的 Layout JSON v0.1，输出 `htmlCode`、`cssCode` 和展示用 `vueCode`，并通过前端 `iframe sandbox` 安全预览。

## 影响

- 当前阶段不接 OpenAI / Claude / Gemini SDK。
- 当前阶段不接 Figma API / Figma MCP。
- 当前阶段不要求 `vueCode` 真正可运行。
- 后续如进入 AI 生成，需要单独确认范围、风险和验收标准。

## 参考

- `docs/plans/week-04.md`
- `docs/specs/layout-to-html-v0.1.md`
- `docs/specs/generated-page-artifact-v0.1.md`

