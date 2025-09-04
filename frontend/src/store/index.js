import { createStore } from 'vuex'

// Load user from localStorage if available
const savedUser = localStorage.getItem('user')
const initialUser = savedUser ? JSON.parse(savedUser) : null

export default createStore({
  state: {
    user: initialUser,
    isAuthenticated: !!initialUser,
    loading: false,
    error: null,
    theme: localStorage.getItem('theme') || 'light',
    notifications: []
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
    loading: state => state.loading,
    error: state => state.error,
    theme: state => state.theme,
    notifications: state => state.notifications,
    unreadNotifications: state => state.notifications.filter(n => !n.read).length
  },
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
      
      // Save to localStorage
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
        localStorage.setItem('token', user.token || 'demo-token')
      } else {
        localStorage.removeItem('user')
        localStorage.removeItem('token')
      }
    },
    LOGOUT(state) {
      state.user = null
      state.isAuthenticated = false
      state.notifications = []
      
      // Clear localStorage
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    SET_THEME(state, theme) {
      state.theme = theme
      localStorage.setItem('theme', theme)
    },
    ADD_NOTIFICATION(state, notification) {
      const newNotification = {
        id: Date.now(),
        read: false,
        timestamp: new Date(),
        ...notification
      }
      state.notifications.unshift(newNotification)
      
      // Keep only last 50 notifications
      if (state.notifications.length > 50) {
        state.notifications = state.notifications.slice(0, 50)
      }
    },
    MARK_NOTIFICATION_READ(state, id) {
      const notification = state.notifications.find(n => n.id === id)
      if (notification) {
        notification.read = true
      }
    },
    MARK_ALL_NOTIFICATIONS_READ(state) {
      state.notifications.forEach(n => n.read = true)
    },
    REMOVE_NOTIFICATION(state, id) {
      const index = state.notifications.findIndex(n => n.id === id)
      if (index > -1) {
        state.notifications.splice(index, 1)
      }
    }
  },
  actions: {
    async login({ commit }, credentials) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        // 模拟登录API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 模拟用户数据
        const user = {
          id: 1,
          name: '管理员',
          email: credentials.email,
          role: 'admin',
          avatar: null,
          token: 'demo-token-' + Date.now()
        }
        
        commit('SET_USER', user)
        commit('ADD_NOTIFICATION', {
          type: 'success',
          title: '登录成功',
          message: `欢迎回来，${user.name}！`
        })
        
        return user
      } catch (error) {
        const errorMsg = error.message || '登录失败'
        commit('SET_ERROR', errorMsg)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        // 模拟注册API调用
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        commit('ADD_NOTIFICATION', {
          type: 'success', 
          title: '注册成功',
          message: '账户创建成功，请登录'
        })
        
        return true
      } catch (error) {
        const errorMsg = error.message || '注册失败'
        commit('SET_ERROR', errorMsg)
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    logout({ commit }) {
      commit('LOGOUT')
      commit('ADD_NOTIFICATION', {
        type: 'info',
        title: '已退出登录',
        message: '您已安全退出系统'
      })
    },
    
    setUser({ commit }, user) {
      commit('SET_USER', user)
    },
    
    setTheme({ commit }, theme) {
      commit('SET_THEME', theme)
    },
    
    addNotification({ commit }, notification) {
      commit('ADD_NOTIFICATION', notification)
    },
    
    markNotificationRead({ commit }, id) {
      commit('MARK_NOTIFICATION_READ', id)
    },
    
    markAllNotificationsRead({ commit }) {
      commit('MARK_ALL_NOTIFICATIONS_READ')
    },
    
    removeNotification({ commit }, id) {
      commit('REMOVE_NOTIFICATION', id)
    },
    
    clearError({ commit }) {
      commit('SET_ERROR', null)
    }
  }
})