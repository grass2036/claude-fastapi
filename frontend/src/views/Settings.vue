<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold primary--text">
          <v-icon left large color="primary">mdi-cog</v-icon>
          系统设置
        </h1>
        <p class="text-subtitle-1 grey--text">配置系统参数和个人偏好</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>主题设置</v-card-title>
          <v-card-text>
            <v-switch
              v-model="darkMode"
              label="深色模式"
              color="primary"
              @change="toggleDarkMode"
            ></v-switch>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>通知设置</v-card-title>
          <v-card-text>
            <v-switch
              v-model="emailNotifications"
              label="邮件通知"
              color="primary"
            ></v-switch>
            <v-switch
              v-model="pushNotifications"
              label="推送通知"
              color="primary"
            ></v-switch>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col>
        <v-card>
          <v-card-title>更多功能</v-card-title>
          <v-card-text>
            <v-alert type="info">
              更多系统设置功能正在开发中，敬请期待！
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Settings',
  setup() {
    const darkMode = ref(false)
    const emailNotifications = ref(true)
    const pushNotifications = ref(false)

    const toggleDarkMode = (value) => {
      // 这里可以实现切换主题的逻辑
      console.log('Dark mode:', value)
    }

    return {
      darkMode,
      emailNotifications,
      pushNotifications,
      toggleDarkMode
    }
  }
}
</script>