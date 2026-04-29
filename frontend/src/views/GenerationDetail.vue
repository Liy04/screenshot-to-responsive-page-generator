<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { getGeneration, getGenerationResult } from '../api/generationApi'
import CodeBlock from '../components/CodeBlock.vue'
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

const layoutJsonText = computed(() => {
  if (!result.value?.layoutJson) {
    return ''
  }

  return JSON.stringify(result.value.layoutJson, null, 2)
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

watch(
  () => props.jobId,
  () => {
    loadGenerationDetail()
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

    <template v-else>
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
  </main>
</template>
