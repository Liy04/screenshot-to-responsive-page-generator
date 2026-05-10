<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { createImagePageJob } from '../api/imageLayoutApi'
import CodeBlock from '../components/CodeBlock.vue'
import GeneratedPagePreview from '../components/generated/GeneratedPagePreview.vue'
import ImageUploader from '../components/ImageUploader.vue'
import StatusTag from '../components/StatusTag.vue'
import JsonPanel from '../components/layout/JsonPanel.vue'

const TEMPLATE_OPTIONS = [
  { label: 'landing-basic', value: 'landing-basic' },
  { label: 'card-list', value: 'card-list' },
  { label: 'invalid-layout', value: 'invalid-layout' },
]

const selectedFile = ref(null)
const templateKey = ref(TEMPLATE_OPTIONS[0].value)
const result = ref(null)
const errorMessage = ref('')
const isLoading = ref(false)
const hasSubmitted = ref(false)

const pageState = computed(() => {
  if (isLoading.value) {
    return 'loading'
  }

  if (errorMessage.value) {
    return 'error'
  }

  if (!result.value) {
    return hasSubmitted.value ? 'empty' : 'empty'
  }

  if (
    result.value.status === 'FAILED'
    || result.value.generatedPageArtifact?.status === 'FAILED'
    || (
      result.value.status === 'SUCCESS'
      && !result.value.generatedPageArtifact
    )
  ) {
    return 'failed'
  }

  if (
    result.value.status === 'SUCCESS'
    && result.value.generatedPageArtifact?.status === 'SUCCESS'
  ) {
    return 'success'
  }

  return 'empty'
})

const layoutArtifact = computed(() => result.value?.layoutArtifact || null)
const generatedPageArtifact = computed(() => result.value?.generatedPageArtifact || null)
const validationErrors = computed(() => result.value?.errors || [])
const validationWarnings = computed(() => result.value?.warnings || [])
const generatedPageStatus = computed(() => generatedPageArtifact.value?.status || '')

function handleFileChange(file) {
  selectedFile.value = file
  errorMessage.value = ''
}

function handleFileError(message) {
  selectedFile.value = null
  errorMessage.value = message
}

async function handleSubmit() {
  if (!selectedFile.value) {
    errorMessage.value = '请先选择一张本地图片'
    hasSubmitted.value = true
    result.value = null
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  result.value = null
  hasSubmitted.value = true

  try {
    result.value = await createImagePageJob({
      imageName: selectedFile.value.name,
      templateKey: templateKey.value,
    })
  } catch (error) {
    errorMessage.value = error.message || '创建 image-page mock job 失败'
  } finally {
    isLoading.value = false
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
      <p class="eyebrow">Week 08 Day 4</p>
      <h1 id="image-layout-title">Image to Page Mock</h1>
      <p class="summary">
        选择本地图片后，只把 <code>imageName</code> 和 <code>templateKey</code>
        发给后端，用于演示 image-page mock 闭环；真实图片不会上传。
      </p>
    </section>

    <section class="image-layout-workbench">
      <ImageUploader :disabled="isLoading" @change="handleFileChange" @error="handleFileError" />

      <form class="detail-card image-layout-form" @submit.prevent="handleSubmit">
        <div class="section-title-row">
          <h2>创建 Mock Job</h2>
          <StatusTag :status="pageState === 'failed' ? 'failed' : result?.status || 'pending'" />
        </div>

        <label class="image-layout-label" for="template-key-select">templateKey</label>
        <select
          id="template-key-select"
          v-model="templateKey"
          class="image-layout-select"
          :disabled="isLoading"
        >
          <option
            v-for="option in TEMPLATE_OPTIONS"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>

        <dl class="task-meta image-layout-meta">
          <div>
            <dt>本地图片</dt>
            <dd>{{ selectedFile?.name || '未选择' }}</dd>
          </div>
          <div>
            <dt>提交字段</dt>
            <dd>imageName / templateKey</dd>
          </div>
        </dl>

        <div class="form-actions">
          <button class="primary-button" type="submit" :disabled="isLoading">
            {{ isLoading ? '创建中...' : '创建 Mock Job' }}
          </button>
        </div>
      </form>
    </section>

    <section v-if="pageState === 'loading'" class="detail-card loading-card" aria-live="polite">
      正在创建 image-page mock job...
    </section>

    <section
      v-else-if="pageState === 'error'"
      class="detail-card error-state"
      role="alert"
    >
      <h2>请求失败</h2>
      <p>{{ errorMessage }}</p>
    </section>

    <section v-else-if="pageState === 'empty'" class="detail-card empty-state">
      <h2>{{ hasSubmitted ? '暂无结果' : '等待创建' }}</h2>
      <p>
        {{ hasSubmitted ? '请检查输入后重新发起 mock job。' : '先选择本地图片，再选择 templateKey。' }}
      </p>
    </section>

    <template v-else>
      <section class="detail-card" aria-labelledby="image-layout-result-title">
        <div class="section-title-row">
          <h2 id="image-layout-result-title">Mock Job 结果</h2>
          <StatusTag :status="result.status" />
        </div>

        <dl class="task-meta">
          <div>
            <dt>jobId</dt>
            <dd>{{ result.jobId || '-' }}</dd>
          </div>
          <div>
            <dt>status</dt>
            <dd>{{ result.status || '-' }}</dd>
          </div>
          <div>
            <dt>sourceType</dt>
            <dd>{{ result.sourceType || '-' }}</dd>
          </div>
          <div>
            <dt>imageName</dt>
            <dd>{{ result.imageName || '-' }}</dd>
          </div>
          <div>
            <dt>templateKey</dt>
            <dd>{{ result.templateKey || '-' }}</dd>
          </div>
          <div>
            <dt>layoutArtifact.status</dt>
            <dd>{{ layoutArtifact?.status || '-' }}</dd>
          </div>
          <div>
            <dt>generatedPageArtifact.status</dt>
            <dd>{{ generatedPageStatus || '-' }}</dd>
          </div>
        </dl>
      </section>

      <section class="generated-validation-grid" aria-label="错误与警告">
        <CodeBlock
          title="errors"
          :code="validationErrors.length ? JSON.stringify(validationErrors, null, 2) : ''"
        />
        <CodeBlock
          title="warnings"
          :code="validationWarnings.length ? JSON.stringify(validationWarnings, null, 2) : ''"
        />
        <CodeBlock
          title="layoutArtifact.status"
          :code="layoutArtifact?.status || ''"
        />
      </section>

      <JsonPanel title="layoutArtifact.layoutJson" :value="layoutArtifact?.layoutJson" />

      <section
        class="detail-card generated-page-section"
        aria-labelledby="generated-page-artifact-title"
      >
        <div class="section-title-row">
          <h2 id="generated-page-artifact-title">generatedPageArtifact</h2>
          <StatusTag :status="generatedPageStatus || 'unknown'" />
        </div>

        <p v-if="pageState === 'failed'" class="generated-page-note">
          当前结果为 FAILED 或缺少 generatedPageArtifact，不展示 iframe 预览。
        </p>
        <p
          v-else-if="!generatedPageArtifact"
          class="generated-page-note"
        >
          当前结果暂无 generatedPageArtifact。
        </p>

        <GeneratedPagePreview
          v-if="pageState === 'success' && generatedPageArtifact"
          :html-code="generatedPageArtifact.htmlCode"
          :css-code="generatedPageArtifact.cssCode"
        />

        <section class="result-grid" aria-label="generated-page artifact 代码展示">
          <CodeBlock
            title="generatedPageArtifact.htmlCode"
            :code="generatedPageArtifact?.htmlCode || ''"
          />
          <CodeBlock
            title="generatedPageArtifact.cssCode"
            :code="generatedPageArtifact?.cssCode || ''"
          />
          <CodeBlock
            title="generatedPageArtifact.vueCode"
            :code="generatedPageArtifact?.vueCode || ''"
          />
        </section>
      </section>
    </template>
  </main>
</template>
