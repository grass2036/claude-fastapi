from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import redis.asyncio as redis
import os
from datetime import datetime
from contextlib import asynccontextmanager

from backend.core.config import settings
from backend.db.base import create_tables
from backend.api.v1.auth import router as auth_router
from backend.api.v1.users import router as users_router
from backend.api.v1.departments import router as departments_router
from backend.api.v1.employees import router as employees_router
from backend.api.v1.roles import router as roles_router
from backend.api.v1.system_logs import router as system_logs_router

# Redis客户端全局变量
redis_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    global redis_client
    
    # 创建数据库表
    create_tables()
    
    # 连接Redis
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    print(f"🚀 {settings.PROJECT_NAME} started successfully!")
    print(f"📊 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    
    yield
    
    # 关闭时执行
    if redis_client:
        await redis_client.close()
    print("👋 Application shutdown")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "General",
            "description": "通用接口：健康检查、系统状态等"
        },
        {
            "name": "Authentication",
            "description": "用户认证：注册、登录、令牌管理"
        },
        {
            "name": "User Management", 
            "description": "用户管理：档案管理、密码修改等"
        },
        {
            "name": "Department Management",
            "description": "部门管理：组织架构、部门信息管理"
        },
        {
            "name": "Employee Management",
            "description": "员工管理：员工信息、职位管理"
        },
        {
            "name": "Role Permission Management",
            "description": "角色权限管理：角色分配、权限控制"
        },
        {
            "name": "System Log",
            "description": "系统日志：操作审计、日志查询"
        },
        {
            "name": "Cache",
            "description": "缓存管理：Redis缓存操作"
        }
    ],
    # 添加安全方案配置
    servers=[
        {
            "url": f"http://{settings.HOST}:{settings.PORT}",
            "description": "开发环境服务器"
        }
    ]
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["User Management"])
app.include_router(departments_router, prefix="/api/v1/departments", tags=["Department Management"])
app.include_router(employees_router, prefix="/api/v1/employees", tags=["Employee Management"])
app.include_router(roles_router, prefix="/api/v1/roles", tags=["Role Permission Management"])
app.include_router(system_logs_router, prefix="/api/v1/system-logs", tags=["System Log"])


@app.get("/", 
         summary="根路径", 
         tags=["General"],
         description="应用根路径，返回基本信息",
         responses={
             200: {
                 "description": "成功返回应用信息",
                 "content": {
                     "application/json": {
                         "example": {
                             "message": "Welcome to Claude FastAPI",
                             "version": "1.0.0",
                             "status": "running",
                             "timestamp": "2023-01-01T00:00:00Z"
                         }
                     }
                 }
             }
         })
async def root():
    """应用根路径"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", 
         summary="健康检查", 
         tags=["General"],
         description="检查应用和依赖服务的健康状态",
         responses={
             200: {
                 "description": "应用和Redis连接正常",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "healthy",
                             "redis": "healthy",
                             "timestamp": "2023-01-01T00:00:00Z",
                             "version": "1.0.0"
                         }
                     }
                 }
             },
             503: {
                 "description": "Redis连接异常",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "healthy",
                             "redis": "unhealthy",
                             "timestamp": "2023-01-01T00:00:00Z",
                             "version": "1.0.0"
                         }
                     }
                 }
             }
         })
async def health_check():
    """健康检查端点"""
    # 检查Redis连接
    redis_status = "healthy"
    try:
        if redis_client:
            await redis_client.ping()
        else:
            redis_status = "disconnected"
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "timestamp": datetime.now().isoformat(),
        "version": settings.VERSION
    }


# 缓存测试接口（保留原有功能）
@app.post("/cache/test", 
          summary="测试Redis缓存", 
          tags=["Cache"],
          description="测试Redis缓存功能是否正常工作",
          responses={
              200: {"description": "Redis缓存功能正常"},
              500: {"description": "Redis连接或操作失败"}
          })
async def test_redis_cache():
    """测试Redis缓存功能"""
    try:
        test_key = "test_cache_key"
        test_value = {"message": "Redis is working!", "timestamp": datetime.now().isoformat()}
        
        # 设置缓存
        await redis_client.setex(test_key, 60, str(test_value))
        
        # 获取缓存
        cached_value = await redis_client.get(test_key)
        if cached_value:
            return {"success": True, "cached_data": cached_value}
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve cached data")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")


@app.get("/cache/{key}", 
          summary="获取缓存", 
          tags=["Cache"],
          description="根据键获取Redis缓存值",
          responses={
              200: {"description": "成功获取缓存值"},
              404: {"description": "指定的键不存在"},
              500: {"description": "Redis连接或操作失败"}
          })
async def get_cache(key: str):
    """获取缓存值"""
    try:
        value = await redis_client.get(key)
        if value:
            return {"key": key, "value": value}
        else:
            raise HTTPException(status_code=404, detail="Key not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")


@app.post("/cache/{key}", 
          summary="设置缓存", 
          tags=["Cache"],
          description="设置Redis缓存键值对，带有过期时间",
          responses={
              200: {"description": "成功设置缓存"},
              500: {"description": "Redis连接或操作失败"}
          })
async def set_cache(key: str, data: dict, ttl: int = 3600):
    """设置缓存值"""
    try:
        await redis_client.setex(key, ttl, str(data))
        return {"success": True, "key": key, "ttl": ttl}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")