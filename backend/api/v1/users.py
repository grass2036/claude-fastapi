from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.base import get_db
from ...schemas.user import (
    UserResponse, UserUpdate, UserProfile
)
from ...crud.user import user_crud
from ...api.deps import (
    get_current_user, get_current_superuser, get_current_active_user
)
from ...models.user import User

router = APIRouter()


@router.get("/me",
            response_model=UserProfile,
            summary="获取当前用户信息",
            description="获取当前登录用户的详细档案信息",
            responses={
                200: {
                    "description": "成功获取用户信息",
                    "content": {
                        "application/json": {
                            "example": {
                                "user": {
                                    "id": 1,
                                    "username": "johndoe",
                                    "email": "john@example.com",
                                    "full_name": "John Doe",
                                    "phone": "13800138000",
                                    "bio": "Software Engineer",
                                    "avatar": "https://example.com/avatar.jpg",
                                    "is_active": True,
                                    "is_verified": True,
                                    "created_at": "2023-01-01T00:00:00Z",
                                    "updated_at": "2023-01-01T00:00:00Z",
                                    "last_login_at": "2023-01-01T00:00:00Z"
                                }
                            }
                        }
                    }
                },
                401: {"description": "未授权访问"}
            })
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前用户档案
    
    **权限要求：** 需要有效的访问令牌
    
    **返回信息：**
    - 用户基本信息
    - 账户状态
    - 时间戳信息
    """
    return {"user": current_user}


@router.put("/me",
            response_model=UserResponse,
            summary="更新当前用户信息",
            description="更新当前登录用户的个人资料",
            responses={
                200: {"description": "成功更新用户信息"},
                401: {"description": "未授权访问"},
                422: {"description": "输入数据验证失败"}
            })
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户档案
    
    **可更新字段：**
    - full_name: 全名
    - phone: 手机号
    - bio: 个人简介
    - avatar: 头像URL
    
    **权限要求：** 需要有效的访问令牌
    """
    updated_user = user_crud.update_user(db, current_user.id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return updated_user


@router.get("/{user_id}",
            response_model=UserResponse,
            summary="获取指定用户信息",
            description="管理员获取指定用户的详细信息",
            responses={
                200: {"description": "成功获取用户信息"},
                401: {"description": "未授权访问"},
                403: {"description": "权限不足"},
                404: {"description": "用户不存在"}
            })
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    获取指定用户信息
    
    **权限要求：** 超级管理员权限
    
    **参数说明：**
    - user_id: 用户ID
    """
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user


@router.post("/{user_id}/activate",
             summary="激活用户",
             description="管理员激活指定用户账户",
             responses={
                200: {"description": "成功激活用户"},
                401: {"description": "未授权访问"},
                403: {"description": "权限不足"},
                404: {"description": "用户不存在"}
             })
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    激活用户账户
    
    **权限要求：** 超级管理员权限
    
    **操作结果：**
    - 用户账户状态变为激活
    - 用户可以正常登录使用系统
    """
    success = user_crud.activate_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return {"message": "用户已激活", "user_id": user_id}


@router.post("/{user_id}/deactivate",
             summary="停用用户",
             description="管理员停用指定用户账户",
             responses={
                200: {"description": "成功停用用户"},
                401: {"description": "未授权访问"},
                403: {"description": "权限不足"},
                404: {"description": "用户不存在"}
             })
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    停用用户账户
    
    **权限要求：** 超级管理员权限
    
    **操作结果：**
    - 用户账户状态变为停用
    - 用户无法登录系统
    - 现有的访问令牌仍然有效（直到过期）
    """
    success = user_crud.deactivate_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return {"message": "用户已停用", "user_id": user_id}