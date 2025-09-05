from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# 绝对导入，避免相对导入问题
try:
    from backend.db.base import Base
except ImportError:
    from db.base import Base


class LogLevel(str, enum.Enum):
    """日志级别枚举"""
    DEBUG = "debug"       # 调试
    INFO = "info"         # 信息
    WARNING = "warning"   # 警告
    ERROR = "error"       # 错误
    CRITICAL = "critical" # 严重错误


class LogType(str, enum.Enum):
    """日志类型枚举"""
    LOGIN = "login"           # 登录日志
    LOGOUT = "logout"         # 登出日志
    CREATE = "create"         # 创建操作
    UPDATE = "update"         # 更新操作
    DELETE = "delete"         # 删除操作
    VIEW = "view"             # 查看操作
    EXPORT = "export"         # 导出操作
    IMPORT = "import"         # 导入操作
    SYSTEM = "system"         # 系统操作
    SECURITY = "security"     # 安全相关
    API_CALL = "api_call"     # API调用


class SystemLog(Base):
    """系统日志模型"""
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True, index=True, comment="日志ID")
    
    # 用户信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="操作用户ID")
    username = Column(String(50), nullable=True, index=True, comment="用户名")
    
    # 日志基本信息
    level = Column(Enum(LogLevel), default=LogLevel.INFO, index=True, comment="日志级别")
    log_type = Column(Enum(LogType), nullable=False, index=True, comment="日志类型")
    action = Column(String(100), nullable=False, index=True, comment="操作动作")
    message = Column(Text, nullable=False, comment="日志消息")
    
    # 请求信息
    method = Column(String(10), nullable=True, comment="HTTP请求方法")
    url = Column(String(500), nullable=True, comment="请求URL")
    endpoint = Column(String(200), nullable=True, index=True, comment="API端点")
    
    # 客户端信息
    ip_address = Column(String(45), nullable=True, index=True, comment="客户端IP地址")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    
    # 操作对象信息
    resource_type = Column(String(50), nullable=True, index=True, comment="资源类型")
    resource_id = Column(String(50), nullable=True, index=True, comment="资源ID")
    
    # 详细信息
    request_data = Column(JSON, nullable=True, comment="请求数据")
    response_data = Column(JSON, nullable=True, comment="响应数据")
    
    # 状态信息
    status_code = Column(Integer, nullable=True, comment="响应状态码")
    is_success = Column(Boolean, default=True, comment="是否成功")
    error_message = Column(Text, nullable=True, comment="错误信息")
    
    # 性能信息
    duration = Column(Integer, nullable=True, comment="执行时长(毫秒)")
    
    # 时间字段
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        index=True,
        comment="创建时间"
    )
    
    # 关系
    user = relationship("User", backref="system_logs")
    
    def __repr__(self):
        return f"<SystemLog(id={self.id}, action='{self.action}', user='{self.username}')>"
    
    @property
    def duration_seconds(self):
        """获取执行时长（秒）"""
        if self.duration:
            return round(self.duration / 1000, 3)
        return None
    
    @property
    def is_slow_request(self):
        """判断是否为慢请求（超过3秒）"""
        return self.duration and self.duration > 3000
    
    @classmethod
    def create_log(cls, **kwargs):
        """创建日志记录的便捷方法"""
        return cls(**kwargs)