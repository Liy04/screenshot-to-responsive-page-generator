# Worker

## 文件目的

本目录用于放置 Python worker 代码。当前阶段只提供最小 smoke 入口，验证 worker 可以独立运行。

## 运行方式

项目推荐目标版本为 Python 3.11。当前 smoke 脚本只使用 Python 标准库，允许使用 Python 3.10+ 本地验证。

在本目录执行：

```bash
python main.py --smoke
```

预期输出：

```text
worker smoke pass
```

成功时进程退出码为 0。

## 当前范围

当前只实现 smoke 分支，不接入真实模型 API、不接入 Figma API、不实现真实截图解析，也不实现真实页面代码生成。

## 后续扩展点

后续真实任务处理可以在保持 `main()` 入口清晰的前提下逐步扩展：

- 输入任务文件
- 解析任务参数
- 输出 mock 结果
- 与后端任务状态联动
