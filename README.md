# Claude FastAPI

一个基于 FastAPI + Vue.js 的全栈企业级应用，使用 Docker 微服务架构。

## 🚀 快速开始

### 使用 Docker Compose（推荐）
```bash
# 启动所有服务
make docker-up

# 或直接使用 docker-compose
docker-compose up -d
```

### 本地开发
```bash
# 后端开发（带热重载）
make run
# 或
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 前端开发
cd frontend && npm run dev
```

## 📊 服务地址

- **前端应用**: http://localhost:3000
- **后端 API**: http://localhost:8000  
- **API 文档**: http://localhost:8000/docs
- **Nginx 反向代理**: http://localhost:80
- **数据库**: PostgreSQL (localhost:5433)

## 🛠 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **PostgreSQL** - 关系型数据库
- **Redis** - 缓存和会话存储
- **JWT** - 身份认证
- **Alembic** - 数据库迁移

### 前端  
- **Vue.js 3** - 渐进式 JavaScript 框架
- **Vuetify 3** - Material Design 组件库
- **Vue Router 4** - 路由管理
- **Vuex 4** - 状态管理

### 基础设施
- **Docker & Docker Compose** - 容器化部署
- **Nginx** - 反向代理和负载均衡

## 📁 项目结构

```
├── backend/                 # FastAPI 后端
│   ├── main.py             # 应用入口
│   ├── core/               # 核心配置 (JWT, 设置)
│   ├── db/                 # 数据库配置
│   ├── models/             # SQLAlchemy 模型
│   ├── schemas/            # Pydantic 模式
│   ├── crud/               # 数据库操作层
│   ├── api/v1/             # REST API 端点
│   └── alembic/            # 数据库迁移
├── frontend/               # Vue.js 前端
│   ├── src/
│   │   ├── api/           # HTTP 客户端
│   │   ├── components/    # Vue 组件
│   │   ├── views/         # 页面组件
│   │   ├── router/        # 路由配置
│   │   └── store/         # 状态管理
├── docker-compose.yml      # Docker 服务编排
├── Makefile               # 开发命令
└── README.md              # 项目文档
```

## 🔧 开发命令

### Docker 管理
```bash
make docker-up      # 启动 Docker 环境
make docker-down    # 停止 Docker 环境
make docker-restart # 重启 Docker 环境
make logs           # 查看服务日志
make status         # 查看服务状态
```

### 数据库管理
```bash
make migration msg="描述"  # 创建数据库迁移
make upgrade               # 执行数据库升级
```

### 开发工具
```bash
make run     # 启动 FastAPI 开发服务器
make test    # 运行测试
make clean   # 清理缓存文件
make help    # 显示所有可用命令
```

## 🔐 认证系统

采用 JWT 基于角色的访问控制 (RBAC)：
- **访问令牌**: 30分钟有效期
- **刷新令牌**: 7天有效期  
- **多级权限**: 基础用户、激活用户、验证用户、超级用户

## 📊 核心功能

- ✅ 企业级用户管理系统
- ✅ 员工、部门、角色管理
- ✅ JWT 身份认证和授权
- ✅ 系统操作审计日志
- ✅ Redis 缓存和会话管理
- ✅ 完整的 API 文档
- ✅ 健康检查端点
- ✅ CORS 跨域支持

## 🌐 API 端点

所有 API 端点前缀为 `/api/v1/`：
- `/auth/*` - 身份认证
- `/users/*` - 用户管理  
- `/employees/*` - 员工信息
- `/departments/*` - 部门管理
- `/roles/*` - 角色权限
- `/system-logs/*` - 审计日志

## ⚙️ 环境配置

关键环境变量（`.env` 文件）：
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/claude_fastapi
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
```

## 🧪 测试

```bash
# 后端测试
cd backend && pytest

# 前端构建测试
cd frontend && npm run build
```

## 📝 开发规范

1. **代码提交前** 确保通过 lint 检查
2. **数据库变更** 必须创建迁移文件
3. **API 变更** 需要更新文档
4. **重要功能** 需要添加测试用例

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交变更: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。