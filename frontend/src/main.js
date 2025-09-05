import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { initializeAuth, setupTokenAutoRefresh, setupVisibilityChangeListener } from './utils/auth'

// 权限控制相关
import PermissionWrapper from './components/PermissionWrapper.vue'
import permissionDirective from './directives/permission.js'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light'
  }
})

// 初始化应用
async function initializeApp() {
  const app = createApp(App)

  app.use(store)
  app.use(router)
  app.use(vuetify)

  // 注册全局权限组件和指令
  app.component('PermissionWrapper', PermissionWrapper)
  app.directive('permission', permissionDirective)

  // 初始化认证状态
  await initializeAuth()
  
  // 设置Token自动刷新
  setupTokenAutoRefresh()
  
  // 设置页面可见性监听
  setupVisibilityChangeListener()

  app.mount('#app')
}

// 启动应用
initializeApp().catch(error => {
  console.error('应用初始化失败:', error)
  // 即使初始化失败也要挂载应用
  const app = createApp(App)
  app.use(store)
  app.use(router)
  app.use(vuetify)
  
  // 注册全局权限组件和指令
  app.component('PermissionWrapper', PermissionWrapper)
  app.directive('permission', permissionDirective)
  
  app.mount('#app')
})