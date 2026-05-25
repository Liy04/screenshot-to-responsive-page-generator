<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { generateImagePage, uploadImagePageSource } from '../api/imageLayoutApi'
import CodeBlock from '../components/CodeBlock.vue'
import GeneratedPagePreview from '../components/generated/GeneratedPagePreview.vue'
import ImageUploader from '../components/ImageUploader.vue'
import StatusTag from '../components/StatusTag.vue'
import JsonPanel from '../components/layout/JsonPanel.vue'

const selectedFile = ref(null)
const uploadedSource = ref(null)
const generateResult = ref(null)
const uploadStage = ref('idle')
const generateStage = ref('idle')
const uploadErrorMessage = ref('')
const generateErrorMessage = ref('')
const copyMessage = ref('')
const copyMessageType = ref('')
const downloadMessage = ref('')
const downloadMessageType = ref('')

function normalizeItems(value) {
  if (Array.isArray(value)) {
    return value
  }

  if (value === undefined || value === null || value === '') {
    return []
  }

  return [value]
}

function isTimeoutMessage(message) {
  if (!message) {
    return false
  }

  return /timeout|timed out|超时/i.test(message)
}

const layoutJson = computed(() => generateResult.value?.layoutJson || null)
const previewHtml = computed(() => generateResult.value?.previewHtml || '')
const copyHtmlCode = computed(() => extractHtmlWithoutStyle(previewHtml.value))
const copyCssCode = computed(() => extractCssFromHtml(previewHtml.value))
const copyFullHtmlDocument = computed(() => {
  const html = previewHtml.value.trim()

  if (!html) {
    return ''
  }

  if (/<!doctype html|<html[\s>]/i.test(html)) {
    return html
  }

  return `<!doctype html>\n<html lang="zh-CN">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <title>Generated Page</title>\n</head>\n<body>\n${html}\n</body>\n</html>`
})
const canCopyHtml = computed(() => !!copyHtmlCode.value)
const canCopyCss = computed(() => !!copyCssCode.value)
const canCopyFullHtml = computed(() => !!copyFullHtmlDocument.value)
const canDownloadFullHtml = computed(() => !!copyFullHtmlDocument.value)
const topLevelErrors = computed(() => normalizeItems(generateResult.value?.errors))
const topLevelWarnings = computed(() => normalizeItems(generateResult.value?.warnings))
const validationErrors = computed(() => normalizeItems(generateResult.value?.validation?.errors))
const validationWarnings = computed(() => normalizeItems(generateResult.value?.validation?.warnings))
const artifactInfo = computed(() => generateResult.value?.artifact || null)
const promptVersion = computed(() => generateResult.value?.promptVersion || '')
const fallbackReason = computed(() => generateResult.value?.fallbackReason || '')
const displayModel = computed(() => {
  const value = generateResult.value?.model
  return value === undefined || value === null || value === '' ? '-' : String(value)
})
const displayDurationMs = computed(() => {
  const value = generateResult.value?.durationMs
  return value === undefined || value === null || value === '' ? '-' : `${value} ms`
})
const sourcePreviewUrl = computed(() => uploadedSource.value?.sourceUrl || '')
const canUpload = computed(() => {
  return !!selectedFile.value && uploadStage.value !== 'uploading' && generateStage.value !== 'generating'
})
const canGenerate = computed(() => {
  return !!uploadedSource.value?.jobId && generateStage.value !== 'generating'
})
const showPreviewIframe = computed(() => {
  return generateResult.value?.status === 'SUCCESS' && generateStage.value !== 'timeout' && !!previewHtml.value
})
const displaySourceType = computed(() => {
  return generateResult.value?.sourceType || uploadedSource.value?.sourceType || ''
})
const displayAiUsed = computed(() => {
  const value = generateResult.value?.aiUsed
  return value === undefined || value === null ? '-' : String(value)
})
const artifactReused = computed(() => {
  const value = artifactInfo.value?.reused
  return value === undefined || value === null ? '-' : String(value)
})
const resultState = computed(() => {
  if (generateStage.value === 'timeout') {
    return 'timeout'
  }

  if (generateResult.value?.status === 'FAILED' || generateStage.value === 'failed') {
    return 'failed'
  }

  if (generateResult.value?.fallbackUsed === true) {
    return 'fallback'
  }

  if (generateResult.value?.sourceType === 'REAL_AI' && generateResult.value?.fallbackUsed === false) {
    return 'real-ai'
  }

  if (generateResult.value?.status === 'SUCCESS') {
    return 'success'
  }

  return ''
})
const resultHeadline = computed(() => {
  const textMap = {
    'real-ai': 'REAL_AI 成功：可交付',
    fallback: 'FALLBACK：保底结果可预览',
    failed: 'FAILED：暂无可交付结果',
    timeout: 'TIMEOUT：生成超时',
    success: 'SUCCESS：可查看结果',
  }

  return textMap[resultState.value] || '生成结果'
})
const resultDescription = computed(() => {
  if (resultState.value === 'real-ai') {
    return '当前结果由真实 AI 直接生成，未触发 fallback。请先检查预览质量，再复制 HTML / CSS 或下载完整 HTML。'
  }

  if (resultState.value === 'fallback') {
    return '当前结果来自 fallback 保底规则，仍可用于预览和交付检查，但不代表真实 AI 命中。'
  }

  if (resultState.value === 'timeout') {
    return '真实链路耗时过长，本次没有可交付结果。建议稍后重试，或换一张更简单、更清晰的截图。'
  }

  if (resultState.value === 'failed') {
    return '当前生成失败，暂时没有可预览或可下载的页面。请查看失败原因后重试或检查输入图片。'
  }

  return '当前结果已返回，可继续查看预览、Layout JSON 和 previewHtml。'
})
const resultNextActions = computed(() => {
  if (resultState.value === 'real-ai' || resultState.value === 'success') {
    return [
      '对比原图和生成预览，确认结构是否满足演示要求。',
      '使用下方按钮复制 HTML / CSS，或下载完整 HTML。',
      '如果结果不满意，可以重新上传或重新生成。',
    ]
  }

  if (resultState.value === 'fallback') {
    return [
      '先把它当作保底预览结果检查，不要当作真实 AI 命中结果。',
      '如预览可接受，仍可复制或下载；如质量不足，建议重新生成或检查输入图。',
      '展开调试详情查看 fallbackReason、warnings 和 errors。',
    ]
  }

  if (resultState.value === 'timeout') {
    return [
      '本次没有可复制或下载的交付结果。',
      '稍后重试，或换一张内容更少、更清晰的截图。',
      '如果持续超时，请检查后端 timeout、Python Worker 和模型服务状态。',
    ]
  }

  if (resultState.value === 'failed') {
    return [
      '本次没有可复制或下载的交付结果。',
      '查看 errors / validation.errors 定位失败原因。',
      '修正输入图片或稍后重试。',
    ]
  }

  return []
})

function extractCssFromHtml(html) {
  if (!html) {
    return ''
  }

  const styleBlocks = []
  const styleRegex = /<style\b[^>]*>([\s\S]*?)<\/style>/gi
  let match = styleRegex.exec(html)

  while (match) {
    styleBlocks.push(match[1].trim())
    match = styleRegex.exec(html)
  }

  return styleBlocks.filter(Boolean).join('\n\n')
}

function extractHtmlWithoutStyle(html) {
  if (!html) {
    return ''
  }

  return html
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '')
    .trim()
}

async function copyText(label, text) {
  copyMessage.value = ''
  copyMessageType.value = ''

  if (!text) {
    copyMessage.value = `${label} 暂无可复制内容`
    copyMessageType.value = 'error'
    return
  }

  try {
    await navigator.clipboard.writeText(text)
    copyMessage.value = `${label} 已复制`
    copyMessageType.value = 'success'
  } catch (error) {
    copyMessage.value = `${label} 复制失败，请检查浏览器剪贴板权限`
    copyMessageType.value = 'error'
  }
}

function buildDownloadFileName() {
  const jobId = uploadedSource.value?.jobId || 'generated-page'
  const safeJobId = String(jobId).replace(/[^a-zA-Z0-9_-]/g, '-')
  return `${safeJobId || 'generated-page'}.html`
}

function downloadTextFile(label, text, fileName) {
  downloadMessage.value = ''
  downloadMessageType.value = ''

  if (!text) {
    downloadMessage.value = `${label} 暂无可下载内容`
    downloadMessageType.value = 'error'
    return
  }

  try {
    const blob = new Blob([text], { type: 'text/html;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = fileName
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
    downloadMessage.value = `${label} 已开始下载`
    downloadMessageType.value = 'success'
  } catch (error) {
    downloadMessage.value = `${label} 下载失败，请稍后重试`
    downloadMessageType.value = 'error'
  }
}

function handleFileChange(file) {
  selectedFile.value = file
  uploadedSource.value = null
  generateResult.value = null
  uploadStage.value = 'idle'
  generateStage.value = 'idle'
  uploadErrorMessage.value = ''
  generateErrorMessage.value = ''
  copyMessage.value = ''
  copyMessageType.value = ''
  downloadMessage.value = ''
  downloadMessageType.value = ''
}

function handleFileError(message) {
  selectedFile.value = null
  uploadedSource.value = null
  generateResult.value = null
  uploadStage.value = 'upload-error'
  generateStage.value = 'idle'
  uploadErrorMessage.value = message
  generateErrorMessage.value = ''
  copyMessage.value = ''
  copyMessageType.value = ''
  downloadMessage.value = ''
  downloadMessageType.value = ''
}

async function handleUpload() {
  if (!selectedFile.value) {
    uploadStage.value = 'upload-error'
    uploadErrorMessage.value = '请先选择一张本地图片'
    return
  }

  uploadStage.value = 'uploading'
  uploadErrorMessage.value = ''
  generateErrorMessage.value = ''
  copyMessage.value = ''
  copyMessageType.value = ''
  downloadMessage.value = ''
  downloadMessageType.value = ''
  uploadedSource.value = null
  generateResult.value = null
  generateStage.value = 'idle'

  try {
    uploadedSource.value = await uploadImagePageSource(selectedFile.value)
    uploadStage.value = 'uploaded'
  } catch (error) {
    uploadStage.value = 'upload-error'
    uploadErrorMessage.value = error.message || '上传图片失败'
  }
}

async function handleGenerate() {
  const jobId = uploadedSource.value?.jobId

  if (!jobId) {
    generateStage.value = 'error'
    generateErrorMessage.value = '请先上传图片，再开始生成'
    return
  }

  generateStage.value = 'generating'
  generateErrorMessage.value = ''
  generateResult.value = null
  copyMessage.value = ''
  copyMessageType.value = ''
  downloadMessage.value = ''
  downloadMessageType.value = ''

  try {
    const result = await generateImagePage(jobId)
    generateResult.value = result
    generateStage.value = result?.status === 'SUCCESS' ? 'success' : 'failed'
  } catch (error) {
    const message = error.message || '生成失败'
    generateErrorMessage.value = message
    generateStage.value = isTimeoutMessage(message) ? 'timeout' : 'error'
  }
}
</script>

<template>
  <main class="page-shell image-layout-page">
    <nav class="top-nav" aria-label="页面导航">
      <RouterLink to="/">返回工作台</RouterLink>
      <RouterLink to="/layout-json-viewer">查看 Layout JSON</RouterLink>
    </nav>

    <section class="page-heading" aria-labelledby="image-layout-title">
      <p class="eyebrow">Week 10 Day 05</p>
      <h1 id="image-layout-title">Image to Page 真实链路</h1>
      <p class="summary">
        选择单张真实图片后，先上传到后端，再触发真实生成链路，展示原图、Layout
        JSON、状态元信息和 <code>previewHtml</code> iframe 预览。
      </p>
    </section>

    <section class="image-layout-workbench">
      <ImageUploader
        :disabled="uploadStage === 'uploading' || generateStage === 'generating'"
        @change="handleFileChange"
        @error="handleFileError"
      />

      <form class="detail-card image-layout-form" @submit.prevent="handleUpload">
        <div class="section-title-row">
          <h2>上传与生成</h2>
          <StatusTag
            :status="
              generateStage === 'success'
                ? 'success'
                : generateStage === 'failed' || generateStage === 'error' || generateStage === 'timeout'
                  ? 'failed'
                  : uploadStage === 'uploaded'
                    ? 'running'
                    : uploadStage === 'uploading'
                      ? 'running'
                      : 'pending'
            "
          />
        </div>

        <dl class="task-meta image-layout-meta">
          <div>
            <dt>本地图片</dt>
            <dd>{{ selectedFile?.name || '未选择' }}</dd>
          </div>
          <div>
            <dt>上传阶段</dt>
            <dd>{{ uploadStage }}</dd>
          </div>
          <div>
            <dt>生成阶段</dt>
            <dd>{{ generateStage }}</dd>
          </div>
          <div>
            <dt>真实链路</dt>
            <dd>upload -> generate -> previewHtml</dd>
          </div>
        </dl>

        <p v-if="uploadErrorMessage" class="error-message">{{ uploadErrorMessage }}</p>
        <p
          v-if="generateErrorMessage && (generateStage === 'error' || generateStage === 'timeout')"
          class="error-message"
        >
          {{ generateErrorMessage }}
        </p>

        <div class="form-actions">
          <button class="primary-button" type="submit" :disabled="!canUpload">
            {{ uploadStage === 'uploading' ? '上传中...' : '上传图片' }}
          </button>
          <button
            class="primary-button secondary-button"
            type="button"
            :disabled="!canGenerate"
            @click="handleGenerate"
          >
            {{ generateStage === 'generating' ? '生成中...' : '开始生成' }}
          </button>
        </div>
      </form>
    </section>

    <section
      v-if="uploadStage === 'uploading'"
      class="detail-card loading-card"
      aria-live="polite"
    >
      正在上传真实图片...
    </section>

    <section
      v-else-if="uploadStage === 'upload-error' && !uploadedSource"
      class="detail-card error-state"
      role="alert"
    >
      <h2>上传失败</h2>
      <p>{{ uploadErrorMessage }}</p>
    </section>

    <section v-else-if="!uploadedSource" class="detail-card empty-state">
      <h2>等待上传</h2>
      <p>
        先选择一张真实图片并上传，上传成功后再触发生成。
      </p>
    </section>

    <template v-else-if="uploadedSource">
      <section class="detail-card" aria-labelledby="source-upload-title">
        <div class="section-title-row">
          <h2 id="source-upload-title">原图信息</h2>
          <StatusTag :status="uploadStage === 'uploaded' ? 'success' : 'running'" />
        </div>

        <dl class="task-meta">
          <div>
            <dt>jobId</dt>
            <dd>{{ uploadedSource.jobId || '-' }}</dd>
          </div>
          <div>
            <dt>fileName</dt>
            <dd>{{ uploadedSource.fileName || selectedFile?.name || '-' }}</dd>
          </div>
          <div>
            <dt>sourceUrl</dt>
            <dd>
              <a
                v-if="uploadedSource.sourceUrl"
                :href="uploadedSource.sourceUrl"
                target="_blank"
                rel="noreferrer"
              >
                {{ uploadedSource.sourceUrl }}
              </a>
              <span v-else>-</span>
            </dd>
          </div>
          <div>
            <dt>本地文件名</dt>
            <dd>{{ selectedFile?.name || '-' }}</dd>
          </div>
        </dl>

        <div v-if="sourcePreviewUrl" class="source-image-preview">
          <img :src="sourcePreviewUrl" alt="上传后的原图" />
        </div>
      </section>

      <section
        v-if="generateStage === 'generating'"
        class="detail-card loading-card"
        aria-live="polite"
      >
        正在调用真实生成链路...
      </section>

      <section
        v-else-if="generateStage === 'error' || generateStage === 'timeout'"
        class="detail-card error-state"
        role="alert"
      >
        <h2>{{ generateStage === 'timeout' ? 'TIMEOUT：生成超时' : '生成失败' }}</h2>
        <p>{{ generateErrorMessage }}</p>
        <ul v-if="generateStage === 'timeout'" class="next-action-list" aria-label="超时后下一步动作">
          <li>稍后重试，或换一张内容更少、更清晰的截图。</li>
          <li>如果持续超时，请检查后端 timeout、Python Worker 和模型服务状态。</li>
        </ul>
      </section>

      <section
        v-else-if="generateResult"
        class="detail-card mvp-result-card"
        aria-labelledby="generate-result-title"
      >
        <div class="section-title-row">
          <h2 id="generate-result-title">生成状态</h2>
          <StatusTag :status="resultState || generateResult.status || 'unknown'" />
        </div>

        <div class="result-summary-copy">
          <p class="result-summary-title">{{ resultHeadline }}</p>
          <p class="generated-page-note">{{ resultDescription }}</p>
          <div v-if="resultNextActions.length" class="next-action-panel">
            <p class="next-action-title">下一步</p>
            <ul class="next-action-list" aria-label="下一步动作">
              <li v-for="item in resultNextActions" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>

        <dl class="task-meta">
          <div>
            <dt>status</dt>
            <dd>{{ generateResult.status || '-' }}</dd>
          </div>
          <div>
            <dt>mode</dt>
            <dd>{{ generateResult.mode || '-' }}</dd>
          </div>
          <div>
            <dt>fallbackUsed</dt>
            <dd>{{ generateResult.fallbackUsed === undefined ? '-' : String(generateResult.fallbackUsed) }}</dd>
          </div>
          <div>
            <dt>sourceType</dt>
            <dd>{{ displaySourceType || '-' }}</dd>
          </div>
          <div>
            <dt>aiUsed</dt>
            <dd>{{ displayAiUsed }}</dd>
          </div>
          <div>
            <dt>promptVersion</dt>
            <dd>{{ promptVersion || '-' }}</dd>
          </div>
          <div>
            <dt>model</dt>
            <dd>{{ displayModel }}</dd>
          </div>
          <div>
            <dt>durationMs</dt>
            <dd>{{ displayDurationMs }}</dd>
          </div>
          <div>
            <dt>fallbackReason</dt>
            <dd>{{ fallbackReason || '-' }}</dd>
          </div>
        </dl>
      </section>

      <section
        v-if="generateResult"
        class="detail-card generated-page-section image-compare-section"
        aria-labelledby="preview-html-title"
      >
        <div class="section-title-row">
          <h2 id="preview-html-title">原图 / 生成预览</h2>
          <StatusTag :status="resultState || generateResult.status || 'unknown'" />
        </div>

        <p
          v-if="generateStage === 'timeout'"
          class="generated-page-note"
        >
          当前请求已超时，暂无可预览内容。
        </p>
        <p
          v-else-if="generateStage === 'failed' || generateResult.status === 'FAILED'"
          class="generated-page-note"
        >
          当前结果为 FAILED，不展示 iframe 预览。
        </p>
        <p
          v-else-if="!previewHtml"
          class="generated-page-note"
        >
          当前结果暂无可预览的 previewHtml。
        </p>

        <div
          class="image-compare-grid"
          aria-label="原图与生成结果对比"
        >
          <section class="compare-pane" aria-labelledby="source-compare-title">
            <div class="compare-pane-header">
              <h3 id="source-compare-title">上传原图</h3>
              <span>source</span>
            </div>
            <div class="compare-image-frame">
              <img :src="sourcePreviewUrl" alt="用于生成的上传原图" />
            </div>
          </section>

          <section class="compare-pane" aria-labelledby="generated-compare-title">
            <div class="compare-pane-header">
              <h3 id="generated-compare-title">生成预览</h3>
              <span>{{ showPreviewIframe ? 'sandbox iframe' : '暂无 iframe' }}</span>
            </div>
            <GeneratedPagePreview
              v-if="showPreviewIframe"
              :srcdoc-html="previewHtml"
            />
            <div v-else class="preview-empty-state">
              生成成功且存在 previewHtml 后，这里会展示安全 iframe 预览。
            </div>
          </section>
        </div>
      </section>

      <section
        v-if="generateResult"
        class="detail-card delivery-actions-card"
        aria-labelledby="delivery-actions-title"
      >
        <div class="section-title-row">
          <h2 id="delivery-actions-title">交付操作</h2>
          <StatusTag status="pending" />
        </div>

        <p class="generated-page-note">
          可复制和下载的内容来自 Worker 静态编译后的 previewHtml。当前下载为单个完整 HTML 文件。
        </p>

        <p
          v-if="copyMessage"
          class="copy-feedback"
          :class="copyMessageType === 'error' ? 'copy-feedback-error' : 'copy-feedback-success'"
          aria-live="polite"
        >
          {{ copyMessage }}
        </p>
        <p
          v-if="downloadMessage"
          class="copy-feedback"
          :class="downloadMessageType === 'error' ? 'copy-feedback-error' : 'copy-feedback-success'"
          aria-live="polite"
        >
          {{ downloadMessage }}
        </p>

        <div class="delivery-action-grid" aria-label="交付操作">
          <button
            class="primary-button secondary-button"
            type="button"
            :disabled="!canCopyHtml"
            @click="copyText('HTML', copyHtmlCode)"
          >
            复制 HTML
          </button>
          <button
            class="primary-button secondary-button"
            type="button"
            :disabled="!canCopyCss"
            @click="copyText('CSS', copyCssCode)"
          >
            复制 CSS
          </button>
          <button
            class="primary-button secondary-button"
            type="button"
            :disabled="!canCopyFullHtml"
            @click="copyText('完整 HTML', copyFullHtmlDocument)"
          >
            复制完整 HTML
          </button>
          <button
            class="primary-button secondary-button"
            type="button"
            :disabled="!canDownloadFullHtml"
            @click="downloadTextFile('完整 HTML', copyFullHtmlDocument, buildDownloadFileName())"
          >
            下载 HTML
          </button>
        </div>
      </section>

      <section
        v-if="generateResult"
        class="detail-card debug-details-card"
        aria-labelledby="debug-details-title"
      >
        <div class="section-title-row">
          <h2 id="debug-details-title">调试详情</h2>
          <StatusTag :status="artifactInfo ? 'success' : 'pending'" />
        </div>

        <dl class="task-meta">
          <div>
            <dt>artifact.reused</dt>
            <dd>{{ artifactReused }}</dd>
          </div>
          <div>
            <dt>layoutFileName</dt>
            <dd>{{ artifactInfo?.layoutFileName || '-' }}</dd>
          </div>
          <div>
            <dt>previewFileName</dt>
            <dd>{{ artifactInfo?.previewFileName || '-' }}</dd>
          </div>
          <div>
            <dt>metadataFileName</dt>
            <dd>{{ artifactInfo?.metadataFileName || '-' }}</dd>
          </div>
        </dl>

        <div
          class="generated-validation-grid"
          aria-label="错误、警告与调试信息"
        >
          <CodeBlock
            title="errors"
            :code="topLevelErrors.length ? JSON.stringify(topLevelErrors, null, 2) : ''"
          />
          <CodeBlock
            title="warnings"
            :code="topLevelWarnings.length ? JSON.stringify(topLevelWarnings, null, 2) : ''"
          />
          <CodeBlock
            title="validation.errors"
            :code="validationErrors.length ? JSON.stringify(validationErrors, null, 2) : ''"
          />
          <CodeBlock
            title="validation.warnings"
            :code="validationWarnings.length ? JSON.stringify(validationWarnings, null, 2) : ''"
          />
          <CodeBlock
            title="previewHtml"
            :code="previewHtml"
          />
        </div>

        <JsonPanel
          title="layoutJson"
          :value="layoutJson"
        />
      </section>
    </template>
  </main>
</template>
