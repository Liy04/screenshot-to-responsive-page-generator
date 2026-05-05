# 《截图 / Figma 到响应式页面生成器》轻量版 PRD v0.1（长期产品愿景草案）

## 0. 范围声明

本文档用于描述项目的长期产品愿景和后续演进方向，不作为 Week 01 或当前 MVP 第一版的执行范围。

当前阶段范围以以下文档为准：

- Week 01 初始化阶段：以 `docs/week/01-plan.md` 和 `docs/week/01-status.md` 为准。
- 当前阶段轻量上下文：以 `docs/context/current-phase.md` 为准。
- 当前 MVP 第一版：以 `docs/mvp-scope.md` 为准。

当前 MVP 第一版只做：

```text
上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果
```

当前 MVP 第一版明确不做：

- 不做 Figma 集成。
- 不接入真实 AI 模型 API。
- 不做真实截图解析。
- 不做真实响应式页面生成。
- 不做拖拽编辑器。
- 不做导出 ZIP。
- 不引入 Redis / RabbitMQ 作为运行前置依赖。
- 未确认数据库任务前，不设计数据库表、不创建数据库访问层。

本文档中涉及 Figma、真实 AI、页面代码生成、在线编辑、导出 ZIP、Redis、RabbitMQ、数据库表结构等内容，均表示后续产品方向或草案，不能直接下沉为当前 Week 02 / MVP 第一版开发任务。

## 1. 产品一句话说明

本项目是一个面向前端开发者、学生和低代码原型开发者的 AI 辅助页面生成工具。用户上传一张页面截图，或输入 Figma 设计稿链接，系统自动分析页面结构，并生成可预览、可编辑、可导出的 Vue3 响应式页面代码。

简单说：

> 把“设计图 / 截图”变成“能运行的 Vue 页面”。

---

## 2. 项目背景

当前前端开发中，很多页面开发流程是：

设计师在 Figma 中画页面，开发者根据设计稿手动还原页面，然后进行响应式适配、样式调整、组件拆分和接口联调。

这个过程存在几个问题：

1. **页面还原耗时**  
   简单页面也需要花不少时间写 HTML、CSS、Vue 结构。

2. **设计稿到代码存在重复劳动**  
   很多卡片、按钮、列表、表单布局都是重复结构。

3. **AI 可以生成代码，但直接生成不稳定**  
   如果只把截图丢给 AI，让它直接输出完整页面，容易出现元素缺失、布局混乱、代码不可维护等问题。

4. **你当前正在学习 Codex 的 Vibe Coding 开发方式**  
   所以这个项目既是一个 AI 工具项目，也是一个适合练习“先计划、再编码、最后测试”的实战项目。

---

## 3. 产品目标

### 3.1 核心目标

长期产品目标是让用户最终可以完成下面这条主流程：

> 上传截图 / 输入 Figma 链接 → 创建生成任务 → AI 分析页面 → 生成 Vue3 页面代码 → 在线预览 → 简单修改 → 导出代码。

当前 MVP 第一版的目标更小，只验证：

> 上传截图 → 创建任务 → 查看任务状态 → 查看 mock 生成结果。

### 3.2 学习目标

这个项目不只追求“功能完成”，还要帮助你练习以下能力：

| 目标 | 说明 |
|---|---|
| Codex 项目开发流程 | 练习让 Codex 先分析、再计划、再编码、再测试 |
| Vue3 页面工程能力 | 练习组件封装、页面渲染、样式组织、响应式布局 |
| Spring Boot 项目编排能力 | 练习任务创建、状态流转、文件管理、接口设计 |
| Python Worker 能力 | 练习 AI 调用、截图分析、JSON 处理、异步任务处理 |
| 测试能力 | 练习 Postman、接口测试、页面预览测试、基础自动化测试 |

---

## 4. 目标用户

### 4.1 第一类用户：前端开发学习者

代表用户：你自己。

需求：

- 想快速根据截图生成页面骨架。
- 想学习 Vue3 组件结构。
- 想理解 AI 如何辅助前端开发。
- 想通过项目提升简历含金量。

### 4.2 第二类用户：产品 / 原型人员

需求：

- 有页面截图或 Figma 原型。
- 想快速生成一个可运行页面。
- 不一定追求完全生产可用，但希望快速预览效果。

### 4.3 第三类用户：独立开发者

需求：

- 想快速从设计图生成落地页面。
- 希望减少重复写布局代码的时间。
- 希望生成结果可以继续人工修改。

---

## 5. 产品范围

### 5.1 当前 MVP 第一版必须做

当前 MVP 第一版只包含：

1. 截图上传。
2. 创建生成任务。
3. 查看生成任务状态。
4. 查看 mock 生成结果。

当前 MVP 第一版不接入真实 AI、Figma、Redis、RabbitMQ，也不实现真实页面代码生成、在线编辑或导出 ZIP。

### 5.2 后续产品愿景包含

后续产品版本可以逐步包含：

1. 截图上传。
2. Figma 链接录入。
3. 创建页面生成任务。
4. 查看生成任务状态。
5. AI 生成页面结构 JSON。
6. 根据结构 JSON 生成 Vue3 页面代码。
7. 在线预览生成结果。
8. 简单编辑文字、颜色、间距。
9. 导出代码 ZIP。
10. 查看历史生成记录。

### 5.3 后续产品版本暂不做

为了避免项目过大，第一版暂时不做：

| 暂不做功能 | 原因 |
|---|---|
| 完整拖拽式低代码编辑器 | 难度太高，容易偏离主线 |
| 自动接入真实业务接口 | 第一版重点是页面生成，不是业务系统 |
| 多人协作 | 对 MVP 价值不大 |
| 账号会员 / 付费系统 | 暂时没有商业化需求 |
| AI 模型微调 | 成本高，当前阶段不需要 |
| 完美还原所有复杂页面 | 不现实，第一版先解决中低复杂度页面 |
| 自动生成完整项目工程 | 第一版只导出页面级代码 |

---

## 6. 核心使用场景

### 场景一：用户上传截图生成页面

用户操作流程：

1. 用户进入系统首页。
2. 点击“上传截图”。
3. 选择一张 PNG / JPG / WebP 图片。
4. 选择目标技术栈：Vue3 + CSS。
5. 点击“开始生成”。
6. 系统创建任务，进入生成中状态。
7. AI 分析截图，生成页面结构。
8. 系统生成 Vue 页面代码。
9. 用户查看在线预览。
10. 用户可以导出代码。

成功标准：

- 页面能正常渲染。
- 主要布局和截图接近。
- 代码能在 Vue3 + Vite 项目中运行。
- 用户可以下载生成结果。

---

### 场景二：用户输入 Figma 链接生成页面

用户操作流程：

1. 用户进入“Figma 导入”页面。
2. 粘贴 Figma 文件链接或节点链接。
3. 系统读取 Figma 信息。
4. 系统解析页面结构、颜色、字体、间距。
5. AI 生成页面结构 JSON。
6. 系统生成 Vue 页面代码。
7. 用户在线预览。
8. 用户导出代码。

成功标准：

- 能识别 Figma 页面主要区块。
- 生成页面结构比纯截图模式更稳定。
- 能尽量还原 Figma 中的布局层级。

---

### 场景三：用户二次调整生成结果

用户操作流程：

1. 用户进入生成结果页。
2. 左侧查看原始截图 / Figma 参考图。
3. 中间查看生成页面预览。
4. 右侧修改属性，例如标题、按钮文字、颜色、间距。
5. 页面实时刷新。
6. 用户满意后导出代码。

成功标准：

- 用户可以修改基础内容。
- 修改后预览区域能更新。
- 导出的代码包含修改后的结果。

---

## 7. 功能需求

## 7.1 首页 / 工作台

### 功能说明

首页用于展示项目入口、最近生成记录和创建新任务入口。

### 页面元素

| 元素 | 说明 |
|---|---|
| 项目标题 | 截图 / Figma 到响应式页面生成器 |
| 创建任务按钮 | 新建生成任务 |
| 最近任务列表 | 展示最近生成记录 |
| 任务状态标签 | 待处理、生成中、成功、失败 |
| 快速入口 | 上传截图、导入 Figma、查看历史 |

### 用户操作

用户可以：

- 创建新任务。
- 查看历史任务。
- 进入某个任务详情。
- 删除历史任务。

---

## 7.2 创建生成任务

### 功能说明

用户可以选择“截图模式”或“Figma 模式”创建生成任务。

### 输入字段

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| 任务名称 | 文本 | 否 | 用户可以自定义任务名称 |
| 输入类型 | 枚举 | 是 | screenshot / figma |
| 截图文件 | 文件 | 截图模式必填 | PNG、JPG、WebP |
| Figma 链接 | 文本 | Figma 模式必填 | Figma file URL 或 node URL |
| 目标框架 | 枚举 | 是 | 第一版固定 Vue3 |
| 样式方案 | 枚举 | 是 | 第一版固定普通 CSS |
| 是否开启响应式 | 布尔值 | 是 | 默认开启 |

### 业务规则

1. 截图模式必须上传图片。
2. Figma 模式必须填写链接。
3. 图片大小建议限制在 10MB 内。
4. 第一版只支持单页面生成。
5. 第一版不支持批量上传。

---

## 7.3 截图上传

### 功能说明

用户上传页面截图，系统保存文件，并生成一个可访问的资源地址。

### 支持格式

| 格式 | 是否支持 |
|---|---|
| PNG | 支持 |
| JPG / JPEG | 支持 |
| WebP | 支持 |
| GIF | 暂不支持 |
| PDF | 暂不支持 |

### 校验规则

- 文件不能为空。
- 文件大小不能超过 10MB。
- 文件格式必须是图片。
- 上传成功后返回 assetId。

---

## 7.4 Figma 导入

### 功能说明

用户输入 Figma 链接，系统解析 fileKey 和 nodeId。

### 后续能力

当前 MVP 第一版不做 Figma 集成，不接入 Figma API / Figma MCP。

后续 Figma 模式可以先做轻量实现：

1. 用户粘贴 Figma 链接。
2. 后端保存链接。
3. Python Worker 根据链接调用 Figma API 或后续 MCP 工具。
4. 获取设计节点信息。
5. 转成统一的页面结构 JSON。

### 链接示例

```text
https://www.figma.com/design/xxxx/project-name?node-id=1-2
```

### 需要解析的信息

| 字段 | 说明 |
|---|---|
| fileKey | Figma 文件唯一标识 |
| nodeId | 选中的设计节点 |
| fileName | 文件名称 |
| frameName | 页面 / Frame 名称 |
| width | 设计稿宽度 |
| height | 设计稿高度 |

---

## 7.5 AI 页面结构分析

### 功能说明

这是项目的核心功能。

系统不会直接让 AI 一步生成完整代码，而是先让 AI 生成一个中间层 JSON。

这个中间层可以理解为：

> AI 先把页面“看懂”，再让程序根据这个理解去生成代码。

### 页面结构 JSON 示例

```json
{
  "pageName": "LandingPage",
  "layoutType": "marketing",
  "breakpoints": ["desktop", "tablet", "mobile"],
  "tokens": {
    "colors": {
      "primary": "#2563eb",
      "background": "#ffffff",
      "text": "#111827"
    },
    "spacing": {
      "small": "8px",
      "medium": "16px",
      "large": "32px"
    },
    "radius": {
      "card": "16px",
      "button": "8px"
    }
  },
  "sections": [
    {
      "id": "hero",
      "type": "hero",
      "layout": "two-column",
      "responsiveRule": "mobile-column",
      "children": [
        {
          "type": "text",
          "role": "title",
          "content": "页面主标题"
        },
        {
          "type": "button",
          "role": "primary-action",
          "content": "立即开始"
        }
      ]
    }
  ]
}
```

### 为什么要有中间层 JSON？

因为直接生成代码有几个问题：

1. 代码容易乱。
2. 很难二次编辑。
3. 失败后不好修复。
4. 很难知道 AI 到底理解了什么。
5. 响应式规则容易缺失。

有了中间层后，系统可以：

- 先校验结构是否合理。
- 再生成代码。
- 后续可以做可视化编辑。
- 失败时可以定位是哪一层出错。

---

## 7.6 Vue3 页面代码生成

### 功能说明

系统根据页面结构 JSON 生成 Vue3 页面代码。

### 后续输出内容

当前 MVP 第一版不做真实页面代码生成，只返回 mock 结果。

| 输出文件 | 说明 |
|---|---|
| `GeneratedPage.vue` | 主页面组件 |
| `style.css` | 页面样式 |
| `metadata.json` | 生成信息 |
| `preview.png` | 页面预览截图，后续可选 |

### Vue 文件示例结构

```vue
<template>
  <main class="generated-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1>页面主标题</h1>
        <p>页面副标题内容</p>
        <button>立即开始</button>
      </div>
    </section>
  </main>
</template>

<script setup>
</script>

<style scoped>
.generated-page {
  width: 100%;
  min-height: 100vh;
}

.hero-section {
  padding: 64px 24px;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 16px;
  }
}
</style>
```

### 生成规则

1. 第一版优先使用普通 CSS。
2. 不默认使用 Tailwind。
3. 尽量使用语义化 class 名称。
4. 避免大量绝对定位。
5. 必须包含移动端适配。
6. 生成代码要可读、可维护。
7. 不引入多余依赖。

---

## 7.7 在线预览

### 功能说明

用户可以在浏览器中查看生成页面效果。

### 预览模式

| 模式 | 尺寸示例 |
|---|---|
| 桌面端 | 1440px |
| 平板端 | 768px |
| 移动端 | 390px |

### 页面布局建议

生成结果页建议分为三栏：

```text
左侧：原始截图 / Figma 参考图
中间：生成页面预览
右侧：属性编辑面板
```

### 用户可以操作

- 切换桌面 / 平板 / 移动端预览。
- 查看生成代码。
- 修改基础属性。
- 重新生成。
- 导出代码。

---

## 7.8 简单属性编辑

### 功能说明

当前 MVP 第一版不做属性编辑。后续轻量编辑版本不做完整拖拽编辑，只做轻量属性编辑。

### 可编辑内容

| 类型 | 可编辑字段 |
|---|---|
| 文本 | 标题、段落、按钮文字 |
| 颜色 | 主色、背景色、文字色 |
| 间距 | section padding、card gap |
| 圆角 | 按钮圆角、卡片圆角 |
| 布局 | 横向 / 纵向、是否居中 |
| 响应式 | 移动端是否堆叠 |

### 不做内容

- 不做自由拖拽。
- 不做复杂图层面板。
- 不做像 Figma 一样的编辑器。
- 不做完整低代码平台。

---

## 7.9 重新生成 / 二次优化

### 功能说明

用户可以输入自然语言要求系统重新优化页面。

### 示例指令

```text
按钮颜色改成蓝色，整体间距再大一点，移动端标题居中。
```

```text
这个页面太拥挤了，把卡片之间的距离加大。
```

```text
让这个页面更像后台管理系统风格。
```

### 系统处理逻辑

1. 用户输入修改要求。
2. 系统读取当前页面结构 JSON。
3. AI 根据要求修改 JSON 或代码。
4. 系统重新生成预览。
5. 保存新版本。

### 版本规则

每次重新生成都保存一个版本：

| 字段 | 说明 |
|---|---|
| version | 版本号 |
| prompt | 用户修改指令 |
| layoutJson | 当前结构 |
| code | 当前代码 |
| createdAt | 生成时间 |

---

## 7.10 导出代码

### 功能说明

当前 MVP 第一版不做导出 ZIP。后续导出能力中，用户可以把生成页面导出为 ZIP。

### ZIP 内容

```text
generated-page.zip
├── GeneratedPage.vue
├── style.css
├── metadata.json
└── README.md
```

### README 内容

README 中需要说明：

- 生成时间。
- 技术栈。
- 如何放入 Vue3 项目。
- 有哪些已知限制。
- 哪些地方需要人工检查。

---

## 8. 系统角色与权限

后续产品版本可以先不做复杂权限，默认只有一个普通用户角色。

### 普通用户权限

| 功能 | 是否允许 |
|---|---|
| 创建任务 | 允许 |
| 上传截图 | 允许 |
| 导入 Figma | 允许 |
| 查看任务 | 允许 |
| 编辑生成结果 | 允许 |
| 导出代码 | 允许 |
| 删除任务 | 允许 |

### 后续可扩展角色

后续可以增加：

- 管理员。
- 团队成员。
- 只读用户。
- 审核用户。

第一版不需要做。

---

## 9. 页面清单

### 9.1 页面结构

| 页面 | 路径建议 | 说明 |
|---|---|---|
| 首页 / 工作台 | `/dashboard` | 展示任务列表和入口 |
| 创建任务页 | `/generation/create` | 上传截图或输入 Figma 链接 |
| 任务详情页 | `/generation/:jobId` | 查看生成状态 |
| 生成结果页 | `/generation/:jobId/result` | 预览、编辑、导出 |
| 历史记录页 | `/history` | 查看历史生成任务 |
| 设置页 | `/settings` | 配置模型 Key、Figma Token 等，可后续做 |

---

## 10. 后续核心业务流程

本节描述后续完整产品形态的业务流程，不代表当前 MVP 第一版必须实现。当前 MVP 第一版仍以“上传截图 -> 创建任务 -> 查看任务状态 -> 查看 mock 生成结果”为准。

### 10.1 截图生成流程

```text
用户上传截图
↓
后端保存图片
↓
创建 generation_job 任务
↓
RabbitMQ 投递任务
↓
Python Worker 消费任务
↓
AI 分析截图
↓
生成 layout JSON
↓
生成 Vue 代码
↓
保存生成结果
↓
前端展示预览和代码
```

---

### 10.2 Figma 生成流程

```text
用户输入 Figma 链接
↓
后端解析 fileKey / nodeId
↓
创建 generation_job 任务
↓
Python Worker 获取 Figma 数据
↓
转换为 layout JSON
↓
生成 Vue 代码
↓
保存结果
↓
前端展示预览和代码
```

---

### 10.3 二次优化流程

```text
用户输入修改要求
↓
后端创建 refine 任务
↓
Worker 读取旧版本 JSON 和代码
↓
AI 根据要求修改
↓
生成新版本
↓
前端刷新预览
```

---

## 11. 数据库设计草案

本节仅为后续数据库任务的草案，不代表当前 Week 02 或 MVP 第一版需要创建数据库表。

当前 Week 02 / MVP 第一版不设计数据库表；在用户确认数据库任务前，不新增 Mapper、实体表映射、数据库配置或数据库访问层。

### 11.1 project 项目表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigint | 主键 |
| name | varchar | 项目名称 |
| description | varchar | 项目描述 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

---

### 11.2 design_source 设计来源表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigint | 主键 |
| project_id | bigint | 项目 ID |
| source_type | varchar | screenshot / figma |
| file_url | varchar | 截图地址 |
| figma_url | varchar | Figma 链接 |
| figma_file_key | varchar | Figma fileKey |
| figma_node_id | varchar | Figma nodeId |
| width | int | 原始宽度 |
| height | int | 原始高度 |
| created_at | datetime | 创建时间 |

---

### 11.3 generation_job 生成任务表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigint | 主键 |
| project_id | bigint | 项目 ID |
| source_id | bigint | 设计来源 ID |
| status | varchar | pending / running / success / failed |
| mode | varchar | screenshot / figma |
| model_name | varchar | 使用的模型 |
| error_message | text | 失败原因 |
| started_at | datetime | 开始时间 |
| finished_at | datetime | 结束时间 |
| created_at | datetime | 创建时间 |

---

### 11.4 generation_artifact 生成产物表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigint | 主键 |
| job_id | bigint | 任务 ID |
| version | int | 版本号 |
| layout_json | longtext | 页面结构 JSON |
| vue_code | longtext | Vue 代码 |
| css_code | longtext | CSS 代码 |
| preview_url | varchar | 预览地址 |
| zip_url | varchar | 导出包地址 |
| created_at | datetime | 创建时间 |

---

### 11.5 generation_refine 重新生成记录表

| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigint | 主键 |
| artifact_id | bigint | 原始产物 ID |
| prompt | text | 用户修改要求 |
| new_artifact_id | bigint | 新产物 ID |
| created_at | datetime | 创建时间 |

---

## 12. 接口设计草案

### 12.1 创建项目

```http
POST /api/projects
```

请求：

```json
{
  "name": "首页生成项目",
  "description": "根据截图生成首页"
}
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "projectId": 1
  }
}
```

---

### 12.2 上传截图

```http
POST /api/assets/upload
```

请求：

```text
multipart/form-data
file: screenshot.png
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "assetId": 1001,
    "fileUrl": "/uploads/screenshot.png"
  }
}
```

---

### 12.3 创建生成任务

```http
POST /api/generations
```

请求：

```json
{
  "projectId": 1,
  "mode": "screenshot",
  "assetId": 1001,
  "targetStack": "vue3-css",
  "responsive": true
}
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": 2001,
    "status": "pending"
  }
}
```

---

### 12.4 查询任务状态

```http
GET /api/generations/{jobId}
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "jobId": 2001,
    "status": "running",
    "progress": 60
  }
}
```

---

### 12.5 获取生成结果

```http
GET /api/generations/{jobId}/result
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "artifactId": 3001,
    "layoutJson": {},
    "vueCode": "...",
    "cssCode": "...",
    "previewUrl": "/preview/3001"
  }
}
```

---

### 12.6 二次优化

```http
POST /api/generations/{jobId}/refine
```

请求：

```json
{
  "artifactId": 3001,
  "prompt": "把按钮颜色改成蓝色，并让移动端居中显示"
}
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "newJobId": 2002
  }
}
```

---

### 12.7 导出代码

```http
POST /api/exports
```

请求：

```json
{
  "artifactId": 3001,
  "format": "zip"
}
```

响应：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "downloadUrl": "/exports/generated-page.zip"
  }
}
```

---

## 13. 技术选型建议

结合你当前技术栈，第一版建议如下：

| 模块 | 技术 | 是否推荐 | 说明 |
|---|---|---|---|
| 前端 | Vue3 + Vite | 推荐 | 你熟悉，适合做工作台和预览页 |
| 样式 | 普通 CSS / CSS Variables | 推荐 | 第一版更容易理解和维护 |
| 后端 | Java + Spring Boot | 推荐 | 负责业务接口、任务管理、文件管理 |
| ORM | MyBatis-Plus | 推荐 | 适合快速开发 CRUD |
| 数据库 | MySQL | 推荐 | 存项目、任务、生成记录 |
| 缓存 | Redis | 后续可选 | 可用于存任务状态、临时结果；当前 MVP 不作为运行前置依赖 |
| 消息队列 | RabbitMQ | 后续可选 | AI 生成任务适合异步处理；当前 MVP 不作为运行前置依赖 |
| AI Worker | Python | 推荐新增 | 负责调用模型、处理图片、生成 JSON |
| 测试 | Postman + JMeter + Playwright | 推荐 | 你已有测试基础，可以形成亮点 |
| Figma 对接 | Figma API / MCP | 后续增强 | 后续可以先做 URL 保存和简单解析 |

### 结论

技术选型不需要大改。

后续完整产品形态可以演进为：

```text
Vue3 前端
↓
Spring Boot 后端
↓
RabbitMQ 任务队列（后续可选）
↓
Python AI Worker
↓
MySQL / Redis / 文件存储（后续逐步引入）
```

---

## 14. 非功能需求

### 14.1 性能需求

| 项目 | 要求 |
|---|---|
| 图片上传 | 10MB 内图片 3 秒内上传完成 |
| 创建任务 | 1 秒内返回任务 ID |
| 任务状态查询 | 500ms 内返回 |
| 页面生成 | MVP 阶段允许 30 秒到 2 分钟 |
| 代码导出 | 5 秒内生成 ZIP |

---

### 14.2 稳定性需求

- AI 生成失败时，不能让任务一直卡在 running。
- 任务必须有 failed 状态。
- 失败原因要保存。
- 用户可以重新生成。
- Worker 崩溃后，任务不应丢失。

---

### 14.3 安全需求

- 上传文件需要限制格式和大小。
- Figma Token、模型 API Key 不能写死在前端。
- 生成代码不能直接执行危险脚本。
- 导出文件只包含必要代码。
- 用户上传的图片后续应支持删除。

---

### 14.4 可维护性需求

- Prompt 模板单独管理。
- 页面结构 JSON 需要有版本号。
- 生成代码和任务记录需要关联。
- Worker 日志需要记录模型调用结果。
- 后续可以扩展 React / Tailwind / UniApp 等输出目标。

---

## 15. 验收标准

### 15.1 当前 MVP 第一版验收

当前 MVP 第一版以 `docs/mvp-scope.md` 为准，满足以下条件即可：

1. 用户可以上传一张截图。
2. 系统可以创建一个生成任务。
3. 用户可以查看任务状态。
4. 用户可以查看 mock 生成结果。
5. 不接入真实 AI、Figma、Redis、RabbitMQ，不实现真实代码生成和导出 ZIP。

### 15.2 后续产品总体验收

满足以下条件，后续完整产品版本算完成：

1. 用户可以上传一张截图。
2. 系统可以创建生成任务。
3. 任务状态可以从 pending → running → success / failed。
4. 系统可以生成页面结构 JSON。
5. 系统可以生成 Vue3 页面代码。
6. 用户可以在线预览生成页面。
7. 用户可以修改基础文本和颜色。
8. 用户可以导出 ZIP。
9. 至少完成 5 个不同页面样例测试。
10. 有 README、接口文档和演示截图。

---

### 15.3 截图模式验收

| 验收项 | 标准 |
|---|---|
| 上传截图 | 支持 PNG / JPG / WebP |
| 页面结构识别 | 能识别主要 section、标题、按钮、卡片 |
| 代码生成 | 生成 Vue3 单文件组件 |
| 响应式 | 至少支持 desktop / mobile |
| 预览 | 页面可以正常打开 |

---

### 15.4 Figma 模式验收

| 验收项 | 标准 |
|---|---|
| 链接录入 | 可以保存 Figma URL |
| 信息解析 | 可以解析 fileKey / nodeId |
| 任务创建 | 可以创建 Figma 生成任务 |
| 结果生成 | 可以生成初步页面代码 |
| 错误处理 | 链接无效时有错误提示 |

---

### 15.5 二次编辑验收

| 验收项 | 标准 |
|---|---|
| 修改文字 | 标题、按钮文字可修改 |
| 修改颜色 | 主色、背景色可修改 |
| 修改间距 | section padding 可调整 |
| 实时预览 | 修改后页面刷新 |
| 保存版本 | 每次修改保留版本记录 |

---

## 16. 项目里程碑

### 第一阶段：基础工程搭建

时间建议：第 1 周

交付物：

- Vue3 + Vite 前端项目。
- Spring Boot 后端项目。
- Python Worker 空项目。
- README。
- AGENTS.md。
- smoke 测试文档。
- 协作规则文档。

---

### 第二阶段：截图上传和任务流

时间建议：第 2 周

交付物：

- 上传截图接口。
- 创建任务接口。
- 查询任务状态接口。
- 前端创建任务页面。
- Mock 生成结果。
- Worker mock 处理入口。

---

### 第三阶段：AI 结构分析

时间建议：第 3 到 4 周

交付物：

- 截图转 layout JSON。
- Prompt 模板。
- JSON Schema 校验。
- 失败重试机制。
- 任务日志记录。

---

### 第四阶段：Vue 代码生成和预览

时间建议：第 5 周

交付物：

- layout JSON 转 Vue 代码。
- 代码预览页面。
- 桌面端 / 移动端预览。
- 生成结果保存。

---

### 第五阶段：编辑和导出

时间建议：第 6 周

交付物：

- 文本编辑。
- 颜色编辑。
- 间距编辑。
- 导出 ZIP。
- 版本记录。

---

### 第六阶段：Figma 模式和测试优化

时间建议：第 7 到 8 周

交付物：

- Figma URL 解析。
- Figma 任务创建。
- 基础 Figma 数据读取。
- 5 到 10 个样例测试。
- 演示视频 / 项目文档。
- 简历项目描述。

---

## 17. 风险与应对

| 风险 | 说明 | 应对方案 |
|---|---|---|
| AI 生成页面不稳定 | 截图理解可能出错 | 先生成 JSON，再生成代码 |
| 响应式效果差 | 截图只有一个尺寸 | 强制生成 desktop / mobile 规则 |
| 代码不可维护 | AI 可能生成混乱代码 | 固定 Vue 代码模板和 CSS 规范 |
| 项目范围过大 | 容易做成低代码平台 | 第一版不做拖拽编辑器 |
| Figma 接入复杂 | Token、权限、节点解析有门槛 | 第一版先支持链接保存和基础解析 |
| 生成耗时较长 | AI 调用需要时间 | 使用异步任务 + 状态轮询 |
| 文件安全问题 | 用户上传未知文件 | 限制格式、大小、存储路径 |
| 成本不可控 | 多次生成会消耗模型费用 | 限制生成轮次，记录 token 消耗 |

---

## 18. 第一版推荐产品形态

第一版不要做成复杂平台，建议做成一个清晰的三步工具：

```text
第一步：输入设计
上传截图 / 输入 Figma 链接

第二步：生成页面
AI 分析结构并生成 Vue3 页面

第三步：预览导出
在线预览、简单编辑、导出代码
```

产品界面可以命名为：

> Design2Vue

或者中文名：

> 设计稿转 Vue 页面生成器

---

## 19. 简历项目描述参考

后续你可以在简历中这样写：

> 设计并实现一款基于 AI 的截图 / Figma 到 Vue3 响应式页面生成器，支持截图上传、Figma 链接导入、异步生成任务、页面结构 JSON 分析、Vue3 代码生成、在线预览、属性编辑与代码导出。后端基于 Spring Boot、MyBatis-Plus、MySQL、Redis、RabbitMQ 实现任务编排与状态管理，使用 Python Worker 调用多模态模型完成页面结构识别与代码生成，前端基于 Vue3 + Vite 实现生成工作台、预览面板和编辑器。项目通过 Postman、Playwright 等工具进行接口与页面渲染验证。

---

## 20. 给 Codex 的开发提示词

你后续可以把下面这段直接给 Codex：

```text
你现在是本项目的项目经理 + 工程师。

项目名称：截图 / Figma 到响应式 Vue 页面生成器。

请先阅读 PRD，并按以下原则工作：

1. 不要直接开始写代码，先输出开发计划。
2. 第一版只做 MVP，不做完整低代码拖拽编辑器。
3. 长期技术栈方向为：
   - 前端：Vue3 + Vite
   - 后端：Spring Boot + MyBatis-Plus
   - 数据库：MySQL
   - 缓存：Redis（后续可选）
   - 队列：RabbitMQ（后续可选）
   - AI Worker：Python
4. 当前 MVP 第一版以 docs/mvp-scope.md 为准：
   上传截图 → 创建任务 → 查看任务状态 → 查看 mock 生成结果。
5. 优先实现截图上传和任务流，不要一开始就做复杂 Figma 集成、真实模型接入、Redis / RabbitMQ 或导出 ZIP。
6. 每完成一个模块，都要给出：
   - 修改了哪些文件
   - 如何运行
   - 如何测试
   - 还有哪些风险

请先为我生成第一阶段的开发计划和项目目录结构。
```

---

## 21. 最终结论

这个项目第一版的正确定位是：

> 不是做一个“完美替代前端开发者”的工具，而是做一个“帮开发者快速生成页面初稿”的 AI 辅助开发工具。

你的技术栈完全适合做这个项目，不需要推翻重来。

最推荐的 MVP 路线是：

```text
先做截图上传
再做异步任务
再做 AI 结构分析
再做 Vue 页面生成
再做在线预览
最后做简单编辑和导出
```

不要一开始就做完整拖拽编辑器，也不要一开始追求“截图 100% 还原”。第一版只要能稳定生成 5 到 10 个中等复杂度页面，并且代码能运行、能预览、能导出，这个项目就已经非常适合作为你的 Codex Vibe Coding 实战项目。
