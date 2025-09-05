from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...db.base import get_db
from ...schemas.department import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse, 
    DepartmentListResponse, DepartmentTree
)
from ...crud.department import department_crud
from ...api.deps import get_current_user, get_current_superuser
from ...models.user import User

router = APIRouter()


@router.post("/",
             response_model=DepartmentResponse,
             status_code=status.HTTP_201_CREATED,
             summary="创建部门",
             description="创建新的部门",
             responses={
                 201: {"description": "部门创建成功"},
                 400: {"description": "部门编码已存在或父部门不存在"},
                 401: {"description": "未授权访问"},
                 403: {"description": "权限不足"}
             })
async def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    创建部门
    
    **权限要求：** 超级管理员权限
    
    **可设置字段：**
    - name: 部门名称（必填）
    - code: 部门编码（必填，唯一）
    - description: 部门描述
    - parent_id: 上级部门ID
    - manager_id: 部门负责人ID
    - phone: 部门电话
    - email: 部门邮箱
    - address: 部门地址
    - sort_order: 排序顺序
    """
    try:
        return department_crud.create_department(db, department)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建部门失败"
        )


@router.get("/",
            response_model=DepartmentListResponse,
            summary="获取部门列表",
            description="获取部门列表（支持分页和筛选）",
            responses={
                200: {"description": "成功获取部门列表"},
                401: {"description": "未授权访问"}
            })
async def get_departments(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="部门名称（模糊匹配）"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    parent_id: Optional[int] = Query(None, description="上级部门ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取部门列表
    
    **权限要求：** 需要有效的访问令牌
    
    **查询参数：**
    - page: 页码（默认1）
    - size: 每页数量（默认10，最大100）
    - name: 部门名称筛选（支持模糊匹配）
    - is_active: 是否启用筛选
    - parent_id: 上级部门ID筛选
    """
    skip = (page - 1) * size
    
    # 获取部门列表
    departments = department_crud.get_departments(
        db=db,
        skip=skip,
        limit=size,
        name=name,
        is_active=is_active,
        parent_id=parent_id
    )
    
    # 获取总数
    total = department_crud.get_departments_count(
        db=db,
        name=name,
        is_active=is_active,
        parent_id=parent_id
    )
    
    # 计算总页数
    pages = (total + size - 1) // size
    
    # 构建响应数据
    items = []
    for dept in departments:
        dept_data = DepartmentResponse.model_validate(dept)
        dept_data.manager_name = dept.manager.display_name if dept.manager else None
        dept_data.parent_name = dept.parent.name if dept.parent else None
        dept_data.employee_count = dept.employee_count
        items.append(dept_data)
    
    return DepartmentListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/tree",
            response_model=List[DepartmentTree],
            summary="获取部门树形结构",
            description="获取部门的层级树形结构",
            responses={
                200: {"description": "成功获取部门树形结构"},
                401: {"description": "未授权访问"}
            })
async def get_department_tree(
    parent_id: Optional[int] = Query(None, description="父部门ID（不传则获取顶级部门）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取部门树形结构
    
    **权限要求：** 需要有效的访问令牌
    
    **查询参数：**
    - parent_id: 父部门ID（不传则获取顶级部门）
    
    **返回数据：**
    - 层级树形结构，包含子部门信息
    """
    def build_tree(departments: List) -> List[DepartmentTree]:
        """递归构建部门树"""
        result = []
        for dept in departments:
            # 获取子部门
            children = department_crud.get_child_departments(db, dept.id)
            children_tree = build_tree(children) if children else []
            
            dept_tree = DepartmentTree(
                id=dept.id,
                name=dept.name,
                code=dept.code,
                level=dept.level,
                is_active=dept.is_active,
                employee_count=dept.employee_count,
                children=children_tree
            )
            result.append(dept_tree)
        return result
    
    root_departments = department_crud.get_department_tree(db, parent_id)
    return build_tree(root_departments)


@router.get("/{department_id}",
            response_model=DepartmentResponse,
            summary="获取部门详情",
            description="根据ID获取部门详细信息",
            responses={
                200: {"description": "成功获取部门详情"},
                401: {"description": "未授权访问"},
                404: {"description": "部门不存在"}
            })
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取部门详情
    
    **权限要求：** 需要有效的访问令牌
    
    **路径参数：**
    - department_id: 部门ID
    """
    department = department_crud.get_department(db, department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="部门不存在"
        )
    
    dept_data = DepartmentResponse.model_validate(department)
    dept_data.manager_name = department.manager.display_name if department.manager else None
    dept_data.parent_name = department.parent.name if department.parent else None
    dept_data.employee_count = department.employee_count
    
    return dept_data


@router.put("/{department_id}",
            response_model=DepartmentResponse,
            summary="更新部门信息",
            description="更新指定部门的信息",
            responses={
                200: {"description": "部门更新成功"},
                400: {"description": "父部门不存在"},
                401: {"description": "未授权访问"},
                403: {"description": "权限不足"},
                404: {"description": "部门不存在"}
            })
async def update_department(
    department_id: int,
    department_update: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    更新部门信息
    
    **权限要求：** 超级管理员权限
    
    **路径参数：**
    - department_id: 部门ID
    
    **可更新字段：**
    - name: 部门名称
    - description: 部门描述
    - parent_id: 上级部门ID
    - manager_id: 部门负责人ID
    - phone: 部门电话
    - email: 部门邮箱
    - address: 部门地址
    - is_active: 是否启用
    - sort_order: 排序顺序
    """
    try:
        updated_department = department_crud.update_department(db, department_id, department_update)
        if not updated_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        dept_data = DepartmentResponse.model_validate(updated_department)
        dept_data.manager_name = updated_department.manager.display_name if updated_department.manager else None
        dept_data.parent_name = updated_department.parent.name if updated_department.parent else None
        dept_data.employee_count = updated_department.employee_count
        
        return dept_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新部门失败"
        )


@router.delete("/{department_id}",
               summary="删除部门",
               description="删除指定部门（软删除）",
               responses={
                   200: {"description": "部门删除成功"},
                   400: {"description": "部门下存在子部门或员工，无法删除"},
                   401: {"description": "未授权访问"},
                   403: {"description": "权限不足"},
                   404: {"description": "部门不存在"}
               })
async def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    删除部门
    
    **权限要求：** 超级管理员权限
    
    **路径参数：**
    - department_id: 部门ID
    
    **注意事项：**
    - 部门下存在子部门时无法删除
    - 部门下存在员工时无法删除
    - 执行软删除（is_active设为False）
    """
    try:
        success = department_crud.delete_department(db, department_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="部门不存在"
            )
        
        return {"message": "部门删除成功", "department_id": department_id}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除部门失败"
        )