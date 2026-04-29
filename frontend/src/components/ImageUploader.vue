<script setup>
import { onBeforeUnmount, ref } from 'vue'

const emit = defineEmits(['change', 'error'])

defineProps({
  disabled: {
    type: Boolean,
    default: false,
  },
})

const allowedTypes = ['image/png', 'image/jpeg', 'image/webp']
const previewUrl = ref('')
const fileName = ref('')

function revokePreview() {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = ''
  }
}

function clearSelection(input) {
  revokePreview()
  fileName.value = ''
  if (input) {
    input.value = ''
  }
  emit('change', null)
}

function handleFileChange(event) {
  const input = event.target
  const file = input.files?.[0]

  if (!file) {
    clearSelection(input)
    return
  }

  if (!allowedTypes.includes(file.type)) {
    clearSelection(input)
    emit('error', '只支持 PNG、JPG、JPEG、WebP 图片')
    return
  }

  revokePreview()
  fileName.value = file.name
  previewUrl.value = URL.createObjectURL(file)
  emit('change', file)
}

onBeforeUnmount(() => {
  revokePreview()
})
</script>

<template>
  <section class="upload-panel" aria-labelledby="upload-title">
    <div class="upload-copy">
      <h2 id="upload-title">选择截图</h2>
      <p>支持 PNG、JPG、JPEG、WebP，建议上传清晰的单页截图。</p>
    </div>

    <label class="file-picker">
      <input
        type="file"
        accept="image/png,image/jpeg,image/webp"
        :disabled="disabled"
        @change="handleFileChange"
      />
      <span>{{ fileName || '选择图片' }}</span>
    </label>

    <div v-if="previewUrl" class="preview-frame">
      <img :src="previewUrl" alt="已选择截图预览" />
    </div>
    <div v-else class="preview-placeholder">
      选择图片后将在这里预览
    </div>
  </section>
</template>
