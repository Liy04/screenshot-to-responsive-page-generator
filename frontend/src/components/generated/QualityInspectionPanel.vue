<script setup>
import { computed } from 'vue'
import StatusTag from '../StatusTag.vue'

const props = defineProps({
  fileName: {
    type: String,
    default: '',
  },
  resultState: {
    type: String,
    default: '',
  },
  hasPreview: {
    type: Boolean,
    default: false,
  },
  canCopy: {
    type: Boolean,
    default: false,
  },
  canDownload: {
    type: Boolean,
    default: false,
  },
})

const week15Samples = [
  {
    id: 'W15-S1',
    label: 'Simple card',
    fileName: '01-simple-card-page.png',
    intent: '检查简单营销 / 内容卡片布局是否保留。',
    traits: '页面容器、主卡片或 hero、标题/正文/行动层级、圆角面板、居中或均衡间距。',
  },
  {
    id: 'W15-S2',
    label: 'Simple form',
    fileName: '02-simple-form-page.png',
    intent: '检查基础表单页面的标签、输入框和提交动作。',
    traits: '表单容器、标签贴近字段、输入和按钮可区分、稳定纵向节奏、主操作清楚。',
  },
  {
    id: 'W15-S3',
    label: 'Dashboard cards',
    fileName: '03-dashboard-cards-page.png',
    intent: '检查 dashboard 重复卡片 / 指标布局。',
    traits: '顶部区域、重复卡片网格或行、标题/数值/辅助文案分组、主层级清楚。',
  },
]

const qualityMetrics = [
  'Structure',
  'Main visual hierarchy',
  'Spacing and grouping',
  'Typography',
  'Component fidelity',
  'Responsive sanity',
  'Safety and delivery',
]

const normalizedFileName = computed(() => props.fileName.toLowerCase())
const matchedSample = computed(() => {
  return week15Samples.find((sample) => normalizedFileName.value.includes(sample.fileName)) || null
})
const sampleStatus = computed(() => (matchedSample.value ? 'success' : 'pending'))
const stateStatus = computed(() => (props.resultState ? props.resultState : 'pending'))
const previewStatus = computed(() => (props.hasPreview ? 'success' : 'pending'))
const copyStatus = computed(() => (props.canCopy ? 'success' : 'pending'))
const downloadStatus = computed(() => (props.canDownload ? 'success' : 'pending'))
</script>

<template>
  <section class="detail-card quality-inspection-card" aria-labelledby="quality-inspection-title">
    <div class="section-title-row">
      <h2 id="quality-inspection-title">Week 15 质量检查</h2>
      <StatusTag :status="sampleStatus" />
    </div>

    <div class="quality-inspection-grid">
      <section class="quality-panel" aria-labelledby="sample-match-title">
        <div class="quality-panel-heading">
          <h3 id="sample-match-title">固定样例</h3>
          <StatusTag :status="sampleStatus" />
        </div>
        <template v-if="matchedSample">
          <p class="quality-sample-title">
            {{ matchedSample.id }} {{ matchedSample.label }}
          </p>
          <p>{{ matchedSample.intent }}</p>
          <p class="quality-traits">{{ matchedSample.traits }}</p>
        </template>
        <p v-else>
          当前文件名未命中 Week 15 固定样例；仍可按右侧指标人工检查。
        </p>
      </section>

      <section class="quality-panel" aria-labelledby="metric-checklist-title">
        <div class="quality-panel-heading">
          <h3 id="metric-checklist-title">人工评分项</h3>
          <span class="quality-score-legend">pass / partial / fail / blocked</span>
        </div>
        <ul class="quality-metric-list" aria-label="Week 15 lightweight quality metrics">
          <li v-for="metric in qualityMetrics" :key="metric">{{ metric }}</li>
        </ul>
      </section>
    </div>

    <dl class="quality-safety-list" aria-label="安全与交付检查">
      <div>
        <dt>结果状态</dt>
        <dd><StatusTag :status="stateStatus" /></dd>
      </div>
      <div>
        <dt>生成预览</dt>
        <dd><StatusTag :status="previewStatus" /></dd>
      </div>
      <div>
        <dt>复制</dt>
        <dd><StatusTag :status="copyStatus" /></dd>
      </div>
      <div>
        <dt>下载</dt>
        <dd><StatusTag :status="downloadStatus" /></dd>
      </div>
      <div>
        <dt>iframe sandbox</dt>
        <dd><code>sandbox=""</code> / no <code>allow-scripts</code></dd>
      </div>
    </dl>
  </section>
</template>
