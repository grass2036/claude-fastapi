<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="5">
        <v-card class="elevation-12">
          <v-card-title class="text-center success white--text py-6">
            <div class="d-flex align-center justify-center">
              <v-icon large left color="white">mdi-account-plus</v-icon>
              <span class="text-h5">用户注册</span>
            </div>
          </v-card-title>
          
          <v-card-text class="pa-6">
            <v-form ref="form" v-model="valid" @submit.prevent="register">
              <v-text-field
                v-model="name"
                :rules="nameRules"
                label="姓名"
                prepend-icon="mdi-account"
                outlined
                class="mb-3"
              ></v-text-field>

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

              <v-text-field
                v-model="confirmPassword"
                :rules="confirmPasswordRules"
                label="确认密码"
                prepend-icon="mdi-lock-check"
                :type="showConfirmPassword ? 'text' : 'password'"
                :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showConfirmPassword = !showConfirmPassword"
                outlined
                class="mb-3"
              ></v-text-field>

              <v-select
                v-model="role"
                :items="roleOptions"
                label="用户角色"
                prepend-icon="mdi-account-cog"
                outlined
                class="mb-3"
              ></v-select>

              <v-checkbox
                v-model="agreeToTerms"
                :rules="termsRules"
                color="success"
                class="mb-3"
              >
                <template v-slot:label>
                  <div>
                    我同意
                    <v-btn text color="success" small class="pa-0">
                      用户协议
                    </v-btn>
                    和
                    <v-btn text color="success" small class="pa-0">
                      隐私政策
                    </v-btn>
                  </div>
                </template>
              </v-checkbox>

              <v-btn
                type="submit"
                color="success"
                block
                large
                :loading="loading"
                :disabled="!valid"
                class="mb-3"
              >
                <v-icon left>mdi-account-plus</v-icon>
                注册
              </v-btn>

              <v-divider class="my-4"></v-divider>
              
              <div class="text-center">
                <span class="text-body-2">已有账户？</span>
                <v-btn text color="success" @click="goToLogin">
                  立即登录
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

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    
    const form = ref(null)
    const valid = ref(false)
    const loading = ref(false)
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const agreeToTerms = ref(false)
    
    const name = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const role = ref('user')
    
    const roleOptions = [
      { title: '普通用户', value: 'user' },
      { title: '管理员', value: 'admin' },
      { title: '编辑员', value: 'editor' }
    ]
    
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    const nameRules = [
      v => !!v || '姓名不能为空',
      v => (v && v.length >= 2) || '姓名至少2个字符'
    ]

    const emailRules = [
      v => !!v || '邮箱不能为空',
      v => /.+@.+\..+/.test(v) || '邮箱格式不正确'
    ]

    const passwordRules = [
      v => !!v || '密码不能为空',
      v => (v && v.length >= 6) || '密码至少6位',
      v => /(?=.*[a-z])(?=.*[A-Z])/.test(v) || '密码需包含大小写字母'
    ]

    const confirmPasswordRules = [
      v => !!v || '请确认密码',
      v => v === password.value || '两次输入的密码不一致'
    ]

    const termsRules = [
      v => !!v || '请同意用户协议和隐私政策'
    ]

    const showMessage = (text, color = 'success') => {
      snackbar.value = {
        show: true,
        text,
        color
      }
    }

    const register = async () => {
      if (!valid.value) return
      
      loading.value = true
      try {
        // 模拟注册API调用
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        showMessage('注册成功！请登录')
        
        setTimeout(() => {
          router.push('/login')
        }, 1500)
        
      } catch (error) {
        showMessage('注册失败，请稍后重试', 'error')
      } finally {
        loading.value = false
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      form,
      valid,
      loading,
      showPassword,
      showConfirmPassword,
      agreeToTerms,
      name,
      email,
      password,
      confirmPassword,
      role,
      roleOptions,
      nameRules,
      emailRules,
      passwordRules,
      confirmPasswordRules,
      termsRules,
      snackbar,
      register,
      goToLogin
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.v-card {
  border-radius: 15px;
}
</style>