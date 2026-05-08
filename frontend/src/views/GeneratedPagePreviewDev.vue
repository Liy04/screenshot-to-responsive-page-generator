<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { getGeneratedPageArtifact } from '../api/devGeneratedPageArtifact'
import CodeBlock from '../components/CodeBlock.vue'
import GeneratedPageMeta from '../components/generated/GeneratedPageMeta.vue'
import GeneratedPagePreview from '../components/generated/GeneratedPagePreview.vue'

const props = defineProps({
  jobId: {
    type: String,
    required: true,
  },
})

const artifact = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const errorKind = ref('')

const previewState = computed(() => {
  if (isLoading.value) {
    return 'loading'
  }

  if (artifact.value?.status === 'SUCCESS') {
    return 'success'
  }

  if (artifact.value?.status === 'FAILED') {
    return 'failed'
  }

  if (errorKind.value === 'empty') {
    return 'empty'
  }

  if (errorMessage.value) {
    return 'error'
  }

  return 'empty'
})

const validationErrors = computed(() => artifact.value?.validation?.errors || [])

async function loadArtifact() {
  if (!props.jobId) {
    errorMessage.value = '缺少 jobId，无法查询 generated-page artifact'
    errorKind.value = 'error'
    return
  }

  artifact.value = null
  errorMessage.value = ''
  errorKind.value = ''
  isLoading.value = true

  try {
    artifact.value = await getGeneratedPageArtifact(props.jobId)
  } catch (error) {
    const message = error.message || 'generated-page artifact 查询失败'
    errorMessage.value = message
    errorKind.value = message.includes('不存在') ? 'empty' : 'error'
  } finally {
    isLoading.value = false
  }
}

watch(
  () => props.jobId,
  () => {
    loadArtifact()
  },
  { immediate: true },
)
</script>

<template>
  <main class="page-shell generated-dev-page">
    <nav class="top-nav" aria-label="页面导航">
      <RouterLink to="/">返回工作台</RouterLink>
      <RouterLink :to="`/generation/${jobId}`">查看任务详情</RouterLink>
    </nav>

    <section class="page-heading" aria-labelledby="generated-dev-title">
      <p class="eyebrow">Week 05 Dev Preview</p>
      <h1 id="generated-dev-title">generated-page 独立预览</h1>
      <p class="summary">
        当前页面只查询 generated-page artifact，不依赖旧 generation job 详情接口。
      </p>
    </section>

    <section class="detail-card" aria-labelledby="generated-dev-job-title">
      <h2 id="generated-dev-job-title">查询目标</h2>
      <dl class="task-meta">
        <div>
          <dt>jobId</dt>
          <dd>{{ jobId }}</dd>
        </div>
      </dl>
    </section>

    <section v-if="previewState === 'loading'" class="detail-card loading-card">
      正在加载 generated-page artifact...
    </section>

    <section
      v-else-if="previewState === 'empty'"
      class="detail-card empty-state"
      role="status"
    >
      <h2>暂无 generated-page artifact</h2>
      <p>{{ errorMessage || '当前 jobId 还没有可展示的静态编译产物。' }}</p>
    </section>

    <section
      v-else-if="previewState === 'error'"
      class="detail-card error-state"
      role="alert"
    >
      <h2>查询失败</h2>
      <p>{{ errorMessage }}</p>
    </section>

    <template v-else>
      <GeneratedPageMeta :artifact="artifact" />

      <section v-if="previewState === 'failed'" class="detail-card error-state">
        <h2>静态编译失败</h2>
        <p>artifact status=FAILED，不展示可视化预览。</p>
        <ul v-if="validationErrors.length" class="message-list">
          <li v-for="error in validationErrors" :key="JSON.stringify(error)">
            <strong>{{ error.code || 'ERROR' }}</strong>
            <span>{{ error.message || error }}</span>
          </li>
        </ul>
      </section>

      <GeneratedPagePreview
        v-if="previewState === 'success'"
        :html-code="artifact.htmlCode"
        :css-code="artifact.cssCode"
      />

      <section class="result-grid" aria-label="generated-page 代码展示">
        <CodeBlock title="htmlCode" :code="artifact.htmlCode" />
        <CodeBlock title="cssCode" :code="artifact.cssCode" />
        <CodeBlock title="vueCode" :code="artifact.vueCode" />
      </section>
    </template>
  </main>
</template>
