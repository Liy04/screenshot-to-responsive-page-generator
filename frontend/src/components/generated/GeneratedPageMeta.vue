<script setup>
import { computed } from 'vue'
import JsonPanel from '../layout/JsonPanel.vue'
import StatusTag from '../StatusTag.vue'

const props = defineProps({
  artifact: {
    type: Object,
    required: true,
  },
})

const validationErrors = computed(() => props.artifact.validation?.errors || [])
const validationWarnings = computed(() => props.artifact.validation?.warnings || [])
const unsupportedNodes = computed(() => props.artifact.unsupportedNodes || [])
const generator = computed(() => props.artifact.generator || {})
const source = computed(() => props.artifact.source || {})

const errorPanelValue = computed(() => {
  return validationErrors.value.length ? validationErrors.value : '暂无 errors'
})

const warningPanelValue = computed(() => {
  return validationWarnings.value.length ? validationWarnings.value : '暂无 warnings'
})

const unsupportedPanelValue = computed(() => {
  return unsupportedNodes.value.length
    ? unsupportedNodes.value
    : '暂无 unsupportedNodes'
})
</script>

<template>
  <section class="detail-card" aria-labelledby="generated-meta-title">
    <div class="section-title-row">
      <h2 id="generated-meta-title">Generated Page Artifact</h2>
      <StatusTag :status="artifact.status" />
    </div>

    <dl class="task-meta">
      <div>
        <dt>status</dt>
        <dd>{{ artifact.status || '-' }}</dd>
      </div>
      <div>
        <dt>artifactType</dt>
        <dd>{{ artifact.artifactType || '-' }}</dd>
      </div>
      <div>
        <dt>layoutHash</dt>
        <dd>{{ source.layoutHash || '-' }}</dd>
      </div>
      <div>
        <dt>layoutVersion</dt>
        <dd>{{ source.layoutVersion || '-' }}</dd>
      </div>
      <div>
        <dt>layoutSourceType</dt>
        <dd>{{ source.layoutSourceType || '-' }}</dd>
      </div>
      <div>
        <dt>generator</dt>
        <dd>{{ generator.name || '-' }} {{ generator.version || '' }}</dd>
      </div>
      <div v-if="artifact.createdAt">
        <dt>createdAt</dt>
        <dd>{{ artifact.createdAt }}</dd>
      </div>
    </dl>
  </section>

  <section class="generated-validation-grid" aria-label="generated-page 校验信息">
    <JsonPanel title="validation.errors" :value="errorPanelValue" />
    <JsonPanel title="validation.warnings" :value="warningPanelValue" />
    <JsonPanel title="unsupportedNodes" :value="unsupportedPanelValue" />
  </section>
</template>
