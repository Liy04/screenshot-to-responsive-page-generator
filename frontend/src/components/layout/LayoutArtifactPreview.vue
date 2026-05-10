<script setup>
import { computed } from 'vue'

const props = defineProps({
  layoutJson: {
    type: Object,
    default: null,
  },
})

const SAFE_STYLE_KEYS = {
  backgroundColor: 'background-color',
  color: 'color',
  fontSize: 'font-size',
  fontWeight: 'font-weight',
  borderRadius: 'border-radius',
  padding: 'padding',
  margin: 'margin',
  display: 'display',
  flexDirection: 'flex-direction',
  gap: 'gap',
  justifyContent: 'justify-content',
  alignItems: 'align-items',
  width: 'width',
  height: 'height',
  textAlign: 'text-align',
  objectFit: 'object-fit',
}

const FLEX_VALUES = new Set([
  'flex-start',
  'center',
  'flex-end',
  'space-between',
  'space-around',
  'space-evenly',
  'stretch',
])
const DISPLAY_VALUES = new Set(['block', 'inline-block', 'flex', 'grid', 'none'])
const FLEX_DIRECTION_VALUES = new Set([
  'row',
  'row-reverse',
  'column',
  'column-reverse',
])
const TEXT_ALIGN_VALUES = new Set(['left', 'center', 'right', 'justify'])
const OBJECT_FIT_VALUES = new Set(['contain', 'cover', 'fill', 'none', 'scale-down'])
const FONT_WEIGHT_VALUES = new Set([
  'normal',
  'bold',
  '100',
  '200',
  '300',
  '400',
  '500',
  '600',
  '700',
  '800',
  '900',
])

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function isSafeColor(value) {
  return /^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(value)
    || /^rgba?\([\d\s,.%]+\)$/.test(value)
    || /^[a-zA-Z]{3,20}$/.test(value)
}

function isSafeLength(value) {
  return /^-?\d+(\.\d+)?(px|rem|em|%)$/.test(value) || value === '0'
}

function isSafeStyleValue(key, value) {
  const normalizedValue = String(value ?? '').trim()
  if (!normalizedValue || /url\(|expression\(|javascript:|<|>/i.test(normalizedValue)) {
    return false
  }

  if (key === 'backgroundColor' || key === 'color') {
    return isSafeColor(normalizedValue)
  }

  if (
    key === 'fontSize'
    || key === 'borderRadius'
    || key === 'padding'
    || key === 'margin'
    || key === 'gap'
    || key === 'width'
    || key === 'height'
  ) {
    return isSafeLength(normalizedValue)
  }

  if (key === 'fontWeight') {
    return FONT_WEIGHT_VALUES.has(normalizedValue)
  }

  if (key === 'display') {
    return DISPLAY_VALUES.has(normalizedValue)
  }

  if (key === 'flexDirection') {
    return FLEX_DIRECTION_VALUES.has(normalizedValue)
  }

  if (key === 'justifyContent' || key === 'alignItems') {
    return FLEX_VALUES.has(normalizedValue)
  }

  if (key === 'textAlign') {
    return TEXT_ALIGN_VALUES.has(normalizedValue)
  }

  if (key === 'objectFit') {
    return OBJECT_FIT_VALUES.has(normalizedValue)
  }

  return false
}

function toInlineStyle(style) {
  if (!style || typeof style !== 'object') {
    return ''
  }

  return Object.entries(style)
    .filter(([key, value]) => SAFE_STYLE_KEYS[key] && isSafeStyleValue(key, value))
    .map(([key, value]) => `${SAFE_STYLE_KEYS[key]}:${String(value).trim()}`)
    .join(';')
}

function getNodeChildren(node) {
  return Array.isArray(node?.children) ? node.children : []
}

function getTextContent(node) {
  return escapeHtml(node?.content ?? node?.text ?? node?.label ?? node?.title ?? '')
}

function getTextTag(node) {
  if (node?.role === 'heading') {
    return node?.level === 2 ? 'h2' : 'h1'
  }

  if (node?.role === 'label' || node?.role === 'caption') {
    return 'span'
  }

  return 'p'
}

function isSafeImageSource(value) {
  const normalizedValue = String(value ?? '').trim()
  return /^(https?:\/\/|\/uploads\/)/.test(normalizedValue)
    && !/[<>]/.test(normalizedValue)
    && !normalizedValue.includes('../')
}

function renderChildren(node) {
  return getNodeChildren(node).map((child) => renderNode(child)).join('')
}

function renderNode(node) {
  if (!node || typeof node !== 'object') {
    return ''
  }

  const inlineStyle = toInlineStyle(node.style)
  const styleAttr = inlineStyle ? ` style="${escapeHtml(inlineStyle)}"` : ''

  switch (node.type) {
    case 'page':
      return `<div class="layout-preview-page"${styleAttr}>${renderChildren(node)}</div>`
    case 'section':
      return `<section class="layout-preview-section"${styleAttr}>${renderChildren(node)}</section>`
    case 'container':
      return `<div class="layout-preview-container"${styleAttr}>${renderChildren(node)}</div>`
    case 'card':
      return `<article class="layout-preview-card"${styleAttr}>${renderChildren(node)}</article>`
    case 'text': {
      const tagName = getTextTag(node)
      return `<${tagName} class="layout-preview-text"${styleAttr}>${getTextContent(node)}</${tagName}>`
    }
    case 'button':
      return `<button type="button" class="layout-preview-button"${styleAttr}>${getTextContent(node)}</button>`
    case 'image': {
      const src = node?.src
      if (isSafeImageSource(src)) {
        return `<img class="layout-preview-image" src="${escapeHtml(src)}" alt="${escapeHtml(node?.alt || 'preview image')}"${styleAttr} />`
      }

      return `<div class="layout-preview-image layout-preview-image-placeholder"${styleAttr}>Image</div>`
    }
    case 'list':
      return `<ul class="layout-preview-list"${styleAttr}>${renderChildren(node)}</ul>`
    case 'listItem':
      return `<li class="layout-preview-list-item"${styleAttr}>${renderChildren(node)}</li>`
    case 'form':
      return `<form class="layout-preview-form"${styleAttr}>${renderChildren(node)}</form>`
    case 'input':
      return `<input class="layout-preview-input" placeholder="${escapeHtml(node?.placeholder || '')}" value="${escapeHtml(node?.value || '')}"${styleAttr} />`
    default:
      return `<div class="layout-preview-unsupported"${styleAttr}>Unsupported: ${escapeHtml(node.type || 'unknown')}</div>`
  }
}

const previewSrcdoc = computed(() => {
  const rootNode = props.layoutJson?.layout
  const renderedNode = renderNode(rootNode)
  const bodyContent =
    renderedNode
    || '<div class="layout-preview-empty">Layout JSON 中暂无可预览节点</div>'

  return `<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      * { box-sizing: border-box; }
      body {
        margin: 0;
        padding: 24px;
        background: #f8fafc;
        color: #111827;
        font-family: Inter, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
      }
      .layout-preview-page,
      .layout-preview-section,
      .layout-preview-container,
      .layout-preview-card,
      .layout-preview-form,
      .layout-preview-list {
        display: grid;
        gap: 16px;
      }
      .layout-preview-page {
        min-height: 100%;
      }
      .layout-preview-section,
      .layout-preview-container,
      .layout-preview-card,
      .layout-preview-form {
        padding: 16px;
        border: 1px solid #dbe2ea;
        border-radius: 12px;
        background: #ffffff;
      }
      .layout-preview-text {
        margin: 0;
        line-height: 1.6;
      }
      .layout-preview-button {
        width: fit-content;
        min-height: 40px;
        border: 0;
        border-radius: 8px;
        padding: 10px 16px;
        background: #2563eb;
        color: #ffffff;
        font-weight: 700;
      }
      .layout-preview-image,
      .layout-preview-image-placeholder {
        display: block;
        width: 100%;
        min-height: 180px;
        border-radius: 10px;
        background: #e5e7eb;
        object-fit: cover;
      }
      .layout-preview-image-placeholder {
        display: grid;
        place-items: center;
        color: #6b7280;
        font-weight: 600;
      }
      .layout-preview-list {
        margin: 0;
        padding-left: 20px;
      }
      .layout-preview-list-item {
        line-height: 1.6;
      }
      .layout-preview-input {
        min-height: 40px;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 10px 12px;
      }
      .layout-preview-unsupported,
      .layout-preview-empty {
        padding: 16px;
        border: 1px dashed #cbd5e1;
        border-radius: 10px;
        color: #475569;
        background: #ffffff;
      }
    </style>
  </head>
  <body>
    ${bodyContent}
  </body>
</html>`
})
</script>

<template>
  <section class="generated-preview" aria-labelledby="layout-preview-title">
    <h2 id="layout-preview-title">Layout Mock 预览</h2>
    <iframe
      title="Layout JSON 安全预览"
      sandbox=""
      :srcdoc="previewSrcdoc"
    ></iframe>
  </section>
</template>
