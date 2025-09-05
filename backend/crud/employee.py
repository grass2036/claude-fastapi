from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from ..models.employee import Employee, EmployeeStatus
from ..models.user import User
from ..models.department import Department
from ..schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeCRUD:
    """员工CRUD操作类"""
    
    @staticmethod
    def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
        """根据ID获取员工"""
        return db.query(Employee).options(
            joinedload(Employee.user),
            joinedload(Employee.department)
        ).filter(Employee.id == employee_id).first()
    
    @staticmethod
    def get_employee_by_no(db: Session, employee_no: str) -> Optional[Employee]:
        """根据员工工号获取员工"""
        return db.query(Employee).filter(Employee.employee_no == employee_no).first()
    
    @staticmethod
    def get_employee_by_user_id(db: Session, user_id: int) -> Optional[Employee]:
        """根据用户ID获取员工"""
        return db.query(Employee).options(
            joinedload(Employee.user),
            joinedload(Employee.department)
        ).filter(Employee.user_id == user_id).first()
    
    @staticmethod
    def get_employees(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        employee_no: Optional[str] = None,
        department_id: Optional[int] = None,
        position: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
        is_active: Optional[bool] = None
    ) -> List[Employee]:
        """获取员工列表"""
        query = db.query(Employee).options(
            joinedload(Employee.user),
            joinedload(Employee.department)
        )
        
        # 添加筛选条件
        if name:
            query = query.filter(Employee.name.contains(name))
        
        if employee_no:
            query = query.filter(Employee.employee_no.contains(employee_no))
        
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        
        if position:
            query = query.filter(Employee.position.contains(position))
        
        if status:
            query = query.filter(Employee.status == status)
        
        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)
        
        return query.order_by(Employee.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_employees_count(
        db: Session,
        name: Optional[str] = None,
        employee_no: Optional[str] = None,
        department_id: Optional[int] = None,
        position: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """获取员工总数"""
        query = db.query(Employee)
        
        if name:
            query = query.filter(Employee.name.contains(name))
        
        if employee_no:
            query = query.filter(Employee.employee_no.contains(employee_no))
        
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        
        if position:
            query = query.filter(Employee.position.contains(position))
        
        if status:
            query = query.filter(Employee.status == status)
        
        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)
        
        return query.count()
    
    @staticmethod
    def create_employee(db: Session, employee: EmployeeCreate) -> Employee:
        """创建员工"""
        # 检查员工工号是否已存在
        if EmployeeCRUD.get_employee_by_no(db, employee.employee_no):
            raise ValueError("员工工号已存在")
        
        # 检查用户ID是否已被其他员工使用
        if EmployeeCRUD.get_employee_by_user_id(db, employee.user_id):
            raise ValueError("该用户已有员工档案")
        
        # 检查用户是否存在
        user = db.query(User).filter(User.id == employee.user_id).first()
        if not user:
            raise ValueError("用户不存在")
        
        # 检查部门是否存在
        if employee.department_id:
            department = db.query(Department).filter(Department.id == employee.department_id).first()
            if not department:
                raise ValueError("部门不存在")
        
        # 创建员工对象
        db_employee = Employee(
            employee_no=employee.employee_no,
            user_id=employee.user_id,
            name=employee.name,
            english_name=employee.english_name,
            id_card=employee.id_card,
            gender=employee.gender,
            birth_date=employee.birth_date,
            phone=employee.phone,
            email=employee.email,
            department_id=employee.department_id,
            position=employee.position,
            job_level=employee.job_level,
            hire_date=employee.hire_date,
            contract_start_date=employee.contract_start_date,
            contract_end_date=employee.contract_end_date,
            probation_months=employee.probation_months,
            base_salary=employee.base_salary,
            emergency_contact=employee.emergency_contact,
            emergency_phone=employee.emergency_phone,
            address=employee.address,
            notes=employee.notes,
            status=EmployeeStatus.PROBATION,
            is_active=True
        )
        
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate) -> Optional[Employee]:
        """更新员工信息"""
        db_employee = EmployeeCRUD.get_employee(db, employee_id)
        if not db_employee:
            return None
        
        update_data = employee_update.model_dump(exclude_unset=True)
        
        # 检查部门是否存在
        if 'department_id' in update_data and update_data['department_id']:
            department = db.query(Department).filter(Department.id == update_data['department_id']).first()
            if not department:
                raise ValueError("部门不存在")
        
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        
        db.commit()
        db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def delete_employee(db: Session, employee_id: int) -> bool:
        """删除员工（软删除）"""
        db_employee = EmployeeCRUD.get_employee(db, employee_id)
        if not db_employee:
            return False
        
        db_employee.is_active = False
        db_employee.status = EmployeeStatus.INACTIVE
        db.commit()
        return True
    
    @staticmethod
    def get_employees_by_department(db: Session, department_id: int) -> List[Employee]:
        """获取指定部门的员工列表"""
        return db.query(Employee).options(
            joinedload(Employee.user)
        ).filter(
            Employee.department_id == department_id,
            Employee.is_active == True
        ).order_by(Employee.hire_date).all()
    
    @staticmethod
    def get_employee_statistics(db: Session) -> Dict[str, Any]:
        """获取员工统计信息"""
        # 基本统计
        total_employees = db.query(Employee).filter(Employee.is_active == True).count()
        
        status_stats = db.query(
            Employee.status,
            func.count(Employee.id).label('count')
        ).filter(Employee.is_active == True).group_by(Employee.status).all()
        
        # 按部门统计
        department_stats = db.query(
            Department.name,
            func.count(Employee.id).label('count')
        ).join(Employee, Department.id == Employee.department_id).filter(
            Employee.is_active == True
        ).group_by(Department.name).all()
        
        # 按职级统计
        level_stats = db.query(
            Employee.job_level,
            func.count(Employee.id).label('count')
        ).filter(
            Employee.is_active == True,
            Employee.job_level.isnot(None)
        ).group_by(Employee.job_level).all()
        
        # 处理状态统计
        status_dict = {status.value: 0 for status in EmployeeStatus}
        for status, count in status_stats:
            status_dict[status.value] = count
        
        return {
            "total_employees": total_employees,
            "active_employees": status_dict.get(EmployeeStatus.ACTIVE.value, 0),
            "inactive_employees": status_dict.get(EmployeeStatus.INACTIVE.value, 0),
            "probation_employees": status_dict.get(EmployeeStatus.PROBATION.value, 0),
            "suspended_employees": status_dict.get(EmployeeStatus.SUSPENDED.value, 0),
            "department_stats": [
                {"department": name, "count": count} for name, count in department_stats
            ],
            "level_stats": [
                {"level": level, "count": count} for level, count in level_stats
            ]
        }
    
    @staticmethod
    def search_employees(db: Session, keyword: str, limit: int = 10) -> List[Employee]:
        """搜索员工（支持姓名、工号、职位模糊匹配）"""
        return db.query(Employee).options(
            joinedload(Employee.user),
            joinedload(Employee.department)
        ).filter(
            Employee.is_active == True,
            or_(
                Employee.name.contains(keyword),
                Employee.employee_no.contains(keyword),
                Employee.position.contains(keyword)
            )
        ).limit(limit).all()


# 创建全局实例
employee_crud = EmployeeCRUD()