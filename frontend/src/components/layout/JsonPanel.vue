<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [Object, Array, String, Number, Boolean, null],
    default: null,
  },
})

const formattedJson = computed(() => {
  if (props.value === null || props.value === undefined || props.value === '') {
    return '暂无 Layout JSON'
  }

  if (typeof props.value === 'string') {
    return props.value
  }

  return JSON.stringify(props.value, null, 2)
})
</script>

<template>
  <section class="json-panel" :aria-labelledby="`${title}-title`">
    <h2 :id="`${title}-title`">{{ title }}</h2>
    <pre><code>{{ formattedJson }}</code></pre>
  </section>
</template>
