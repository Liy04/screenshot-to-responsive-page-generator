<script setup>
const statusItems = [
  '前端工程已初始化',
  '当前仅展示占位首页',
  '暂不接入真实截图解析或代码生成',
]
</script>

<template>
  <main class="home-page">
    <section class="hero" aria-labelledby="page-title">
      <p class="eyebrow">Week 01 初始化中</p>
      <h1 id="page-title">截图 / Figma 到响应式页面生成器</h1>
      <p class="summary">
        当前阶段先完成前端工程骨架和最小可访问页面，为后续任务闭环开发做准备。
      </p>
      <ul class="status-list" aria-label="当前状态">
        <li v-for="item in statusItems" :key="item">
          {{ item }}
        </li>
      </ul>
    </section>
  </main>
</template>
