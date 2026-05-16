# Week 10 Day 03

## 线程

Worker 线程

## 任务目标

对轻微缺字段尝试 repair；repair 失败再 fallback；fallback 时返回 `fallbackReason`。

## 必须完成

1. 增加轻量 repair 逻辑。
2. repair 失败后进入 fallback。
3. 返回 `fallbackReason`。
4. 约定并实现建议的 `fallbackReason` 枚举。

## 禁止事项

- 不扩大成复杂修复系统。
- 不改后端和前端。

## 验收标准

- Worker 单测覆盖 repair 成功。
- Worker 单测覆盖 repair 失败。
- Worker 单测覆盖 `fallbackReason`。
