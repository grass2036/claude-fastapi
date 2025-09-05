import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import { authAPI } from '../api/auth'

// Import components
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register', 
    component: Register,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Home
      },
      {
        path: '/users',
        name: 'Users',
        component: Users
      },
      {
        path: '/monitoring',
        name: 'Monitoring',
        component: () => import('../views/Monitoring.vue')
      },
      {
        path: '/logs',
        name: 'Logs',
        component: () => import('../views/Logs.vue')
      },
      {
        path: '/settings',
        name: 'Settings',
        component: () => import('../views/Settings.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Route Guards
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  const token = localStorage.getItem('token')
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated || !token) {
      // 没有认证信息，跳转登录
      next('/login')
      return
    }
    
    // 检查token是否有效
    if (!authAPI.isTokenValid()) {
      const refreshToken = localStorage.getItem('refresh_token')
      
      if (refreshToken) {
        try {
          // 尝试刷新token
          await authAPI.refreshToken(refreshToken)
          next()
          return
        } catch (error) {
          console.warn('Token刷新失败:', error)
          // 刷新失败，清除认证信息并跳转登录
          authAPI.clearAuth()
          store.commit('LOGOUT')
          next('/login')
          return
        }
      } else {
        // 没有刷新token，跳转登录
        authAPI.clearAuth()
        store.commit('LOGOUT')
        next('/login')
        return
      }
    }
    
    next()
  }
  // Check if route requires guest (not authenticated)
  else if (to.matched.some(record => record.meta.requiresGuest)) {
    if (isAuthenticated && token && authAPI.isTokenValid()) {
      next('/dashboard')
    } else {
      // Token无效，清除认证状态
      if (isAuthenticated) {
        authAPI.clearAuth()
        store.commit('LOGOUT')
      }
      next()
    }
  }
  else {
    next()
  }
})

export default router