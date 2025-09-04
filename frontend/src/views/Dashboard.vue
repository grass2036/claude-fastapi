<template>
  <v-app>
    <!-- Navigation Drawer -->
    <v-navigation-drawer
      v-model="drawer"
      app
      temporary
      width="280"
    >
      <v-list-item class="pa-4">
        <v-list-item-avatar>
          <v-icon size="40" color="primary">mdi-account-circle</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="text-h6">
            {{ user.name || '管理员' }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ user.email || 'admin@example.com' }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
          router
          exact
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider class="my-2"></v-divider>

        <v-list-item @click="logout">
          <v-list-item-icon>
            <v-icon color="red">mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="red--text">退出登录</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar
      app
      color="primary"
      dark
      elevate-on-scroll
    >
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      
      <v-toolbar-title class="d-flex align-center">
        <v-icon left>mdi-view-dashboard</v-icon>
        Claude FastAPI 管理系统
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Notifications -->
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-badge
              color="red"
              content="3"
              overlap
            >
              <v-icon>mdi-bell</v-icon>
            </v-badge>
          </v-btn>
        </template>
        <v-card width="300">
          <v-card-title>
            <v-icon left>mdi-bell</v-icon>
            通知消息
          </v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>新用户注册</v-list-item-title>
                  <v-list-item-subtitle>5分钟前</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>系统更新完成</v-list-item-title>
                  <v-list-item-subtitle>1小时前</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-menu>

      <!-- User Menu -->
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-avatar size="36">
              <v-icon>mdi-account</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>个人资料</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-icon>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>系统设置</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="logout">
            <v-list-item-icon>
              <v-icon color="red">mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title class="red--text">退出登录</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="pa-6">
        <router-view />
      </v-container>
    </v-main>

    <!-- Logout Confirmation Dialog -->
    <v-dialog v-model="logoutDialog" max-width="400">
      <v-card>
        <v-card-title>
          <v-icon left color="warning">mdi-help-circle</v-icon>
          确认退出
        </v-card-title>
        <v-card-text>
          您确定要退出登录吗？
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="logoutDialog = false">
            取消
          </v-btn>
          <v-btn color="red" text @click="confirmLogout">
            确认退出
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    const drawer = ref(false)
    const logoutDialog = ref(false)
    
    const user = computed(() => store.getters.user || {})
    
    const menuItems = [
      {
        title: '仪表盘',
        icon: 'mdi-view-dashboard',
        to: '/dashboard'
      },
      {
        title: '用户管理',
        icon: 'mdi-account-group',
        to: '/users'
      },
      {
        title: '系统监控',
        icon: 'mdi-monitor',
        to: '/monitoring'
      },
      {
        title: '日志管理',
        icon: 'mdi-text-box-multiple',
        to: '/logs'
      },
      {
        title: '系统设置',
        icon: 'mdi-cog',
        to: '/settings'
      }
    ]

    const logout = () => {
      logoutDialog.value = true
    }

    const confirmLogout = () => {
      store.dispatch('logout')
      logoutDialog.value = false
      router.push('/login')
    }

    return {
      drawer,
      logoutDialog,
      user,
      menuItems,
      logout,
      confirmLogout
    }
  }
}
</script>

<style scoped>
.v-navigation-drawer {
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);
}
</style>