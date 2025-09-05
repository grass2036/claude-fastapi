from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# 绝对导入，避免相对导入问题
try:
    from backend.db.base import Base
except ImportError:
    from db.base import Base


class EmployeeStatus(str, enum.Enum):
    """员工状态枚举"""
    ACTIVE = "active"          # 在职
    INACTIVE = "inactive"      # 离职
    SUSPENDED = "suspended"    # 停职
    PROBATION = "probation"    # 试用期


class Gender(str, enum.Enum):
    """性别枚举"""
    MALE = "male"      # 男
    FEMALE = "female"  # 女
    OTHER = "other"    # 其他


class Employee(Base):
    """员工模型"""
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True, comment="员工ID")
    employee_no = Column(String(50), unique=True, nullable=False, index=True, comment="员工工号")
    
    # 关联用户
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, comment="用户ID")
    
    # 基本信息
    name = Column(String(100), nullable=False, comment="姓名")
    english_name = Column(String(100), nullable=True, comment="英文名")
    id_card = Column(String(20), nullable=True, unique=True, comment="身份证号")
    gender = Column(Enum(Gender), nullable=True, comment="性别")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    phone = Column(String(20), nullable=True, comment="手机号码")
    email = Column(String(100), nullable=True, comment="邮箱地址")
    
    # 组织信息
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True, comment="部门ID")
    position = Column(String(100), nullable=True, comment="职位")
    job_level = Column(String(50), nullable=True, comment="职级")
    
    # 入职信息
    hire_date = Column(Date, nullable=True, comment="入职日期")
    contract_start_date = Column(Date, nullable=True, comment="合同开始日期")
    contract_end_date = Column(Date, nullable=True, comment="合同结束日期")
    probation_months = Column(Integer, default=3, comment="试用期月数")
    
    # 薪资信息
    base_salary = Column(Numeric(10, 2), nullable=True, comment="基本工资")
    
    # 联系信息
    emergency_contact = Column(String(100), nullable=True, comment="紧急联系人")
    emergency_phone = Column(String(20), nullable=True, comment="紧急联系电话")
    address = Column(Text, nullable=True, comment="家庭地址")
    
    # 状态
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.PROBATION, comment="员工状态")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    # 备注
    notes = Column(Text, nullable=True, comment="备注信息")
    
    # 时间字段
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        comment="更新时间"
    )
    
    # 关系
    user = relationship("User", backref="employee_profile")
    department = relationship("Department", back_populates="employees")
    
    def __repr__(self):
        return f"<Employee(id={self.id}, name='{self.name}', employee_no='{self.employee_no}')>"
    
    @property
    def age(self):
        """计算年龄"""
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    @property
    def work_years(self):
        """计算工作年限"""
        if self.hire_date:
            from datetime import date
            today = date.today()
            years = today.year - self.hire_date.year
            if (today.month, today.day) < (self.hire_date.month, self.hire_date.day):
                years -= 1
            return max(0, years)
        return 0
    
    @property
    def is_probation_expired(self):
        """检查试用期是否到期"""
        if self.hire_date and self.probation_months:
            from datetime import date
            from dateutil.relativedelta import relativedelta
            probation_end = self.hire_date + relativedelta(months=self.probation_months)
            return date.today() > probation_end
        return True