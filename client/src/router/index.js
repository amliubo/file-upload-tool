import { createRouter, createWebHistory } from 'vue-router'
import index from '../components/index.vue'
import pkg from '../components/pkg.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: index,
    },
    {
      path: '/pkg',
      name: 'pkg',
      component: pkg,
    }
  ]
})

export default router
