from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import os
import json
from datetime import datetime

app = FastAPI(
    title="Claude FastAPI", 
    description="FastAPI backend for management system with Redis cache", 
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis连接
redis_client = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis_client = redis.from_url(redis_url, decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    global redis_client
    if redis_client:
        await redis_client.close()

@app.get("/")
async def root():
    return {"message": "Hello World", "status": "running", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    # 检查Redis连接
    redis_status = "healthy"
    try:
        await redis_client.ping()
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy",
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/cache/test")
async def test_redis_cache():
    """测试Redis缓存功能"""
    try:
        test_key = "test_cache_key"
        test_value = {"message": "Redis is working!", "timestamp": datetime.now().isoformat()}
        
        # 设置缓存
        await redis_client.setex(test_key, 60, json.dumps(test_value))
        
        # 获取缓存
        cached_value = await redis_client.get(test_key)
        if cached_value:
            cached_data = json.loads(cached_value)
            return {"success": True, "cached_data": cached_data}
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve cached data")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/cache/{key}")
async def get_cache(key: str):
    """获取缓存值"""
    try:
        value = await redis_client.get(key)
        if value:
            return {"key": key, "value": json.loads(value)}
        else:
            raise HTTPException(status_code=404, detail="Key not found")
    except json.JSONDecodeError:
        return {"key": key, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.post("/cache/{key}")
async def set_cache(key: str, data: dict, ttl: int = 3600):
    """设置缓存值"""
    try:
        await redis_client.setex(key, ttl, json.dumps(data))
        return {"success": True, "key": key, "ttl": ttl}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")