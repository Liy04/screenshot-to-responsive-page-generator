# ADR-0002: Layout JSON 优先

## 状态

Accepted

## 背景

如果直接从截图或 Figma 信息进入 Vue / HTML 代码生成，结构、校验、调试和追踪都会变得不稳定。

## 决策

先建立 Layout JSON v0.1 中间层，再进入后续校验、保存、查看和静态编译。

Layout JSON 用于描述页面结构、节点语义、资源引用、响应式规则、假设和风险。

## 影响

- Week 03 先稳定 Layout JSON v0.1、Schema、示例和校验器。
- 后续生成或编译能力以 Layout JSON 为输入。
- Layout JSON 不是 HTML / Vue，也不代表真实 AI / Figma 接入。

## 参考

- `docs/specs/layout-json-v0.1.md`

