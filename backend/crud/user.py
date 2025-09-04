from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import security


class UserCRUD:
    """用户CRUD操作类"""
    
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username_or_email(db: Session, username: str) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        return db.query(User).filter(
            or_(User.username == username, User.email == username)
        ).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """创建用户"""
        # 验证确认密码
        if user.password != user.confirm_password:
            raise ValueError("密码和确认密码不匹配")
        
        # 检查用户名是否已存在
        if UserCRUD.get_user_by_username(db, user.username):
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        if UserCRUD.get_user_by_email(db, user.email):
            raise ValueError("邮箱已存在")
        
        # 加密密码
        hashed_password = security.hash_password(user.password)
        
        # 创建用户对象
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            phone=user.phone,
            bio=user.bio,
            is_active=True,
            is_verified=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """验证用户登录"""
        user = UserCRUD.get_user_by_username_or_email(db, username)
        
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not security.verify_password(password, user.hashed_password):
            return None
        
        # 更新最后登录时间
        user.last_login_at = datetime.now()
        db.commit()
        
        return user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        db_user = UserCRUD.get_user(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def change_password(db: Session, user_id: int, current_password: str, new_password: str) -> bool:
        """修改密码"""
        user = UserCRUD.get_user(db, user_id)
        if not user:
            return False
        
        # 验证当前密码
        if not security.verify_password(current_password, user.hashed_password):
            return False
        
        # 更新密码
        user.hashed_password = security.hash_password(new_password)
        db.commit()
        return True
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> bool:
        """停用用户"""
        user = UserCRUD.get_user(db, user_id)
        if not user:
            return False
        
        user.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def activate_user(db: Session, user_id: int) -> bool:
        """激活用户"""
        user = UserCRUD.get_user(db, user_id)
        if not user:
            return False
        
        user.is_active = True
        db.commit()
        return True


# 创建全局实例
user_crud = UserCRUD()