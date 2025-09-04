<template>
  <div class="dashboard-home">
    <!-- Welcome Section -->
    <v-row class="mb-6">
      <v-col>
        <v-card class="gradient-card" dark>
          <v-card-text class="pa-6">
            <v-row align="center">
              <v-col cols="12" md="8">
                <h1 class="text-h3 font-weight-bold mb-2">
                  欢迎回来！
                </h1>
                <p class="text-h6 mb-0 opacity-90">
                  今天是个美好的一天，让我们开始工作吧
                </p>
              </v-col>
              <v-col cols="12" md="4" class="text-center">
                <v-icon size="100" class="opacity-50">mdi-view-dashboard</v-icon>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Stats Cards -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <p class="text-caption grey--text mb-1">总用户数</p>
                <h2 class="text-h4 primary--text font-weight-bold">{{ stats.totalUsers }}</h2>
                <p class="text-caption success--text mb-0">
                  <v-icon small color="success">mdi-arrow-up</v-icon>
                  +12% 本月
                </p>
              </div>
              <v-avatar size="60" color="primary" class="ml-4">
                <v-icon size="30" color="white">mdi-account-group</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <p class="text-caption grey--text mb-1">活跃用户</p>
                <h2 class="text-h4 success--text font-weight-bold">{{ stats.activeUsers }}</h2>
                <p class="text-caption success--text mb-0">
                  <v-icon small color="success">mdi-arrow-up</v-icon>
                  +8% 本月
                </p>
              </div>
              <v-avatar size="60" color="success" class="ml-4">
                <v-icon size="30" color="white">mdi-account-check</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <p class="text-caption grey--text mb-1">系统负载</p>
                <h2 class="text-h4 warning--text font-weight-bold">{{ stats.systemLoad }}%</h2>
                <p class="text-caption error--text mb-0">
                  <v-icon small color="error">mdi-arrow-up</v-icon>
                  +3% 今日
                </p>
              </div>
              <v-avatar size="60" color="warning" class="ml-4">
                <v-icon size="30" color="white">mdi-cpu-64-bit</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card class="stat-card">
          <v-card-text>
            <div class="d-flex align-center">
              <div class="flex-grow-1">
                <p class="text-caption grey--text mb-1">存储空间</p>
                <h2 class="text-h4 info--text font-weight-bold">{{ stats.storage }}GB</h2>
                <p class="text-caption success--text mb-0">
                  <v-icon small color="success">mdi-arrow-down</v-icon>
                  -2% 本月
                </p>
              </div>
              <v-avatar size="60" color="info" class="ml-4">
                <v-icon size="30" color="white">mdi-harddisk</v-icon>
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- System Status and Quick Actions -->
    <v-row class="mb-6">
      <v-col cols="12" md="6">
        <v-card class="fill-height">
          <v-card-title>
            <v-icon left color="primary">mdi-heart-pulse</v-icon>
            系统状态
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-icon>
                  <v-icon :color="backendStatus === '正常' ? 'success' : 'error'">
                    {{ backendStatus === '正常' ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                  </v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>FastAPI 后端</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip 
                      :color="backendStatus === '正常' ? 'success' : 'error'" 
                      small
                      text-color="white"
                    >
                      {{ backendStatus }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-icon>
                  <v-icon :color="redisStatus === '正常' ? 'success' : 'error'">
                    {{ redisStatus === '正常' ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                  </v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Redis 缓存</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip 
                      :color="redisStatus === '正常' ? 'success' : 'error'" 
                      small
                      text-color="white"
                    >
                      {{ redisStatus }}
                    </v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-icon>
                  <v-icon color="success">mdi-check-circle</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>PostgreSQL 数据库</v-list-item-title>
                  <v-list-item-subtitle>
                    <v-chip color="success" small text-color="white">正常</v-chip>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-btn 
              color="primary" 
              @click="checkStatus"
              :loading="loading"
              outlined
            >
              <v-icon left>mdi-refresh</v-icon>
              刷新状态
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card class="fill-height">
          <v-card-title>
            <v-icon left color="primary">mdi-lightning-bolt</v-icon>
            快速操作
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6">
                <v-btn
                  color="success"
                  block
                  large
                  @click="testRedis"
                  :loading="testingRedis"
                  class="mb-3"
                >
                  <v-icon left>mdi-database</v-icon>
                  测试Redis
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn
                  color="primary"
                  block
                  large
                  @click="$router.push('/users')"
                  class="mb-3"
                >
                  <v-icon left>mdi-account-group</v-icon>
                  用户管理
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn
                  color="info"
                  block
                  large
                  @click="clearCache"
                  :loading="clearingCache"
                  class="mb-3"
                >
                  <v-icon left>mdi-cached</v-icon>
                  清理缓存
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6">
                <v-btn
                  color="warning"
                  block
                  large
                  @click="viewLogs"
                  class="mb-3"
                >
                  <v-icon left>mdi-text-box-multiple</v-icon>
                  查看日志
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Activity -->
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            <v-icon left color="primary">mdi-history</v-icon>
            最近活动
          </v-card-title>
          <v-card-text>
            <v-timeline dense>
              <v-timeline-item
                v-for="(activity, index) in recentActivity"
                :key="index"
                :color="activity.color"
                small
              >
                <v-row>
                  <v-col>
                    <strong>{{ activity.title }}</strong>
                    <div class="text-caption grey--text">{{ activity.time }}</div>
                    <p class="mb-0">{{ activity.description }}</p>
                  </v-col>
                </v-row>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="snackbar.show = false"
        >
          关闭
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Home',
  setup() {
    const backendStatus = ref('检查中...')
    const redisStatus = ref('检查中...')
    const loading = ref(false)
    const testingRedis = ref(false)
    const clearingCache = ref(false)
    
    const stats = ref({
      totalUsers: 1248,
      activeUsers: 892,
      systemLoad: 67,
      storage: 128
    })

    const recentActivity = ref([
      {
        title: '新用户注册',
        description: '用户 "张三" 完成注册',
        time: '5 分钟前',
        color: 'success'
      },
      {
        title: '系统更新',
        description: 'FastAPI 后端服务已更新至最新版本',
        time: '1 小时前',
        color: 'info'
      },
      {
        title: '缓存清理',
        description: 'Redis 缓存已自动清理过期数据',
        time: '2 小时前',
        color: 'warning'
      },
      {
        title: '用户登录',
        description: '管理员用户登录系统',
        time: '3 小时前',
        color: 'primary'
      }
    ])
    
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    const showMessage = (text, color = 'success') => {
      snackbar.value = {
        show: true,
        text,
        color
      }
    }

    const checkStatus = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/health')
        backendStatus.value = '正常'
        redisStatus.value = response.data.redis === 'healthy' ? '正常' : '异常'
        showMessage('系统状态检查完成')
      } catch (error) {
        backendStatus.value = '异常'
        redisStatus.value = '未知'
        showMessage('状态检查失败', 'error')
      } finally {
        loading.value = false
      }
    }

    const testRedis = async () => {
      testingRedis.value = true
      try {
        await axios.post('/api/cache/test')
        showMessage('Redis缓存测试成功')
      } catch (error) {
        showMessage('Redis测试失败', 'error')
      } finally {
        testingRedis.value = false
      }
    }

    const clearCache = async () => {
      clearingCache.value = true
      try {
        // 模拟清理缓存
        await new Promise(resolve => setTimeout(resolve, 1500))
        showMessage('缓存清理完成')
      } catch (error) {
        showMessage('缓存清理失败', 'error')
      } finally {
        clearingCache.value = false
      }
    }

    const viewLogs = () => {
      showMessage('日志查看功能开发中', 'info')
    }

    onMounted(() => {
      checkStatus()
    })

    return {
      backendStatus,
      redisStatus,
      loading,
      testingRedis,
      clearingCache,
      stats,
      recentActivity,
      snackbar,
      checkStatus,
      testRedis,
      clearCache,
      viewLogs
    }
  }
}
</script>

<style scoped>
.dashboard-home {
  padding: 24px;
}

.gradient-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.v-timeline {
  padding-top: 0;
}
</style>