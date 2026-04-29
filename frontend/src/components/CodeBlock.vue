<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  code: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <section class="code-block" :aria-labelledby="`${title}-title`">
    <h2 :id="`${title}-title`">{{ title }}</h2>
    <pre><code>{{ code || '暂无内容' }}</code></pre>
  </section>
</template>
