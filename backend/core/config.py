from pydantic_settings import BaseSettings
from typing import Optional, Union
import os


class Settings(BaseSettings):
    # 应用配置
    PROJECT_NAME: str = "Claude FastAPI"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI backend for management system with Redis cache"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/claude_fastapi"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 密码加密配置
    PASSWORD_HASH_ALGORITHM: str = "bcrypt"
    BCRYPT_ROUNDS: int = 12
    
    # CORS配置
    ALLOWED_ORIGINS: Union[list[str], str] = ["http://localhost:3000", "http://frontend:3000"]
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """将ALLOWED_ORIGINS转换为列表格式"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
        return self.ALLOWED_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()