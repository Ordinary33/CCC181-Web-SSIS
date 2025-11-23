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
      component: Home,
      meta: { title: 'Dashboard' }
    },
    {
      path: '/students',
      name: 'Students',
      component: Students,
      meta: { title: 'Students' }
    },
    {
      path: '/programs',
      name: 'Programs',
      component: Programs,
      meta: { title: 'Programs' }
    },
    {
      path: '/colleges',
      name: 'Colleges',
      component: Colleges,
      meta: { title: 'Colleges' }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    },

  ],
})

const DEFAULT_TITLE = 'Veridia';

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} | ${DEFAULT_TITLE}` : DEFAULT_TITLE;
  next();
});

export default router
