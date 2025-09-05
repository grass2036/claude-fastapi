from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# 绝对导入，避免相对导入问题
try:
    from backend.db.base import Base
except ImportError:
    from db.base import Base


class Department(Base):
    """部门模型"""
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True, comment="部门ID")
    name = Column(String(100), nullable=False, index=True, comment="部门名称")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="部门编码")
    description = Column(Text, nullable=True, comment="部门描述")
    
    # 层级结构
    parent_id = Column(Integer, ForeignKey("departments.id"), nullable=True, comment="上级部门ID")
    level = Column(Integer, default=1, comment="部门层级")
    path = Column(String(500), nullable=True, comment="部门路径")
    
    # 负责人
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="部门负责人ID")
    
    # 联系信息
    phone = Column(String(20), nullable=True, comment="部门电话")
    email = Column(String(100), nullable=True, comment="部门邮箱")
    address = Column(String(255), nullable=True, comment="部门地址")
    
    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
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
    parent = relationship("Department", remote_side=[id], backref="children")
    manager = relationship("User", foreign_keys=[manager_id], backref="managed_departments")
    employees = relationship("Employee", back_populates="department")
    
    def __repr__(self):
        return f"<Department(id={self.id}, name='{self.name}', code='{self.code}')>"
    
    @property
    def full_name(self):
        """获取完整部门名称（包含父级）"""
        if self.parent:
            return f"{self.parent.full_name} > {self.name}"
        return self.name
    
    @property
    def employee_count(self):
        """获取部门员工数量"""
        return len(self.employees) if self.employees else 0