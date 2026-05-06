<script setup>
import { computed } from 'vue'

const props = defineProps({
  htmlCode: {
    type: String,
    default: '',
  },
  cssCode: {
    type: String,
    default: '',
  },
})

const previewSrcdoc = computed(() => {
  return `<style>${props.cssCode || ''}</style>\n${props.htmlCode || ''}`
})
</script>

<template>
  <section class="generated-preview" aria-labelledby="generated-preview-title">
    <h2 id="generated-preview-title">安全预览</h2>
    <iframe
      title="generated-page 安全预览"
      sandbox=""
      :srcdoc="previewSrcdoc"
    ></iframe>
  </section>
</template>
