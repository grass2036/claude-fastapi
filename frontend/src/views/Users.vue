<template>
  <div>
    <!-- Page Header -->
    <v-row class="mb-4">
      <v-col>
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h4 font-weight-bold primary--text">
              <v-icon left large color="primary">mdi-account-group</v-icon>
              用户管理
            </h1>
            <p class="text-subtitle-1 grey--text">管理系统用户信息</p>
          </div>
          <v-btn
            color="primary"
            large
            @click="openAddDialog"
          >
            <v-icon left>mdi-plus</v-icon>
            添加用户
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Filters and Search -->
    <v-card class="mb-4">
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              v-model="search"
              label="搜索用户"
              prepend-inner-icon="mdi-magnify"
              outlined
              dense
              clearable
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="roleFilter"
              :items="roleOptions"
              label="筛选角色"
              outlined
              dense
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-select
              v-model="statusFilter"
              :items="statusOptions"
              label="筛选状态"
              outlined
              dense
              clearable
            ></v-select>
          </v-col>
          <v-col cols="12" md="2">
            <v-btn
              color="primary"
              outlined
              block
              @click="refreshUsers"
              :loading="loading"
            >
              <v-icon left>mdi-refresh</v-icon>
              刷新
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Users Table -->
    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        :search="search"
        class="elevation-1"
        :items-per-page="10"
        :footer-props="{
          'items-per-page-text': '每页显示',
          'items-per-page-options': [5, 10, 25, 50]
        }"
      >
        <!-- Avatar Column -->
        <template v-slot:item.avatar="{ item }">
          <v-avatar size="40" class="my-2">
            <v-img v-if="item.avatar" :src="item.avatar"></v-img>
            <v-icon v-else color="grey">mdi-account</v-icon>
          </v-avatar>
        </template>

        <!-- Role Column -->
        <template v-slot:item.role="{ item }">
          <v-chip
            :color="getRoleColor(item.role)"
            small
            text-color="white"
          >
            {{ getRoleText(item.role) }}
          </v-chip>
        </template>

        <!-- Status Column -->
        <template v-slot:item.is_active="{ item }">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            small
            text-color="white"
          >
            <v-icon left small>
              {{ item.is_active ? 'mdi-check' : 'mdi-close' }}
            </v-icon>
            {{ item.is_active ? '活跃' : '禁用' }}
          </v-chip>
        </template>

        <!-- Created At Column -->
        <template v-slot:item.created_at="{ item }">
          <span>{{ formatDate(item.created_at) }}</span>
        </template>

        <!-- Actions Column -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex">
            <v-btn
              icon
              small
              color="primary"
              @click="viewUser(item)"
            >
              <v-icon>mdi-eye</v-icon>
            </v-btn>
            <v-btn
              icon
              small
              color="warning"
              @click="editUser(item)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              icon
              small
              :color="item.is_active ? 'error' : 'success'"
              @click="toggleUserStatus(item)"
            >
              <v-icon>{{ item.is_active ? 'mdi-account-off' : 'mdi-account-check' }}</v-icon>
            </v-btn>
            <v-btn
              icon
              small
              color="error"
              @click="deleteUser(item)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit User Dialog -->
    <v-dialog v-model="dialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEdit ? '编辑用户' : '添加用户' }}</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editedUser.name"
                  :rules="nameRules"
                  label="姓名 *"
                  outlined
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editedUser.email"
                  :rules="emailRules"
                  label="邮箱 *"
                  type="email"
                  outlined
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="editedUser.phone"
                  label="手机号"
                  outlined
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="editedUser.role"
                  :items="roleOptions"
                  label="用户角色 *"
                  outlined
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" v-if="!isEdit">
                <v-text-field
                  v-model="editedUser.password"
                  :rules="passwordRules"
                  label="密码 *"
                  type="password"
                  outlined
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedUser.bio"
                  label="个人简介"
                  outlined
                  rows="3"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-switch
                  v-model="editedUser.is_active"
                  label="启用用户"
                  color="success"
                ></v-switch>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">
            取消
          </v-btn>
          <v-btn
            color="primary"
            :loading="saving"
            @click="saveUser"
          >
            {{ isEdit ? '更新' : '创建' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>
          <v-icon left color="error">mdi-delete</v-icon>
          确认删除
        </v-card-title>
        <v-card-text>
          确定要删除用户 <strong>{{ userToDelete?.name }}</strong> 吗？此操作不可恢复。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog = false">
            取消
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            @click="confirmDelete"
          >
            删除
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
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
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'Users',
  setup() {
    const search = ref('')
    const roleFilter = ref(null)
    const statusFilter = ref(null)
    const loading = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    const dialog = ref(false)
    const deleteDialog = ref(false)
    const valid = ref(false)
    const isEdit = ref(false)
    const form = ref(null)
    
    const users = ref([
      {
        id: 1,
        name: '张三',
        email: 'zhangsan@example.com',
        phone: '13800138001',
        role: 'admin',
        is_active: true,
        bio: '系统管理员',
        created_at: '2024-01-01T10:00:00Z',
        avatar: null
      },
      {
        id: 2,
        name: '李四',
        email: 'lisi@example.com',
        phone: '13800138002',
        role: 'user',
        is_active: true,
        bio: '普通用户',
        created_at: '2024-01-02T10:00:00Z',
        avatar: null
      },
      {
        id: 3,
        name: '王五',
        email: 'wangwu@example.com',
        phone: '13800138003',
        role: 'editor',
        is_active: false,
        bio: '内容编辑',
        created_at: '2024-01-03T10:00:00Z',
        avatar: null
      }
    ])

    const editedUser = ref({
      id: null,
      name: '',
      email: '',
      phone: '',
      role: 'user',
      password: '',
      bio: '',
      is_active: true
    })

    const userToDelete = ref(null)
    
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    const headers = [
      { text: '头像', value: 'avatar', sortable: false, width: '80px' },
      { text: '姓名', value: 'name' },
      { text: '邮箱', value: 'email' },
      { text: '手机', value: 'phone' },
      { text: '角色', value: 'role' },
      { text: '状态', value: 'is_active' },
      { text: '创建时间', value: 'created_at' },
      { text: '操作', value: 'actions', sortable: false, width: '200px' }
    ]

    const roleOptions = [
      { title: '管理员', value: 'admin' },
      { title: '编辑员', value: 'editor' },
      { title: '普通用户', value: 'user' }
    ]

    const statusOptions = [
      { title: '活跃', value: true },
      { title: '禁用', value: false }
    ]

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
      v => (v && v.length >= 6) || '密码至少6位'
    ]

    const filteredUsers = computed(() => {
      let filtered = users.value

      if (roleFilter.value !== null) {
        filtered = filtered.filter(user => user.role === roleFilter.value)
      }

      if (statusFilter.value !== null) {
        filtered = filtered.filter(user => user.is_active === statusFilter.value)
      }

      return filtered
    })

    const getRoleColor = (role) => {
      const colors = {
        'admin': 'red',
        'editor': 'orange',
        'user': 'blue'
      }
      return colors[role] || 'grey'
    }

    const getRoleText = (role) => {
      const texts = {
        'admin': '管理员',
        'editor': '编辑员',
        'user': '普通用户'
      }
      return texts[role] || role
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleString('zh-CN')
    }

    const showMessage = (text, color = 'success') => {
      snackbar.value = {
        show: true,
        text,
        color
      }
    }

    const refreshUsers = async () => {
      loading.value = true
      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000))
      loading.value = false
      showMessage('用户列表已刷新')
    }

    const openAddDialog = () => {
      isEdit.value = false
      editedUser.value = {
        id: null,
        name: '',
        email: '',
        phone: '',
        role: 'user',
        password: '',
        bio: '',
        is_active: true
      }
      dialog.value = true
    }

    const editUser = (user) => {
      isEdit.value = true
      editedUser.value = { ...user }
      dialog.value = true
    }

    const viewUser = (user) => {
      // 实现查看用户详情
      showMessage('查看用户详情功能待实现', 'info')
    }

    const closeDialog = () => {
      dialog.value = false
      if (form.value) {
        form.value.reset()
      }
    }

    const saveUser = async () => {
      if (!valid.value) return

      saving.value = true
      
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        if (isEdit.value) {
          const index = users.value.findIndex(u => u.id === editedUser.value.id)
          if (index !== -1) {
            users.value[index] = { ...editedUser.value }
          }
          showMessage('用户更新成功')
        } else {
          const newUser = {
            ...editedUser.value,
            id: users.value.length + 1,
            created_at: new Date().toISOString(),
            avatar: null
          }
          delete newUser.password // 实际项目中不应该在前端存储密码
          users.value.push(newUser)
          showMessage('用户创建成功')
        }
        
        closeDialog()
      } catch (error) {
        showMessage('操作失败，请稍后重试', 'error')
      } finally {
        saving.value = false
      }
    }

    const toggleUserStatus = async (user) => {
      try {
        user.is_active = !user.is_active
        showMessage(`用户已${user.is_active ? '启用' : '禁用'}`)
      } catch (error) {
        showMessage('操作失败，请稍后重试', 'error')
      }
    }

    const deleteUser = (user) => {
      userToDelete.value = user
      deleteDialog.value = true
    }

    const confirmDelete = async () => {
      deleting.value = true
      
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        const index = users.value.findIndex(u => u.id === userToDelete.value.id)
        if (index !== -1) {
          users.value.splice(index, 1)
        }
        
        showMessage('用户删除成功')
        deleteDialog.value = false
      } catch (error) {
        showMessage('删除失败，请稍后重试', 'error')
      } finally {
        deleting.value = false
      }
    }

    onMounted(() => {
      refreshUsers()
    })

    return {
      search,
      roleFilter,
      statusFilter,
      loading,
      saving,
      deleting,
      dialog,
      deleteDialog,
      valid,
      isEdit,
      form,
      users,
      editedUser,
      userToDelete,
      snackbar,
      headers,
      roleOptions,
      statusOptions,
      nameRules,
      emailRules,
      passwordRules,
      filteredUsers,
      getRoleColor,
      getRoleText,
      formatDate,
      refreshUsers,
      openAddDialog,
      editUser,
      viewUser,
      closeDialog,
      saveUser,
      toggleUserStatus,
      deleteUser,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.v-data-table {
  border-radius: 10px;
}
</style>