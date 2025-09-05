/**
 * 认证相关的工具函数
 */
import { authAPI } from '../api/auth'
import store from '../store'

/**
 * 初始化应用认证状态
 * 检查本地存储的token，如果有效则恢复用户状态
 */
export async function initializeAuth() {
  const token = localStorage.getItem('token')
  const refreshToken = localStorage.getItem('refresh_token')
  const savedUser = localStorage.getItem('user')
  
  if (!token || !savedUser) {
    return false
  }
  
  try {
    // 检查token是否有效
    if (authAPI.isTokenValid()) {
      // Token有效，恢复用户状态
      const user = JSON.parse(savedUser)
      store.commit('SET_USER', user)
      return true
    } else if (refreshToken) {
      // Token过期但有refresh token，尝试刷新
      try {
        await authAPI.refreshToken(refreshToken)
        
        // 重新获取用户信息
        const userInfo = await authAPI.getUserInfo()
        const user = {
          id: userInfo.id,
          name: userInfo.full_name || userInfo.username,
          email: userInfo.email,
          username: userInfo.username,
          role: userInfo.is_superuser ? 'admin' : 'user',
          avatar: userInfo.avatar,
          token: localStorage.getItem('token')
        }
        
        store.commit('SET_USER', user)
        return true
      } catch (error) {
        console.warn('Token刷新失败:', error)
        authAPI.clearAuth()
        store.commit('LOGOUT')
        return false
      }
    } else {
      // 没有有效token或refresh token
      authAPI.clearAuth()
      store.commit('LOGOUT')
      return false
    }
  } catch (error) {
    console.error('初始化认证状态失败:', error)
    authAPI.clearAuth()
    store.commit('LOGOUT')
    return false
  }
}

/**
 * 设置Token自动刷新
 * 在token即将过期时自动刷新
 */
export function setupTokenAutoRefresh() {
  const checkTokenExpiration = async () => {
    const token = localStorage.getItem('token')
    const refreshToken = localStorage.getItem('refresh_token')
    
    if (!token || !refreshToken) {
      return
    }
    
    try {
      // 解析token获取过期时间
      const payload = JSON.parse(atob(token.split('.')[1]))
      const expirationTime = payload.exp * 1000 // 转换为毫秒
      const currentTime = Date.now()
      const timeUntilExpiration = expirationTime - currentTime
      
      // 如果token在5分钟内过期，则刷新
      if (timeUntilExpiration < 5 * 60 * 1000 && timeUntilExpiration > 0) {
        try {
          await authAPI.refreshToken(refreshToken)
          console.log('Token自动刷新成功')
        } catch (error) {
          console.warn('Token自动刷新失败:', error)
          authAPI.clearAuth()
          store.commit('LOGOUT')
          // 跳转到登录页面
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
        }
      }
    } catch (error) {
      console.error('Token检查失败:', error)
    }
  }
  
  // 每分钟检查一次token状态
  setInterval(checkTokenExpiration, 60 * 1000)
  
  // 立即检查一次
  checkTokenExpiration()
}

/**
 * 监听页面可见性变化，在页面重新可见时检查token状态
 */
export function setupVisibilityChangeListener() {
  document.addEventListener('visibilitychange', async () => {
    if (!document.hidden) {
      // 页面变为可见时检查认证状态
      await initializeAuth()
    }
  })
}

export default {
  initializeAuth,
  setupTokenAutoRefresh,
  setupVisibilityChangeListener
}