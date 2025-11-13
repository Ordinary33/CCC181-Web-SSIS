import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/home.vue'
import Students from '../pages/Students.vue'
import Programs from '../pages/Programs.vue'
import Colleges from '../pages/Colleges.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/students',
      name: 'Students',
      component: Students,
    },
    {
      path: '/programs',
      name: 'Programs',
      component: Programs,
    },
    {
      path: '/colleges',
      name: 'Colleges',
      component: Colleges,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    },

  ],
})

export default router
