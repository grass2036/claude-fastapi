"""数据库种子数据脚本"""
from sqlalchemy.orm import Session
from .base import SessionLocal, engine
from ..models.user import User
from ..core.security import security


def create_superuser():
    """创建超级管理员用户"""
    db = SessionLocal()
    try:
        # 检查是否已存在超级用户
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("超级用户 'admin' 已存在")
            return existing_admin
        
        # 创建超级用户
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=security.hash_password("admin123456"),
            full_name="System Administrator",
            is_active=True,
            is_superuser=True,
            is_verified=True,
            bio="系统超级管理员"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"超级用户创建成功:")
        print(f"- 用户名: {admin_user.username}")
        print(f"- 邮箱: {admin_user.email}")
        print(f"- 密码: admin123456")
        print(f"- ID: {admin_user.id}")
        
        return admin_user
        
    except Exception as e:
        print(f"创建超级用户失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_test_users():
    """创建测试用户"""
    db = SessionLocal()
    try:
        test_users_data = [
            {
                "username": "testuser1",
                "email": "test1@example.com",
                "password": "testpass123",
                "full_name": "Test User One",
                "bio": "第一个测试用户"
            },
            {
                "username": "testuser2",
                "email": "test2@example.com",
                "password": "testpass123",
                "full_name": "Test User Two",
                "bio": "第二个测试用户"
            },
            {
                "username": "developer",
                "email": "dev@example.com",
                "password": "devpass123",
                "full_name": "Developer User",
                "bio": "开发者测试账户"
            }
        ]
        
        created_users = []
        for user_data in test_users_data:
            # 检查用户是否已存在
            existing_user = db.query(User).filter(
                User.username == user_data["username"]
            ).first()
            
            if existing_user:
                print(f"用户 '{user_data['username']}' 已存在")
                continue
            
            # 创建用户
            new_user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=security.hash_password(user_data["password"]),
                full_name=user_data["full_name"],
                bio=user_data["bio"],
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
            
            db.add(new_user)
            created_users.append(new_user)
        
        db.commit()
        
        if created_users:
            print(f"成功创建 {len(created_users)} 个测试用户:")
            for user in created_users:
                db.refresh(user)
                print(f"- {user.username} ({user.email}) - ID: {user.id}")
        
        return created_users
        
    except Exception as e:
        print(f"创建测试用户失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def seed_database():
    """运行所有种子数据脚本"""
    print("🌱 开始初始化数据库种子数据...")
    
    try:
        # 创建超级用户
        print("\n1. 创建超级管理员...")
        create_superuser()
        
        # 创建测试用户
        print("\n2. 创建测试用户...")
        create_test_users()
        
        print("\n✅ 数据库种子数据初始化完成！")
        print("\n📋 默认账户信息:")
        print("   超级管理员:")
        print("   - 用户名: admin")
        print("   - 密码: admin123456")
        print("   - 邮箱: admin@example.com")
        print("\n   测试账户:")
        print("   - 用户名: testuser1, testuser2, developer")
        print("   - 密码: testpass123 / devpass123")
        
    except Exception as e:
        print(f"❌ 数据库种子数据初始化失败: {e}")
        raise


def reset_database():
    """重置数据库（删除所有数据）"""
    print("⚠️  警告: 即将删除所有用户数据！")
    confirm = input("确认重置数据库？(输入 'yes' 确认): ")
    
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    db = SessionLocal()
    try:
        # 删除所有用户
        db.query(User).delete()
        db.commit()
        print("✅ 数据库重置完成")
        
        # 重新创建种子数据
        seed_database()
        
    except Exception as e:
        print(f"❌ 数据库重置失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "reset":
            reset_database()
        elif command == "seed":
            seed_database()
        else:
            print("用法: python seed.py [seed|reset]")
    else:
        seed_database()