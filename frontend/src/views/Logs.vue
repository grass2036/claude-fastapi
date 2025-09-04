<template>
  <div>
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 font-weight-bold primary--text">
          <v-icon left large color="primary">mdi-text-box-multiple</v-icon>
          日志管理
        </h1>
        <p class="text-subtitle-1 grey--text">查看和管理系统日志</p>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>功能开发中</v-card-title>
      <v-card-text>
        <v-alert type="info">
          日志管理功能正在开发中，将包括：
          <ul class="mt-2">
            <li>实时日志查看</li>
            <li>日志级别过滤</li>
            <li>日志搜索功能</li>
            <li>日志导出功能</li>
          </ul>
        </v-alert>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'Logs'
}
</script>