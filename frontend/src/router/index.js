import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import GenerationCreate from '../views/GenerationCreate.vue'
import GenerationDetail from '../views/GenerationDetail.vue'

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
