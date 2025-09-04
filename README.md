# Claude FastAPI 管理系统

使用 FastAPI + Vue.js + Vuetify 实现的现代化后台管理系统

## 技术栈

### 后端
- **FastAPI** - 现代、快速的 Python Web 框架
- **Redis** - 高性能缓存数据库
- **PostgreSQL** - 关系型数据库
- **SQLAlchemy** - ORM 框架
- **Uvicorn** - ASGI 服务器

### 前端
- **Vue.js 3** - 渐进式 JavaScript 框架
- **Vuetify 3** - Material Design 组件库
- **Vue Router** - 官方路由管理器
- **Vuex** - 状态管理模式
- **Axios** - HTTP 客户端
- **Vite** - 现代前端构建工具

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Nginx** - 反向代理服务器

## 快速开始

### 启动所有服务
```bash
docker-compose up --build -d
```

### 访问应用
- **前端界面**: http://localhost
- **API 文档**: http://localhost/docs  
- **API 接口**: http://localhost/api/

### 停止服务
```bash
docker-compose down
```

## 项目特性

✅ **完整的容器化部署**  
✅ **Redis 缓存支持**  
✅ **Material Design UI**  
✅ **响应式布局**  
✅ **API 健康检查**  
✅ **热重载开发**  
✅ **Nginx 反向代理**  

## 详细文档

更多详细信息请查看 [DEPLOYMENT.md](DEPLOYMENT.md)