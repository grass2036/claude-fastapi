from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PermissionBase(BaseModel):
    """权限基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="权限名称")
    code: str = Field(..., min_length=1, max_length=100, description="权限编码")
    description: Optional[str] = Field(None, max_length=500, description="权限描述")
    module: Optional[str] = Field(None, max_length=50, description="所属模块")
    resource: Optional[str] = Field(None, max_length=100, description="资源")
    action: Optional[str] = Field(None, max_length=50, description="操作动作")


class PermissionCreate(PermissionBase):
    """创建权限模型"""
    class Config:
        json_schema_extra = {
            "example": {
                "name": "查看用户",
                "code": "user:view",
                "description": "查看用户信息的权限",
                "module": "user",
                "resource": "user",
                "action": "view"
            }
        }


class PermissionResponse(PermissionBase):
    """权限响应模型"""
    id: int
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    """角色基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="角色名称")
    code: str = Field(..., min_length=1, max_length=50, description="角色编码")
    description: Optional[str] = Field(None, max_length=500, description="角色描述")


class RoleCreate(RoleBase):
    """创建角色模型"""
    permission_ids: Optional[List[int]] = Field([], description="权限ID列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "管理员",
                "code": "admin",
                "description": "系统管理员角色",
                "permission_ids": [1, 2, 3]
            }
        }


class RoleResponse(RoleBase):
    """角色响应模型"""
    id: int
    is_active: bool
    is_system: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
    permissions: Optional[List[PermissionResponse]] = []
    
    class Config:
        from_attributes = True