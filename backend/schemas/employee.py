from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class GenderEnum(str, Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class EmployeeStatusEnum(str, Enum):
    """员工状态枚举"""
    ACTIVE = "active"          # 在职
    INACTIVE = "inactive"      # 离职
    SUSPENDED = "suspended"    # 停职
    PROBATION = "probation"    # 试用期


class EmployeeBase(BaseModel):
    """员工基础模型"""
    employee_no: str = Field(..., min_length=1, max_length=50, description="员工工号")
    name: str = Field(..., min_length=1, max_length=100, description="员工姓名")
    english_name: Optional[str] = Field(None, max_length=100, description="英文名")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    gender: Optional[GenderEnum] = Field(None, description="性别")
    birth_date: Optional[date] = Field(None, description="出生日期")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    
    # 组织信息
    department_id: Optional[int] = Field(None, description="部门ID")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    job_level: Optional[str] = Field(None, max_length=50, description="职级")
    
    # 入职信息
    hire_date: Optional[date] = Field(None, description="入职日期")
    contract_start_date: Optional[date] = Field(None, description="合同开始日期")
    contract_end_date: Optional[date] = Field(None, description="合同结束日期")
    probation_months: int = Field(3, ge=0, le=12, description="试用期月数")
    
    # 薪资信息
    base_salary: Optional[float] = Field(None, ge=0, description="基本工资")
    
    # 联系信息
    emergency_contact: Optional[str] = Field(None, max_length=100, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")
    address: Optional[str] = Field(None, max_length=500, description="家庭地址")
    
    # 备注
    notes: Optional[str] = Field(None, max_length=1000, description="备注信息")


class EmployeeCreate(EmployeeBase):
    """创建员工模型"""
    user_id: int = Field(..., description="关联用户ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_no": "EMP001",
                "user_id": 1,
                "name": "张三",
                "english_name": "John Zhang",
                "id_card": "110101199001011234",
                "gender": "male",
                "birth_date": "1990-01-01",
                "phone": "13800138000",
                "email": "zhang.san@company.com",
                "department_id": 1,
                "position": "高级工程师",
                "job_level": "P6",
                "hire_date": "2023-01-01",
                "contract_start_date": "2023-01-01",
                "contract_end_date": "2025-12-31",
                "probation_months": 3,
                "base_salary": 15000.00,
                "emergency_contact": "李四",
                "emergency_phone": "13900139000",
                "address": "北京市朝阳区xxx街道xxx号",
                "notes": "技术骨干"
            }
        }


class EmployeeUpdate(BaseModel):
    """更新员工模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="员工姓名")
    english_name: Optional[str] = Field(None, max_length=100, description="英文名")
    id_card: Optional[str] = Field(None, max_length=20, description="身份证号")
    gender: Optional[GenderEnum] = Field(None, description="性别")
    birth_date: Optional[date] = Field(None, description="出生日期")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    
    # 组织信息
    department_id: Optional[int] = Field(None, description="部门ID")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    job_level: Optional[str] = Field(None, max_length=50, description="职级")
    
    # 入职信息
    contract_start_date: Optional[date] = Field(None, description="合同开始日期")
    contract_end_date: Optional[date] = Field(None, description="合同结束日期")
    probation_months: Optional[int] = Field(None, ge=0, le=12, description="试用期月数")
    
    # 薪资信息
    base_salary: Optional[float] = Field(None, ge=0, description="基本工资")
    
    # 联系信息
    emergency_contact: Optional[str] = Field(None, max_length=100, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")
    address: Optional[str] = Field(None, max_length=500, description="家庭地址")
    
    # 状态和备注
    status: Optional[EmployeeStatusEnum] = Field(None, description="员工状态")
    is_active: Optional[bool] = Field(None, description="是否启用")
    notes: Optional[str] = Field(None, max_length=1000, description="备注信息")


class EmployeeResponse(EmployeeBase):
    """员工响应模型"""
    id: int
    user_id: int
    status: EmployeeStatusEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    username: Optional[str] = None
    user_email: Optional[str] = None
    department_name: Optional[str] = None
    
    # 计算字段
    age: Optional[int] = None
    work_years: Optional[int] = None
    is_probation_expired: Optional[bool] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "employee_no": "EMP001",
                "user_id": 1,
                "username": "zhangsan",
                "user_email": "zhang.san@company.com",
                "name": "张三",
                "english_name": "John Zhang",
                "id_card": "110101199001011234",
                "gender": "male",
                "birth_date": "1990-01-01",
                "age": 34,
                "phone": "13800138000",
                "email": "zhang.san@company.com",
                "department_id": 1,
                "department_name": "技术开发部",
                "position": "高级工程师",
                "job_level": "P6",
                "hire_date": "2023-01-01",
                "work_years": 1,
                "contract_start_date": "2023-01-01",
                "contract_end_date": "2025-12-31",
                "probation_months": 3,
                "is_probation_expired": True,
                "base_salary": 15000.00,
                "emergency_contact": "李四",
                "emergency_phone": "13900139000",
                "address": "北京市朝阳区xxx街道xxx号",
                "status": "active",
                "is_active": True,
                "notes": "技术骨干",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }


class EmployeeListResponse(BaseModel):
    """员工列表响应模型"""
    items: List[EmployeeResponse]
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
                        "employee_no": "EMP001",
                        "name": "张三",
                        "position": "高级工程师",
                        "department_name": "技术开发部",
                        "status": "active",
                        "hire_date": "2023-01-01",
                        "phone": "13800138000",
                        "email": "zhang.san@company.com"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        }


class EmployeeStats(BaseModel):
    """员工统计模型"""
    total_employees: int = Field(description="员工总数")
    active_employees: int = Field(description="在职员工数")
    inactive_employees: int = Field(description="离职员工数")
    probation_employees: int = Field(description="试用期员工数")
    suspended_employees: int = Field(description="停职员工数")
    
    # 按部门统计
    department_stats: List[dict] = Field(description="按部门统计")
    
    # 按职级统计
    level_stats: List[dict] = Field(description="按职级统计")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_employees": 100,
                "active_employees": 85,
                "inactive_employees": 10,
                "probation_employees": 5,
                "suspended_employees": 0,
                "department_stats": [
                    {"department": "技术开发部", "count": 30},
                    {"department": "产品设计部", "count": 15},
                    {"department": "市场营销部", "count": 20}
                ],
                "level_stats": [
                    {"level": "P6", "count": 25},
                    {"level": "P7", "count": 15},
                    {"level": "P8", "count": 8}
                ]
            }
        }