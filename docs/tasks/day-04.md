# Week 10 Day 04

## 线程

后端线程

## 任务目标

保存 `layout.json`、`preview.html`、`metadata.json`，并支持同一 `jobId` 成功 artifact 复用。

## 必须完成

1. 保存本地 artifact 文件。
2. 同一 `jobId` 已有成功 artifact 时，不重复调用真实 AI。
3. 返回结构包含 artifact / metadata / `fallbackReason` / `warnings` / `errors`。

## 禁止事项

- 不接 MySQL。
- 不创建 Entity / Mapper。

## 验收标准

- 后端测试覆盖保存、读取、复用、worker failure、timeout。
- 不提交 storage 运行副产物。
