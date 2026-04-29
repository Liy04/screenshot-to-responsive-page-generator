<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import ImageUploader from '../components/ImageUploader.vue'
import { uploadAsset } from '../api/assetApi'
import { createGeneration } from '../api/generationApi'

const router = useRouter()
const selectedFile = ref(null)
const isSubmitting = ref(false)
const errorMessage = ref('')

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
    errorMessage.value = '请先选择一张 PNG、JPG、JPEG 或 WebP 图片'
    return
  }

  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const asset = await uploadAsset(selectedFile.value)
    if (!asset?.assetId) {
      throw new Error('上传成功但未返回 assetId')
    }

    const generation = await createGeneration({
      assetId: asset.assetId,
      mode: 'screenshot',
      targetStack: 'vue3-css',
      responsive: true,
    })
    if (!generation?.jobId) {
      throw new Error('创建任务成功但未返回 jobId')
    }

    await router.push({
      name: 'generation-detail',
      params: { jobId: generation.jobId },
    })
  } catch (error) {
    errorMessage.value = error.message || '创建任务失败，请稍后重试'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="page-shell create-page">
    <nav class="top-nav" aria-label="页面导航">
      <RouterLink to="/">返回工作台</RouterLink>
    </nav>

    <section class="page-heading" aria-labelledby="create-title">
      <p class="eyebrow">创建生成任务</p>
      <h1 id="create-title">上传截图并开始生成</h1>
      <p class="summary">
        选择截图后会先上传图片，再创建一个 mock 生成任务。
      </p>
    </section>

    <ImageUploader
      :disabled="isSubmitting"
      @change="handleFileChange"
      @error="handleFileError"
    />

    <p v-if="errorMessage" class="error-message" role="alert">
      {{ errorMessage }}
    </p>

    <div class="form-actions">
      <button
        class="primary-button"
        type="button"
        :disabled="!selectedFile || isSubmitting"
        @click="handleSubmit"
      >
        {{ isSubmitting ? '正在创建...' : '开始生成' }}
      </button>
    </div>
  </main>
</template>
