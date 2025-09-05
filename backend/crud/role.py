from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import List, Optional
from ..models.role import Role, Permission, role_permissions
from ..schemas.role import RoleCreate, PermissionCreate


class RoleCRUD:
    """角色CRUD操作类"""
    
    @staticmethod
    def get_role(db: Session, role_id: int) -> Optional[Role]:
        """根据ID获取角色"""
        return db.query(Role).options(
            joinedload(Role.permissions)
        ).filter(Role.id == role_id).first()
    
    @staticmethod
    def get_role_by_code(db: Session, code: str) -> Optional[Role]:
        """根据编码获取角色"""
        return db.query(Role).filter(Role.code == code).first()
    
    @staticmethod
    def get_roles(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[Role]:
        """获取角色列表"""
        query = db.query(Role).options(joinedload(Role.permissions))
        
        if name:
            query = query.filter(Role.name.contains(name))
        
        if is_active is not None:
            query = query.filter(Role.is_active == is_active)
        
        return query.order_by(Role.sort_order, Role.created_at).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_role(db: Session, role: RoleCreate) -> Role:
        """创建角色"""
        if RoleCRUD.get_role_by_code(db, role.code):
            raise ValueError("角色编码已存在")
        
        db_role = Role(
            name=role.name,
            code=role.code,
            description=role.description,
            is_active=True,
            is_system=False,
            sort_order=0
        )
        
        db.add(db_role)
        db.flush()
        
        # 分配权限
        if role.permission_ids:
            permissions = db.query(Permission).filter(
                Permission.id.in_(role.permission_ids)
            ).all()
            db_role.permissions = permissions
        
        db.commit()
        db.refresh(db_role)
        return db_role


class PermissionCRUD:
    """权限CRUD操作类"""
    
    @staticmethod
    def get_permission(db: Session, permission_id: int) -> Optional[Permission]:
        """根据ID获取权限"""
        return db.query(Permission).filter(Permission.id == permission_id).first()
    
    @staticmethod
    def get_permissions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        module: Optional[str] = None
    ) -> List[Permission]:
        """获取权限列表"""
        query = db.query(Permission)
        
        if module:
            query = query.filter(Permission.module == module)
        
        return query.filter(Permission.is_active == True).order_by(
            Permission.sort_order, Permission.created_at
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_permission(db: Session, permission: PermissionCreate) -> Permission:
        """创建权限"""
        db_permission = Permission(
            name=permission.name,
            code=permission.code,
            description=permission.description,
            module=permission.module,
            resource=permission.resource,
            action=permission.action,
            is_active=True,
            sort_order=0
        )
        
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission


# 创建全局实例
role_crud = RoleCRUD()
permission_crud = PermissionCRUD()