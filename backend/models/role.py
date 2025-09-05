from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# 绝对导入，避免相对导入问题
try:
    from backend.db.base import Base
except ImportError:
    from db.base import Base


# 用户角色关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, comment="用户ID"),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True, comment="角色ID"),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), comment="分配时间")
)

# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True, comment="角色ID"),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True, comment="权限ID"),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), comment="分配时间")
)


class Role(Base):
    """角色模型"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, comment="角色ID")
    name = Column(String(50), unique=True, nullable=False, index=True, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, index=True, comment="角色编码")
    description = Column(Text, nullable=True, comment="角色描述")
    
    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_system = Column(Boolean, default=False, comment="是否系统内置角色")
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
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}', code='{self.code}')>"


class Permission(Base):
    """权限模型"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True, comment="权限ID")
    name = Column(String(50), nullable=False, index=True, comment="权限名称")
    code = Column(String(100), unique=True, nullable=False, index=True, comment="权限编码")
    description = Column(Text, nullable=True, comment="权限描述")
    
    # 权限分组
    module = Column(String(50), nullable=True, index=True, comment="所属模块")
    resource = Column(String(100), nullable=True, comment="资源")
    action = Column(String(50), nullable=True, comment="操作动作")
    
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
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}', code='{self.code}')>"