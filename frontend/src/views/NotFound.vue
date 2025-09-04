<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center" class="fill-height">
      <v-col cols="12" md="6" class="text-center">
        <v-icon size="150" color="grey lighten-1" class="mb-4">
          mdi-alert-circle-outline
        </v-icon>
        <h1 class="text-h2 font-weight-bold grey--text mb-4">404</h1>
        <h2 class="text-h4 mb-4">页面未找到</h2>
        <p class="text-body-1 grey--text mb-6">
          抱歉，您访问的页面不存在或已被删除。
        </p>
        <v-btn
          color="primary"
          large
          @click="$router.push('/dashboard')"
        >
          <v-icon left>mdi-home</v-icon>
          返回首页
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>