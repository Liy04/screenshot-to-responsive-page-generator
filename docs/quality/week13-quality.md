# Week 13 Output Quality Standard

## 1. 目标

Week 13 的质量目标不是 1:1 高保真，而是让同一组简单 samples 的生成结果更稳定、更像原图，并且在顺序 smoke 中保持可复现。

本文件同时作为质量标准和人工评分表，避免 Docs 过重。

## 2. 适用样例

- `samples/01-simple-card-page.png`
- `samples/02-simple-form-page.png`
- `samples/03-dashboard-cards-page.png`

## 3. 总分

每张 sample 总分 35 分。

通过线：

- `< 20`：不通过，需要继续 prompt / mapper / compiler / repair。
- `20 ~ 24`：基本可接受，但仍需继续质量增强。
- `25 ~ 28`：通过，具备稳定的简单截图还原能力。
- `>= 29`：优秀，可以考虑更广的样例覆盖，但仍不自动进入重型系统。

## 4. 评分维度

| 维度 | 分值 | 说明 |
|---|---:|---|
| 视觉清单稳定性 | 8 | `texts / regions / components` 是否稳定、是否减少同图漂移 |
| Layout JSON 映射质量 | 8 | 页面、section、card、form、button、input、text 等映射是否准确 |
| preview 样式表达 | 8 | card / button / input / text 的视觉层次是否明显，是否比裸 HTML 更接近原图 |
| 顺序 smoke 可复现性 | 5 | 是否可以按固定顺序重复跑完，记录是否完整 |
| 安全与边界 | 6 | 无 script、无 inline event、无 javascript URL，iframe sandbox 不放宽 |

## 5. 必填记录

每张 sample 的 smoke 记录必须包含：

- 评分人
- 评分日期
- 运行顺序
- 模型
- `promptVersion`
- `sourceType`
- `fallbackUsed`
- `artifact.reused`
- `previewHtml` 是否非空
- iframe 是否渲染
- 总分
- 主要缺陷

## 6. 安全规则

Week 13 不允许为了质量放宽安全边界。

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

Week 13 优先支持以下 style key：

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

- 如果平均分 `< 20`：继续 prompt / mapper / compiler / repair。
- 如果平均分 `20 ~ 24`：继续质量增强，并把顺序 smoke 先跑稳。
- 如果平均分 `25 ~ 28`：可以认为 Week 13 达到稳定通过线。
- 如果平均分 `>= 29`：可以开始考虑更广的样例覆盖，但不自动进入 MySQL、Figma 或复杂编辑器。
