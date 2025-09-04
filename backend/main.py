from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import os
from datetime import datetime
from contextlib import asynccontextmanager

from .core.config import settings
from .db.base import create_tables
from .api.v1.auth import router as auth_router

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
    lifespan=lifespan
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])


@app.get("/", summary="根路径", tags=["General"])
async def root():
    """应用根路径"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", summary="健康检查", tags=["General"])
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
@app.post("/cache/test", summary="测试Redis缓存", tags=["Cache"])
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


@app.get("/cache/{key}", summary="获取缓存", tags=["Cache"])
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


@app.post("/cache/{key}", summary="设置缓存", tags=["Cache"])
async def set_cache(key: str, data: dict, ttl: int = 3600):
    """设置缓存值"""
    try:
        await redis_client.setex(key, ttl, str(data))
        return {"success": True, "key": key, "ttl": ttl}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")