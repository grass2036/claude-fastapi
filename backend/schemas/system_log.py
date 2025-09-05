from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime
from enum import Enum


class LogLevelEnum(str, Enum):
    """日志级别枚举"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogTypeEnum(str, Enum):
    """日志类型枚举"""
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    VIEW = "view"
    EXPORT = "export"
    IMPORT = "import"
    SYSTEM = "system"
    SECURITY = "security"
    API_CALL = "api_call"


class SystemLogBase(BaseModel):
    """系统日志基础模型"""
    level: LogLevelEnum = Field(LogLevelEnum.INFO, description="日志级别")
    log_type: LogTypeEnum = Field(..., description="日志类型")
    action: str = Field(..., min_length=1, max_length=100, description="操作动作")
    message: str = Field(..., min_length=1, description="日志消息")
    
    # 请求信息
    method: Optional[str] = Field(None, max_length=10, description="HTTP请求方法")
    url: Optional[str] = Field(None, max_length=500, description="请求URL")
    endpoint: Optional[str] = Field(None, max_length=200, description="API端点")
    
    # 客户端信息
    ip_address: Optional[str] = Field(None, max_length=45, description="客户端IP地址")
    user_agent: Optional[str] = Field(None, description="用户代理")
    
    # 操作对象信息
    resource_type: Optional[str] = Field(None, max_length=50, description="资源类型")
    resource_id: Optional[str] = Field(None, max_length=50, description="资源ID")
    
    # 详细信息
    request_data: Optional[Dict[str, Any]] = Field(None, description="请求数据")
    response_data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    
    # 状态信息
    status_code: Optional[int] = Field(None, description="响应状态码")
    is_success: bool = Field(True, description="是否成功")
    error_message: Optional[str] = Field(None, description="错误信息")
    
    # 性能信息
    duration: Optional[int] = Field(None, description="执行时长(毫秒)")


class SystemLogCreate(SystemLogBase):
    """创建系统日志模型"""
    user_id: Optional[int] = Field(None, description="操作用户ID")
    username: Optional[str] = Field(None, max_length=50, description="用户名")
    
    class Config:
        json_schema_extra = {
            "example": {
                "level": "info",
                "log_type": "login",
                "action": "用户登录",
                "message": "用户张三成功登录系统",
                "method": "POST",
                "url": "/api/v1/auth/login",
                "endpoint": "login",
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "resource_type": "user",
                "resource_id": "1",
                "status_code": 200,
                "is_success": True,
                "duration": 150,
                "user_id": 1,
                "username": "zhangsan"
            }
        }


class SystemLogResponse(SystemLogBase):
    """系统日志响应模型"""
    id: int
    user_id: Optional[int] = None
    username: Optional[str] = None
    created_at: datetime
    
    # 计算字段
    duration_seconds: Optional[float] = None
    is_slow_request: Optional[bool] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "username": "zhangsan",
                "level": "info",
                "log_type": "login",
                "action": "用户登录",
                "message": "用户张三成功登录系统",
                "method": "POST",
                "url": "/api/v1/auth/login",
                "endpoint": "login",
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "resource_type": "user",
                "resource_id": "1",
                "request_data": {"username": "zhangsan"},
                "response_data": {"success": True},
                "status_code": 200,
                "is_success": True,
                "error_message": None,
                "duration": 150,
                "duration_seconds": 0.15,
                "is_slow_request": False,
                "created_at": "2023-01-01T00:00:00Z"
            }
        }


class SystemLogListResponse(BaseModel):
    """系统日志列表响应模型"""
    items: List[SystemLogResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "username": "zhangsan",
                        "level": "info",
                        "log_type": "login",
                        "action": "用户登录",
                        "message": "用户张三成功登录系统",
                        "ip_address": "192.168.1.100",
                        "status_code": 200,
                        "is_success": True,
                        "duration": 150,
                        "created_at": "2023-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        }


class SystemLogStats(BaseModel):
    """系统日志统计模型"""
    total_logs: int = Field(description="日志总数")
    today_logs: int = Field(description="今日日志数")
    error_logs: int = Field(description="错误日志数")
    warning_logs: int = Field(description="警告日志数")
    
    # 按类型统计
    type_stats: List[Dict[str, Any]] = Field(description="按类型统计")
    
    # 按小时统计（最近24小时）
    hourly_stats: List[Dict[str, Any]] = Field(description="按小时统计")
    
    # 热门API
    popular_apis: List[Dict[str, Any]] = Field(description="热门API")
    
    # 慢请求
    slow_requests: int = Field(description="慢请求数量")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_logs": 1000,
                "today_logs": 150,
                "error_logs": 5,
                "warning_logs": 10,
                "type_stats": [
                    {"type": "login", "count": 50},
                    {"type": "api_call", "count": 800},
                    {"type": "create", "count": 30}
                ],
                "hourly_stats": [
                    {"hour": "00:00", "count": 10},
                    {"hour": "01:00", "count": 15}
                ],
                "popular_apis": [
                    {"endpoint": "/api/v1/users/", "count": 100},
                    {"endpoint": "/api/v1/departments/", "count": 80}
                ],
                "slow_requests": 5
            }
        }