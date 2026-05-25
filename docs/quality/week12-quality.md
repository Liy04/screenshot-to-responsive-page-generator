# Week 12 Output Quality Standard

## 1. 目标

Week 12 的质量目标不是 1:1 高保真，而是让三张简单 samples 的生成结果不再像裸 HTML，能够在结构、层级和基础视觉样式上更接近原图。

本文件同时作为质量标准和人工评分表，避免 Docs 过重。

## 2. 适用样例

- `samples/01-simple-card-page.png`
- `samples/02-simple-form-page.png`
- `samples/03-dashboard-cards-page.png`

## 3. 总分

每张 sample 总分 35 分。

通过线：

- `< 20`：不通过，需要继续 prompt / compiler / repair。
- `20 ~ 24`：基本可接受，但仍需继续质量增强。
- `24 ~ 27`：通过，具备简单截图还原雏形。
- `>= 28`：优秀，可以考虑进入更高级质量方向。

## 4. 评分维度

| 维度 | 分值 | 说明 |
|---|---:|---|
| 页面结构 | 7 | 是否识别 header / section / card / form / dashboard 等主要结构 |
| 内容层级 | 6 | 标题、正文、按钮、输入框、列表等层级是否接近原图 |
| 布局与间距 | 6 | flex/grid、padding、gap、margin 是否有基本表达 |
| 视觉样式 | 8 | 颜色、圆角、边框、阴影、字体大小、按钮样式是否可见 |
| 安全与稳定性 | 5 | 无 script、无 inline event、无 javascript URL，iframe sandbox 不放宽 |
| 可解释性 | 3 | promptVersion、sourceType、fallbackUsed、warnings/errors、artifact 信息清楚 |

## 5. 必填记录

每张 sample 的 smoke 记录必须包含：

- 评分人
- 评分日期
- 模型
- promptVersion
- sourceType
- fallbackUsed
- artifact.reused
- previewHtml 是否非空
- iframe 是否渲染
- 总分
- 主要缺陷

## 6. 安全规则

Week 12 不允许为了质量放宽安全边界。

禁止：

- 模型原始 HTML 直接作为最终页面代码。
- `<script>`
- inline event，例如 `onclick=`、`onerror=`、`onload=`
- `javascript:` URL
- CSS `url(`
- CSS `expression(`
- CSS `@import`
- `data:text/html`
- `position: fixed`
- `position: absolute`
- iframe `allow-scripts`

## 7. style key 白名单

Week 12 优先支持以下 style key：

- `backgroundColor`
- `color`
- `fontSize`
- `fontWeight`
- `textAlign`
- `padding`
- `margin`
- `gap`
- `borderRadius`
- `boxShadow`
- `border`
- `width`
- `height`
- `display`
- `flexDirection`
- `alignItems`
- `justifyContent`
- `objectFit`

未列入白名单的 style key 应进入 warnings，不能静默编译为 CSS。

## 8. style value 允许类型

颜色：

- `#fff`
- `#ffffff`
- `rgb(...)`
- `rgba(...)`
- `hsl(...)`
- `hsla(...)`
- 常见安全颜色名

尺寸：

- `px`
- `rem`
- `em`
- `%`
- `auto`
- `0`

布局：

- `flex`
- `grid`
- `block`
- `inline-block`
- `row`
- `column`
- `center`
- `space-between`
- `flex-start`
- `flex-end`
- `stretch`

## 9. Week 13 判断标准

- 如果平均分 `< 20`：Week 13 继续 prompt / compiler / repair。
- 如果平均分 `20 ~ 24`：Week 13 继续质量增强，谨慎探索视觉回归。
- 如果平均分 `>= 24`：Week 13 可以考虑 Layout JSON schema v0.2 或轻量视觉回归。
- 如果平均分 `>= 28`：可以开始 Figma 或持久化前置探索。
