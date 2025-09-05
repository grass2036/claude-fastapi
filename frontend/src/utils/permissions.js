/**
 * 权限管理工具
 */
import store from '../store'

// 权限定义
export const PERMISSIONS = {
  // 用户管理权限
  USER_VIEW: 'user:view',
  USER_CREATE: 'user:create', 
  USER_EDIT: 'user:edit',
  USER_DELETE: 'user:delete',
  USER_STATUS: 'user:status',
  
  // 系统管理权限
  SYSTEM_CONFIG: 'system:config',
  SYSTEM_LOGS: 'system:logs',
  SYSTEM_MONITOR: 'system:monitor',
  
  // 部门管理权限
  DEPT_VIEW: 'dept:view',
  DEPT_CREATE: 'dept:create',
  DEPT_EDIT: 'dept:edit',
  DEPT_DELETE: 'dept:delete',
  
  // 角色管理权限
  ROLE_VIEW: 'role:view',
  ROLE_CREATE: 'role:create',
  ROLE_EDIT: 'role:edit',
  ROLE_DELETE: 'role:delete'
}

// 角色权限映射
export const ROLE_PERMISSIONS = {
  'admin': [
    // 管理员拥有所有权限
    ...Object.values(PERMISSIONS)
  ],
  'manager': [
    // 管理员权限（除了系统配置）
    PERMISSIONS.USER_VIEW,
    PERMISSIONS.USER_CREATE,
    PERMISSIONS.USER_EDIT,
    PERMISSIONS.USER_STATUS,
    PERMISSIONS.DEPT_VIEW,
    PERMISSIONS.DEPT_CREATE,
    PERMISSIONS.DEPT_EDIT,
    PERMISSIONS.ROLE_VIEW,
    PERMISSIONS.SYSTEM_LOGS,
    PERMISSIONS.SYSTEM_MONITOR
  ],
  'user': [
    // 普通用户权限
    PERMISSIONS.USER_VIEW,
    PERMISSIONS.DEPT_VIEW,
    PERMISSIONS.SYSTEM_MONITOR
  ]
}

/**
 * 检查用户是否有指定权限
 * @param {string} permission - 权限标识
 * @param {Object} user - 用户对象，如果不传则从store获取
 * @returns {boolean} 是否有权限
 */
export function hasPermission(permission, user = null) {
  if (!user) {
    user = store.getters.user
  }
  
  if (!user) {
    return false
  }
  
  // 超级管理员拥有所有权限
  if (user.role === 'admin' || user.is_superuser) {
    return true
  }
  
  // 检查角色权限
  const rolePermissions = ROLE_PERMISSIONS[user.role] || []
  return rolePermissions.includes(permission)
}

/**
 * 检查用户是否有任意一个权限
 * @param {Array<string>} permissions - 权限数组
 * @param {Object} user - 用户对象
 * @returns {boolean} 是否有权限
 */
export function hasAnyPermission(permissions, user = null) {
  return permissions.some(permission => hasPermission(permission, user))
}

/**
 * 检查用户是否拥有所有权限
 * @param {Array<string>} permissions - 权限数组
 * @param {Object} user - 用户对象
 * @returns {boolean} 是否有权限
 */
export function hasAllPermissions(permissions, user = null) {
  return permissions.every(permission => hasPermission(permission, user))
}

/**
 * 获取用户的所有权限
 * @param {Object} user - 用户对象
 * @returns {Array<string>} 权限数组
 */
export function getUserPermissions(user = null) {
  if (!user) {
    user = store.getters.user
  }
  
  if (!user) {
    return []
  }
  
  // 超级管理员拥有所有权限
  if (user.role === 'admin' || user.is_superuser) {
    return Object.values(PERMISSIONS)
  }
  
  return ROLE_PERMISSIONS[user.role] || []
}

/**
 * 检查是否是管理员
 * @param {Object} user - 用户对象
 * @returns {boolean} 是否是管理员
 */
export function isAdmin(user = null) {
  if (!user) {
    user = store.getters.user
  }
  
  return user && (user.role === 'admin' || user.is_superuser)
}

/**
 * 检查是否是当前用户
 * @param {number} userId - 用户ID
 * @param {Object} user - 用户对象
 * @returns {boolean} 是否是当前用户
 */
export function isCurrentUser(userId, user = null) {
  if (!user) {
    user = store.getters.user
  }
  
  return user && user.id === userId
}

/**
 * 权限守卫 - 用于路由守卫
 * @param {string|Array<string>} permissions - 需要的权限
 * @param {Function} next - 路由next函数
 * @returns {boolean} 是否通过
 */
export function permissionGuard(permissions, next) {
  const user = store.getters.user
  
  if (!user) {
    next('/login')
    return false
  }
  
  let hasAccess = false
  
  if (Array.isArray(permissions)) {
    hasAccess = hasAnyPermission(permissions, user)
  } else {
    hasAccess = hasPermission(permissions, user)
  }
  
  if (!hasAccess) {
    // 可以跳转到无权限页面或显示提示
    console.warn('用户无权访问:', permissions)
    next('/unauthorized')
    return false
  }
  
  return true
}

export default {
  PERMISSIONS,
  ROLE_PERMISSIONS,
  hasPermission,
  hasAnyPermission,
  hasAllPermissions,
  getUserPermissions,
  isAdmin,
  isCurrentUser,
  permissionGuard
}