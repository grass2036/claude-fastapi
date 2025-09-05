import axios from 'axios'
import { useStore } from 'vuex'

// 创建axios实例
const http = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const originalRequest = error.config
    
    // 处理401未授权错误
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // 尝试刷新token
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post(`${http.defaults.baseURL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken
          })
          
          const { access_token, refresh_token: newRefreshToken } = response.data
          localStorage.setItem('token', access_token)
          localStorage.setItem('refresh_token', newRefreshToken)
          
          // 重试原请求
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return http(originalRequest)
          
        } catch (refreshError) {
          console.error('Token刷新失败:', refreshError)
          
          // 清除无效token并跳转到登录页
          localStorage.removeItem('token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          
          if (window.location.pathname !== '/login') {
            window.location.href = '/login'
          }
          
          return Promise.reject(refreshError)
        }
      } else {
        // 没有refresh token，直接跳转登录
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      }
    }
    
    // 处理其他错误
    const errorMessage = error.response?.data?.detail || error.message || '请求失败'
    console.error('API请求错误:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      message: errorMessage
    })
    
    return Promise.reject({
      ...error,
      message: errorMessage
    })
  }
)

export default http