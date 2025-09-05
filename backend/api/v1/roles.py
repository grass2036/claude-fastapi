from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.base import get_db
from ...schemas.role import (
    RoleCreate, RoleResponse, PermissionCreate, PermissionResponse
)
from ...crud.role import role_crud, permission_crud
from ...api.deps import get_current_user, get_current_superuser
from ...models.user import User

router = APIRouter()


# ========== 角色管理接口 ==========

@router.post("/",
             response_model=RoleResponse,
             status_code=status.HTTP_201_CREATED,
             summary="创建角色",
             description="创建新的角色并分配权限",
             responses={
                 201: {
                     "description": "角色创建成功",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "name": "管理员",
                                 "code": "admin", 
                                 "description": "系统管理员角色",
                                 "is_active": True,
                                 "is_system": False,
                                 "sort_order": 0,
                                 "permissions": []
                             }
                         }
                     }
                 },
                 400: {"description": "角色编码已存在"},
                 401: {"description": "未授权访问"},
                 403: {"description": "权限不足"}
             })
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    创建角色
    
    **权限要求：** 超级管理员权限
    
    **必填字段：**
    - name: 角色名称（1-50字符）
    - code: 角色编码（1-50字符，唯一）
    
    **可选字段：**
    - description: 角色描述（最多500字符）
    - permission_ids: 权限ID列表
    
    **业务规则：**
    - 角色编码必须唯一
    - 新建角色默认为启用状态
    - 可同时分配多个权限
    """
    try:
        return role_crud.create_role(db, role)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/",
            response_model=List[RoleResponse],
            summary="获取角色列表",
            description="获取系统中所有角色列表（支持筛选）",
            responses={
                200: {
                    "description": "成功获取角色列表",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "id": 1,
                                    "name": "管理员",
                                    "code": "admin",
                                    "description": "系统管理员角色",
                                    "is_active": True,
                                    "is_system": False,
                                    "sort_order": 0,
                                    "permissions": []
                                }
                            ]
                        }
                    }
                },
                401: {"description": "未授权访问"}
            })
async def get_roles(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回的记录数"),
    name: Optional[str] = Query(None, description="角色名称（模糊匹配）"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取角色列表
    
    **权限要求：** 需要有效的访问令牌
    
    **查询参数：**
    - skip: 跳过的记录数（默认0）
    - limit: 返回的记录数（默认100，最大100）
    - name: 角色名称筛选（支持模糊匹配）
    - is_active: 是否启用筛选
    
    **返回数据：**
    - 角色基本信息
    - 关联的权限列表
    - 按排序字段和创建时间排序
    """
    return role_crud.get_roles(
        db=db, 
        skip=skip, 
        limit=limit, 
        name=name, 
        is_active=is_active
    )


@router.get("/{role_id}",
            response_model=RoleResponse,
            summary="获取角色详情",
            description="根据ID获取角色详细信息",
            responses={
                200: {"description": "成功获取角色详情"},
                401: {"description": "未授权访问"},
                404: {"description": "角色不存在"}
            })
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取角色详情
    
    **权限要求：** 需要有效的访问令牌
    
    **路径参数：**
    - role_id: 角色ID
    
    **返回信息：**
    - 角色完整信息
    - 角色拥有的所有权限
    """
    role = role_crud.get_role(db, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    return role


# ========== 权限管理接口 ==========

@router.post("/permissions",
             response_model=PermissionResponse,
             status_code=status.HTTP_201_CREATED,
             summary="创建权限",
             description="创建新的系统权限",
             responses={
                 201: {
                     "description": "权限创建成功",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "name": "查看用户",
                                 "code": "user:view",
                                 "description": "查看用户信息的权限",
                                 "module": "user",
                                 "resource": "user",
                                 "action": "view",
                                 "is_active": True,
                                 "sort_order": 0
                             }
                         }
                     }
                 },
                 401: {"description": "未授权访问"},
                 403: {"description": "权限不足"}
             })
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    创建权限
    
    **权限要求：** 超级管理员权限
    
    **必填字段：**
    - name: 权限名称（1-50字符）
    - code: 权限编码（1-100字符，建议格式：module:resource:action）
    
    **可选字段：**
    - description: 权限描述
    - module: 所属模块（如：user、department、role）
    - resource: 资源名称（如：user、department）
    - action: 操作动作（如：view、create、update、delete）
    
    **编码规范：**
    - 建议使用 module:resource:action 格式
    - 例如：user:profile:view（查看用户档案）
    - 例如：department:info:create（创建部门信息）
    """
    return permission_crud.create_permission(db, permission)


@router.get("/permissions",
            response_model=List[PermissionResponse],
            summary="获取权限列表",
            description="获取系统中所有权限列表",
            responses={
                200: {
                    "description": "成功获取权限列表",
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "id": 1,
                                    "name": "查看用户",
                                    "code": "user:view",
                                    "description": "查看用户信息的权限",
                                    "module": "user",
                                    "resource": "user", 
                                    "action": "view",
                                    "is_active": True,
                                    "sort_order": 0
                                }
                            ]
                        }
                    }
                },
                401: {"description": "未授权访问"}
            })
async def get_permissions(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=100, description="返回的记录数"),
    module: Optional[str] = Query(None, description="模块筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取权限列表
    
    **权限要求：** 需要有效的访问令牌
    
    **查询参数：**
    - skip: 跳过的记录数（默认0）
    - limit: 返回的记录数（默认100，最大100）
    - module: 模块筛选（如：user、department、role）
    
    **返回数据：**
    - 权限完整信息
    - 按模块和排序字段分组
    - 仅返回启用的权限
    """
    return permission_crud.get_permissions(
        db=db,
        skip=skip,
        limit=limit,
        module=module
    )


@router.get("/permissions/{permission_id}",
            response_model=PermissionResponse,
            summary="获取权限详情",
            description="根据ID获取权限详细信息",
            responses={
                200: {"description": "成功获取权限详情"},
                401: {"description": "未授权访问"},
                404: {"description": "权限不存在"}
            })
async def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取权限详情
    
    **权限要求：** 需要有效的访问令牌
    
    **路径参数：**
    - permission_id: 权限ID
    
    **返回信息：**
    - 权限完整详细信息
    - 包含模块、资源、操作等分类信息
    """
    permission = permission_crud.get_permission(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    return permission