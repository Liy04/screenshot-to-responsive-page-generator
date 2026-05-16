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
const topLevelErrors = computed(() => normalizeItems(generateResult.value?.errors))
const topLevelWarnings = computed(() => normalizeItems(generateResult.value?.warnings))
const validationErrors = computed(() => normalizeItems(generateResult.value?.validation?.errors))
const validationWarnings = computed(() => normalizeItems(generateResult.value?.validation?.warnings))
const artifactInfo = computed(() => generateResult.value?.artifact || null)
const promptVersion = computed(() => generateResult.value?.promptVersion || '')
const fallbackReason = computed(() => generateResult.value?.fallbackReason || '')
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
    'real-ai': 'REAL_AI 成功',
    fallback: 'FALLBACK',
    failed: 'FAILED',
    timeout: 'TIMEOUT',
    success: 'SUCCESS',
  }

  return textMap[resultState.value] || '生成结果'
})
const resultDescription = computed(() => {
  if (resultState.value === 'real-ai') {
    return '当前结果由真实 AI 直接生成，未触发 fallback。'
  }

  if (resultState.value === 'fallback') {
    return '当前结果使用 fallback 口径返回，请结合 fallbackReason、warnings 和 errors 一起判断。'
  }

  if (resultState.value === 'timeout') {
    return '当前请求已超时，本次没有可预览内容。'
  }

  if (resultState.value === 'failed') {
    return '当前结果为 FAILED，请优先查看 errors、warnings 和 artifact 信息。'
  }

  return '当前结果已返回，可继续查看 layoutJson 和 previewHtml。'
})

function handleFileChange(file) {
  selectedFile.value = file
  uploadedSource.value = null
  generateResult.value = null
  uploadStage.value = 'idle'
  generateStage.value = 'idle'
  uploadErrorMessage.value = ''
  generateErrorMessage.value = ''
}

function handleFileError(message) {
  selectedFile.value = null
  uploadedSource.value = null
  generateResult.value = null
  uploadStage.value = 'upload-error'
  generateStage.value = 'idle'
  uploadErrorMessage.value = message
  generateErrorMessage.value = ''
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
        <h2>{{ generateStage === 'timeout' ? '生成超时' : '生成失败' }}</h2>
        <p>{{ generateErrorMessage }}</p>
      </section>

      <section
        v-else-if="generateResult"
        class="detail-card"
        aria-labelledby="generate-result-title"
      >
        <div class="section-title-row">
          <h2 id="generate-result-title">生成结果</h2>
          <StatusTag :status="resultState || generateResult.status || 'unknown'" />
        </div>

        <div class="result-summary-copy">
          <p class="result-summary-title">{{ resultHeadline }}</p>
          <p class="generated-page-note">{{ resultDescription }}</p>
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
            <dt>fallbackReason</dt>
            <dd>{{ fallbackReason || '-' }}</dd>
          </div>
        </dl>
      </section>

      <section
        v-if="generateResult"
        class="detail-card"
        aria-labelledby="artifact-info-title"
      >
        <div class="section-title-row">
          <h2 id="artifact-info-title">Artifact 信息</h2>
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
      </section>

      <section
        v-if="generateResult"
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
      </section>

      <JsonPanel
        v-if="generateResult"
        title="layoutJson"
        :value="layoutJson"
      />

      <section
        v-if="generateResult"
        class="detail-card generated-page-section"
        aria-labelledby="preview-html-title"
      >
        <div class="section-title-row">
          <h2 id="preview-html-title">iframe 预览</h2>
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

        <GeneratedPagePreview
          v-if="showPreviewIframe"
          :srcdoc-html="previewHtml"
        />
      </section>
    </template>
  </main>
</template>
