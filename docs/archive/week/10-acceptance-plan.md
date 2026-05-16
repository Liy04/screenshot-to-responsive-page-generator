# Week 10 验收计划

> 项目名称：`screenshot-to-responsive-page-generator`  
> 阶段主题：真实 AI 链路稳定化与可复现验收  
> 验收范围：Week 10  
> 文档用途：用于判断 Week 10 是否真正完成，而不是只看功能是否“能跑一次”。

---

## 一、验收目标

Week 10 最终要验收的不是“项目有没有新增很多功能”，而是这 5 件事：

### 1. 真实 AI 输出更稳定

需要确认：

- prompt 有版本；
- 模型输出能尽量约束成 JSON；
- 非标准 JSON 能清洗；
- 可修复错误先 repair；
- repair 失败再 fallback。

### 2. 失败原因更清楚

fallback 不能只显示：

```text
fallbackUsed=true
```

必须能看到：

```text
fallbackReason
warnings
errors
```

并且至少能区分：

- timeout；
- 模型异常；
- JSON 解析失败；
- schema 校验失败；
- 图片读取失败；
- previewHtml 编译失败。

### 3. 结果可以复现

需要确认：

- 同一个 `jobId` 查询时不能重复调用 AI；
- 已生成结果要保存到本地 artifact；
- `layout.json`、`preview.html`、`metadata.json` 等文件要能查到。

### 4. 前端状态更清楚

需要确认：

- `REAL_AI`、`FALLBACK`、`FAILED`、`TIMEOUT` 状态要能区分；
- `warnings` / `errors` 要能展示；
- iframe 预览区域要稳定；
- iframe 仍然必须保持 `sandbox=""`；
- 不能出现 `allow-scripts`。

### 5. 测试和 smoke 可重复执行

不能只靠手动试一次。

必须有：

- 固定样例图；
- smoke 文档；
- Worker 单元测试；
- 后端接口 / 集成测试；
- 前端状态展示测试。

---

## 二、验收范围

### 2.1 本次验收包含

| 模块 | 验收内容 |
|---|---|
| Worker | prompt、JSON 清洗、repair、fallbackReason、warnings/errors、previewHtml 编译 |
| 后端 | 调用 Worker、timeout 配置、artifact 保存、jobId 复用、异常透传 |
| 前端 | 状态展示、warnings/errors 展示、iframe preview、安全 sandbox |
| 测试 | Worker 单测、后端测试、前端测试、真实链路 smoke |
| 文档 | current、plan、spec、day-xx、smoke、week-10-summary |

### 2.2 本次验收不包含

Week 10 不验收下面这些内容：

- MySQL；
- Entity / Mapper；
- Figma API；
- Figma MCP；
- Redis；
- RabbitMQ；
- 多页面生成；
- 拖拽编辑器；
- 在线编辑器；
- ZIP 导出；
- 登录注册；
- 权限系统；
- 高保真截图还原；
- 复杂历史记录持久化。

原因：

> Week 10 的目标是稳定真实 AI 最小闭环，不是扩展大型功能。

---

## 三、验收前准备

### 3.1 Python 环境检查

验收前必须确认 Python 版本。

```bash
D:\environment\python11\python.exe --version
```

期望结果：

```text
Python 3.11.9
```

或者至少是：

```text
Python 3.11+
```

不建议继续用 Python 3.10.1，因为之前出现过 SiliconFlow TLS EOF 连接问题。

---

### 3.2 环境变量检查

必须确认：

```bash
echo %OPENAI_BASE_URL%
echo %OPENAI_MODEL%
echo %IMAGEPAGE_WORKER_PYTHON_COMMAND%
```

`OPENAI_API_KEY` 只允许检查“是否已设置”，不允许打印真实值到控制台、日志或文档。

期望：

```text
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
OPENAI_MODEL=Qwen/Qwen3-VL-32B-Instruct
OPENAI_API_KEY=已设置，但不能打印真实 key 到日志或文档
IMAGEPAGE_WORKER_PYTHON_COMMAND=D:\environment\python11\python.exe
```

注意：

> `OPENAI_API_KEY` 只能通过环境变量设置，禁止写入代码、文档、日志和 Git 提交。

---

### 3.3 后端启动命令

建议验收时用这个命令：

```bash
java -jar target/backend-0.0.1-SNAPSHOT.jar --imagepage.worker.timeout-seconds=120
```

原因：

> 默认 30 秒 timeout 不适合真实多模态调用，真实 AI 调用建议使用 120 秒 timeout。

---

### 3.4 样例图片准备

建议准备 5 张图：

```text
samples/
├── 01-simple-card-page.png
├── 02-landing-hero.png
├── 03-form-page.png
├── 04-dashboard-lite.png
└── 05-broken-image.png
```

每张图用途：

| 图片 | 用途 |
|---|---|
| `01-simple-card-page.png` | 验证基础识别 |
| `02-landing-hero.png` | 验证首屏布局 |
| `03-form-page.png` | 验证表单类页面 |
| `04-dashboard-lite.png` | 验证稍复杂布局 |
| `05-broken-image.png` | 验证异常图片 fallback / error |

额外要求：

- `samples/` 目录只允许放公开、无隐私、可提交的测试图片。
- 不允许提交私人截图、账号信息、公司资料、密钥或敏感页面。

---

## 四、验收通过标准总览

### 4.1 P0 必须全部通过

| 编号 | 验收项 | 通过标准 |
|---|---|---|
| P0-1 | 真实 AI 链路可运行 | 上传真实图片后返回 HTTP 200 |
| P0-2 | Layout JSON 合法 | `layoutJson.version=0.1`，且 validator 通过 |
| P0-3 | previewHtml 非空 | 返回的 `previewHtml` 不为空 |
| P0-4 | iframe 可预览 | 前端 iframe 能正常显示页面 |
| P0-5 | iframe 安全 | `sandbox=""`，无 `allow-scripts` |
| P0-6 | prompt 有版本 | 返回 `promptVersion` |
| P0-7 | fallback 有原因 | fallback 时必须有 `fallbackReason` |
| P0-8 | warnings/errors 可返回 | 返回结构中有 `warnings` 和 `errors` |
| P0-9 | artifact 可保存 | 本地存在 `layout.json`、`preview.html`、`metadata.json` |
| P0-10 | jobId 可复用 | 同一个 jobId 查询不重复调用 AI |
| P0-11 | timeout 可控 | timeout 使用 120 秒配置 |
| P0-12 | smoke 文档存在 | 有可复现的 Week 10 smoke 文档 |

---

### 4.2 P1 尽量通过

| 编号 | 验收项 | 通过标准 |
|---|---|---|
| P1-1 | 前端状态展示清楚 | REAL_AI / FALLBACK / FAILED / TIMEOUT 可区分 |
| P1-2 | repair 可用 | 缺少轻微字段时能自动修复 |
| P1-3 | Worker 单测通过 | JSON 清洗、repair、fallback 测试通过 |
| P1-4 | 后端测试通过 | artifact、timeout、worker failure 测试通过 |
| P1-5 | 前端测试通过 | 状态展示、warnings/errors、iframe sandbox 测试通过 |

---

### 4.3 P2 可选通过

| 编号 | 验收项 | 通过标准 |
|---|---|---|
| P2-1 | durationMs | 能显示生成耗时 |
| P2-2 | repairUsed | 能显示是否使用 repair |
| P2-3 | sourceType | 能显示 REAL_AI / FALLBACK |
| P2-4 | debug metadata | 能显示 model、promptVersion、artifactPath 等信息 |

---

## 五、每日验收计划

---

## Day 01：文档与范围验收

### 验收目标

确认 Week 10 范围已经收住，不会跑偏。

### 必须检查的文件

```text
docs/current.md
docs/plan.md
docs/spec.md
docs/tasks/day-01.md
docs/tasks/day-02.md
docs/tasks/day-03.md
docs/tasks/day-04.md
docs/tasks/day-05.md
docs/tasks/day-06.md
docs/tasks/day-07.md
```

### 验收标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| `current.md` 更新 Week 10 状态 | 必须 | 明确当前进入 Week 10 |
| `plan.md` 有 P0/P1/P2 | 必须 | 优先级清晰 |
| `spec.md` 有 artifact 契约 | 必须 | 写清楚保存哪些文件 |
| `spec.md` 有 fallbackReason | 必须 | 写清楚 fallback 原因字段 |
| day-01 到 day-07 存在 | 必须 | 每天任务文件完整 |
| 明确禁止事项 | 必须 | 写明不接 MySQL/Figma/Redis/RabbitMQ 等 |

### Day 01 不通过情况

出现下面任意一种，就不通过：

- 没有 day-xx 任务文件；
- 文档没有写 Week 10 目标；
- 文档里混入 MySQL、Figma、拖拽编辑器等大功能；
- 没有明确验收标准。

---

## Day 02：prompt 与 JSON 清洗验收

### 验收目标

确认模型输出能被更稳定地处理。

### Worker 返回中必须包含

```json
{
  "metadata": {
    "promptVersion": "week10-v1",
    "model": "Qwen/Qwen3-VL-32B-Instruct"
  }
}
```

### 必须测试 3 种模型输出

#### 场景 1：纯 JSON

输入：

```json
{
  "version": "0.1",
  "sections": []
}
```

期望：

```text
解析成功
```

#### 场景 2：Markdown 包裹 JSON

输入：

````text
```json
{
  "version": "0.1",
  "sections": []
}
```
````

期望：

```text
能去掉 ```json 和 ```
解析成功
```

#### 场景 3：JSON 前后有废话

输入：

```text
下面是页面结构：
{
  "version": "0.1",
  "sections": []
}
以上是结果。
```

期望：

```text
能截取第一个 { 到最后一个 }
解析成功
```

### 验收标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| promptVersion 存在 | 必须 | `week10-v1` 或类似版本 |
| prompt 要求只输出 JSON | 必须 | prompt 文本中明确约束 |
| 能清理 Markdown 包裹 | 必须 | 单测通过 |
| 能清理前后废话 | 必须 | 单测通过 |
| JSON 解析失败不崩溃 | 必须 | 返回错误或 fallback |

---

## Day 03：repair 与 fallbackReason 验收

### 验收目标

确认模型输出不完美时，系统会先修复，修不好再 fallback。

### 必须支持的 fallbackReason

至少包含这些：

```text
MODEL_EMPTY_OUTPUT
MODEL_NON_JSON_OUTPUT
JSON_PARSE_FAILED
SCHEMA_VALIDATION_FAILED
REPAIR_FAILED
WORKER_TIMEOUT
MODEL_API_ERROR
IMAGE_READ_FAILED
PREVIEW_COMPILE_FAILED
UNKNOWN_ERROR
```

### 必须支持的 warnings

建议至少包含：

```text
REPAIRED_MISSING_VERSION
REPAIRED_MISSING_ID
LOW_SECTION_COUNT
EMPTY_TEXT_CONTENT
MISSING_STYLE_TOKENS
```

### 测试用例

| 场景 | 输入问题 | 期望 |
|---|---|---|
| 缺少 version | 没有 `version` 字段 | 自动补 `0.1`，`repairUsed=true` |
| 缺少 section id | section 没有 id | 自动生成 id，加入 warning |
| 非 JSON 输出 | 模型返回纯文本 | fallback，reason=`MODEL_NON_JSON_OUTPUT` |
| JSON 解析失败 | JSON 格式破损 | fallback，reason=`JSON_PARSE_FAILED` |
| schema 校验失败 | 字段结构严重不合法 | repair，失败后 fallback |
| preview 编译失败 | Layout JSON 合法但 HTML 编译失败 | reason=`PREVIEW_COMPILE_FAILED` |

### 验收标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| repairUsed 字段 | 必须 | metadata 中可见 |
| fallbackReason 字段 | 必须 | fallback 时不能为空 |
| warnings 数组 | 必须 | 可返回空数组或具体 warning |
| errors 数组 | 必须 | 可返回空数组或具体 error |
| repair 单测 | 必须 | 至少覆盖缺 version、缺 id |
| fallback 单测 | 必须 | 至少覆盖非 JSON、解析失败 |

---

## Day 04：后端 artifact 与 jobId 复用验收

### 验收目标

确认生成结果可以保存、复查，并且同一个 jobId 不重复生成。

### 期望目录结构

```text
backend/
└── data/
    └── artifacts/
        └── image-page/
            └── {jobId}/
                ├── input.png
                ├── layout.json
                ├── preview.html
                ├── metadata.json
                ├── warnings.json
                └── errors.json
```

### 验收步骤

#### 步骤 1：上传图片生成任务

期望返回：

```json
{
  "status": "SUCCESS",
  "jobId": "xxx",
  "layoutJson": {},
  "previewHtml": "...",
  "metadata": {}
}
```

#### 步骤 2：检查本地 artifact

必须存在：

```text
layout.json
preview.html
metadata.json
warnings.json
errors.json
```

如果保存原图，也应该存在：

```text
input.png
```

#### 步骤 3：重复查询同一个 jobId

连续查 2 次：

```text
GET /xxx/{jobId}
GET /xxx/{jobId}
```

期望：

- 返回内容一致；
- 不重新调用 Worker；
- 不重新调用真实 AI；
- 日志里能看出命中 artifact 或缓存。

### 验收标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| artifact 目录生成 | 必须 | `{jobId}` 目录存在 |
| layout.json 保存 | 必须 | 文件存在且 JSON 可读 |
| preview.html 保存 | 必须 | 文件存在且非空 |
| metadata.json 保存 | 必须 | 包含 model、promptVersion、durationMs 等 |
| warnings/errors 保存 | 必须 | 文件存在 |
| 同 jobId 复用 | 必须 | 查询不重新生成 |
| 后端测试 | 必须 | artifact 保存/读取测试通过 |

---

## Day 05：前端状态展示验收

### 验收目标

确认用户在页面上能看懂当前生成结果的来源、状态和问题。

### 前端必须展示的字段

```text
status
sourceType
fallbackUsed
fallbackReason
validationOk
repairUsed
promptVersion
model
durationMs
warnings
errors
```

### 页面状态要求

| 状态 | 前端表现 |
|---|---|
| IDLE | 未开始生成 |
| UPLOADING | 上传中 |
| GENERATING | 生成中 |
| SUCCESS | 真实 AI 成功 |
| FALLBACK_SUCCESS | fallback 成功 |
| FAILED | 生成失败 |
| TIMEOUT | 生成超时 |

### iframe 安全要求

必须是：

```html
<iframe sandbox=""></iframe>
```

不能出现：

```html
allow-scripts
```

### 验收标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| REAL_AI 标签 | 必须 | 页面可见 |
| FALLBACK 标签 | 必须 | fallback 时页面可见 |
| fallbackReason | 必须 | fallback 时可见 |
| warnings 展示 | 必须 | 可折叠或直接显示 |
| errors 展示 | 必须 | 可折叠或直接显示 |
| loading 状态 | 必须 | 生成时用户知道正在处理 |
| timeout 状态 | 必须 | 超时时有明确提示 |
| iframe 安全 | 必须 | sandbox=""，无 allow-scripts |
| 前端测试 | 建议必须 | 至少覆盖 3 个状态 |

---

## Day 06：测试与 smoke 验收

### 验收目标

确认 Week 10 不是“手动跑通一次”，而是可以重复验证。

### Worker 测试

必须覆盖：

```text
JSON 清洗测试
repair 测试
fallbackReason 测试
validator 测试
previewHtml 编译测试
异常图片测试
```

### 后端测试

必须覆盖：

```text
Worker 正常返回
Worker timeout
Worker failure
artifact 保存
artifact 查询
jobId 不存在
```

### 前端测试

必须覆盖：

```text
REAL_AI 状态
FALLBACK 状态
FAILED 状态
warnings/errors 展示
iframe sandbox
```

### smoke 验收

至少跑这 4 类：

| 样例 | 期望 |
|---|---|
| 简单页面图 | SUCCESS，REAL_AI，previewHtml 非空 |
| 表单页面图 | SUCCESS 或 FALLBACK_SUCCESS，fallback 有原因 |
| 稍复杂 dashboard 图 | 不崩溃，有 layoutJson 或 fallback |
| 损坏图片 | 不崩溃，有明确 error 或 fallbackReason |

### 验收标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| Worker 测试通过 | 必须 | 单测全绿 |
| 后端测试通过 | 必须 | 关键接口测试通过 |
| 前端测试通过 | 建议必须 | 状态测试通过 |
| smoke 文档存在 | 必须 | 可以照着复现 |
| 样例集存在 | 必须 | 至少 3 正常 + 1 异常 |
| smoke 结果留痕 | 必须 | 有截图、日志或文档记录 |

---

## Day 07：最终收口验收

### 验收目标

确认 Week 10 可以正式关闭，不遗留“文档说完成但代码没完成”的问题。

### 最终必须执行

1. 跑一次完整真实 AI smoke；
2. 跑一次 fallback 场景；
3. 跑一次异常图片场景；
4. 跑一次同 jobId 重复查询；
5. 检查 artifact 文件；
6. 检查前端 iframe；
7. 检查测试结果；
8. 更新 Week 10 summary。

### 必须生成的文档

```text
docs/archive/week-10-summary.md
```

建议内容：

```text
# Week 10 Summary

## 本周目标
## 本周完成内容
## P0 完成情况
## P1 完成情况
## P2 完成情况
## 最终 smoke 结果
## 已知问题
## 未完成事项
## Week 11 建议方向
```

### Day 07 通过标准

| 检查项 | 是否必须 | 通过标准 |
|---|---|---|
| P0 全部完成 | 必须 | 没有 P0 未完成 |
| smoke 通过 | 必须 | 至少主链路通过 |
| artifact 可查 | 必须 | 本地文件存在 |
| jobId 可复用 | 必须 | 不重复调用 AI |
| iframe 安全 | 必须 | sandbox="" |
| 文档归档 | 必须 | `week-10-summary.md` 存在 |
| 已知问题记录 | 必须 | 不隐藏问题 |

---

## 六、最终验收测试用例

---

## 用例 1：真实 AI 正常生成

### 输入

```text
01-simple-card-page.png
```

### 期望结果

```text
HTTP 200
status=SUCCESS
sourceType=REAL_AI
fallbackUsed=false
layoutJson.version=0.1
validationOk=true
previewHtml 非空
iframe 正常渲染
sandbox=""
无 allow-scripts
```

### 是否通过

```text
通过 / 不通过
```

---

## 用例 2：真实 AI 输出需要 repair

### 输入

人为模拟 Worker 返回缺少部分字段的 JSON，例如缺少 section id。

### 期望结果

```text
status=SUCCESS
repairUsed=true
warnings 包含 REPAIRED_MISSING_ID
fallbackUsed=false
layoutJson.version=0.1
previewHtml 非空
```

---

## 用例 3：模型返回非 JSON

### 输入

模拟模型返回：

```text
我无法识别这个页面。
```

### 期望结果

```text
fallbackUsed=true
fallbackReason=MODEL_NON_JSON_OUTPUT
errors 非空
系统不崩溃
前端显示 fallback 状态
```

---

## 用例 4：JSON 解析失败

### 输入

模拟模型返回：

```json
{
  "version": "0.1",
  "sections": [
```

### 期望结果

```text
fallbackUsed=true
fallbackReason=JSON_PARSE_FAILED
errors 非空
前端显示错误原因
```

---

## 用例 5：Worker timeout

### 输入

模拟 Worker 超过 120 秒，或者把测试 timeout 临时调短。

### 期望结果

```text
status=FAILED 或 FALLBACK_SUCCESS
fallbackReason=WORKER_TIMEOUT
前端显示 TIMEOUT 或明确失败提示
后端日志有 timeout 记录
```

---

## 用例 6：损坏图片

### 输入

```text
05-broken-image.png
```

### 期望结果

```text
status=FAILED 或 FALLBACK_SUCCESS
fallbackReason=IMAGE_READ_FAILED
errors 非空
系统不崩溃
前端不白屏
```

---

## 用例 7：artifact 保存

### 输入

任意正常图片生成成功。

### 检查目录

```text
backend/data/artifacts/image-page/{jobId}/
```

### 期望文件

```text
input.png
layout.json
preview.html
metadata.json
warnings.json
errors.json
```

### 期望结果

```text
layout.json 可打开
preview.html 非空
metadata.json 包含 promptVersion/model/durationMs
warnings.json 存在
errors.json 存在
```

---

## 用例 8：同 jobId 复用

### 步骤

1. 上传图片，得到 `jobId`；
2. 查询一次 `jobId`；
3. 再查询一次相同 `jobId`；
4. 查看后端日志。

### 期望结果

```text
两次查询结果一致
第二次查询不调用 Worker
第二次查询不调用真实 AI
日志显示命中本地 artifact 或缓存
```

---

## 用例 9：前端 fallback 展示

### 输入

触发 fallback 场景。

### 期望页面显示

```text
FALLBACK
fallbackReason
warnings
errors
previewHtml 或 fallback preview
```

### 不允许

```text
页面白屏
控制台大量报错
iframe 加 allow-scripts
```

---

## 用例 10：iframe 安全

### 检查方式

浏览器开发者工具查看 iframe。

### 期望

```html
<iframe sandbox=""></iframe>
```

### 不允许

```html
<iframe sandbox="allow-scripts"></iframe>
```

或：

```html
<iframe allow-scripts></iframe>
```

---

## 七、验收评分标准

### 7.1 通过

满足：

```text
P0 全部完成
主链路 smoke 通过
artifact 保存成功
jobId 复用成功
iframe 安全通过
fallbackReason 可见
```

结论：

```text
Week 10 通过，可以进入 Week 11。
```

---

### 7.2 有条件通过

满足：

```text
P0 基本完成
但 P1 有部分未完成
不影响主链路稳定性
已知问题已记录
```

例如：

- 前端测试少了 1 个；
- durationMs 展示不完善；
- warnings 展示样式一般；
- debug metadata 不完整。

结论：

```text
Week 10 有条件通过，可以进入 Week 11，但需要把遗留问题放入 Week 11 backlog。
```

---

### 7.3 不通过

出现任意一种：

```text
真实 AI 主链路跑不通
previewHtml 经常为空
layoutJson.version 不是 0.1
fallback 没有 fallbackReason
artifact 没保存
同 jobId 查询会重复调用 AI
iframe 出现 allow-scripts
OPENAI_API_KEY 被写入代码或文档
```

结论：

```text
Week 10 不通过，不能进入 MySQL/Figma/拖拽编辑器等新阶段。
```

---

## 八、缺陷等级定义

### 8.1 S1 严重缺陷

这些必须当天修。

```text
真实 AI 主链路不可用
后端启动失败
Worker 无法调用
API Key 泄露
iframe 出现 allow-scripts
artifact 完全不保存
```

### 8.2 S2 主要缺陷

这些必须 Week 10 内修。

```text
fallbackReason 缺失
warnings/errors 不返回
jobId 复用失败
timeout 无明确提示
previewHtml 偶发为空
前端 fallback 状态不显示
```

### 8.3 S3 普通缺陷

这些可以进入遗留问题。

```text
前端样式不够好看
durationMs 没展示
debug 信息不够完整
warnings 文案不够友好
样例集数量偏少
```

---

## 九、最终验收报告模板

建议让 Codex 最后生成这个文件：

```text
docs/archive/week-10-acceptance-report.md
```

内容模板如下：

```markdown
# Week 10 验收报告

## 1. 验收结论

- 验收结果：通过 / 有条件通过 / 不通过
- 验收日期：
- 验收分支：
- 验收提交：

## 2. 验收环境

- Java：
- Spring Boot：
- Python：
- Node：
- OPENAI_BASE_URL：
- OPENAI_MODEL：
- Worker Python Path：
- Worker Timeout：

## 3. P0 验收结果

| 编号 | 验收项 | 结果 | 备注 |
|---|---|---|---|
| P0-1 | 真实 AI 链路可运行 | 通过/不通过 | |
| P0-2 | Layout JSON 合法 | 通过/不通过 | |
| P0-3 | previewHtml 非空 | 通过/不通过 | |
| P0-4 | iframe 可预览 | 通过/不通过 | |
| P0-5 | iframe 安全 | 通过/不通过 | |
| P0-6 | prompt 有版本 | 通过/不通过 | |
| P0-7 | fallback 有原因 | 通过/不通过 | |
| P0-8 | warnings/errors 可返回 | 通过/不通过 | |
| P0-9 | artifact 可保存 | 通过/不通过 | |
| P0-10 | jobId 可复用 | 通过/不通过 | |
| P0-11 | timeout 可控 | 通过/不通过 | |
| P0-12 | smoke 文档存在 | 通过/不通过 | |

## 4. Smoke 测试结果

| 样例 | 结果 | sourceType | fallbackUsed | fallbackReason | previewHtml | 备注 |
|---|---|---|---|---|---|---|
| 01-simple-card-page.png | | | | | | |
| 02-landing-hero.png | | | | | | |
| 03-form-page.png | | | | | | |
| 04-dashboard-lite.png | | | | | | |
| 05-broken-image.png | | | | | | |

## 5. 测试结果

- Worker 测试：通过 / 不通过
- 后端测试：通过 / 不通过
- 前端测试：通过 / 不通过
- 真实链路 smoke：通过 / 不通过

## 6. Artifact 检查

- layout.json：存在 / 不存在
- preview.html：存在 / 不存在
- metadata.json：存在 / 不存在
- warnings.json：存在 / 不存在
- errors.json：存在 / 不存在

## 7. 安全检查

- iframe sandbox=""：通过 / 不通过
- 无 allow-scripts：通过 / 不通过
- API Key 未写入代码：通过 / 不通过
- API Key 未写入文档：通过 / 不通过
- API Key 未进入日志：通过 / 不通过

## 8. 已知问题

1.
2.
3.

## 9. 遗留事项

1.
2.
3.

## 10. Week 11 建议

建议方向：

- 继续真实 AI 输出质量提升；
- 或开启本地持久化 / MySQL 周。
```

---

## 十、给 Codex 的验收提示词

你可以直接复制下面这段给 Codex。

```text
请基于当前项目执行 Week 10 验收，不要开发新功能。

项目背景：
screenshot-to-responsive-page-generator 已在 Week 09 跑通真实 AI 最小闭环。
Week 10 的目标是稳定性、质量、可复现性。

验收范围：
1. Worker promptVersion、JSON 清洗、repair、fallbackReason、warnings/errors。
2. 后端 artifact 保存、jobId 复用、timeout、worker failure。
3. 前端 REAL_AI/FALLBACK/FAILED/TIMEOUT 状态展示、warnings/errors 展示、iframe sandbox。
4. Worker/后端/前端测试。
5. 真实 AI smoke 文档和验收报告。

必须检查：
- HTTP 200
- status=SUCCESS 或 FALLBACK_SUCCESS
- sourceType=REAL_AI 或 FALLBACK
- layoutJson.version=0.1
- validationOk=true 或 fallbackReason 明确
- previewHtml 非空
- iframe sandbox=""
- 无 allow-scripts
- artifact 文件存在
- 同 jobId 查询不重复调用 AI
- OPENAI_API_KEY 不得写入代码、文档、日志和提交

禁止：
- 不接 MySQL
- 不接 Figma API/MCP
- 不接 Redis/RabbitMQ
- 不做拖拽编辑器
- 不做多页面
- 不做 ZIP 导出
- 不做登录权限
- 不做高保真截图还原

请输出：
1. 验收执行结果
2. P0/P1/P2 完成情况
3. 测试结果
4. smoke 结果
5. artifact 检查结果
6. iframe 安全检查结果
7. 已知问题
8. 是否建议进入 Week 11
9. 生成 docs/archive/week-10-acceptance-report.md
```

---

## 十一、最终一句话标准

Week 10 验收的核心标准就是：

> 同一条真实 AI 链路，不仅能跑通，还要能解释失败、保存结果、重复查询、前端可读、测试可复现。

只要这句话做到了，Week 10 就算真正过关。
