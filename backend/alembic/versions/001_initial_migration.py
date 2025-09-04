"""Initial migration - create users table

Revision ID: 001
Revises: 
Create Date: 2023-09-04 22:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create users table"""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.Column('username', sa.String(length=50), nullable=False, comment='用户名'),
        sa.Column('email', sa.String(length=100), nullable=False, comment='邮箱'),
        sa.Column('hashed_password', sa.String(length=255), nullable=False, comment='加密密码'),
        sa.Column('full_name', sa.String(length=100), nullable=True, comment='全名'),
        sa.Column('avatar', sa.String(length=255), nullable=True, comment='头像URL'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='手机号'),
        sa.Column('is_active', sa.Boolean(), nullable=True, comment='是否激活'),
        sa.Column('is_superuser', sa.Boolean(), nullable=True, comment='是否超级用户'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, comment='是否验证邮箱'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=func.now(), nullable=True, comment='更新时间'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True, comment='最后登录时间'),
        sa.Column('bio', sa.Text(), nullable=True, comment='个人简介'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # 创建索引
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)


def downgrade() -> None:
    """Drop users table"""
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')