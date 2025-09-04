<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统状态</span>
          </template>
          <p>后端状态: {{ backendStatus }}</p>
          <p>Redis状态: {{ redisStatus }}</p>
          <el-button @click="checkStatus" type="primary">检查状态</el-button>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快速操作</span>
          </template>
          <el-button @click="testRedis" type="success">测试Redis缓存</el-button>
        </el-card>
      </el-col>
    </el-row>
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

    const checkStatus = async () => {
      try {
        const response = await axios.get('/api/health')
        backendStatus.value = '正常'
      } catch (error) {
        backendStatus.value = '异常'
      }
    }

    const testRedis = async () => {
      try {
        await axios.post('/api/cache/test')
        ElMessage.success('Redis测试成功')
      } catch (error) {
        ElMessage.error('Redis测试失败')
      }
    }

    onMounted(() => {
      checkStatus()
    })

    return {
      backendStatus,
      redisStatus,
      checkStatus,
      testRedis
    }
  }
}
</script>