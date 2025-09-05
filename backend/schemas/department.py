from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DepartmentBase(BaseModel):
    """部门基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="部门名称")
    code: str = Field(..., min_length=1, max_length=50, description="部门编码")
    description: Optional[str] = Field(None, max_length=500, description="部门描述")
    parent_id: Optional[int] = Field(None, description="上级部门ID")
    manager_id: Optional[int] = Field(None, description="部门负责人ID")
    phone: Optional[str] = Field(None, max_length=20, description="部门电话")
    email: Optional[str] = Field(None, max_length=100, description="部门邮箱")
    address: Optional[str] = Field(None, max_length=255, description="部门地址")
    sort_order: int = Field(0, description="排序顺序")


class DepartmentCreate(DepartmentBase):
    """创建部门模型"""
    class Config:
        json_schema_extra = {
            "example": {
                "name": "技术开发部",
                "code": "TECH001",
                "description": "负责公司技术开发工作",
                "parent_id": None,
                "manager_id": 1,
                "phone": "010-12345678",
                "email": "tech@company.com",
                "address": "北京市朝阳区科技园区",
                "sort_order": 1
            }
        }


class DepartmentUpdate(BaseModel):
    """更新部门模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="部门名称")
    description: Optional[str] = Field(None, max_length=500, description="部门描述")
    parent_id: Optional[int] = Field(None, description="上级部门ID")
    manager_id: Optional[int] = Field(None, description="部门负责人ID")
    phone: Optional[str] = Field(None, max_length=20, description="部门电话")
    email: Optional[str] = Field(None, max_length=100, description="部门邮箱")
    address: Optional[str] = Field(None, max_length=255, description="部门地址")
    is_active: Optional[bool] = Field(None, description="是否启用")
    sort_order: Optional[int] = Field(None, description="排序顺序")


class DepartmentResponse(DepartmentBase):
    """部门响应模型"""
    id: int
    level: int
    path: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    manager_name: Optional[str] = None
    parent_name: Optional[str] = None
    employee_count: int = 0
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "技术开发部",
                "code": "TECH001",
                "description": "负责公司技术开发工作",
                "parent_id": None,
                "parent_name": None,
                "level": 1,
                "path": "技术开发部",
                "manager_id": 1,
                "manager_name": "张三",
                "phone": "010-12345678",
                "email": "tech@company.com",
                "address": "北京市朝阳区科技园区",
                "is_active": True,
                "sort_order": 1,
                "employee_count": 15,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }


class DepartmentTree(BaseModel):
    """部门树形结构模型"""
    id: int
    name: str
    code: str
    level: int
    is_active: bool
    employee_count: int
    children: List['DepartmentTree'] = []
    
    class Config:
        from_attributes = True


class DepartmentListResponse(BaseModel):
    """部门列表响应模型"""
    items: List[DepartmentResponse]
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
                        "name": "技术开发部",
                        "code": "TECH001",
                        "description": "负责公司技术开发工作",
                        "parent_id": None,
                        "parent_name": None,
                        "level": 1,
                        "path": "技术开发部",
                        "manager_id": 1,
                        "manager_name": "张三",
                        "phone": "010-12345678",
                        "email": "tech@company.com",
                        "address": "北京市朝阳区科技园区",
                        "is_active": True,
                        "sort_order": 1,
                        "employee_count": 15,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        }


# 解决前向引用问题
DepartmentTree.model_rebuild()