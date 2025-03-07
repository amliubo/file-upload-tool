import { createRouter, createWebHistory } from 'vue-router'
import index from '../components/index.vue'
import pkg from '../components/pkg.vue'
import match from '../components/match.vue'

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
    },
    {
      path: '/match',
      name: 'match',
      component: match,
    },
  ]
})

export default router
