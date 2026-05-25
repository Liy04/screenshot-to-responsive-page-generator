# Week 12 开发计划严格验收报告

项目：`screenshot-to-responsive-page-generator`  
验收对象：Week 12 开发计划  
计划主题：AI 输出质量与静态预览还原增强  
工作流：Codex Lead + Lightweight Agents Workflow  
验收结论：**条件通过，不建议原样直接执行**  
最终评级：**A- / 条件通过**  
修正后可达：**A / 可执行**

---

## 1. 严格验收结论

这份 Week 12 计划方向正确，符合当前项目阶段。

项目已经完成真实 AI 链路、artifact 复用、samples、真实 AI smoke 文档和基础测试。当前最大问题已经不是“链路能不能跑通”，而是“生成结果不够像原图”。

因此 Week 12 定位为：

> 从“真实 AI 链路可用”升级到“简单截图生成结果更像原图”。

这个方向正确。

但按严格执行标准看，原计划还需要做一次执行级收口。主要问题不是方向错误，而是以下几点需要补强：

1. 文档数量略重，和 Docs Lite 有轻微冲突。
2. Layout JSON schema 边界需要更清楚。
3. style 安全白名单和 value sanitizer 规则不够细。
4. Day 4 HTML/CSS 静态编译器任务风险最高。
5. P0 范围稍多，需要压实真正核心。
6. 前端对比体验优先级应低于 Worker / compiler 主线。

---

## 2. 用户要求覆盖情况

| 要求 | 验收结果 | 说明 |
|---|---|---|
| Week 12 总体定位 | 通过 | 定位清楚：AI 输出质量与静态预览还原增强 |
| Week 12 总目标 | 通过 | 从链路可用升级到简单截图更像原图 |
| 禁止事项 | 通过 | 禁止事项完整，方向控制正确 |
| P0 / P1 / P2 | 基本通过 | P0 稍多，需要压实核心 P0 |
| 每日任务拆分 | 通过 | Day 1 ~ Day 7 合理 |
| 每日 agent 建议 | 通过 | 符合 Lightweight Agents Workflow |
| 每日验收标准 | 基本通过 | 需要补停止条件和安全验收 |
| 每日 Codex Lead 提示词 | 通过 | 可执行性较强 |
| Week 12 最终交付物 | 基本通过 | 文档交付物略多，和 Docs Lite 有轻微冲突 |
| Week 12 完成后状态预期 | 通过 | 状态预期合理，不追求 1:1 高保真 |

---

## 3. 硬性通过点

### 3.1 Week 12 定位正确

计划把 Week 12 定为：

> AI 输出质量与静态预览还原增强

这是正确的。

当前项目最大问题已经不是链路问题，而是生成结果质量问题。继续做数据库、Figma、编辑器、多页面，都会分散主线。

验收：**通过**

---

### 3.2 禁止事项控制较好

计划明确禁止：

- 不接 MySQL。
- 不创建 Entity / Mapper。
- 不做数据库表。
- 不接 Figma API / MCP。
- 不接 Redis / RabbitMQ。
- 不做多页面生成。
- 不做拖拽编辑器。
- 不做在线编辑器。
- 不做 ZIP 导出。
- 不做登录注册 / 权限。
- 不做复杂真实整站截图。
- 不追求 1:1 高保真。
- 不做 Playwright 视觉回归，除非作为 P2 可选项。
- 不把模型原始 HTML 直接作为最终页面代码。
- 不放宽 iframe sandbox。
- 不允许 `allow-scripts`。
- 不允许 `script` 标签。
- 不允许 inline event。
- 不允许 `javascript:` URL。

验收：**通过**

---

### 3.3 聚焦三张 samples 是正确的

Week 12 只聚焦：

```text
samples/01-simple-card-page.png
samples/02-simple-form-page.png
samples/03-dashboard-cards-page.png
```

这三类样例覆盖：

- card page。
- form page。
- dashboard cards。

可以验证卡片、表单、按钮、布局、颜色、间距、圆角、阴影等基础能力。

验收：**通过**

---

### 3.4 Day 1 ~ Day 7 节奏合理

原计划顺序：

```text
Day 1：质量标准
Day 2：Worker prompt v2
Day 3：Layout JSON style / repair
Day 4：HTML/CSS 静态编译器
Day 5：前端对比体验
Day 6：samples 质量 smoke
Day 7：总结归档
```

这个顺序合理。

先定义质量标准，再改 prompt，再改 repair，再改 compiler，最后做前端对比和 smoke，符合工程闭环。

验收：**通过**

---

## 4. 必须修正的问题

### 4.1 Docs Lite 和文档数量有轻微冲突

原计划建议新增较多文档：

```text
docs/quality/week12-output-quality-standard.md
docs/quality/week12-samples-scorecard.md
docs/smoke/week12-quality-smoke.md
docs/archive/week/12-summary.md
docs/archive/week/12-dev-smoke.md
docs/archive/week/12-acceptance-report.md
docs/tasks/day-12-01.md ~ day-12-07.md
```

这对 Week 12 来说略重。

建议压缩为：

```text
docs/tasks/day-12-01.md ~ day-12-07.md
docs/quality/week12-quality.md
docs/smoke/week12-quality-smoke.md
docs/archive/week/12-summary.md
docs/archive/week/12-acceptance-report.md
```

其中：

- `docs/quality/week12-quality.md` 同时放质量标准和评分表。
- `docs/smoke/week12-quality-smoke.md` 放三张 samples 的 smoke 记录。
- 不强制单独创建 `12-dev-smoke.md`，除非项目已有惯例必须保留。

修正要求：**执行前修改**

---

### 4.2 Day 2 / Day 3 没有明确 schema 边界

计划要求模型输出更多 style 字段，这是对的。

但必须明确：

> Week 12 不做 Layout JSON schema v0.2 大升级。

建议加入硬约束：

```text
Week 12 只在当前 Layout JSON v0.1 可兼容范围内增强 style 表达。
如果当前 schema 不支持 style，则只做最小兼容扩展，并同步更新 validator 和测试。
不得借此升级为 Layout JSON v0.2。
```

修正要求：**执行前修改**

---

### 4.3 style 安全白名单不够具体

计划提到了：

- 禁止 script。
- 禁止 inline event。
- 禁止 javascript URL。
- HTML escape。
- style 白名单。

方向对，但不够严格。

Week 12 的核心是把 AI 输出的 style 编译为 HTML/CSS，这里会出现 CSS 注入风险。

必须补充 style value 安全规则。

禁止 style value 中出现：

```text
javascript:
expression(
url(
<script
onerror=
onclick=
data:text/html
@import
position: fixed
position: absolute
```

说明：

- `position: absolute` 不建议 Week 12 默认支持。
- 后续如果确实需要绝对定位，应单独评审，不应在 Week 12 默认放开。

建议只允许的值类型：

```text
颜色：
- #fff
- #ffffff
- rgb(...)
- rgba(...)
- hsl(...)
- hsla(...)
- 常见安全颜色名

尺寸：
- px
- rem
- em
- %
- auto
- 0

布局：
- flex
- grid
- block
- inline-block
- row
- column
- center
- space-between
- flex-start
- flex-end
```

修正要求：**必须补**

---

### 4.4 Day 4 编译器任务风险最高

Day 4 要把 Layout JSON style 转成 CSS：

- 写得太宽，容易引入安全问题。
- 写得太窄，又提升不了视觉质量。

建议 Day 4 增加停止条件：

```text
如果 style sanitizer、HTML escape、安全测试无法当天完成，
则只合并安全白名单和基础 card/button/input/text 样式，
不继续扩展更多 CSS 能力。
```

Day 4 最低交付应该是：

```text
[ ] card 样式可见
[ ] button 样式可见
[ ] input 样式可见
[ ] text 样式可见
[ ] 安全测试通过
```

不应该一次性追求支持所有视觉字段。

修正要求：**必须补**

---

### 4.5 P0 稍微偏多，需要重新压实

原计划 P0 包括：

- 质量标准。
- 评分表。
- Worker prompt v2。
- Layout JSON style。
- 静态编译器。
- 安全规则。
- 三张 samples smoke。

这些可以接受，但真正 P0 应该压实为：

```text
P0-1：质量标准和评分表
P0-2：promptVersion=week12-v1
P0-3：style 白名单和安全 sanitizer
P0-4：静态编译器支持 card/button/input/text 基础样式
P0-5：三张 samples 完成人工质量 smoke
```

P1 才是：

```text
P1：更完整的 repair 默认样式
P1：前端左右对比体验
P1：dashboard grid 更好看
P1：metadata 展示优化
```

也就是说，前端对比体验不应该压过 Worker / compiler 质量主线。

修正要求：**建议修改**

---

## 5. 逐日严格验收

### 5.1 Day 1：质量标准和评分表

验收：**通过，建议精简文档数量**

建议把文档收敛为一个文件：

```text
docs/quality/week12-quality.md
```

内容包含：

```text
1. 输出质量标准
2. 人工评分表
3. 三张 samples 评分模板
4. Week 12 通过线
```

Day 1 不应该创建太多文档。

---

### 5.2 Day 2：Worker prompt v2

验收：**条件通过**

Day 2 目标正确：

- `promptVersion=week12-v1`
- 禁止输出 HTML。
- 只输出 Layout JSON。
- 要求识别 card / form / dashboard 结构。
- 要求输出 style 字段。

必须补充：

```text
如果模型输出 HTML、Markdown、解释文字，
仍然必须经过 JSON 清洗 / repair / fallback，
不得直接使用模型 HTML。
```

还要补充：

```text
prompt 优化不得降低 FAILED / FALLBACK 的可控性。
```

---

### 5.3 Day 3：Layout JSON style 和 repair

验收：**条件通过，必须补安全边界**

Day 3 要明确：

- repair 是补齐缺失 style，不是编造复杂 UI。
- repair 是 deterministic rule，不是再让模型自由发挥。
- repair 不能把无效字段强行保留。
- repair 不应该绕过 validator。

建议增加：

```text
repair 补默认值只能基于 node role/type。
不能根据不可信字段生成危险 CSS。
```

---

### 5.4 Day 4：HTML/CSS 静态编译器

验收：**高风险，条件通过**

必须补充：

```text
[ ] style key 必须白名单
[ ] style value 必须 sanitizer
[ ] CSS 中禁止 url()
[ ] CSS 中禁止 expression()
[ ] CSS 中禁止 @import
[ ] HTML attribute 禁止 on*
[ ] href/src 禁止 javascript:
[ ] 所有 text content 必须 escape
```

如果这些不补，Day 4 不建议执行。

---

### 5.5 Day 5：前端原图 vs 预览对比

验收：**通过，但优先级应降为 P1**

这个任务有价值，但不是 Week 12 的核心技术突破。

它应该服务于人工验收，而不是变成产品化 UI。

明确不做：

```text
不做拖拽
不做编辑器
不做复杂 tabs
不做复杂状态管理
不做设计工作台
```

只做：

```text
原图
iframe
Layout JSON
warnings/errors
metadata
```

---

### 5.6 Day 6：samples 质量 smoke

验收：**通过**

评分标准建议更明确：

```text
每张 sample 总分 35 分。
最低通过：20 / 35。
理想通过：24 / 35。
优秀：28 / 35。
```

同时记录：

```text
人工评分人
评分日期
模型名称
promptVersion
是否 artifact reused
是否 fallback
主要缺陷
```

---

### 5.7 Day 7：总结归档

验收：**通过**

Week 13 决策标准建议更明确：

```text
如果平均分 < 20：
Week 13 继续 prompt / compiler / repair。

如果平均分 20~24：
Week 13 继续质量增强，谨慎探索视觉回归。

如果平均分 ≥ 24：
Week 13 可以考虑 Layout JSON schema v0.2 或轻量视觉回归。

如果平均分 ≥ 28：
可以开始 Figma 或持久化前置探索。
```

---

## 6. 修正后的 P0 / P1 / P2

### 6.1 P0：必须完成

```text
[ ] Week 12 质量标准和评分表
[ ] promptVersion=week12-v1
[ ] prompt 禁止 HTML，只输出 Layout JSON
[ ] style key 白名单
[ ] style value sanitizer
[ ] 静态编译器支持 card/button/input/text 基础样式
[ ] HTML escape
[ ] 禁止 script / inline event / javascript URL / url() / expression() / @import
[ ] 三张 samples 完成质量 smoke
[ ] Worker / Backend / Frontend 测试通过
```

---

### 6.2 P1：尽量完成

```text
[ ] repair 补齐 page/section/card/button/input/form/text 默认 style
[ ] dashboard cards 支持基础 grid/flex
[ ] /dev/image-to-layout 左右对比
[ ] metadata 展示更清楚
[ ] warnings/errors 更清楚
```

---

### 6.3 P2：可选

```text
[ ] 半自动 smoke 脚本增强
[ ] 额外 samples
[ ] 简单截图尺寸辅助信息
[ ] Playwright 静态截图探索
```

---

## 7. 执行前必须修改的 6 点

```text
[ ] 1. 合并 Week 12 质量标准和评分表，避免 Docs 过重
[ ] 2. 明确 Week 12 不升级 Layout JSON schema v0.2
[ ] 3. 增加 style key 白名单和 style value sanitizer 规则
[ ] 4. Day 4 增加 CSS 安全测试和停止条件
[ ] 5. 将前端对比体验从 P0 降为 P1
[ ] 6. Day 6 质量 smoke 增加评分人、日期、模型、promptVersion、artifact reused 记录
```

---

## 8. 修正后建议定版主线

Week 12 定版主题保持不变：

> Week 12：AI 输出质量与静态预览还原增强

定版主线建议改为：

> 围绕三张 samples，通过 prompt v2、style 白名单、repair 默认样式、静态编译器样式支持和人工质量 smoke，让简单截图生成结果不再像裸 HTML。

---

## 9. 是否能直接交给 Codex Lead？

**不建议原样直接交。**

原因：

1. Day 4 安全规则还不够细。
2. 文档数量略重，不完全符合 Docs Lite。
3. schema 边界需要补清楚。
4. 前端对比体验优先级略高，容易抢占 Worker / compiler 主线。

建议先把第 7 节的 6 个修改点补进计划，然后再交给 Codex Lead 执行。

---

## 10. 最终验收结论

### 是否通过？

**条件通过。**

### 是否需要重写计划？

**不需要重写。**

这份计划主线是对的，只需要做执行级收口。

### 最终验收评级

**A-**

### 扣分原因

1. Day 4 安全规则还不够细。
2. 文档数量略重，不完全符合 Docs Lite。
3. schema 边界需要补清楚。
4. 前端对比体验优先级略高，容易抢占 Worker / compiler 主线。

### 修正后评级

**A / 可执行**

---

## 11. 建议交给 Codex Lead 前的最终指令

```text
请以 Codex Lead 身份修正 Week 12 计划后再执行。

修正要求：
1. 合并 Week 12 质量标准和评分表为 docs/quality/week12-quality.md。
2. 明确 Week 12 不升级 Layout JSON schema v0.2。
3. 增加 style key 白名单和 style value sanitizer 规则。
4. Day 4 增加 CSS 安全测试和停止条件。
5. 将前端对比体验从 P0 降为 P1。
6. Day 6 质量 smoke 增加评分人、日期、模型、promptVersion、artifact reused 记录。

保持：
- Week 12 主题仍为 AI 输出质量与静态预览还原增强。
- 只聚焦三张 samples。
- 不进入 MySQL、Figma、编辑器、多页面、Playwright 视觉回归。
- 不使用 Claude Code agents。
- 不引入 .claude/agents。
- 保持 Docs Lite。
```
