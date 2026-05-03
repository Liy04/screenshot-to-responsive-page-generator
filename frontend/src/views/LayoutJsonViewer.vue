<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { getLayoutJsonArtifact } from '../api/devLayoutArtifact'
import JsonPanel from '../components/layout/JsonPanel.vue'

const route = useRoute()
const router = useRouter()

const routeJobId = computed(() => route.params.jobId || '')
const jobIdInput = ref(routeJobId.value)
const artifact = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const hasSearched = ref(false)

const displayErrorMessage = computed(() => {
  if (!artifact.value) {
    return ''
  }

  return artifact.value.errorMessage || '无'
})

async function loadArtifact(jobId) {
  const normalizedJobId = String(jobId || '').trim()

  if (!normalizedJobId) {
    artifact.value = null
    errorMessage.value = '请输入 jobId'
    hasSearched.value = true
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  artifact.value = null
  hasSearched.value = true

  try {
    artifact.value = await getLayoutJsonArtifact(normalizedJobId)
  } catch (error) {
    errorMessage.value = error.message || '查询 Layout JSON 失败'
  } finally {
    isLoading.value = false
  }
}

async function handleSubmit() {
  const normalizedJobId = jobIdInput.value.trim()

  if (route.name === 'generation-layout-json' && normalizedJobId) {
    await router.replace({
      name: 'generation-layout-json',
      params: { jobId: normalizedJobId },
    })
  }

  await loadArtifact(normalizedJobId)
}

watch(
  routeJobId,
  (jobId) => {
    jobIdInput.value = jobId
    if (jobId) {
      loadArtifact(jobId)
    } else {
      artifact.value = null
      errorMessage.value = ''
      hasSearched.value = false
    }
  },
  { immediate: true },
)
</script>

<template>
  <main class="page-shell layout-viewer-page">
    <nav class="top-nav" aria-label="页面导航">
      <RouterLink to="/">返回工作台</RouterLink>
      <RouterLink to="/generation/create">创建任务</RouterLink>
    </nav>

    <section class="page-heading" aria-labelledby="layout-viewer-title">
      <p class="eyebrow">Week 03 P1</p>
      <h1 id="layout-viewer-title">Layout JSON 基础查看</h1>
      <p class="summary">
        输入 jobId 查询本地 mock Layout JSON，只做格式化查看，不提供编辑或代码生成能力。
      </p>
    </section>

    <form class="layout-query-card" @submit.prevent="handleSubmit">
      <label for="layout-job-id">jobId</label>
      <div class="layout-query-row">
        <input
          id="layout-job-id"
          v-model="jobIdInput"
          type="text"
          placeholder="例如：job_001"
          :disabled="isLoading"
        />
        <button class="primary-button" type="submit" :disabled="isLoading">
          {{ isLoading ? '查询中...' : '查询 Layout JSON' }}
        </button>
      </div>
    </form>

    <section v-if="isLoading" class="detail-card loading-card" aria-live="polite">
      正在加载 Layout JSON...
    </section>

    <section v-else-if="errorMessage" class="detail-card error-state" role="alert">
      <h2>查询失败</h2>
      <p>{{ errorMessage }}</p>
    </section>

    <section v-else-if="artifact" class="layout-artifact-stack">
      <section class="detail-card" aria-labelledby="artifact-meta-title">
        <div class="section-title-row">
          <h2 id="artifact-meta-title">Artifact 信息</h2>
          <span class="status-tag status-running">{{ artifact.status || '未知' }}</span>
        </div>

        <dl class="task-meta">
          <div>
            <dt>jobId</dt>
            <dd>{{ artifact.jobId || jobIdInput }}</dd>
          </div>
          <div>
            <dt>artifactType</dt>
            <dd>{{ artifact.artifactType || '-' }}</dd>
          </div>
          <div>
            <dt>status</dt>
            <dd>{{ artifact.status || '-' }}</dd>
          </div>
          <div>
            <dt>errorMessage</dt>
            <dd>{{ displayErrorMessage }}</dd>
          </div>
        </dl>
      </section>

      <JsonPanel title="layoutJson" :value="artifact.layoutJson" />
    </section>

    <section v-else class="detail-card empty-state">
      <h2>{{ hasSearched ? '暂无数据' : '等待查询' }}</h2>
      <p>请输入 jobId 后查询 Layout JSON mock 结果。</p>
    </section>
  </main>
</template>
