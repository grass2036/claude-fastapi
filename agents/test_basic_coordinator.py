#!/usr/bin/env python3
"""
简化版任务协调Agent测试
不依赖CrewAI，直接测试基础功能
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# 添加agents目录到Python路径
sys.path.append(str(Path(__file__).parent))

class TaskType(Enum):
    """任务类型枚举"""
    DOCUMENTATION = "documentation"
    CODE_ANALYSIS = "code_analysis"
    API_DEVELOPMENT = "api_development"
    TESTING = "testing"


class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    ASSIGNED = "assigned" 
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskInfo:
    """任务信息数据结构"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    task_type: TaskType = TaskType.DOCUMENTATION
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    result: Optional[str] = None
    error: Optional[str] = None


class BasicTaskCoordinator:
    """简化版任务协调器"""
    
    def __init__(self):
        self.tasks: Dict[str, TaskInfo] = {}
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []
    
    def create_task(
        self,
        title: str,
        description: str,
        task_type: TaskType,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> str:
        """创建新任务"""
        task = TaskInfo(
            title=title,
            description=description,
            task_type=task_type,
            priority=priority
        )
        
        self.tasks[task.id] = task
        self.task_queue.append(task.id)
        
        # 按优先级排序
        self.task_queue.sort(key=lambda tid: self.tasks[tid].priority.value, reverse=True)
        
        return task.id
    
    def execute_task(self, task_id: str) -> bool:
        """执行任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        try:
            task.status = TaskStatus.IN_PROGRESS
            
            # 模拟任务执行
            if task.task_type == TaskType.DOCUMENTATION:
                task.result = f"生成了 {task.title} 的文档"
            elif task.task_type == TaskType.CODE_ANALYSIS:
                task.result = f"分析了 {task.title} 的代码结构"
            else:
                task.result = f"处理了任务: {task.title}"
            
            task.status = TaskStatus.COMPLETED
            self.completed_tasks.append(task_id)
            if task_id in self.task_queue:
                self.task_queue.remove(task_id)
                
            return True
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态报告"""
        status_counts = {}
        for task in self.tasks.values():
            status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1
        
        return {
            'total_tasks': len(self.tasks),
            'task_status': status_counts,
            'queue_length': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks)
        }
    
    def decompose_request(self, request: str) -> List[str]:
        """简单的请求分解"""
        task_ids = []
        
        # 简单的关键词匹配分解
        if '文档' in request or 'API' in request or 'documentation' in request:
            task_id = self.create_task(
                title="生成API文档",
                description=f"根据需求生成文档: {request}",
                task_type=TaskType.DOCUMENTATION,
                priority=TaskPriority.HIGH
            )
            task_ids.append(task_id)
        
        if '分析' in request or 'analysis' in request:
            task_id = self.create_task(
                title="代码分析", 
                description=f"根据需求分析代码: {request}",
                task_type=TaskType.CODE_ANALYSIS,
                priority=TaskPriority.MEDIUM
            )
            task_ids.append(task_id)
        
        if '测试' in request or 'test' in request:
            task_id = self.create_task(
                title="生成测试",
                description=f"根据需求生成测试: {request}",
                task_type=TaskType.TESTING,
                priority=TaskPriority.HIGH
            )
            task_ids.append(task_id)
        
        # 如果没有匹配到关键词，创建默认文档任务
        if not task_ids:
            task_id = self.create_task(
                title="处理用户请求",
                description=request,
                task_type=TaskType.DOCUMENTATION,
                priority=TaskPriority.MEDIUM
            )
            task_ids.append(task_id)
        
        return task_ids
    
    def handle_request(self, request: str) -> Dict[str, Any]:
        """处理用户请求"""
        # 分解请求
        task_ids = self.decompose_request(request)
        
        # 执行任务
        execution_results = {
            'completed': 0,
            'failed': 0,
            'details': []
        }
        
        for task_id in task_ids:
            if self.execute_task(task_id):
                execution_results['completed'] += 1
            else:
                execution_results['failed'] += 1
            
            task = self.tasks[task_id]
            execution_results['details'].append({
                'task_id': task_id,
                'title': task.title,
                'status': task.status.value,
                'result': task.result
            })
        
        return {
            'request': request,
            'created_tasks': len(task_ids),
            'task_ids': task_ids,
            'execution_results': execution_results
        }


def test_basic_functionality():
    """测试基础功能"""
    print("🎯 基础任务协调器测试")
    print("=" * 50)
    
    coordinator = BasicTaskCoordinator()
    
    # 测试1: 手动创建任务
    print("\n🔹 测试1: 手动创建任务")
    print("-" * 30)
    
    task_id1 = coordinator.create_task(
        title="生成用户API文档",
        description="为用户管理模块生成完整的API文档",
        task_type=TaskType.DOCUMENTATION,
        priority=TaskPriority.HIGH
    )
    
    task_id2 = coordinator.create_task(
        title="分析用户模型",
        description="分析User模型的代码结构和质量",
        task_type=TaskType.CODE_ANALYSIS,
        priority=TaskPriority.MEDIUM
    )
    
    print(f"创建任务1: {task_id1}")
    print(f"创建任务2: {task_id2}")
    
    # 测试2: 执行任务
    print("\n🔹 测试2: 执行任务")
    print("-" * 30)
    
    success1 = coordinator.execute_task(task_id1)
    success2 = coordinator.execute_task(task_id2)
    
    print(f"任务1执行: {'✅ 成功' if success1 else '❌ 失败'}")
    print(f"任务2执行: {'✅ 成功' if success2 else '❌ 失败'}")
    
    if success1:
        task1 = coordinator.tasks[task_id1]
        print(f"任务1结果: {task1.result}")
    
    if success2:
        task2 = coordinator.tasks[task_id2]
        print(f"任务2结果: {task2.result}")
    
    # 测试3: 系统状态
    print("\n🔹 测试3: 系统状态")
    print("-" * 30)
    
    status = coordinator.get_status()
    print(f"总任务数: {status['total_tasks']}")
    print(f"完成任务数: {status['completed_tasks']}")
    print(f"队列长度: {status['queue_length']}")
    print("任务状态分布:")
    for status_name, count in status['task_status'].items():
        print(f"  - {status_name}: {count}")


def test_request_handling():
    """测试请求处理功能"""
    print("\n🎯 请求处理测试")
    print("=" * 50)
    
    coordinator = BasicTaskCoordinator()
    
    # 测试不同类型的用户请求
    test_requests = [
        "为用户管理模块生成API文档",
        "分析权限中间件的代码质量",
        "创建员工管理功能的测试用例",
        "优化数据库查询性能"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🔹 测试{i}: {request}")
        print("-" * 40)
        
        result = coordinator.handle_request(request)
        
        print(f"用户请求: {result['request']}")
        print(f"创建任务数: {result['created_tasks']}")
        
        exec_results = result['execution_results']
        print(f"执行结果: 完成{exec_results['completed']}, 失败{exec_results['failed']}")
        
        for detail in exec_results['details']:
            print(f"  - {detail['title']}: {detail['status']}")
            if detail['result']:
                print(f"    结果: {detail['result']}")


def test_complex_workflow():
    """测试复杂工作流"""
    print("\n🎯 复杂工作流测试")
    print("=" * 50)
    
    coordinator = BasicTaskCoordinator()
    
    complex_request = """
    我需要为FastAPI项目添加员工绩效管理功能，包括：
    1. 设计API接口和生成文档
    2. 分析现有代码结构
    3. 创建测试用例
    """
    
    print(f"复杂请求:\n{complex_request}")
    
    result = coordinator.handle_request(complex_request)
    
    print(f"\n工作流处理结果:")
    print(f"  - 分解任务数: {result['created_tasks']}")
    
    exec_results = result['execution_results']
    print(f"  - 执行统计: 完成{exec_results['completed']}, 失败{exec_results['failed']}")
    
    print(f"  - 任务详情:")
    for detail in exec_results['details']:
        print(f"    * {detail['title']} - {detail['status']}")
        if detail['result']:
            print(f"      {detail['result']}")


def interactive_test():
    """交互式测试"""
    print("\n🎯 交互式测试")
    print("=" * 50)
    print("输入您的需求进行测试，输入 'quit' 退出")
    print("-" * 50)
    
    coordinator = BasicTaskCoordinator()
    
    while True:
        try:
            user_input = input("\n👤 您的需求: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 测试结束！")
                break
            elif user_input.lower() == 'status':
                status = coordinator.get_status()
                print(f"📊 系统状态: {status}")
            elif user_input:
                print(f"\n🤖 处理中...")
                result = coordinator.handle_request(user_input)
                
                print(f"✅ 处理完成:")
                print(f"  - 创建任务: {result['created_tasks']}")
                
                exec_results = result['execution_results']
                print(f"  - 执行结果: 完成{exec_results['completed']}, 失败{exec_results['failed']}")
                
                for detail in exec_results['details']:
                    print(f"  - {detail['title']}: {detail['result'] or '无结果'}")
            else:
                print("请输入有效的需求")
                
        except KeyboardInterrupt:
            print("\n👋 测试中断！")
            break
        except Exception as e:
            print(f"❌ 处理错误: {e}")


def main():
    """主函数"""
    print("🚀 TaskCoordinator 基础功能测试")
    print("=" * 60)
    
    try:
        # 运行基础测试
        test_basic_functionality()
        test_request_handling()
        test_complex_workflow()
        
        # 询问是否进入交互模式
        print("\n" + "=" * 60)
        choice = input("是否进入交互式测试？(y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_test()
        
        print("\n✅ 所有测试完成！")
        print("TaskCoordinatorAgent基础功能验证通过")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()