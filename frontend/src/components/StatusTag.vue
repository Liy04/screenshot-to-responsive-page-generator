<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    default: '',
  },
})

const normalizedStatus = computed(() => props.status.toLowerCase())

const statusText = computed(() => {
  const textMap = {
    pending: '待处理',
    running: '生成中',
    success: '成功',
    failed: '失败',
  }

  return textMap[normalizedStatus.value] || props.status || '未知'
})

const statusClass = computed(() => {
  const classMap = {
    pending: 'status-pending',
    running: 'status-running',
    success: 'status-success',
    failed: 'status-failed',
  }

  return classMap[normalizedStatus.value] || 'status-unknown'
})
</script>

<template>
  <span class="status-tag" :class="statusClass">
    {{ statusText }}
  </span>
</template>
