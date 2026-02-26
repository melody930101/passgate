import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/components/Layout/TabLayout.vue'),
    redirect: '/issue',
    children: [
      { path: 'issue', name: 'Issue', component: () => import('@/views/Issue/index.vue') },
      { path: 'verify', name: 'Verify', component: () => import('@/views/Verify/index.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/Profile/index.vue') }
    ],
    meta: { requiresAuth: true }
  },
  {
    path: '/issue/history',
    name: 'IssueHistory',
    component: () => import('@/views/Issue/IssueHistory.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/verify/history',
    name: 'VerifyHistory',
    component: () => import('@/views/Verify/VerifyHistory.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/password',
    name: 'ChangePassword',
    component: () => import('@/views/Profile/ChangePassword.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory('/passgate/'),
  routes
})

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  const needAuth = to.meta.requiresAuth !== false

  if (needAuth && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && userStore.isLoggedIn) {
    next({ path: '/' })
  } else {
    next()
  }
})

export default router
