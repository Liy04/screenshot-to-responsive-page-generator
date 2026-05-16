# Week 10 Dev Smoke

## 运行环境

- Java 17
- Maven
- Node.js
- Python 3.11.9
- `IMAGEPAGE_WORKER_PYTHON_COMMAND` 建议显式设置
- 真实 AI 依赖外部模型服务和网络

## 关键配置

- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `OPENAI_API_KEY` 只通过环境变量提供，不写入真实值
- `IMAGEPAGE_WORKER_PYTHON_COMMAND`
- backend 真实链路 timeout 继续使用 `120` 秒

## 测试命令

- Worker：按本周相关 unittest 集合执行，结果 `67 / 67` 通过
- Backend：`mvn test`，结果 `45 / 45` 通过
- Frontend：`npm run test`，结果 `9 / 9` 通过
- 真实链路 smoke：已通过

## smoke 结果表

| 维度 | 结果 |
|---|---|
| REAL_AI | 通过 |
| FALLBACK | 通过 |
| FAILED | 通过 |
| artifact 检查 | 通过 |
| jobId 复用 | 通过 |
| iframe 安全 | 通过 |
| API key 安全 | 通过 |

## artifact 检查

- `layout.json`：通过
- `preview.html`：通过
- `metadata.json`：通过
- `artifact.reused=true`：通过

## iframe 安全检查

- iframe 使用 `sandbox=""`
- 未发现 `allow-scripts`
- preview 区域稳定显示

## API key 安全检查

- 未写入文档
- 未写入仓库
- 未写入日志
- 仅通过环境变量提供

## 风险

- `samples/` 目录尚未正式落地；本轮使用临时公开安全样例图完成 smoke。
- 真实 AI 调用仍依赖外部模型服务和网络。
- 同图多次生成仍可能有轻微差异。
- `backend/storage/`、`frontend/dist/` 等运行副产物不能提交。
