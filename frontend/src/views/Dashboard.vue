<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <main class="page-shell dashboard-page">
    <section class="dashboard-hero" aria-labelledby="dashboard-title">
      <p class="eyebrow">MVP Mock 版本</p>
      <h1 id="dashboard-title">截图 / Figma 到响应式页面生成器</h1>
      <p class="summary">
        当前阶段先跑通截图上传、创建任务和 mock 结果查看的最小闭环。
      </p>
      <div class="actions">
        <RouterLink class="primary-link" to="/generation/create">
          上传截图开始生成
        </RouterLink>
      </div>
    </section>

    <section class="info-grid" aria-label="当前阶段说明">
      <article>
        <h2>支持截图上传</h2>
        <p>本阶段只处理本地图片上传，不接入 Figma。</p>
      </article>
      <article>
        <h2>返回 mock 结果</h2>
        <p>生成结果由后端 mock 返回，不代表真实截图解析。</p>
      </article>
      <article>
        <h2>保持轻量闭环</h2>
        <p>先验证流程稳定，暂不做编辑器、导出或复杂 UI。</p>
      </article>
    </section>
  </main>
</template>
