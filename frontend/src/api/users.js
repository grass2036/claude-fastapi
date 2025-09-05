import http from './http'

/**
 * 用户管理相关的API接口
 */
export const usersAPI = {
  /**
   * 获取用户列表
   * @param {Object} params - 查询参数
   * @param {number} [params.page=1] - 页码
   * @param {number} [params.limit=10] - 每页数量
   * @param {string} [params.search] - 搜索关键词
   * @param {boolean} [params.is_active] - 是否活跃
   * @returns {Promise} 返回用户列表
   */
  async getUsers(params = {}) {
    try {
      const response = await http.get('/api/v1/users', { params })
      return response
    } catch (error) {
      console.error('获取用户列表失败:', error)
      throw error
    }
  },

  /**
   * 获取单个用户详情
   * @param {number} userId - 用户ID
   * @returns {Promise} 返回用户详情
   */
  async getUser(userId) {
    try {
      const response = await http.get(`/api/v1/users/${userId}`)
      return response
    } catch (error) {
      console.error('获取用户详情失败:', error)
      throw error
    }
  },

  /**
   * 创建用户
   * @param {Object} userData - 用户数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.email - 邮箱
   * @param {string} userData.password - 密码
   * @param {string} userData.confirm_password - 确认密码
   * @param {string} [userData.full_name] - 全名
   * @param {string} [userData.phone] - 手机号
   * @param {string} [userData.bio] - 个人简介
   * @returns {Promise} 返回创建的用户信息
   */
  async createUser(userData) {
    try {
      const response = await http.post('/api/v1/users', userData)
      return response
    } catch (error) {
      console.error('创建用户失败:', error)
      throw error
    }
  },

  /**
   * 更新用户信息
   * @param {number} userId - 用户ID
   * @param {Object} userData - 更新的用户数据
   * @returns {Promise} 返回更新后的用户信息
   */
  async updateUser(userId, userData) {
    try {
      const response = await http.put(`/api/v1/users/${userId}`, userData)
      return response
    } catch (error) {
      console.error('更新用户失败:', error)
      throw error
    }
  },

  /**
   * 删除用户
   * @param {number} userId - 用户ID
   * @returns {Promise}
   */
  async deleteUser(userId) {
    try {
      const response = await http.delete(`/api/v1/users/${userId}`)
      return response
    } catch (error) {
      console.error('删除用户失败:', error)
      throw error
    }
  },

  /**
   * 批量删除用户
   * @param {Array<number>} userIds - 用户ID数组
   * @returns {Promise}
   */
  async batchDeleteUsers(userIds) {
    try {
      const response = await http.post('/api/v1/users/batch-delete', {
        user_ids: userIds
      })
      return response
    } catch (error) {
      console.error('批量删除用户失败:', error)
      throw error
    }
  },

  /**
   * 激活/停用用户
   * @param {number} userId - 用户ID
   * @param {boolean} isActive - 是否激活
   * @returns {Promise}
   */
  async toggleUserStatus(userId, isActive) {
    try {
      const response = await http.patch(`/api/v1/users/${userId}/status`, {
        is_active: isActive
      })
      return response
    } catch (error) {
      console.error('修改用户状态失败:', error)
      throw error
    }
  },

  /**
   * 重置用户密码
   * @param {number} userId - 用户ID
   * @param {string} newPassword - 新密码
   * @returns {Promise}
   */
  async resetPassword(userId, newPassword) {
    try {
      const response = await http.post(`/api/v1/users/${userId}/reset-password`, {
        new_password: newPassword
      })
      return response
    } catch (error) {
      console.error('重置密码失败:', error)
      throw error
    }
  }
}

export default usersAPI