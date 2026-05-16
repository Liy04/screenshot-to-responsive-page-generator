# Week 10 Day 02

## 线程

Worker 线程

## 任务目标

增加 `promptVersion` 字段口径，并增强模型输出 JSON 提取 / 清洗能力。

## 必须完成

1. 增加 `promptVersion` 返回口径。
2. 支持处理纯 JSON、markdown code fence 包裹 JSON、前后带废话的 JSON。
3. JSON 解析失败时不崩溃，进入错误或 fallback 流程。

## 禁止事项

- 不改后端。
- 不改前端。

## 验收标准

- Worker 单测覆盖 JSON 清洗。
- 不破坏 Week 09 REAL_AI / fallback 链路。
