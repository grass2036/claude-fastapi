# 用户认证系统 API 文档

## 概述

Claude FastAPI 用户认证系统提供完整的用户注册、登录、令牌管理和用户档案管理功能。基于 JWT (JSON Web Token) 实现无状态认证。

## 技术实现

### 安全特性
- **密码加密**: 使用 bcrypt 哈希算法
- **JWT 令牌**: HS256 算法签名
- **双令牌机制**: 访问令牌 + 刷新令牌
- **用户验证**: 多层次权限验证
- **输入验证**: Pydantic 数据验证

### 令牌策略
- **访问令牌**: 30分钟有效期，用于API访问
- **刷新令牌**: 7天有效期，用于获取新访问令牌
- **令牌类型验证**: 防止令牌类型混用

## API 接口详情

### 基础URL
```
http://localhost:8000/api/v1/auth
```

---

## 1. 用户注册

### `POST /register`

创建新用户账户。

**请求体**
```json
{
  "username": "johndoe",
  "email": "john@example.com", 
  "password": "strongpassword123",
  "confirm_password": "strongpassword123",
  "full_name": "John Doe",
  "phone": "13800138000",
  "bio": "Software Engineer"
}
```

**参数说明**
| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | ✅ | 用户名，3-50字符，唯一 |
| email | string | ✅ | 邮箱地址，唯一 |
| password | string | ✅ | 密码，最少8字符 |
| confirm_password | string | ✅ | 确认密码，必须与password一致 |
| full_name | string | ❌ | 全名，最多100字符 |
| phone | string | ❌ | 手机号，最多20字符 |
| bio | string | ❌ | 个人简介，最多500字符 |

**响应示例**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone": "13800138000",
  "bio": "Software Engineer",
  "avatar": null,
  "is_active": true,
  "is_verified": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "last_login_at": null
}
```

**错误响应**
- `400 Bad Request`: 用户名已存在、邮箱已存在、密码不匹配
- `500 Internal Server Error`: 服务器内部错误

---

## 2. 用户登录

### `POST /login`

用户登录并获取访问令牌。

**请求体**
```json
{
  "username": "johndoe",
  "password": "strongpassword123"
}
```

**参数说明**
| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | ✅ | 用户名或邮箱 |
| password | string | ✅ | 用户密码 |

**响应示例**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**响应字段说明**
| 字段 | 类型 | 描述 |
|------|------|------|
| access_token | string | 访问令牌，用于API调用 |
| refresh_token | string | 刷新令牌，用于获取新访问令牌 |
| token_type | string | 令牌类型，固定为"bearer" |
| expires_in | integer | 访问令牌过期时间（秒） |

**错误响应**
- `401 Unauthorized`: 用户名或密码错误

---

## 3. 刷新令牌

### `POST /refresh`

使用刷新令牌获取新的访问令牌。

**请求体**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**响应示例**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**错误响应**
- `401 Unauthorized`: 刷新令牌无效、过期或用户不存在

---

## 4. 获取用户档案

### `GET /profile`

获取当前登录用户的详细信息。

**请求头**
```
Authorization: Bearer <access_token>
```

**响应示例**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "13800138000",
    "bio": "Software Engineer",
    "avatar": "https://example.com/avatar.jpg",
    "is_active": true,
    "is_verified": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "last_login_at": "2023-01-01T00:00:00Z"
  }
}
```

**错误响应**
- `401 Unauthorized`: 访问令牌无效或过期

---

## 5. 更新用户档案

### `PUT /profile`

更新当前登录用户的个人信息。

**请求头**
```
Authorization: Bearer <access_token>
```

**请求体**
```json
{
  "full_name": "John Smith",
  "phone": "13900139000", 
  "bio": "Senior Software Engineer",
  "avatar": "https://example.com/new-avatar.jpg"
}
```

**参数说明**
| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| full_name | string | ❌ | 全名，最多100字符 |
| phone | string | ❌ | 手机号，最多20字符 |
| bio | string | ❌ | 个人简介，最多500字符 |
| avatar | string | ❌ | 头像URL，最多255字符 |

**响应示例**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Smith",
  "phone": "13900139000",
  "bio": "Senior Software Engineer",
  "avatar": "https://example.com/new-avatar.jpg",
  "is_active": true,
  "is_verified": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z",
  "last_login_at": "2023-01-01T00:00:00Z"
}
```

**错误响应**
- `401 Unauthorized`: 访问令牌无效或过期
- `404 Not Found`: 用户不存在

---

## 6. 修改密码

### `POST /change-password`

修改当前用户的密码。

**请求头**
```
Authorization: Bearer <access_token>
```

**请求体**
```json
{
  "current_password": "oldpassword123",
  "new_password": "newpassword456", 
  "confirm_new_password": "newpassword456"
}
```

**参数说明**
| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| current_password | string | ✅ | 当前密码 |
| new_password | string | ✅ | 新密码，最少8字符 |
| confirm_new_password | string | ✅ | 确认新密码 |

**响应示例**
```json
{
  "message": "密码修改成功"
}
```

**错误响应**
- `400 Bad Request`: 当前密码错误或新密码确认不匹配
- `401 Unauthorized`: 访问令牌无效或过期

---

## 7. 用户登出

### `POST /logout`

用户登出（客户端需要清除令牌）。

**请求头**
```
Authorization: Bearer <access_token>
```

**响应示例**
```json
{
  "message": "登出成功，请清除本地令牌"
}
```

**注意**: 由于JWT是无状态的，服务端无法主动使令牌失效，客户端需要主动删除存储的令牌。

---

## 认证流程

### 1. 用户注册流程
```
1. 用户提交注册信息
2. 服务器验证数据格式
3. 检查用户名和邮箱唯一性
4. 密码bcrypt加密
5. 创建用户记录
6. 返回用户信息
```

### 2. 用户登录流程
```
1. 用户提交登录凭据
2. 验证用户名/邮箱和密码
3. 生成访问令牌和刷新令牌
4. 更新最后登录时间
5. 返回令牌信息
```

### 3. 令牌刷新流程
```
1. 客户端提交刷新令牌
2. 验证刷新令牌有效性
3. 检查用户状态
4. 生成新的访问令牌和刷新令牌
5. 返回新令牌
```

## 安全最佳实践

### 令牌存储
- **访问令牌**: 存储在内存中，不要存储在localStorage
- **刷新令牌**: 可以存储在httpOnly cookie中
- **传输**: 始终使用HTTPS传输令牌

### 错误处理
- 不要在错误消息中泄露敏感信息
- 统一的错误响应格式
- 记录安全相关的错误日志

### 用户管理
- 定期清理过期令牌
- 监控异常登录行为
- 实现账户锁定机制

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 测试示例

### 使用curl测试

**注册用户**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "confirm_password": "testpassword123",
    "full_name": "Test User"
  }'
```

**用户登录**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }'
```

**获取用户档案**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/profile" \
  -H "Authorization: Bearer <your_access_token>"
```

### 使用Python requests测试

```python
import requests

# 注册用户
register_data = {
    "username": "testuser",
    "email": "test@example.com", 
    "password": "testpassword123",
    "confirm_password": "testpassword123",
    "full_name": "Test User"
}

response = requests.post("http://localhost:8000/api/v1/auth/register", json=register_data)
print(response.json())

# 用户登录
login_data = {
    "username": "testuser",
    "password": "testpassword123"
}

response = requests.post("http://localhost:8000/api/v1/auth/login", json=login_data)
token_data = response.json()
access_token = token_data["access_token"]

# 获取用户档案
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get("http://localhost:8000/api/v1/auth/profile", headers=headers)
print(response.json())
```

---

*本文档随着API更新而持续维护*