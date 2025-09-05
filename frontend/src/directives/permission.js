/**
 * 权限控制指令
 * 用法：
 * v-permission="'user:create'" - 单个权限
 * v-permission="['user:create', 'user:edit']" - 多个权限（任意一个）
 * v-permission.all="['user:create', 'user:edit']" - 多个权限（全部需要）
 * v-permission:role="'admin'" - 角色权限
 */
import { hasPermission, hasAnyPermission, hasAllPermissions } from '../utils/permissions'
import store from '../store'

const permissionDirective = {
  mounted(el, binding) {
    checkPermission(el, binding)
  },
  
  updated(el, binding) {
    checkPermission(el, binding)
  }
}

function checkPermission(el, binding) {
  const { value, modifiers, arg } = binding
  const user = store.getters.user
  
  if (!user) {
    // 未登录用户隐藏元素
    hideElement(el)
    return
  }
  
  let hasAccess = false
  
  // 角色验证
  if (arg === 'role') {
    if (Array.isArray(value)) {
      hasAccess = value.includes(user.role)
    } else {
      hasAccess = user.role === value
    }
  }
  // 权限验证
  else {
    if (Array.isArray(value)) {
      // 多个权限
      if (modifiers.all) {
        hasAccess = hasAllPermissions(value, user)
      } else {
        hasAccess = hasAnyPermission(value, user)
      }
    } else {
      // 单个权限
      hasAccess = hasPermission(value, user)
    }
  }
  
  if (hasAccess) {
    showElement(el)
  } else {
    hideElement(el)
  }
}

function hideElement(el) {
  // 移除元素（保持DOM结构）
  if (!el._originalDisplay) {
    el._originalDisplay = el.style.display || ''
  }
  el.style.display = 'none'
  
  // 或者完全移除元素（根据需要选择）
  // if (el.parentNode) {
  //   el.parentNode.removeChild(el)
  // }
}

function showElement(el) {
  if (el._originalDisplay !== undefined) {
    el.style.display = el._originalDisplay
  } else {
    el.style.display = ''
  }
}

export default permissionDirective