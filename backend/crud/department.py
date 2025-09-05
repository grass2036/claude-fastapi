from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import List, Optional
from ..models.department import Department
from ..models.user import User
from ..schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentCRUD:
    """部门CRUD操作类"""
    
    @staticmethod
    def get_department(db: Session, dept_id: int) -> Optional[Department]:
        """根据ID获取部门"""
        return db.query(Department).options(
            joinedload(Department.manager),
            joinedload(Department.parent)
        ).filter(Department.id == dept_id).first()
    
    @staticmethod
    def get_department_by_code(db: Session, code: str) -> Optional[Department]:
        """根据编码获取部门"""
        return db.query(Department).filter(Department.code == code).first()
    
    @staticmethod
    def get_departments(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        parent_id: Optional[int] = None
    ) -> List[Department]:
        """获取部门列表"""
        query = db.query(Department).options(
            joinedload(Department.manager),
            joinedload(Department.parent)
        )
        
        # 添加筛选条件
        if name:
            query = query.filter(Department.name.contains(name))
        
        if is_active is not None:
            query = query.filter(Department.is_active == is_active)
        
        if parent_id is not None:
            query = query.filter(Department.parent_id == parent_id)
        
        return query.order_by(Department.sort_order, Department.created_at).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_departments_count(
        db: Session,
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        parent_id: Optional[int] = None
    ) -> int:
        """获取部门总数"""
        query = db.query(Department)
        
        if name:
            query = query.filter(Department.name.contains(name))
        
        if is_active is not None:
            query = query.filter(Department.is_active == is_active)
        
        if parent_id is not None:
            query = query.filter(Department.parent_id == parent_id)
        
        return query.count()
    
    @staticmethod
    def get_department_tree(db: Session, parent_id: Optional[int] = None) -> List[Department]:
        """获取部门树形结构"""
        query = db.query(Department).options(
            joinedload(Department.manager),
            joinedload(Department.children)
        )
        
        if parent_id is not None:
            query = query.filter(Department.parent_id == parent_id)
        else:
            query = query.filter(Department.parent_id.is_(None))
        
        return query.filter(Department.is_active == True).order_by(Department.sort_order).all()
    
    @staticmethod
    def create_department(db: Session, department: DepartmentCreate) -> Department:
        """创建部门"""
        # 检查部门编码是否已存在
        if DepartmentCRUD.get_department_by_code(db, department.code):
            raise ValueError("部门编码已存在")
        
        # 计算部门层级和路径
        level = 1
        path = department.name
        
        if department.parent_id:
            parent = DepartmentCRUD.get_department(db, department.parent_id)
            if parent:
                level = parent.level + 1
                path = f"{parent.path} > {department.name}"
        
        # 创建部门对象
        db_department = Department(
            name=department.name,
            code=department.code,
            description=department.description,
            parent_id=department.parent_id,
            level=level,
            path=path,
            manager_id=department.manager_id,
            phone=department.phone,
            email=department.email,
            address=department.address,
            sort_order=department.sort_order,
            is_active=True
        )
        
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    @staticmethod
    def update_department(db: Session, dept_id: int, department_update: DepartmentUpdate) -> Optional[Department]:
        """更新部门"""
        db_department = DepartmentCRUD.get_department(db, dept_id)
        if not db_department:
            return None
        
        update_data = department_update.model_dump(exclude_unset=True)
        
        # 如果更新了父部门，重新计算层级和路径
        if 'parent_id' in update_data:
            parent_id = update_data['parent_id']
            if parent_id:
                parent = DepartmentCRUD.get_department(db, parent_id)
                if parent:
                    update_data['level'] = parent.level + 1
                    update_data['path'] = f"{parent.path} > {update_data.get('name', db_department.name)}"
                else:
                    raise ValueError("父部门不存在")
            else:
                update_data['level'] = 1
                update_data['path'] = update_data.get('name', db_department.name)
        
        for field, value in update_data.items():
            setattr(db_department, field, value)
        
        db.commit()
        db.refresh(db_department)
        return db_department
    
    @staticmethod
    def delete_department(db: Session, dept_id: int) -> bool:
        """删除部门（软删除）"""
        db_department = DepartmentCRUD.get_department(db, dept_id)
        if not db_department:
            return False
        
        # 检查是否有子部门
        children_count = db.query(Department).filter(Department.parent_id == dept_id).count()
        if children_count > 0:
            raise ValueError("部门下存在子部门，无法删除")
        
        # 检查是否有员工
        # TODO: 实现员工检查
        # employee_count = db.query(Employee).filter(Employee.department_id == dept_id).count()
        # if employee_count > 0:
        #     raise ValueError("部门下存在员工，无法删除")
        
        db_department.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def get_child_departments(db: Session, parent_id: int) -> List[Department]:
        """获取子部门列表"""
        return db.query(Department).filter(
            Department.parent_id == parent_id,
            Department.is_active == True
        ).order_by(Department.sort_order).all()


# 创建全局实例
department_crud = DepartmentCRUD()