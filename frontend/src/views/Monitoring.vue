<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold primary--text">
          <v-icon left large color="primary">mdi-monitor</v-icon>
          系统监控
        </h1>
        <p class="text-subtitle-1 grey--text">实时监控系统性能和资源使用情况</p>
      </v-col>
    </v-row>

    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>CPU 使用率</v-card-title>
          <v-card-text>
            <v-progress-linear
              :value="cpuUsage"
              color="primary"
              height="20"
              class="mb-2"
            >
              <strong>{{ cpuUsage }}%</strong>
            </v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>内存使用率</v-card-title>
          <v-card-text>
            <v-progress-linear
              :value="memoryUsage"
              color="success"
              height="20"
              class="mb-2"
            >
              <strong>{{ memoryUsage }}%</strong>
            </v-progress-linear>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>功能开发中</v-card-title>
      <v-card-text>
        <v-alert type="info">
          系统监控功能正在开发中，敬请期待更多功能！
        </v-alert>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'Monitoring',
  setup() {
    const cpuUsage = ref(45)
    const memoryUsage = ref(68)
    let interval = null

    const updateStats = () => {
      cpuUsage.value = Math.floor(Math.random() * 100)
      memoryUsage.value = Math.floor(Math.random() * 100)
    }

    onMounted(() => {
      interval = setInterval(updateStats, 3000)
    })

    onUnmounted(() => {
      if (interval) {
        clearInterval(interval)
      }
    })

    return {
      cpuUsage,
      memoryUsage
    }
  }
}
</script>