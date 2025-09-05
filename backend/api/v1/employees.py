from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ...db.base import get_db
from ...schemas.employee import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, 
    EmployeeListResponse, EmployeeStats, EmployeeStatusEnum
)
from ...crud.employee import employee_crud
from ...api.deps import get_current_user, get_current_superuser
from ...models.user import User
from ...models.employee import EmployeeStatus

router = APIRouter()


@router.post("/",
             response_model=EmployeeResponse,
             status_code=status.HTTP_201_CREATED,
             summary="创建员工档案",
             description="为指定用户创建员工档案",
             responses={
                 201: {"description": "员工档案创建成功"},
                 400: {"description": "员工工号已存在、用户不存在或用户已有员工档案"},
                 401: {"description": "未授权访问"},
                 403: {"description": "权限不足"}
             })
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    创建员工档案
    
    **权限要求：** 超级管理员权限
    
    **必填字段：**
    - employee_no: 员工工号（唯一）
    - user_id: 关联用户ID
    - name: 员工姓名
    """
    try:
        db_employee = employee_crud.create_employee(db, employee)
        
        # 构建响应数据
        employee_data = EmployeeResponse.model_validate(db_employee)
        employee_data.username = db_employee.user.username if db_employee.user else None
        employee_data.user_email = db_employee.user.email if db_employee.user else None
        employee_data.department_name = db_employee.department.name if db_employee.department else None
        employee_data.age = db_employee.age
        employee_data.work_years = db_employee.work_years
        employee_data.is_probation_expired = db_employee.is_probation_expired
        
        return employee_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建员工档案失败"
        )


@router.get("/",
            response_model=EmployeeListResponse,
            summary="获取员工列表",
            description="获取员工列表（支持分页和多条件筛选）",
            responses={
                200: {"description": "成功获取员工列表"},
                401: {"description": "未授权访问"}
            })
async def get_employees(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="员工姓名（模糊匹配）"),
    employee_no: Optional[str] = Query(None, description="员工工号（模糊匹配）"),
    department_id: Optional[int] = Query(None, description="部门ID"),
    position: Optional[str] = Query(None, description="职位（模糊匹配）"),
    status: Optional[EmployeeStatusEnum] = Query(None, description="员工状态"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取员工列表
    
    **权限要求：** 需要有效的访问令牌
    """
    skip = (page - 1) * size
    
    # 转换状态枚举
    employee_status = None
    if status:
        employee_status = EmployeeStatus(status.value)
    
    # 获取员工列表
    employees = employee_crud.get_employees(
        db=db,
        skip=skip,
        limit=size,
        name=name,
        employee_no=employee_no,
        department_id=department_id,
        position=position,
        status=employee_status,
        is_active=is_active
    )
    
    # 获取总数
    total = employee_crud.get_employees_count(
        db=db,
        name=name,
        employee_no=employee_no,
        department_id=department_id,
        position=position,
        status=employee_status,
        is_active=is_active
    )
    
    # 计算总页数
    pages = (total + size - 1) // size
    
    # 构建响应数据
    items = []
    for emp in employees:
        emp_data = EmployeeResponse.model_validate(emp)
        emp_data.username = emp.user.username if emp.user else None
        emp_data.user_email = emp.user.email if emp.user else None
        emp_data.department_name = emp.department.name if emp.department else None
        emp_data.age = emp.age
        emp_data.work_years = emp.work_years
        emp_data.is_probation_expired = emp.is_probation_expired
        items.append(emp_data)
    
    return EmployeeListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/statistics",
            response_model=EmployeeStats,
            summary="获取员工统计信息",
            description="获取员工的各类统计数据")
async def get_employee_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取员工统计信息
    
    **权限要求：** 需要有效的访问令牌
    """
    stats = employee_crud.get_employee_statistics(db)
    return EmployeeStats(**stats)


@router.get("/{employee_id}",
            response_model=EmployeeResponse,
            summary="获取员工详情",
            description="根据ID获取员工详细信息")
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取员工详情
    
    **权限要求：** 需要有效的访问令牌
    """
    employee = employee_crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="员工不存在"
        )
    
    # 构建响应数据
    emp_data = EmployeeResponse.model_validate(employee)
    emp_data.username = employee.user.username if employee.user else None
    emp_data.user_email = employee.user.email if employee.user else None
    emp_data.department_name = employee.department.name if employee.department else None
    emp_data.age = employee.age
    emp_data.work_years = employee.work_years
    emp_data.is_probation_expired = employee.is_probation_expired
    
    return emp_data


@router.put("/{employee_id}",
            response_model=EmployeeResponse,
            summary="更新员工信息",
            description="更新指定员工的档案信息")
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    更新员工信息
    
    **权限要求：** 超级管理员权限
    """
    try:
        updated_employee = employee_crud.update_employee(db, employee_id, employee_update)
        if not updated_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="员工不存在"
            )
        
        # 构建响应数据
        emp_data = EmployeeResponse.model_validate(updated_employee)
        emp_data.username = updated_employee.user.username if updated_employee.user else None
        emp_data.user_email = updated_employee.user.email if updated_employee.user else None
        emp_data.department_name = updated_employee.department.name if updated_employee.department else None
        emp_data.age = updated_employee.age
        emp_data.work_years = updated_employee.work_years
        emp_data.is_probation_expired = updated_employee.is_probation_expired
        
        return emp_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新员工信息失败"
        )


@router.delete("/{employee_id}",
               summary="删除员工档案",
               description="删除指定员工的档案（软删除）")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    删除员工档案
    
    **权限要求：** 超级管理员权限
    """
    try:
        success = employee_crud.delete_employee(db, employee_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="员工不存在"
            )
        
        return {"message": "员工档案删除成功", "employee_id": employee_id}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除员工档案失败"
        )