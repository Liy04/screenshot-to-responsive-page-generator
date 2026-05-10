import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import GenerationCreate from '../views/GenerationCreate.vue'
import GenerationDetail from '../views/GenerationDetail.vue'
import GeneratedPagePreviewDev from '../views/GeneratedPagePreviewDev.vue'
import ImageToLayoutDev from '../views/ImageToLayoutDev.vue'
import LayoutJsonViewer from '../views/LayoutJsonViewer.vue'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/dashboard',
    name: 'dashboard-alias',
    component: Dashboard,
  },
  {
    path: '/generation/create',
    name: 'generation-create',
    component: GenerationCreate,
  },
  {
    path: '/layout-json-viewer',
    name: 'layout-json-viewer',
    component: LayoutJsonViewer,
  },
  {
    path: '/generation/:jobId/layout-json',
    name: 'generation-layout-json',
    component: LayoutJsonViewer,
  },
  {
    path: '/dev/generated-page-preview/:jobId',
    name: 'generated-page-preview-dev',
    component: GeneratedPagePreviewDev,
    props: true,
  },
  {
    path: '/dev/image-to-layout',
    name: 'image-to-layout-dev',
    component: ImageToLayoutDev,
  },
  {
    path: '/generation/:jobId',
    name: 'generation-detail',
    component: GenerationDetail,
    props: true,
  },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
