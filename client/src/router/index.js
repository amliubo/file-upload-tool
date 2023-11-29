import { createRouter, createWebHistory } from 'vue-router'
import Files from '../components/Files.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Files',
      component: Files,
    }
  ]
})

export default router
