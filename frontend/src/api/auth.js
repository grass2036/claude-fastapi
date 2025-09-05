import http from './http'

/**
 * 认证相关的API接口
 */
export const authAPI = {
  /**
   * 用户登录
   * @param {Object} loginData - 登录数据
   * @param {string} loginData.username - 用户名或邮箱
   * @param {string} loginData.password - 密码
   * @returns {Promise} 返回包含token的响应
   */
  async login(loginData) {
    try {
      const response = await http.post('/api/v1/auth/login', loginData)
      
      // 保存token到localStorage
      if (response.access_token) {
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
      }
      
      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  },

  /**
   * 用户注册
   * @param {Object} registerData - 注册数据
   * @param {string} registerData.username - 用户名
   * @param {string} registerData.email - 邮箱
   * @param {string} registerData.password - 密码
   * @param {string} registerData.confirm_password - 确认密码
   * @param {string} [registerData.full_name] - 全名
   * @param {string} [registerData.phone] - 手机号
   * @param {string} [registerData.bio] - 个人简介
   * @returns {Promise} 返回用户信息
   */
  async register(registerData) {
    try {
      const response = await http.post('/api/v1/auth/register', registerData)
      return response
    } catch (error) {
      console.error('注册失败:', error)
      throw error
    }
  },

  /**
   * 获取当前用户信息
   * @returns {Promise} 返回用户信息
   */
  async getUserInfo() {
    try {
      const response = await http.get('/api/v1/auth/me')
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  },

  /**
   * 刷新access token
   * @param {string} refreshToken - 刷新令牌
   * @returns {Promise} 返回新的token信息
   */
  async refreshToken(refreshToken) {
    try {
      const response = await http.post('/api/v1/auth/refresh', {
        refresh_token: refreshToken
      })
      
      // 更新localStorage中的token
      if (response.access_token) {
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
      }
      
      return response
    } catch (error) {
      console.error('刷新token失败:', error)
      throw error
    }
  },

  /**
   * 用户登出
   * @returns {Promise}
   */
  async logout() {
    try {
      await http.post('/api/v1/auth/logout')
    } catch (error) {
      console.error('登出请求失败:', error)
      // 即使请求失败也要清除本地token
    } finally {
      // 清除本地存储的认证信息
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  },

  /**
   * 修改密码
   * @param {Object} passwordData - 密码数据
   * @param {string} passwordData.current_password - 当前密码
   * @param {string} passwordData.new_password - 新密码
   * @param {string} passwordData.confirm_new_password - 确认新密码
   * @returns {Promise}
   */
  async changePassword(passwordData) {
    try {
      const response = await http.post('/api/v1/auth/change-password', passwordData)
      return response
    } catch (error) {
      console.error('修改密码失败:', error)
      throw error
    }
  },

  /**
   * 检查token是否有效
   * @returns {boolean} token是否有效
   */
  isTokenValid() {
    const token = localStorage.getItem('token')
    if (!token) return false
    
    try {
      // 解析JWT token
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      
      return payload.exp > currentTime
    } catch (error) {
      console.error('Token解析失败:', error)
      return false
    }
  },

  /**
   * 清除所有认证信息
   */
  clearAuth() {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }
}

export default authAPI