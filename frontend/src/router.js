import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from './api'
import Login from './views/Login.vue'
import Projects from './views/Projects.vue'
import Tasks from './views/Tasks.vue'
import Dashboard from './views/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/projects' },
    { path: '/login', component: Login },
    { path: '/projects', component: Projects, meta: { auth: true } },
    { path: '/projects/:id/tasks', component: Tasks, meta: { auth: true } },
    { path: '/dashboard', component: Dashboard, meta: { auth: true } },
  ],
})
router.beforeEach((to) => {
  if (to.meta.auth && !getToken()) return '/login'
})
export default router
