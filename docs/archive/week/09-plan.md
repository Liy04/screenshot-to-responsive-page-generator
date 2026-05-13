# screenshot-to-responsive-page-generator  
# Week 09 正式开发计划：真实 AI 最小接入

本文件是 Week 09 的原始长计划，日常执行不默认读取；正式执行以 `AGENTS.md`、`docs/current.md`、`docs/plan.md`、`docs/tasks/day-xx.md` 和 `docs/spec.md` 为准。

你现在负责 `screenshot-to-responsive-page-generator` 项目的 Week 09 开发与验收。

Week 08 已经完成 mock 链路，包括：

- 前端本地图片选择与预览；
- 后端 mock API；
- Worker 本地 mock resolver；
- generated-page mock 展示；
- iframe sandbox 安全预览；
- 测试、smoke、summary、report material 已收口。

从 Week 09 开始，项目不再继续围绕 mock 优化，而是正式进入真实主链路。

---

## 一、Week 09 正式定位

Week 09 的正式定位是：

> **真实 AI 最小接入，打通单张图片到 Layout JSON / generated-page 预览的最小闭环。**

本周只追求一件事：

```text
单张真实图片
-> 后端保存临时文件
-> 后端创建本地 jobId
-> 后端调用 Python Worker
-> Worker 读取真实图片
-> Worker 调用真实多模态模型
-> 模型输出 Layout JSON 草稿
-> Worker 校验 Layout JSON
-> 校验失败则轻量修正 / fallback
-> Worker 编译 generated-page HTML
-> 后端返回 layoutJson + previewHtml
-> 前端展示 Layout JSON + iframe 预览
```

Week 09 不追求生成质量最优。

本周重点是：

```text
真实链路打通
结构数据可校验
失败情况可兜底
页面结果可预览
```

不是重点：

```text
高保真还原
复杂 prompt 调优
复杂响应式
直接生成 Vue
批量上传
多页面生成
在线编辑器
ZIP 导出
```

---

## 二、Week 09 总路线

Week 09 采用以下方案：

```text
主线：方案 B，真实 AI 最小接入
兜底：方案 A，规则 resolver 保底
```

也就是说：

```text
优先走真实 AI：
真实图片 -> 多模态模型 -> Layout JSON -> 校验 -> generated-page

如果 AI 失败：
真实图片 -> fallback rule resolver -> Layout JSON -> 校验 -> generated-page
```

AI 不是直接生成最终页面。

正确职责划分是：

```text
AI 负责：
根据截图生成 Layout JSON 草稿

Worker 负责：
解析模型输出
校验 Layout JSON
修正轻微问题
失败时 fallback
把 Layout JSON 编译成 generated-page HTML

前端负责：
展示原图
展示 Layout JSON
使用 iframe 预览 generated-page
```

---

## 三、Week 09 硬边界

### 1. 输入边界

Week 09 只支持：

```text
单张图片输入
```

不支持：

```text
批量上传
多文件输入
多页面任务
文件夹上传
ZIP 上传
```

---

### 2. 输出边界

Week 09 只输出：

```text
layout.json
generated.html
previewHtml
```

不输出：

```text
Vue SFC
完整 Vue 项目
CSS 文件
JS 文件
ZIP 包
组件源码
多份代码产物
```

本周只打通：

```text
图片 -> Layout JSON -> generated-page 预览
```

不扩展成：

```text
图片 -> Vue 项目
图片 -> 可编辑页面
图片 -> ZIP 导出
```

---

### 3. 模型输出边界

模型原始输出不能直接给前端使用，也不能直接进入 validator / compiler。

必须经过：

```text
模型原始输出
-> JSON 解析
-> 简化中间结构映射
-> Layout JSON 校验
-> 安全校验
-> 轻量修正
-> 修正失败则 fallback
-> generated-page 编译
-> 前端 iframe 预览
```

前端永远不能直接接收：

```text
模型原始字符串
模型直接生成的 HTML
模型直接生成的 JavaScript
模型直接生成的 Vue
未经校验的 Layout JSON
```

---

### 4. 质量边界

Week 09 不追求：

```text
页面高度还原截图
文字完全识别正确
颜色完全一致
间距完全一致
复杂布局识别
复杂响应式
像素级还原
```

Week 09 只追求：

```text
真实图片能上传
后端能保存
后端能调用 Python Worker
Worker 能读取真实图片
Worker 能调用真实 AI
Worker 能生成 Layout JSON
Layout JSON 能通过校验
失败能 fallback
Layout JSON 能编译成 HTML
前端 iframe 能预览
```

---

## 四、Week 09 明确禁止事项

本周禁止实现以下内容：

```text
不接 Figma API / MCP
不接 MySQL
不创建数据库表
不创建 Entity / Mapper
不接 Redis / RabbitMQ
不做 Playwright 视觉回归
不做多页面
不做批量任务
不做登录注册
不做复杂权限系统
不做拖拽编辑器
不做在线编辑器
不做 ZIP 导出
不直接生成 Vue 页面
不做高保真复杂页面还原
不做大量 prompt 微调
不做 JMeter 压测
不做 OSS / MinIO
不做历史任务列表
不做异步任务队列
```

判断一个任务是否允许，只看一个标准：

> 这个任务是否直接推进“单张图片 -> Layout JSON -> generated-page 预览”？

如果不是，Week 09 不做。

---

## 五、修正后的开发顺序

Week 09 的正确顺序是：

```text
Day 1：锁定范围和协议
Day 2：单张图片上传 + 临时保存
Day 3：后端真实调用 Python Worker
Day 4：Worker 读取图片 + fallback + validator + 真实 AI
Day 5：Layout JSON -> generated-page HTML compiler
Day 6：前端接入真实链路
Day 7：全链路 smoke 验收与阻断问题修复
```

特别注意：

```text
Day 3 不强制要求 previewHtml 完整可用。
Day 3 的重点是 Java 后端能真实调用 Python Worker。

Day 4 不要先死磕 AI。
Day 4 必须先保证 fallback 和 validator 稳定，再接真实 AI。

Day 5 才正式要求 generated.html 可用。
```

---

## 六、Week 09 核心交付物

Week 09 结束时必须交付：

```text
1. 单张图片上传接口
2. sourceUrl 原图访问接口
3. 后端本地 jobId
4. 后端临时文件保存
5. 后端调用 Python Worker 能力
6. Worker 图片读取能力
7. Worker fallback rule resolver
8. Worker Layout JSON validator
9. Worker 真实 AI 最小接入
10. Layout JSON 输出
11. generated-page HTML compiler
12. generated.html 输出
13. 后端 generate 接口返回 layoutJson + previewHtml
14. 前端展示原图
15. 前端展示 Layout JSON
16. 前端 iframe 预览 generated-page
17. Week 09 smoke report
```

---

## 七、Week 09 数据与文件结构建议

本周不接数据库，只用本地临时目录。

建议目录结构：

```text
storage/
  temp/
    job_20260510_223015_a8f3/
      input.png
      layout.json
      generated.html
      worker-result.json
```

其中：

```text
input.png：用户上传的单张原始图片
layout.json：Worker 生成并校验后的 Layout JSON
generated.html：由 Layout JSON 编译出的静态 HTML
worker-result.json：Worker 执行结果摘要
```

注意：

```text
后端内部可以使用 imagePath
但不要把后端本地 imagePath 返回给前端
```

前端只需要：

```text
jobId
fileName
sourceUrl
layoutJson
previewHtml
aiUsed
mode
warnings
```

---

## 八、接口设计建议

### 1. 单张图片上传接口

```http
POST /api/image-page/upload
Content-Type: multipart/form-data
```

请求字段：

```text
file: 单张图片
```

只允许一个文件。

允许类型：

```text
png
jpg
jpeg
webp
```

不允许：

```text
svg
gif
pdf
zip
html
js
vue
exe
```

文件大小：

```text
最大 5MB
```

成功返回：

```json
{
  "code": 200,
  "message": "upload success",
  "data": {
    "jobId": "job_20260510_223015_a8f3",
    "fileName": "input.png",
    "sourceUrl": "/api/image-page/jobs/job_20260510_223015_a8f3/source"
  }
}
```

不要返回：

```json
{
  "imagePath": "storage/temp/job_xxx/input.png"
}
```

本地路径属于后端内部实现，不能暴露给前端。

Week 09 的新真实链路接口是新增实现；Week 08 的 `/api/dev/image-page-jobs*` 先保留，用于回退和对照。不要在 Week 09 计划里默认要求 Day 2 / Day 6 直接删除旧 dev mock 接口。

---

### 2. 原图访问接口

```http
GET /api/image-page/jobs/{jobId}/source
```

用于前端展示上传后的原图。

安全要求：

```text
jobId 必须校验格式
必须防路径穿越
不能允许 ../../ 之类路径
```

建议 jobId 格式：

```text
^job_\d{8}_\d{6}_[a-z0-9]{4,8}$
```

示例：

```text
job_20260510_223015_a8f3
```

---

### 3. 生成接口

```http
POST /api/image-page/jobs/{jobId}/generate
Content-Type: application/json
```

请求：

```json
{
  "mode": "real-ai",
  "fallback": true
}
```

成功返回：

```json
{
  "code": 200,
  "message": "generation success",
  "data": {
    "jobId": "job_20260510_223015_a8f3",
    "status": "SUCCESS",
    "mode": "real-ai",
    "aiUsed": true,
    "layoutJson": {},
    "previewHtml": "<!doctype html>...",
    "warnings": []
  }
}
```

如果 AI 失败但 fallback 成功：

```json
{
  "code": 200,
  "message": "generation success with fallback",
  "data": {
    "jobId": "job_20260510_223015_a8f3",
    "status": "SUCCESS",
    "mode": "fallback-rule",
    "aiUsed": false,
    "layoutJson": {},
    "previewHtml": "<!doctype html>...",
    "warnings": [
      "AI call failed, fallback rule resolver used."
    ]
  }
}
```

如果完全失败：

```json
{
  "code": 500,
  "message": "generation failed",
  "data": {
    "jobId": "job_20260510_223015_a8f3",
    "status": "FAILED",
    "error": "worker execution failed"
  }
}
```

---

## 九、Layout JSON 最小契约（仍沿用 v0.1）

Week 09 默认继续沿用项目当前 Layout JSON v0.1 主结构，不新增新的顶层 Schema。

AI 可以先输出较简化的中间结构，但 Worker 在进入 validator / compiler 前必须把它转换成当前项目的 Layout JSON v0.1 契约。

当前 v0.1 必需顶层字段仍是：

```text
version
page
source
tokens
layout
assets
responsive
assumptions
warnings
```

AI 的简化中间结构只用于 Worker 内部，不是对外契约，也不能直接喂给 validator。

fallback layout 也必须先落到当前 v0.1 结构，再进入 validator / compiler。示例：

```json
{
  "version": "0.1",
  "page": {
    "title": "Fallback Generated Page"
  },
  "source": {
    "sourceType": "fallback-rule",
    "imageName": "input.png",
    "templateKey": "landing-basic"
  },
  "tokens": {},
  "layout": {
    "type": "page",
    "children": [
      {
        "type": "section",
        "children": [
          {
            "type": "text",
            "role": "heading",
            "text": "Generated Preview"
          }
        ]
      }
    ]
  },
  "assets": [],
  "responsive": {},
  "assumptions": [],
  "warnings": [
    "AI output invalid or AI call failed, fallback rule resolver used."
  ]
}
```

---

## 十、Validator 校验规则

validator 只校验已经转换好的 Layout JSON v0.1，不直接校验 AI 原始输出。

最低校验要求：

```text
1. 必须能解析为 JSON
2. 必须包含当前 v0.1 必需顶层字段：version / page / source / tokens / layout / assets / responsive / assumptions / warnings
3. layout 必须是根节点字段，不能改成 root
4. 每个节点 type 必须在当前 spec 白名单中
5. style 必须是对象
6. text 必须是字符串
7. 不允许 rawHtml
8. 不允许 script
9. 不允许 onclick / onload / onerror 等事件字段
10. 不允许 iframe / object / embed
11. 不允许外部 JS
```

---

## 十一、轻量修正规则

如果模型输出存在轻微问题，可以轻量修正。

允许修正：

```text
缺 page.title -> 补 "Generated Page"
缺 page.viewport -> 使用图片真实宽高补充
缺 page.background -> 补 "#ffffff"
缺 section.children -> 补 []
缺 section.style -> 补 {}
style 不是对象 -> 改成 {}
未知 type -> 改成 text 或 section
缺 id -> 自动生成 id
缺 layout -> 补 column
```

不允许复杂修正：

```text
不做二次 AI 修复
不做多轮 prompt
不做复杂结构重排
不做高保真优化
```

如果轻量修正后仍不合法：

```text
直接 fallback
```

---

## 十二、安全规则

### 1. 文本安全

所有 `text` 内容在编译 HTML 前必须做 HTML escape。

例如模型输出：

```html
<script>alert(1)</script>
```

最终只能作为普通文本显示，不能执行。

---

### 2. style 白名单

Week 09 只允许以下 style 字段：

```text
background
color
fontSize
fontWeight
padding
margin
borderRadius
border
display
gap
textAlign
width
maxWidth
minHeight
```

其他 style 字段全部丢弃。

禁止：

```text
position: fixed
z-index 超大值
url(javascript:...)
expression(...)
behavior
filter 可疑内容
```

---

### 3. image 安全

Week 09 不信任模型输出的 image src。

建议 image 节点先编译成：

```html
<div class="image-placeholder">Image</div>
```

不要让模型生成：

```text
file://
javascript:
data:
外部 http 图片
base64 大图片
```

---

### 4. HTML 安全

generated.html 中禁止出现：

```text
<script>
onclick
onload
onerror
iframe
object
embed
外部 JS
外部 CSS
```

---

### 5. iframe 安全

前端 iframe 建议使用：

```html
<iframe sandbox :srcdoc="previewHtml"></iframe>
```

不要添加：

```text
allow-scripts
allow-same-origin
allow-forms
allow-popups
```

Week 09 只是静态预览，不需要这些权限。

---

## 十三、Day 1 开发计划

### 线程

文档线程

### 目标

锁定 Week 09 范围、链路、协议和禁止事项，避免 Codex 发散。

### 必须完成

新增或更新：

```text
docs/current.md
docs/plan.md
docs/spec.md
docs/INDEX.md
docs/tasks/day-01.md
docs/tasks/day-02.md
docs/tasks/day-03.md
docs/tasks/day-04.md
docs/tasks/day-05.md
docs/tasks/day-06.md
docs/tasks/day-07.md
```

文档必须写清：

```text
Week 09 正式定位
主链路
只支持单张图片
只输出 Layout JSON + generated-page HTML
模型输出必须经过 validator
失败必须 fallback
不追求生成质量
禁止事项
Worker 输入输出协议
Layout JSON Schema
validator 规则
安全规则
```

`docs/week09-plan.md` 只作为原始长计划来源，后续应归档，不作为日常默认上下文。

### 禁止事项

```text
不写长篇 PRD
不设计数据库
不设计登录注册
不扩展 Figma
不设计批量任务
不设计在线编辑器
不写未来大而全架构
```

### 验收标准

Day 1 结束后，文档能清楚回答：

```text
Week 09 做什么？
Week 09 不做什么？
主链路是什么？
模型输出为什么不能直接给前端？
失败时怎么 fallback？
最终交付物是什么？
```

---

## 十四、Day 2 开发计划

### 线程

后端开发线程

### 目标

实现单张真实图片上传和 sourceUrl 原图访问。

### 必须完成

实现：

```http
POST /api/image-page/upload
GET /api/image-page/jobs/{jobId}/source
```

上传接口必须做到：

```text
只支持单张图片
限制大小 5MB
限制类型 png / jpg / jpeg / webp
校验文件后缀
校验 Content-Type
最好实际读取图片确认合法
生成本地 jobId
保存到 storage/temp/{jobId}/input.xxx
返回 jobId、fileName、sourceUrl
不返回本地 imagePath
```

source 接口必须做到：

```text
校验 jobId 格式
防路径穿越
读取对应 job 目录下的 input 图片
返回图片内容
图片不存在时返回 404
```

### 禁止事项

```text
不接 MySQL
不创建上传记录表
不创建 Entity
不创建 Mapper
不做 OSS / MinIO
不做永久存储
不做批量上传
不做任务列表
不做登录校验
```

### 验收标准

至少完成以下测试：

```text
1 张 PNG 上传成功
1 张 JPG 上传成功
1 个非图片文件被拒绝
1 次多文件上传被拒绝
1 个超过 5MB 文件被拒绝
sourceUrl 可以在浏览器访问原图
本地 storage/temp/{jobId}/input.xxx 存在
接口没有返回本地 imagePath
```

---

## 十五、Day 3 开发计划

### 线程

后端开发线程

### 目标

打通：

```text
Spring Boot 后端 -> Python Worker -> worker-result.json -> Spring Boot 后端
```

Day 3 的重点是后端真实调用 Python Worker。

Day 3 不强制要求：

```text
真实 AI 成功
layout.json 完整可用
generated.html 完整可用
previewHtml 完整返回
```

### 必须完成

实现：

```http
POST /api/image-page/jobs/{jobId}/generate
```

后端调用 Worker 示例：

```bash
python worker/main.py \
  --job-id job_20260510_223015_a8f3 \
  --image-path storage/temp/job_20260510_223015_a8f3/input.png \
  --mode real-ai \
  --fallback true
```

Day 3 Worker 可以先返回 stub：

```json
{
  "jobId": "job_20260510_223015_a8f3",
  "status": "SUCCESS",
  "mode": "worker-stub",
  "aiUsed": false,
  "layoutJsonPath": null,
  "htmlPath": null,
  "warnings": []
}
```

后端必须做到：

```text
校验 jobId
校验 input 图片存在
通过 ProcessBuilder 或等价方式启动 Python Worker
读取 stdout
读取 stderr
处理 exitCode
设置 60 秒超时
读取 worker-result.json
把 Worker 执行结果返回
错误时返回明确错误信息
```

### 禁止事项

```text
不接 RabbitMQ
不接 Redis
不做异步队列
不做任务状态表
不做任务列表页
不做重试队列
不做并发调度
不做性能优化
不做分布式 Worker
```

### 验收标准

Day 3 结束时必须能证明：

```text
上传图片后调用 generate
后端真实启动 Python Worker
Worker 生成 worker-result.json
后端读取 worker-result.json
后端返回 Worker 结果
控制台能看到 Worker 启动日志
Worker 失败时后端能返回错误摘要
```

---

## 十六、Day 4 开发计划

### 线程

Worker 开发线程

### 目标

Worker 能根据真实图片生成经过校验的 layout.json。

Day 4 的正确开发顺序：

```text
1. Worker 读取真实图片
2. fallback resolver 稳定生成 Layout JSON v0.1
3. validator 稳定校验 Layout JSON v0.1
4. 接入真实多模态模型
5. AI 简化输出先映射为 Layout JSON v0.1
6. AI 失败或校验失败时 fallback
```

不要先死磕 AI。

fallback 和 validator 是 Week 09 的安全垫，必须先稳定。

### 必须完成

Worker 支持参数：

```bash
python worker/main.py \
  --job-id job_xxx \
  --image-path storage/temp/job_xxx/input.png \
  --mode real-ai \
  --fallback true
```

Worker 必须读取：

```text
图片宽度
图片高度
图片格式
文件大小
```

Worker 必须实现：

```text
fallback rule resolver
Layout JSON validator
轻量修正逻辑
真实 AI 调用
AI 失败 fallback
校验失败 fallback
layout.json 输出
worker-result.json 输出
```

AI 配置必须通过环境变量：

```env
AI_PROVIDER=openai
AI_API_KEY=your_api_key
AI_MODEL=your_model_name
AI_TIMEOUT=45
```

不要把 API key 写死到代码里。

### AI Prompt 要求

AI 只允许输出简化中间结构 JSON，不要直接输出最终 Layout JSON v0.1、HTML、Vue 或 JavaScript。

核心要求：

```text
你是页面结构分析器。
请根据输入截图生成一个简化 Layout JSON，用于后续编译为静态 HTML 预览。

要求：
1. 只输出 JSON，不要输出解释文字。
2. 不要输出 Markdown。
3. 不要输出 HTML。
4. 不要输出 Vue。
5. 不要输出 JavaScript。
6. 页面只需要识别主要区域，不追求高保真。
7. 如果无法识别真实文字，可以使用语义相近的中文占位文案。
8. 只输出简化的区域 / 文本 / 图片语义结构，不要假设它已经是最终 Layout JSON v0.1。
9. 不要直接输出 `root` 或新的顶层 schema。
10. Worker 会在进入 validator / compiler 前把中间结构映射成当前 Layout JSON v0.1。
```

### fallback layout 示例

```json
{
  "version": "0.1",
  "page": {
    "title": "Fallback Generated Page"
  },
  "source": {
    "sourceType": "fallback-rule",
    "imageName": "input.png",
    "templateKey": "landing-basic"
  },
  "tokens": {},
  "layout": {
    "type": "page",
    "children": [
      {
        "type": "section",
        "children": [
          {
            "type": "text",
            "role": "heading",
            "text": "Generated Preview"
          }
        ]
      }
    ]
  },
  "assets": [],
  "responsive": {},
  "assumptions": [],
  "warnings": [
    "AI output invalid or AI call failed, fallback rule resolver used."
  ]
}
```

### 输出要求

AI 成功：

```json
{
  "jobId": "job_xxx",
  "status": "SUCCESS",
  "mode": "real-ai",
  "aiUsed": true,
  "layoutJsonPath": "storage/temp/job_xxx/layout.json",
  "htmlPath": null,
  "warnings": []
}
```

fallback 成功：

```json
{
  "jobId": "job_xxx",
  "status": "SUCCESS",
  "mode": "fallback-rule",
  "aiUsed": false,
  "layoutJsonPath": "storage/temp/job_xxx/layout.json",
  "htmlPath": null,
  "warnings": [
    "AI output invalid or AI call failed, fallback rule resolver used."
  ]
}
```

### 禁止事项

```text
不让 AI 直接输出 HTML
不让 AI 直接输出 Vue
不让 AI 输出多个文件
不做多轮 prompt 微调
不做复杂 OCR
不做图像分割算法
不做高保真还原
不做多模型对比
不把模型原始输出给前端
不把 API key 写进代码
```

### 验收标准

命令行执行 Worker 后：

```bash
python worker/main.py --job-id job_demo --image-path storage/temp/job_demo/input.png --mode real-ai --fallback true
```

必须生成：

```text
layout.json
worker-result.json
```

并且满足：

```text
layout.json 能被 JSON 解析
layout.json 通过 validator
worker-result.json 记录 aiUsed=true 或 false
AI 失败时 fallback 能生成 layout.json
模型原始输出没有直接保存为前端结果
```

---

## 十七、Day 5 开发计划

### 线程

Worker 开发线程（HTML compiler 子任务）

### 目标

把 layout.json 编译为 generated.html。

Day 5 才正式要求 generated-page HTML 可用。

### 必须完成

新增 HTML compiler，例如：

```text
worker/compiler/html_compiler.py
```

输入：

```text
layout.json
```

这里的 `layout.json` 指已经转换成当前 Layout JSON v0.1 契约的结果，不是 AI 原始输出；compiler 不负责协议升级。

输出：

```text
generated.html
```

支持节点：

```text
section -> <section>
text -> <h1> / <p> / <span>
button -> <button>
image -> <div class="image-placeholder">
card -> <div class="card">
grid -> <div class="grid">
footer -> <footer>
```

必须生成完整 HTML：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Generated Page</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      background: #ffffff;
      color: #111111;
    }

    .generated-page {
      width: 100%;
      min-height: 100vh;
    }

    .section {
      width: 100%;
      padding: 64px 24px;
    }

    .section-inner {
      max-width: 1120px;
      margin: 0 auto;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 24px;
    }

    .card {
      border: 1px solid #eeeeee;
      border-radius: 16px;
      padding: 24px;
      background: #ffffff;
    }

    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 20px;
      border-radius: 8px;
      border: none;
      cursor: default;
    }

    .image-placeholder {
      width: 100%;
      min-height: 180px;
      border-radius: 16px;
      background: #eeeeee;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #777777;
    }

    @media (max-width: 768px) {
      .section {
        padding: 40px 16px;
      }

      .grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <main class="generated-page">
    <!-- generated content -->
  </main>
</body>
</html>
```

编译前必须再次校验 Layout JSON。

### 安全要求

generated.html 中禁止出现：

```text
<script>
onclick
onload
onerror
iframe
object
embed
外部 JS
外部 CSS
raw HTML
```

所有文本必须 HTML escape。

style 只能使用白名单字段。

### 输出文件

```text
storage/temp/{jobId}/layout.json
storage/temp/{jobId}/generated.html
storage/temp/{jobId}/worker-result.json
```

worker-result.json 更新为：

```json
{
  "jobId": "job_xxx",
  "status": "SUCCESS",
  "mode": "real-ai",
  "aiUsed": true,
  "layoutJsonPath": "storage/temp/job_xxx/layout.json",
  "htmlPath": "storage/temp/job_xxx/generated.html",
  "warnings": []
}
```

### 禁止事项

```text
不生成 Vue
不生成多个代码文件
不生成 CSS 文件
不生成 JS
不做 ZIP
不做代码下载
不做组件库
不做 Tailwind 输出
不做复杂响应式
不做高保真调参
```

### 验收标准

Worker 执行后必须生成：

```text
layout.json
generated.html
worker-result.json
```

浏览器直接打开 generated.html，必须满足：

```text
页面不是空白
页面没有脚本
页面结构来自 layout.json
移动端宽度下不完全炸裂
fallback 也能编译成 HTML
```

Day 5 结束后，后端 generate 接口可以正式返回：

```json
{
  "layoutJson": {},
  "previewHtml": "<!doctype html>..."
}
```

---

## 十八、Day 6 开发计划

### 线程

前端开发线程

### 目标

前端接入真实主链路，用户能在浏览器里完整操作：

```text
选择图片 -> 上传 -> 生成 -> 查看 Layout JSON -> iframe 预览
```

### 必须完成

前端页面必须支持：

```text
单张图片选择
本地图片预览
上传图片到后端
展示 sourceUrl 原图
保存 jobId
点击开始生成
显示生成中状态
接收 layoutJson
接收 previewHtml
展示 Layout JSON
iframe 展示 previewHtml
展示 aiUsed
展示 mode
展示 warnings
展示错误信息
```

状态至少包括：

```text
未选择图片
已选择图片
上传中
上传成功
生成中
生成成功
生成失败
```

iframe 使用：

```html
<iframe sandbox :srcdoc="previewHtml"></iframe>
```

不要加：

```text
allow-scripts
allow-same-origin
allow-forms
allow-popups
```

### 前端多图限制

前端必须限制：

```text
只允许选择 1 张图片
```

如果用户选择多张，提示：

```text
Week 09 暂只支持单张图片输入
```

### 禁止事项

```text
不做拖拽编辑器
不做在线编辑
不做代码编辑器
不做导出按钮
不做历史记录
不做多页面 tab
不做批量任务 UI
不做登录注册
不做复杂 UI 美化
不继续围绕 templateKey mock 展示开发
```

### 验收标准

浏览器里能完整跑通：

```text
选择一张真实图片
-> 本地预览
-> 上传到后端
-> 后端返回 jobId 和 sourceUrl
-> 前端展示原图
-> 点击开始生成
-> 后端调用 Worker
-> Worker 调用 AI 或 fallback
-> Worker 输出 layout.json 和 generated.html
-> 后端返回 layoutJson 和 previewHtml
-> 前端展示 Layout JSON
-> iframe 展示 generated-page
-> 前端展示 aiUsed / mode / warnings
```

---

## 十九、Day 7 验收计划

### 线程

测试线程

### 目标

用 3 张真实截图进行全链路 smoke 验收，并给出通过 / 不通过 结论；如发现阻断问题，由项目经理额外拆给对应开发线程处理。

### 测试图片

准备：

```text
test-assets/week09/case-01-landing.png
test-assets/week09/case-02-cards.png
test-assets/week09/case-03-form.png
```

建议类型：

```text
case-01：简单 landing page
case-02：卡片列表页面
case-03：登录 / 表单页面
```

不要使用过于复杂的后台系统截图作为 Week 09 主验收图。

### 每张图必须记录

```text
上传是否成功
sourceUrl 是否可访问
Worker 是否启动
AI 是否调用成功
是否 fallback
layout.json 是否生成
validator 是否通过
generated.html 是否生成
iframe 是否可预览
是否存在阻断 bug
```

### smoke report

新增或更新：

```text
docs/archive/week/09-smoke-report.md
```

记录格式：

```markdown
# Week 09 Smoke Report

## Case 1：case-01-landing.png

- 上传是否成功：
- jobId：
- sourceUrl 是否可访问：
- Worker 是否启动：
- AI 是否调用成功：
- 是否 fallback：
- layout.json 是否生成：
- validator 是否通过：
- generated.html 是否生成：
- iframe 是否可预览：
- 主要问题：
- 结论：

## Case 2：case-02-cards.png

...

## Case 3：case-03-form.png

...
```

### 阻断级问题

测试线程发现以下问题时，只负责记录并上报；如果需要修复，由项目经理额外拆给对应开发线程处理：

```text
图片上传失败
sourceUrl 无法访问
后端无法调用 Worker
Worker 找不到图片
AI 失败后 fallback 也失败
layout.json 不生成
validator 不工作
generated.html 不生成
iframe 空白
前端无法展示错误
模型原始输出直接进入前端
generated.html 出现 script
jobId 存在路径穿越风险
```

### 暂时只记录、不展开修复的问题

以下问题 Week 09 可以先记录，不作为失败：

```text
页面不够像截图
颜色不准
文字不准
间距不好看
布局层级不够精细
响应式一般
生成页面不够美观
```

### 禁止事项

```text
不做视觉回归
不做 JMeter 压测
不做复杂自动化
不做 UI 美化
不为了提高还原度反复调 prompt
不加入数据库
不加入队列
不加入导出功能
```

### 验收标准

Day 7 结束时必须给出明确结论：

```text
Week 09 是否已经打通：
单张真实图片 -> 真实 AI / fallback -> Layout JSON -> generated-page -> iframe 预览
```

最低通过标准：

```text
3 张真实截图中，至少 2 张完整跑通：
上传 -> Worker -> AI/fallback -> layout.json -> generated.html -> iframe 预览

AI 失败时 fallback 能稳定生成 layout.json 和 generated.html。
模型原始输出没有直接进入前端。
```

AI 最小通过标准：

```text
至少 1 张真实截图真实调用 AI 成功；
AI 输出通过 validator；
最终生成 layout.json 和 generated.html。
```

安全通过标准：

```text
generated.html 不包含 script
iframe 没有 allow-scripts
前端不接收本地 imagePath
jobId 防路径穿越
模型原始输出不直接给前端
所有文本已 HTML escape
```

---

## 二十、Week 09 最终完成定义

Week 09 完成必须同时满足：

```text
1. 单张真实图片可以上传
2. 后端可以保存临时文件
3. 后端可以创建本地 jobId
4. sourceUrl 可以访问原图
5. 后端可以真实调用 Python Worker
6. Worker 可以读取真实图片
7. Worker 可以生成 fallback layout.json
8. Worker validator 可以校验 Layout JSON
9. Worker 可以调用真实多模态模型
10. AI 成功时可以生成 Layout JSON
11. AI 失败时可以 fallback
12. Layout JSON 可以编译成 generated.html
13. 后端 generate 接口可以返回 layoutJson + previewHtml
14. 前端可以展示原图
15. 前端可以展示 Layout JSON
16. 前端可以 iframe 预览 generated-page
17. 3 张测试图至少 2 张完整跑通
18. 至少 1 张测试图真实 AI 调用成功
19. generated.html 不包含脚本
20. 模型原始输出没有直接给前端
21. docs/week09-smoke-report.md 已完成
```

---

## 二十一、Codex 验收重点

请 Codex 严格检查以下问题：

```text
1. 是否还在继续做 mock 优化？
2. 是否支持了批量上传？如果支持了，说明跑偏。
3. 是否创建了数据库表？如果创建了，说明跑偏。
4. 是否创建了 Entity / Mapper？如果创建了，说明跑偏。
5. 是否接了 Redis / RabbitMQ？如果接了，说明跑偏。
6. 是否直接生成 Vue？如果生成了，说明跑偏。
7. 是否直接把模型输出 HTML 给前端？如果是，必须修改。
8. 是否没有 validator？如果没有，必须补。
9. 是否没有 fallback？如果没有，必须补。
10. 是否把本地 imagePath 返回给前端？如果是，必须删除。
11. iframe 是否带 allow-scripts？如果有，必须删除。
12. generated.html 是否包含 script？如果有，必须删除。
13. jobId 是否可能路径穿越？如果可能，必须修。
14. Day 3 是否错误要求完整 previewHtml？如果是，调整为只验 Java 调 Python。
15. Day 4 是否先死磕 AI 而没有 fallback？如果是，调整为 fallback + validator 优先。
```

---

## 二十二、最终一句话

Week 09 的核心不是“生成得多像”，而是：

> **第一次真正打通单张真实图片到 Layout JSON，再到 generated-page iframe 预览的完整链路。**

执行优先级必须是：

```text
fallback 稳定
> validator 稳定
> Worker 调用稳定
> HTML 编译稳定
> 真实 AI 最小接入
> 前端完整预览
> 生成效果优化
```

Week 09 不要追求大而全。

只打一条最关键的真链路：

```text
单张图片 -> Worker -> AI/fallback -> Layout JSON 校验 -> generated-page HTML -> iframe 预览
```
