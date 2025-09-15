import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/home.vue'
import Test from '../components/Test.vue'
import Students from '../components/Students.vue'
import Programs from '../components/Programs.vue'
import Colleges from '../components/Colleges.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/test',
      name: 'Test',
      component: Test,
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

  ],
})

export default router
