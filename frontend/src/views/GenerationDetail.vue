<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { getGeneratedPageArtifact } from '../api/devGeneratedPageArtifact'
import { getGeneration, getGenerationResult } from '../api/generationApi'
import CodeBlock from '../components/CodeBlock.vue'
import GeneratedPageMeta from '../components/generated/GeneratedPageMeta.vue'
import GeneratedPagePreview from '../components/generated/GeneratedPagePreview.vue'
import StatusTag from '../components/StatusTag.vue'

const props = defineProps({
  jobId: {
    type: String,
    required: true,
  },
})

const generation = ref(null)
const result = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const generatedArtifact = ref(null)
const generatedIsLoading = ref(false)
const generatedErrorMessage = ref('')

const layoutJsonText = computed(() => {
  if (!result.value?.layoutJson) {
    return ''
  }

  return JSON.stringify(result.value.layoutJson, null, 2)
})

const generatedStatus = computed(() => generatedArtifact.value?.status || '')
const isGeneratedFailed = computed(() => generatedStatus.value === 'FAILED')
const generatedErrors = computed(() => {
  return generatedArtifact.value?.validation?.errors || []
})

async function loadGenerationDetail() {
  if (!props.jobId) {
    errorMessage.value = '任务 ID 缺失，请返回创建页重新创建任务'
    return
  }

  generation.value = null
  result.value = null
  errorMessage.value = ''
  isLoading.value = true

  try {
    const [generationData, resultData] = await Promise.all([
      getGeneration(props.jobId),
      getGenerationResult(props.jobId),
    ])

    generation.value = generationData
    result.value = resultData
  } catch (error) {
    errorMessage.value = error.message || '加载任务详情失败'
  } finally {
    isLoading.value = false
  }
}

async function loadGeneratedPageArtifact() {
  if (!props.jobId) {
    generatedErrorMessage.value = '任务 ID 缺失，无法查询 generated-page artifact'
    return
  }

  generatedArtifact.value = null
  generatedErrorMessage.value = ''
  generatedIsLoading.value = true

  try {
    generatedArtifact.value = await getGeneratedPageArtifact(props.jobId)
  } catch (error) {
    generatedErrorMessage.value =
      error.message || 'generated-page artifact 暂不可用'
  } finally {
    generatedIsLoading.value = false
  }
}

watch(
  () => props.jobId,
  () => {
    loadGenerationDetail()
    loadGeneratedPageArtifact()
  },
  { immediate: true },
)
</script>

<template>
  <main class="page-shell detail-page">
    <nav class="top-nav" aria-label="页面导航">
      <RouterLink to="/generation/create">返回创建任务</RouterLink>
    </nav>

    <section class="page-heading detail-heading" aria-labelledby="detail-title">
      <p class="eyebrow">任务详情</p>
      <h1 id="detail-title">任务 {{ jobId }}</h1>
      <p class="summary">
        查看当前任务状态、进度和 mock 生成结果。
      </p>
    </section>

    <section v-if="isLoading" class="detail-card loading-card" aria-live="polite">
      正在加载任务详情...
    </section>

    <section v-else-if="errorMessage" class="detail-card error-state" role="alert">
      <h2>加载失败</h2>
      <p>{{ errorMessage }}</p>
    </section>

    <template v-if="!isLoading && !errorMessage">
      <section class="detail-card" aria-labelledby="task-info-title">
        <div class="section-title-row">
          <h2 id="task-info-title">任务状态</h2>
          <StatusTag :status="generation?.status" />
        </div>

        <dl class="task-meta">
          <div>
            <dt>jobId</dt>
            <dd>{{ generation?.jobId || jobId }}</dd>
          </div>
          <div>
            <dt>assetId</dt>
            <dd>{{ generation?.assetId || '-' }}</dd>
          </div>
          <div>
            <dt>progress</dt>
            <dd>{{ generation?.progress ?? 0 }}%</dd>
          </div>
          <div>
            <dt>mode</dt>
            <dd>{{ generation?.mode || '-' }}</dd>
          </div>
          <div v-if="generation?.createdAt">
            <dt>createdAt</dt>
            <dd>{{ generation.createdAt }}</dd>
          </div>
        </dl>

        <div class="progress-track" aria-label="任务进度">
          <div
            class="progress-value"
            :style="{ width: `${generation?.progress ?? 0}%` }"
          ></div>
        </div>
      </section>

      <section class="result-grid" aria-label="mock 生成结果">
        <CodeBlock title="layoutJson" :code="layoutJsonText" />
        <CodeBlock title="vueCode" :code="result?.vueCode" />
        <CodeBlock title="cssCode" :code="result?.cssCode" />
      </section>
    </template>

    <section class="generated-page-section" aria-labelledby="generated-page-title">
      <section class="page-heading generated-page-heading">
        <p class="eyebrow">Week 04 安全预览</p>
        <h1 id="generated-page-title">generated-page artifact</h1>
        <p class="summary">
          展示静态编译产物，iframe 使用 sandbox="" 且不启用脚本权限。
        </p>
      </section>

      <section
        v-if="generatedIsLoading"
        class="detail-card loading-card"
        aria-live="polite"
      >
        正在加载 generated-page artifact...
      </section>

      <section
        v-else-if="generatedErrorMessage"
        class="detail-card empty-state"
        role="status"
      >
        <h2>generated-page artifact 暂不可用</h2>
        <p>{{ generatedErrorMessage }}</p>
      </section>

      <template v-else-if="generatedArtifact">
        <GeneratedPageMeta :artifact="generatedArtifact" />

        <section v-if="isGeneratedFailed" class="detail-card error-state">
          <h2>静态编译失败</h2>
          <p>artifact status=FAILED，不展示可视化预览。</p>
          <ul v-if="generatedErrors.length" class="message-list">
            <li v-for="error in generatedErrors" :key="JSON.stringify(error)">
              <strong>{{ error.code || 'ERROR' }}</strong>
              <span>{{ error.message || error }}</span>
            </li>
          </ul>
        </section>

        <GeneratedPagePreview
          v-else
          :html-code="generatedArtifact.htmlCode"
          :css-code="generatedArtifact.cssCode"
        />

        <section class="result-grid" aria-label="generated-page 代码展示">
          <CodeBlock title="htmlCode" :code="generatedArtifact.htmlCode" />
          <CodeBlock title="cssCode" :code="generatedArtifact.cssCode" />
          <CodeBlock title="vueCode" :code="generatedArtifact.vueCode" />
        </section>
      </template>

      <section v-else class="detail-card empty-state">
        <h2>暂无 generated-page artifact</h2>
        <p>当前任务还没有可展示的静态编译产物。</p>
      </section>
    </section>
  </main>
</template>
