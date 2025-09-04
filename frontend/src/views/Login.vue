<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center primary white--text py-6">
            <div class="d-flex align-center justify-center">
              <v-icon large left color="white">mdi-account-circle</v-icon>
              <span class="text-h5">用户登录</span>
            </div>
          </v-card-title>
          
          <v-card-text class="pa-6">
            <v-form ref="form" v-model="valid" @submit.prevent="login">
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="邮箱"
                prepend-icon="mdi-email"
                type="email"
                outlined
                class="mb-3"
              ></v-text-field>

              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="密码"
                prepend-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                outlined
                class="mb-3"
              ></v-text-field>

              <v-row class="mb-3">
                <v-col cols="6">
                  <v-checkbox
                    v-model="rememberMe"
                    label="记住我"
                    color="primary"
                  ></v-checkbox>
                </v-col>
                <v-col cols="6" class="text-right">
                  <v-btn text color="primary" small>
                    忘记密码？
                  </v-btn>
                </v-col>
              </v-row>

              <v-btn
                type="submit"
                color="primary"
                block
                large
                :loading="loading"
                :disabled="!valid"
                class="mb-3"
              >
                <v-icon left>mdi-login</v-icon>
                登录
              </v-btn>

              <v-divider class="my-4"></v-divider>
              
              <div class="text-center">
                <span class="text-body-2">还没有账户？</span>
                <v-btn text color="primary" @click="goToRegister">
                  立即注册
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="3000"
    >
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.show = false">
          关闭
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    const form = ref(null)
    const valid = ref(false)
    const loading = ref(false)
    const showPassword = ref(false)
    const rememberMe = ref(false)
    
    const email = ref('')
    const password = ref('')
    
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    const emailRules = [
      v => !!v || '邮箱不能为空',
      v => /.+@.+\..+/.test(v) || '邮箱格式不正确'
    ]

    const passwordRules = [
      v => !!v || '密码不能为空',
      v => (v && v.length >= 6) || '密码至少6位'
    ]

    const showMessage = (text, color = 'success') => {
      snackbar.value = {
        show: true,
        text,
        color
      }
    }

    const login = async () => {
      if (!valid.value) return
      
      loading.value = true
      try {
        // 模拟登录API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 这里应该调用真实的登录API
        const userData = {
          id: 1,
          email: email.value,
          name: '管理员',
          role: 'admin'
        }
        
        store.dispatch('setUser', userData)
        showMessage('登录成功！')
        
        setTimeout(() => {
          router.push('/dashboard')
        }, 1000)
        
      } catch (error) {
        showMessage('登录失败，请检查邮箱和密码', 'error')
      } finally {
        loading.value = false
      }
    }

    const goToRegister = () => {
      router.push('/register')
    }

    return {
      form,
      valid,
      loading,
      showPassword,
      rememberMe,
      email,
      password,
      emailRules,
      passwordRules,
      snackbar,
      login,
      goToRegister
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.v-card {
  border-radius: 15px;
}
</style>