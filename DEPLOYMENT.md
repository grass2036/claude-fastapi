# Claude FastAPI 容器化部署指南

## 项目架构

本项目采用微服务架构，包含以下服务：

- **Backend (FastAPI)**: 后端API服务，端口8000，支持Redis缓存
- **Frontend (Vue.js + Vuetify)**: 前端界面，端口3000，使用Vuetify Material Design组件  
- **Database (PostgreSQL)**: 数据库，端口5433
- **Cache (Redis)**: 缓存服务，端口6379
- **Proxy (Nginx)**: 反向代理，端口80

## 快速启动

### 启动所有服务
```bash
docker-compose up --build -d
```

### 查看服务状态
```bash
docker-compose ps
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

### 停止服务
```bash
docker-compose down
```

### 停止并清理
```bash
docker-compose down --volumes --remove-orphans
```

## 服务访问地址

### 通过Nginx代理访问 (推荐)
- **前端界面**: http://localhost
- **API接口**: http://localhost/api/
- **API文档**: http://localhost/docs

### 直接访问各服务
- **FastAPI后端**: http://localhost:8000
- **Vue前端**: http://localhost:3000
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6379

## API测试

### 健康检查
```bash
curl http://localhost/api/health
```

### 测试Redis缓存
```bash
curl -X POST http://localhost/api/cache/test
```

### 设置缓存
```bash
curl -X POST http://localhost/api/cache/mykey \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World", "data": 123}'
```

### 获取缓存
```bash
curl http://localhost/api/cache/mykey
```

## 开发环境配置

### 环境变量
项目支持以下环境变量：

```bash
# 后端配置
ENV=development
DATABASE_URL=postgresql://postgres:postgres@db:5432/claude_fastapi
REDIS_URL=redis://redis:6379/0

# 前端配置
NODE_ENV=development
VUE_APP_API_URL=http://localhost:8000
```

### 热重载开发
前端和后端都支持热重载：
- 后端代码修改会自动重启
- 前端代码修改会自动刷新

## 生产环境部署

### 生产环境构建
```bash
# 构建生产版本前端
docker-compose -f docker-compose.prod.yml up --build -d
```

### 环境变量配置
创建 `.env` 文件：
```bash
ENV=production
DATABASE_URL=postgresql://user:password@db:5432/database_name
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
```

## 数据持久化

项目使用Docker volumes进行数据持久化：
- `postgres_data`: PostgreSQL数据
- `redis_data`: Redis数据

## 扩展和自定义

### 添加新的API端点
1. 在 `app/main.py` 中添加新路由
2. 重启backend容器：`docker-compose restart backend`

### 修改前端页面
1. 编辑 `frontend/src/` 下的Vue组件，使用Vuetify Material Design组件
2. 修改会自动热重载
3. 可使用Material Design Icons (mdi-*)

### 数据库迁移
```bash
# 进入backend容器
docker-compose exec backend bash

# 运行迁移
alembic upgrade head
```

## 故障排除

### 端口冲突
如果遇到端口冲突，可以修改 `docker-compose.yml` 中的端口映射。

### 容器无法启动
```bash
# 查看详细日志
docker-compose logs [service-name]

# 重新构建
docker-compose up --build --force-recreate
```

### 数据库连接问题
检查PostgreSQL容器是否正常运行：
```bash
docker-compose exec db psql -U postgres -d claude_fastapi
```

### Redis连接问题
检查Redis容器状态：
```bash
docker-compose exec redis redis-cli ping
```

## 性能优化

### 生产环境建议
1. 使用生产级数据库配置
2. 启用Redis持久化
3. 配置Nginx缓存
4. 使用HTTPS证书
5. 设置适当的资源限制

### 监控和日志
建议添加：
- 日志聚合 (ELK Stack)
- 监控系统 (Prometheus + Grafana)  
- 健康检查端点
- 错误追踪 (Sentry)

## 前端技术栈

### Vuetify Material Design
项目前端使用Vuetify 3.x，提供以下特性：
- **Material Design 3** 设计规范
- **响应式布局** - 自动适配桌面和移动端
- **主题系统** - 支持亮色/暗色主题切换
- **图标库** - 内置Material Design Icons
- **组件库** - 丰富的UI组件（卡片、按钮、表单等）

### 主要组件使用示例
```vue
<!-- 卡片组件 -->
<v-card>
  <v-card-title>标题</v-card-title>
  <v-card-text>内容</v-card-text>
  <v-card-actions>
    <v-btn color="primary">操作按钮</v-btn>
  </v-card-actions>
</v-card>

<!-- 响应式布局 -->
<v-row>
  <v-col cols="12" md="6">
    <!-- 内容 -->
  </v-col>
</v-row>
```

## 目录结构
```
claude-fastapi/
├── app/                    # FastAPI后端代码
├── frontend/               # Vue.js + Vuetify前端代码
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面组件
│   │   ├── router/         # 路由配置
│   │   └── store/          # 状态管理
├── docker-compose.yml      # Docker编排配置
├── Dockerfile.backend      # 后端容器配置
├── Dockerfile.frontend     # 前端容器配置
├── nginx.conf             # Nginx配置
├── requirements.txt       # Python依赖
└── DEPLOYMENT.md          # 部署指南
```