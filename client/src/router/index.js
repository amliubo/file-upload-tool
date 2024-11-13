import { createRouter, createWebHistory } from 'vue-router'
import index from '../components/index.vue'
import jenkins from '../components/package.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: index,
    },
    {
      path: '/package',
      name: 'package',
      component: jenkins,
    }
  ]
})

export default router
