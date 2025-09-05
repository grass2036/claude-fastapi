<template>
  <div v-if="hasAccess">
    <slot></slot>
  </div>
  <div v-else-if="showFallback">
    <slot name="fallback">
      <v-alert
        type="warning"
        dense
        text
        class="ma-2"
      >
        <v-icon left>mdi-shield-off</v-icon>
        您没有权限访问此功能
      </v-alert>
    </slot>
  </div>
</template>

<script>
import { computed, toRef } from 'vue'
import { useStore } from 'vuex'
import { hasPermission, hasAnyPermission, hasAllPermissions } from '../utils/permissions'

export default {
  name: 'PermissionWrapper',
  props: {
    // 单个权限
    permission: {
      type: String,
      default: null
    },
    
    // 权限数组
    permissions: {
      type: Array,
      default: () => []
    },
    
    // 权限验证模式
    // 'any': 拥有任意一个权限即可 (default)
    // 'all': 必须拥有所有权限
    mode: {
      type: String,
      default: 'any',
      validator: (value) => ['any', 'all'].includes(value)
    },
    
    // 是否显示无权限提示
    showFallback: {
      type: Boolean,
      default: false
    },
    
    // 角色验证（可选）
    roles: {
      type: Array,
      default: () => []
    },
    
    // 是否反向验证（没有权限时显示）
    reverse: {
      type: Boolean,
      default: false
    }
  },
  
  setup(props) {
    const store = useStore()
    const user = computed(() => store.getters.user)
    
    const hasAccess = computed(() => {
      if (!user.value) {
        return props.reverse
      }
      
      let result = false
      
      // 角色验证
      if (props.roles.length > 0) {
        result = props.roles.includes(user.value.role)
        if (!result) {
          return props.reverse
        }
      }
      
      // 权限验证
      if (props.permission) {
        result = hasPermission(props.permission, user.value)
      } else if (props.permissions.length > 0) {
        if (props.mode === 'all') {
          result = hasAllPermissions(props.permissions, user.value)
        } else {
          result = hasAnyPermission(props.permissions, user.value)
        }
      } else {
        // 没有指定权限要求，默认允许访问
        result = true
      }
      
      return props.reverse ? !result : result
    })
    
    return {
      hasAccess
    }
  }
}
</script>

<style scoped>
/* 可以添加一些样式 */
</style>