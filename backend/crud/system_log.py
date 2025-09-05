from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc, text
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ..models.system_log import SystemLog, LogLevel, LogType
from ..schemas.system_log import SystemLogCreate


class SystemLogCRUD:
    """系统日志CRUD操作类"""
    
    @staticmethod
    def get_log(db: Session, log_id: int) -> Optional[SystemLog]:
        """根据ID获取日志"""
        return db.query(SystemLog).filter(SystemLog.id == log_id).first()
    
    @staticmethod
    def get_logs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        level: Optional[LogLevel] = None,
        log_type: Optional[LogType] = None,
        username: Optional[str] = None,
        action: Optional[str] = None,
        is_success: Optional[bool] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        ip_address: Optional[str] = None
    ) -> List[SystemLog]:
        """获取日志列表"""
        query = db.query(SystemLog)
        
        # 添加筛选条件
        if level:
            query = query.filter(SystemLog.level == level)
        
        if log_type:
            query = query.filter(SystemLog.log_type == log_type)
        
        if username:
            query = query.filter(SystemLog.username.contains(username))
        
        if action:
            query = query.filter(SystemLog.action.contains(action))
        
        if is_success is not None:
            query = query.filter(SystemLog.is_success == is_success)
        
        if start_time:
            query = query.filter(SystemLog.created_at >= start_time)
        
        if end_time:
            query = query.filter(SystemLog.created_at <= end_time)
        
        if ip_address:
            query = query.filter(SystemLog.ip_address == ip_address)
        
        return query.order_by(desc(SystemLog.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_logs_count(
        db: Session,
        level: Optional[LogLevel] = None,
        log_type: Optional[LogType] = None,
        username: Optional[str] = None,
        action: Optional[str] = None,
        is_success: Optional[bool] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        ip_address: Optional[str] = None
    ) -> int:
        """获取日志总数"""
        query = db.query(SystemLog)
        
        if level:
            query = query.filter(SystemLog.level == level)
        
        if log_type:
            query = query.filter(SystemLog.log_type == log_type)
        
        if username:
            query = query.filter(SystemLog.username.contains(username))
        
        if action:
            query = query.filter(SystemLog.action.contains(action))
        
        if is_success is not None:
            query = query.filter(SystemLog.is_success == is_success)
        
        if start_time:
            query = query.filter(SystemLog.created_at >= start_time)
        
        if end_time:
            query = query.filter(SystemLog.created_at <= end_time)
        
        if ip_address:
            query = query.filter(SystemLog.ip_address == ip_address)
        
        return query.count()
    
    @staticmethod
    def create_log(db: Session, log: SystemLogCreate) -> SystemLog:
        """创建日志记录"""
        db_log = SystemLog(
            user_id=log.user_id,
            username=log.username,
            level=log.level,
            log_type=log.log_type,
            action=log.action,
            message=log.message,
            method=log.method,
            url=log.url,
            endpoint=log.endpoint,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            request_data=log.request_data,
            response_data=log.response_data,
            status_code=log.status_code,
            is_success=log.is_success,
            error_message=log.error_message,
            duration=log.duration
        )
        
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log
    
    @staticmethod
    def get_log_statistics(db: Session) -> Dict[str, Any]:
        """获取日志统计信息"""
        # 基本统计
        total_logs = db.query(SystemLog).count()
        
        # 今日日志
        today = datetime.now().date()
        today_logs = db.query(SystemLog).filter(
            func.date(SystemLog.created_at) == today
        ).count()
        
        # 错误和警告日志
        error_logs = db.query(SystemLog).filter(
            SystemLog.level == LogLevel.ERROR
        ).count()
        
        warning_logs = db.query(SystemLog).filter(
            SystemLog.level == LogLevel.WARNING
        ).count()
        
        # 按类型统计
        type_stats = db.query(
            SystemLog.log_type,
            func.count(SystemLog.id).label('count')
        ).group_by(SystemLog.log_type).all()
        
        # 最近24小时按小时统计
        last_24_hours = datetime.now() - timedelta(hours=24)
        hourly_stats = db.query(
            func.extract('hour', SystemLog.created_at).label('hour'),
            func.count(SystemLog.id).label('count')
        ).filter(
            SystemLog.created_at >= last_24_hours
        ).group_by(
            func.extract('hour', SystemLog.created_at)
        ).all()
        
        # 热门API
        popular_apis = db.query(
            SystemLog.endpoint,
            func.count(SystemLog.id).label('count')
        ).filter(
            SystemLog.endpoint.isnot(None),
            SystemLog.created_at >= last_24_hours
        ).group_by(SystemLog.endpoint).order_by(
            desc(func.count(SystemLog.id))
        ).limit(10).all()
        
        # 慢请求（超过3秒）
        slow_requests = db.query(SystemLog).filter(
            SystemLog.duration > 3000
        ).count()
        
        return {
            "total_logs": total_logs,
            "today_logs": today_logs,
            "error_logs": error_logs,
            "warning_logs": warning_logs,
            "type_stats": [
                {"type": log_type.value, "count": count} for log_type, count in type_stats
            ],
            "hourly_stats": [
                {"hour": f"{int(hour):02d}:00", "count": count} for hour, count in hourly_stats
            ],
            "popular_apis": [
                {"endpoint": endpoint, "count": count} for endpoint, count in popular_apis
            ],
            "slow_requests": slow_requests
        }
    
    @staticmethod
    def delete_old_logs(db: Session, days: int = 30) -> int:
        """删除旧日志（清理任务）"""
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = db.query(SystemLog).filter(
            SystemLog.created_at < cutoff_date
        ).count()
        
        db.query(SystemLog).filter(
            SystemLog.created_at < cutoff_date
        ).delete()
        
        db.commit()
        return deleted_count
    
    @staticmethod
    def get_user_activity_logs(
        db: Session, 
        user_id: int, 
        limit: int = 50
    ) -> List[SystemLog]:
        """获取用户活动日志"""
        return db.query(SystemLog).filter(
            SystemLog.user_id == user_id
        ).order_by(desc(SystemLog.created_at)).limit(limit).all()


# 创建全局实例
system_log_crud = SystemLogCRUD()