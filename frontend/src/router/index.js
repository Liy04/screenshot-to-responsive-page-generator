import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import GenerationCreate from '../views/GenerationCreate.vue'
import GenerationDetail from '../views/GenerationDetail.vue'
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
