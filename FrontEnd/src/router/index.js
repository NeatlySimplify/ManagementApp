import { createRouter, createWebHistory } from 'vue-router'
import RootView from '@/views/RootView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: '/mfa',
      name: 'mfa',
      component: RootView,
      meta: { guestOnly: true },
    },
    {
      path: '/forgot_password',
      name: 'forgot_password',
      component: RootView,
      meta: { guestOnly: true },
    },
    // {
    //   path: '/app/board',
    //   name: 'board',
    //   component: () => import('@/views/BoardView'),
    //   meta: { requiresAuth: true },
    // },
    // {
    //   path: '/app/user',
    //   name: 'user',
    //   component: () => import('@/views/UserView'),
    //   meta: { requiresAuth: true },
    // },
    // {
    //   path: '/app/unit',
    //   name: 'unit',
    //   component: () => import('@/views/UnitView'),
    //   meta: { requiresAuth: true },
    // },
    {
      path: '/:pathMatch(.*)*',
      name: 'root',
      component: RootView, //fallback page component
      guestOnly: true,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.guestOnly && token) {
    next('/board')
  } else {
    next()
  }
})

export default router
