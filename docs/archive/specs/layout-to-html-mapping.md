# Layout JSON 到 HTML / CSS 映射规则

## 文件目的

本文档定义 Week 04 静态编译器 v0.1 的确定性映射规则。

这些规则只用于把已通过校验的 Layout JSON v0.1 编译为可预览的 `htmlCode + cssCode`，不代表真实 AI 生成能力。

## 节点映射

| Layout JSON 节点 | HTML 输出 | class | 说明 |
|---|---|---|---|
| `page` | `div` | `lg-page` | 页面根容器 |
| `section` | `section` | `lg-section` | 页面区块 |
| `container` | `div` | `lg-container` | 普通容器 |
| `text` | `h1` / `h2` / `p` / `span` | `lg-text` | 根据 role 选择标签 |
| `button` | `button` | `lg-button` | 按钮文本必须 escape |
| `image` | `img` | `lg-image` | `src` 必须是安全 URL 或本地相对路径 |
| `card` | `div` | `lg-card` | 卡片容器 |
| `list` | `ul` | `lg-list` | 列表容器 |
| `listItem` | `li` | `lg-list-item` | 列表项 |
| `form` | `form` | `lg-form` | 仅静态展示，不提交 |
| `input` | `input` | `lg-input` | 仅静态展示 |

## text 标签选择

Week 04 不做复杂语义推断，只按 `role` 选择：

| role | 标签 |
|---|---|
| `heading` | `h1` 或 `h2` |
| `paragraph` | `p` |
| 其它或缺失 | `span` |

如果 Layout JSON 已提供 `level`，可以将 `level=1` 映射为 `h1`，`level=2` 映射为 `h2`；其它情况默认 `p` 或 `span`。

## style subset

Week 04 只支持以下 style 字段：

- `backgroundColor`
- `color`
- `fontSize`
- `fontWeight`
- `borderRadius`
- `padding`
- `margin`
- `display`
- `flexDirection`
- `gap`
- `justifyContent`
- `alignItems`

处理规则：

- 已支持字段按确定性规则映射为 CSS。
- 缺失字段跳过。
- 未知 style 字段不报错，但必须写入 `warnings`。
- CSS 值必须做最小白名单或安全过滤。

## CSS 值安全过滤

建议 Week 04 使用保守规则：

- 颜色只允许 hex、rgb、rgba、常见安全颜色名。
- 长度只允许数字加 `px`、`rem`、`em`、`%`。
- `fontWeight` 只允许 `normal`、`bold`、`100` 到 `900`。
- `display` 只允许 `block`、`inline-block`、`flex`、`grid`、`none`。
- `flexDirection` 只允许 `row`、`row-reverse`、`column`、`column-reverse`。
- `justifyContent` 和 `alignItems` 只允许常见 flex 对齐值。
- CSS 值中禁止 `url(`、`expression(`、`javascript:`、`<`、`>`。
- 不安全值跳过，并写入 `warnings`。

## HTML 安全规则

- `text` content 必须 HTML escape。
- `button` content 必须 HTML escape。
- `input` 的 `placeholder` / `value` 必须 HTML escape。
- 禁止输出 `script` 标签。
- 禁止输出 `onclick`、`onload` 等内联事件。
- 禁止输出 `javascript:` URL。
- 禁止把未知字段直接拼进 HTML 属性。
- 未知节点类型不直接渲染为原始 HTML，记录到 `unsupportedNodes` 或 `warnings`。

## image src 规则

`image` 的 `src` 只允许：

- `http://` 或 `https://` URL。
- `/uploads/...` 本地上传资源路径。
- `./` 或 `../` 以外的安全相对路径。

禁止：

- `javascript:` URL。
- `data:` URL。
- 包含 `<` 或 `>` 的 URL。
- 包含内联事件的伪属性。

如果 image 缺少安全 `src`，可以跳过 `src`，并写入 warning。

## iframe 预览规则

前端预览必须使用：

```html
<iframe sandbox=""></iframe>
```

不得添加：

- `allow-scripts`
- `allow-same-origin`
- 其它会扩大预览权限的 sandbox 放行项

iframe 内容建议由前端拼接：

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* cssCode */
  </style>
</head>
<body>
  <!-- htmlCode -->
</body>
</html>
```

## 当前限制

- Week 04 不做真实截图解析。
- Week 04 不做 AI 生成。
- Week 04 不做 Vue 页面代码生成。
- Week 04 不要求 `vueCode` 可运行。
- Week 04 不做拖拽编辑器、在线编辑器或 ZIP 导出。
- Week 04 不做 Playwright 视觉回归。

## 后续扩展方向

- 扩展更多节点类型和 style 字段。
- 增加响应式断点映射。
- 生成可运行 Vue 单文件组件。
- 增加 ZIP 导出。
- 增加 Playwright 截图和视觉回归。
- 在产品负责人确认后引入数据库持久化。
