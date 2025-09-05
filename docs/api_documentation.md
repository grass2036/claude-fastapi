# Claude FastAPI 接口文档

## 概述

这是一个基于 FastAPI 的后端管理系统，包含用户认证、用户管理、缓存管理等功能。

## 服务地址

- **开发环境**: http://localhost:8000
- **Swagger 文档**: http://localhost:8000/docs
- **ReDoc 文档**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 接口分组

### 1. General (通用接口)
通用接口：健康检查、系统状态等

### 2. Authentication (用户认证)
用户认证：注册、登录、令牌管理

### 3. User Management (用户管理)
用户管理：档案管理、密码修改等

### 4. Cache (缓存管理)
缓存管理：Redis缓存操作

## 详细接口说明

### General 通用接口

#### GET /
- **功能**: 应用根路径，返回基本信息
- **响应**: 200 - 成功返回应用信息

#### GET /health
- **功能**: 检查应用和依赖服务的健康状态
- **响应**: 
  - 200 - 应用和Redis连接正常
  - 503 - Redis连接异常

### Authentication 用户认证

#### POST /api/v1/auth/register
- **功能**: 用户注册，创建新用户账户
- **请求体**: UserCreate (包含用户名、邮箱、密码等)
- **响应**: 
  - 201 - 用户注册成功
  - 400 - 注册数据验证失败
  - 422 - 输入数据格式错误

#### POST /api/v1/auth/login
- **功能**: 用户登录并获取访问令牌
- **请求体**: UserLogin (用户名和密码)
- **响应**: 
  - 200 - 登录成功，返回访问令牌
  - 401 - 用户名或密码错误
  - 422 - 输入数据格式错误

#### POST /api/v1/auth/refresh
- **功能**: 使用刷新令牌获取新的访问令牌
- **请求体**: TokenRefresh (刷新令牌)
- **响应**: 
  - 200 - 令牌刷新成功
  - 401 - 刷新令牌无效或已过期
  - 422 - 输入数据格式错误

#### POST /api/v1/auth/change-password
- **功能**: 修改当前用户密码
- **权限**: 需要有效的访问令牌
- **请求体**: UserChangePassword
- **响应**: 
  - 200 - 密码修改成功
  - 400 - 当前密码错误或新密码不匹配
  - 401 - 未授权访问
  - 422 - 输入数据格式错误

#### POST /api/v1/auth/logout
- **功能**: 用户登出
- **权限**: 需要有效的访问令牌
- **响应**: 
  - 200 - 登出成功
  - 401 - 未授权访问

### User Management 用户管理

#### GET /api/v1/users/me
- **功能**: 获取当前用户信息
- **权限**: 需要有效的访问令牌
- **响应**: 
  - 200 - 成功获取用户信息
  - 401 - 未授权访问

#### PUT /api/v1/users/me
- **功能**: 更新当前用户信息
- **权限**: 需要有效的访问令牌
- **请求体**: UserUpdate
- **响应**: 
  - 200 - 成功更新用户信息
  - 401 - 未授权访问
  - 422 - 输入数据验证失败

#### GET /api/v1/users/{user_id}
- **功能**: 管理员获取指定用户信息
- **权限**: 超级管理员权限
- **响应**: 
  - 200 - 成功获取用户信息
  - 401 - 未授权访问
  - 403 - 权限不足
  - 404 - 用户不存在

#### POST /api/v1/users/{user_id}/activate
- **功能**: 管理员激活指定用户账户
- **权限**: 超级管理员权限
- **响应**: 
  - 200 - 成功激活用户
  - 401 - 未授权访问
  - 403 - 权限不足
  - 404 - 用户不存在

#### POST /api/v1/users/{user_id}/deactivate
- **功能**: 管理员停用指定用户账户
- **权限**: 超级管理员权限
- **响应**: 
  - 200 - 成功停用用户
  - 401 - 未授权访问
  - 403 - 权限不足
  - 404 - 用户不存在

### Cache 缓存管理

#### POST /cache/test
- **功能**: 测试Redis缓存功能是否正常工作
- **响应**: 
  - 200 - Redis缓存功能正常
  - 500 - Redis连接或操作失败

#### GET /cache/{key}
- **功能**: 根据键获取Redis缓存值
- **参数**: key - 缓存键名
- **响应**: 
  - 200 - 成功获取缓存值
  - 404 - 指定的键不存在
  - 500 - Redis连接或操作失败

#### POST /cache/{key}
- **功能**: 设置Redis缓存键值对，带有过期时间
- **参数**: key - 缓存键名
- **请求体**: data (dict), ttl (int, 可选，默认3600秒)
- **响应**: 
  - 200 - 成功设置缓存
  - 500 - Redis连接或操作失败

## 认证方式

系统使用 JWT Bearer Token 进行认证：

1. 通过 `/api/v1/auth/login` 获取访问令牌
2. 在请求头中添加：`Authorization: Bearer <access_token>`
3. 访问令牌有效期：30分钟
4. 刷新令牌有效期：7天
5. 可通过 `/api/v1/auth/refresh` 刷新访问令牌

## 数据模型

### 用户模型 (User)
- id: 用户ID
- username: 用户名 (3-50字符)
- email: 邮箱地址
- full_name: 全名 (可选)
- phone: 手机号 (可选)
- bio: 个人简介 (可选)
- avatar: 头像URL (可选)
- is_active: 是否激活
- is_verified: 是否验证邮箱
- is_superuser: 是否超级用户
- created_at: 创建时间
- updated_at: 更新时间
- last_login_at: 最后登录时间

### 令牌模型 (Token)
- access_token: 访问令牌
- refresh_token: 刷新令牌
- token_type: 令牌类型 (bearer)
- expires_in: 过期时间 (秒)

## 错误处理

系统统一使用HTTP状态码：

- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权访问
- 403: 权限不足
- 404: 资源不存在
- 422: 数据验证失败
- 500: 服务器内部错误
- 503: 服务不可用

## 开发说明

### 启动服务
```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn backend.main:app --reload --port 8000
```

### 访问文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 测试API
可以使用 Swagger UI 直接测试API，或使用 curl/Postman 等工具。

示例测试流程：
1. 注册用户: POST /api/v1/auth/register
2. 登录获取令牌: POST /api/v1/auth/login
3. 使用令牌访问保护接口: GET /api/v1/users/me