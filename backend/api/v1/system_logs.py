from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ...db.base import get_db
from ...schemas.system_log import (
    SystemLogCreate, SystemLogResponse, SystemLogListResponse, 
    SystemLogStatistics, LogLevelEnum, LogTypeEnum
)
from ...crud.system_log import system_log_crud
from ...api.deps import get_current_user, get_current_superuser
from ...models.user import User
from ...models.system_log import LogLevel, LogType

router = APIRouter()


@router.post("/",
             response_model=SystemLogResponse,
             status_code=status.HTTP_201_CREATED,
             summary="创建系统日志",
             description="手动创建系统日志记录（通常由系统自动调用）",
             responses={
                 201: {
                     "description": "日志记录创建成功",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "user_id": 1,
                                 "username": "admin",
                                 "level": "INFO",
                                 "log_type": "LOGIN",
                                 "action": "用户登录",
                                 "message": "用户成功登录系统",
                                 "method": "POST",
                                 "url": "/api/v1/auth/login",
                                 "endpoint": "/auth/login",
                                 "ip_address": "192.168.1.100",
                                 "user_agent": "Mozilla/5.0...",
                                 "is_success": True,
                                 "status_code": 200,
                                 "duration": 150,
                                 "created_at": "2024-01-01T12:00:00Z"
                             }
                         }
                     }
                 },
                 401: {"description": "未授权访问"},
                 403: {"description": "权限不足"}
             })
async def create_system_log(
    log: SystemLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    创建系统日志
    
    **权限要求：** 超级管理员权限
    
    **必填字段：**
    - level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    - log_type: 日志类型（LOGIN, LOGOUT, CREATE, UPDATE, DELETE, ACCESS等）
    - action: 操作描述
    - message: 日志消息
    
    **可选字段：**
    - user_id: 操作用户ID
    - username: 操作用户名
    - method: HTTP方法
    - url: 请求URL
    - endpoint: API端点
    - ip_address: IP地址
    - user_agent: 用户代理
    - resource_type: 资源类型
    - resource_id: 资源ID
    - request_data: 请求数据（JSON）
    - response_data: 响应数据（JSON）
    - status_code: HTTP状态码
    - is_success: 是否成功
    - error_message: 错误消息
    - duration: 请求耗时（毫秒）
    
    **注意：** 此接口主要供系统内部调用，记录各种操作日志
    """
    try:
        return system_log_crud.create_log(db, log)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建日志记录失败"
        )


@router.get("/",
            response_model=SystemLogListResponse,
            summary="获取系统日志列表",
            description="分页获取系统日志列表（支持多条件筛选）",
            responses={
                200: {
                    "description": "成功获取日志列表",
                    "content": {
                        "application/json": {
                            "example": {
                                "items": [
                                    {
                                        "id": 1,
                                        "user_id": 1,
                                        "username": "admin",
                                        "level": "INFO",
                                        "log_type": "LOGIN",
                                        "action": "用户登录",
                                        "message": "用户成功登录系统",
                                        "method": "POST",
                                        "url": "/api/v1/auth/login",
                                        "endpoint": "/auth/login",
                                        "ip_address": "192.168.1.100",
                                        "is_success": True,
                                        "status_code": 200,
                                        "duration": 150,
                                        "created_at": "2024-01-01T12:00:00Z"
                                    }
                                ],
                                "total": 1,
                                "page": 1,
                                "size": 10,
                                "pages": 1
                            }
                        }
                    }
                },
                401: {"description": "未授权访问"}
            })
async def get_system_logs(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    level: Optional[LogLevelEnum] = Query(None, description="日志级别"),
    log_type: Optional[LogTypeEnum] = Query(None, description="日志类型"),
    username: Optional[str] = Query(None, description="用户名（模糊匹配）"),
    action: Optional[str] = Query(None, description="操作（模糊匹配）"),
    is_success: Optional[bool] = Query(None, description="是否成功"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    ip_address: Optional[str] = Query(None, description="IP地址"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取系统日志列表
    
    **权限要求：** 需要有效的访问令牌
    
    **查询参数：**
    - page: 页码（默认1）
    - size: 每页数量（默认20，最大100）
    - level: 日志级别筛选
    - log_type: 日志类型筛选
    - username: 用户名筛选（支持模糊匹配）
    - action: 操作筛选（支持模糊匹配）
    - is_success: 成功状态筛选
    - start_time: 开始时间筛选
    - end_time: 结束时间筛选
    - ip_address: IP地址筛选
    
    **返回数据：**
    - 按创建时间倒序排列
    - 包含完整日志信息
    - 支持分页
    """
    skip = (page - 1) * size
    
    # 转换枚举
    log_level = LogLevel(level.value) if level else None
    log_type_value = LogType(log_type.value) if log_type else None
    
    # 获取日志列表
    logs = system_log_crud.get_logs(
        db=db,
        skip=skip,
        limit=size,
        level=log_level,
        log_type=log_type_value,
        username=username,
        action=action,
        is_success=is_success,
        start_time=start_time,
        end_time=end_time,
        ip_address=ip_address
    )
    
    # 获取总数
    total = system_log_crud.get_logs_count(
        db=db,
        level=log_level,
        log_type=log_type_value,
        username=username,
        action=action,
        is_success=is_success,
        start_time=start_time,
        end_time=end_time,
        ip_address=ip_address
    )
    
    # 计算总页数
    pages = (total + size - 1) // size
    
    # 构建响应数据
    items = [SystemLogResponse.model_validate(log) for log in logs]
    
    return SystemLogListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/statistics",
            response_model=SystemLogStatistics,
            summary="获取系统日志统计",
            description="获取系统日志的各类统计信息",
            responses={
                200: {
                    "description": "成功获取日志统计",
                    "content": {
                        "application/json": {
                            "example": {
                                "total_logs": 1000,
                                "today_logs": 50,
                                "error_logs": 10,
                                "warning_logs": 25,
                                "type_stats": [
                                    {"type": "LOGIN", "count": 100},
                                    {"type": "CREATE", "count": 50}
                                ],
                                "hourly_stats": [
                                    {"hour": "00:00", "count": 5},
                                    {"hour": "01:00", "count": 8}
                                ],
                                "popular_apis": [
                                    {"endpoint": "/auth/login", "count": 100}
                                ],
                                "slow_requests": 5
                            }
                        }
                    }
                },
                401: {"description": "未授权访问"}
            })
async def get_system_log_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取系统日志统计
    
    **权限要求：** 需要有效的访问令牌
    
    **统计维度：**
    - 总日志数
    - 今日日志数
    - 错误日志数
    - 警告日志数
    - 按类型分类统计
    - 最近24小时按小时统计
    - 热门API端点（前10）
    - 慢请求统计（超过3秒）
    
    **用途：**
    - 系统监控面板
    - 运维统计分析
    - 性能监控
    """
    stats = system_log_crud.get_log_statistics(db)
    return SystemLogStatistics(**stats)


@router.get("/{log_id}",
            response_model=SystemLogResponse,
            summary="获取日志详情",
            description="根据ID获取系统日志详细信息",
            responses={
                200: {"description": "成功获取日志详情"},
                401: {"description": "未授权访问"},
                404: {"description": "日志不存在"}
            })
async def get_system_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取日志详情
    
    **权限要求：** 需要有效的访问令牌
    
    **路径参数：**
    - log_id: 日志ID
    
    **返回信息：**
    - 日志完整详细信息
    - 包含请求和响应数据
    - 错误信息和堆栈跟踪
    """
    log = system_log_crud.get_log(db, log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="日志记录不存在"
        )
    
    return SystemLogResponse.model_validate(log)


@router.get("/users/{user_id}/activity",
            response_model=List[SystemLogResponse],
            summary="获取用户活动日志",
            description="获取指定用户的活动日志",
            responses={
                200: {"description": "成功获取用户活动日志"},
                401: {"description": "未授权访问"}
            })
async def get_user_activity_logs(
    user_id: int,
    limit: int = Query(50, ge=1, le=200, description="最大返回数量"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户活动日志
    
    **权限要求：** 需要有效的访问令牌
    
    **路径参数：**
    - user_id: 用户ID
    
    **查询参数：**
    - limit: 最大返回数量（默认50，最大200）
    
    **返回数据：**
    - 指定用户的活动记录
    - 按时间倒序排列
    - 用于用户行为分析
    """
    logs = system_log_crud.get_user_activity_logs(db, user_id, limit)
    return [SystemLogResponse.model_validate(log) for log in logs]


@router.delete("/cleanup",
               summary="清理旧日志",
               description="清理指定天数前的旧日志记录",
               responses={
                   200: {"description": "日志清理完成"},
                   401: {"description": "未授权访问"},
                   403: {"description": "权限不足"}
               })
async def cleanup_old_logs(
    days: int = Query(30, ge=1, le=365, description="保留天数（删除N天前的日志）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    清理旧日志
    
    **权限要求：** 超级管理员权限
    
    **查询参数：**
    - days: 保留天数（默认30天，最大365天）
    
    **操作说明：**
    - 删除指定天数前的所有日志记录
    - 不可恢复的物理删除
    - 建议在系统维护期间执行
    - 可配置为定时任务自动执行
    
    **注意事项：**
    - 请谨慎使用此功能
    - 建议先备份重要日志
    - 可能影响审计追溯
    """
    try:
        deleted_count = system_log_crud.delete_old_logs(db, days)
        return {
            "message": f"成功清理 {deleted_count} 条日志记录",
            "deleted_count": deleted_count,
            "retention_days": days
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="清理日志失败"
        )