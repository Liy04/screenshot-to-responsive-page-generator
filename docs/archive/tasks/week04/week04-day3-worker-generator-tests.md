# Week 04 Day 3：Worker 静态编译器测试

## 任务目标

线程：Worker 测试线程。

实现 `worker/test_layout_static_generator.py`，验证静态编译器和已有 validator 协同工作。

## 必须完成

- 新增 `worker/test_layout_static_generator.py`。
- 覆盖 5 个 valid 示例可以生成 `htmlCode` / `cssCode`。
- 覆盖 3 个 invalid 示例不能生成可预览代码。
- 覆盖 text 节点 content 出现在 `htmlCode`。
- 覆盖 button 节点 content 出现在 `htmlCode`。
- 覆盖 image 缺 src / assetId 时生成 warning。
- 覆盖 `layoutHash` 稳定生成。
- 覆盖 `validation.errors` 非空时 `status=FAILED`。

## 禁止事项

- 不修改静态编译器实现，除非测试暴露问题且用户确认进入修复。
- 不接 AI / Figma。
- 不接 MySQL / Redis / RabbitMQ。
- 不修改前端或后端代码。
- 不新增依赖。

## 建议读取文件

- `AGENTS.md`
- `docs/context/current-phase.md`
- `docs/tasks/week04-day3-worker-generator-tests.md`
- `docs/generated-page-artifact-design.md`
- `docs/layout-to-html-mapping.md`
- `worker/layout_static_generator.py`
- `worker/layout_validator.py`
- `examples/valid/*.layout.json`
- `examples/invalid/*.layout.json`

## 建议修改文件

- `worker/test_layout_static_generator.py`

## 验收标准

执行通过：

```bash
python -m unittest worker.test_layout_validator
python -m unittest worker.test_layout_static_generator
```

## Codex 执行要求

先输出计划，等待确认后再写测试。测试线程如果发现问题，优先记录问题，不直接扩大修复范围。
