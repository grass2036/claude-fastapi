/**
 * API接口统一入口文件
 * 导出所有API模块，方便统一管理和使用
 */

import http from './http'
import authAPI from './auth'
import usersAPI from './users'

// 基础HTTP客户端
export { http }

// 认证相关API
export { authAPI }

// 用户管理API
export { usersAPI }

// 系统信息API
export const systemAPI = {
  /**
   * 获取系统健康状态
   * @returns {Promise}
   */
  async getHealthStatus() {
    try {
      const response = await http.get('/health')
      return response
    } catch (error) {
      console.error('获取系统状态失败:', error)
      throw error
    }
  },

  /**
   * 获取系统基本信息
   * @returns {Promise}
   */
  async getSystemInfo() {
    try {
      const response = await http.get('/')
      return response
    } catch (error) {
      console.error('获取系统信息失败:', error)
      throw error
    }
  }
}

// 缓存API (用于测试)
export const cacheAPI = {
  /**
   * 测试Redis缓存
   * @returns {Promise}
   */
  async testCache() {
    try {
      const response = await http.post('/cache/test')
      return response
    } catch (error) {
      console.error('缓存测试失败:', error)
      throw error
    }
  },

  /**
   * 获取缓存值
   * @param {string} key - 缓存键
   * @returns {Promise}
   */
  async getCache(key) {
    try {
      const response = await http.get(`/cache/${key}`)
      return response
    } catch (error) {
      console.error('获取缓存失败:', error)
      throw error
    }
  },

  /**
   * 设置缓存值
   * @param {string} key - 缓存键
   * @param {Object} data - 缓存数据
   * @param {number} [ttl=3600] - 过期时间(秒)
   * @returns {Promise}
   */
  async setCache(key, data, ttl = 3600) {
    try {
      const response = await http.post(`/cache/${key}`, data, {
        params: { ttl }
      })
      return response
    } catch (error) {
      console.error('设置缓存失败:', error)
      throw error
    }
  }
}

// 默认导出所有API
export default {
  auth: authAPI,
  users: usersAPI,
  system: systemAPI,
  cache: cacheAPI
}