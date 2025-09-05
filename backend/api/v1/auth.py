from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ...db.base import get_db
from ...schemas.user import (
    UserCreate, UserLogin, UserResponse, Token, 
    TokenRefresh, UserProfile, UserChangePassword, UserUpdate
)
from ...crud.user import user_crud
from ...core.security import security
from ...core.config import settings
from ...api.deps import get_current_user
from ...models.user import User

router = APIRouter()


@router.post("/register", 
             response_model=UserResponse, 
             status_code=status.HTTP_201_CREATED,
             summary="用户注册",
             description="创建新用户账户",
             responses={
                 201: {
                     "description": "用户注册成功",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "username": "johndoe",
                                 "email": "john@example.com",
                                 "full_name": "John Doe",
                                 "phone": "13800138000",
                                 "bio": "Software Engineer",
                                 "avatar": None,
                                 "is_active": True,
                                 "is_verified": False,
                                 "created_at": "2023-01-01T00:00:00Z",
                                 "updated_at": "2023-01-01T00:00:00Z",
                                 "last_login_at": None
                             }
                         }
                     }
                 },
                 400: {"description": "注册数据验证失败（用户名/邮箱已存在、密码不匹配等）"},
                 422: {"description": "输入数据格式错误"}
             })
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    
    - **username**: 用户名 (3-50字符)
    - **email**: 邮箱地址
    - **password**: 密码 (最少8字符)
    - **confirm_password**: 确认密码
    - **full_name**: 全名 (可选)
    - **phone**: 手机号 (可选)
    - **bio**: 个人简介 (可选)
    """
    try:
        # 创建用户
        db_user = user_crud.create_user(db, user_data)
        return db_user
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败，请稍后重试"
        )


@router.post("/login", 
             response_model=Token,
             summary="用户登录",
             description="用户登录并获取访问令牌",
             responses={
                 200: {
                     "description": "登录成功，返回访问令牌",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                 "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                 "token_type": "bearer",
                                 "expires_in": 1800
                             }
                         }
                     }
                 },
                 401: {"description": "用户名或密码错误"},
                 422: {"description": "输入数据格式错误"}
             })
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    
    返回访问令牌和刷新令牌
    """
    # 验证用户凭据
    user = user_crud.authenticate_user(db, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 生成令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"user_id": user.id, "username": user.username},
        expires_delta=access_token_expires
    )
    
    refresh_token = security.create_refresh_token(
        data={"user_id": user.id, "username": user.username}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh", 
             response_model=Token,
             summary="刷新令牌",
             description="使用刷新令牌获取新的访问令牌",
             responses={
                 200: {"description": "令牌刷新成功"},
                 401: {"description": "刷新令牌无效或已过期"},
                 422: {"description": "输入数据格式错误"}
             })
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    
    返回新的访问令牌和刷新令牌
    """
    try:
        # 验证刷新令牌
        payload = security.verify_token(token_data.refresh_token, token_type="refresh")
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
        
        # 验证用户是否存在且活跃
        user = user_crud.get_user(db, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在或已被禁用"
            )
        
        # 生成新令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"user_id": user.id, "username": user.username},
            expires_delta=access_token_expires
        )
        
        refresh_token = security.create_refresh_token(
            data={"user_id": user.id, "username": user.username}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌刷新失败"
        )


@router.post("/change-password",
             summary="修改密码",
             description="修改当前用户密码",
             responses={
                 200: {"description": "密码修改成功"},
                 400: {"description": "当前密码错误或新密码不匹配"},
                 401: {"description": "未授权访问"},
                 422: {"description": "输入数据格式错误"}
             })
async def change_password(
    password_data: UserChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    修改用户密码
    
    - **current_password**: 当前密码
    - **new_password**: 新密码
    - **confirm_new_password**: 确认新密码
    """
    # 验证新密码确认
    if password_data.new_password != password_data.confirm_new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码和确认密码不匹配"
        )
    
    # 修改密码
    success = user_crud.change_password(
        db, 
        current_user.id, 
        password_data.current_password, 
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    return {"message": "密码修改成功"}


@router.post("/logout",
             summary="用户登出",
             description="用户登出（客户端需要清除令牌）",
             responses={
                 200: {"description": "登出成功"},
                 401: {"description": "未授权访问"}
             })
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    用户登出
    
    由于JWT是无状态的，服务端无法主动使令牌失效
    客户端需要主动删除存储的令牌
    """
    return {"message": "登出成功，请清除本地令牌"}